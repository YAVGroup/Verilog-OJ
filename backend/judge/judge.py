import tempfile
import os, sys
import subprocess
import requests
import traceback

def move_status(status_msg, submission_detail, judger_config):
    with requests.Session() as sess:
        sess.headers.update({'X-JudgerSecret': judge_config['judger_secret']})
        
        r = sess.patch(
                "{}/api/submission-results/{}/".format(
                    judge_config['url_host'],
                    submission_result_id
                ),
                data={
                    'status': status_msg
                }
            )
        # print(r.content.decode("utf-8"))
        r.raise_for_status()

def download_file(path, uuid):
    # Download file and store it in path (a dir)
    r_file = requests.get('{}/api/files/{}'.format(
        judge_config['url_host'],
        uuid
    ), headers={'X-JudgerSecret': judge_config['judger_secret']})

    r_file.raise_for_status()
    # Filename obtained from Content-Disposition, e.g.
    # Content-Disposition: attachment; filename="decoder_ref.v"
    filename = r_file.headers.get('content-disposition')
    filename = filename[filename.find("filename=") + 10 : -1]
    print(filename)

    with open(os.path.join(path, filename), "wb") as f:
        f.write(r_file.content)

def push_result(result, submission_id, testcase_id, submission_result_id, judge_config):
    # todo: post to the result
    # result: {}
    with requests.Session() as sess:
        sess.headers.update({'X-JudgerSecret': judge_config['judger_secret']})

        # NOTE: when app_data == '', the requests library will probably
        # ignore sending it (?)
        r = sess.patch("{}/api/submission-results/{}/".format(judge_config['url_host'], submission_result_id), data={
            'grade': str(result['score']),
            'log': "stderr:\n{}\n\nstdout:\n{}".format(
                result['log_err'], result['log_out']),
            'status': 'DONE',
            'app_data': result['appdata'] if judge_config['submit_appdata'] else 'N/A',
            'possible_failure': result['possible_failure']
        })
        #print(r.text)
        try:
            r.raise_for_status()
        except:
            print(r.text)
            raise Exception("Bad response code")
    return True

def prepare_and_run(detail, judge_config):
    # make a new folder in /tmp
    with tempfile.TemporaryDirectory() as tmpdirname:
        print('Created temporary directory {}'.format(tmpdirname))
        BASE_PATH = tmpdirname
        TESTCASE_DIR = os.path.join(BASE_PATH, "./testcase")
        PROBLEM_DIR = os.path.join(BASE_PATH, "./problem")
        SUBMIT_DIR = os.path.join(BASE_PATH, "./submit")

        os.mkdir(TESTCASE_DIR)
        os.mkdir(PROBLEM_DIR)
        os.mkdir(SUBMIT_DIR)

        # download all contents in place
        for f in detail['testcase_files']:
            download_file(TESTCASE_DIR, f['uuid'])
        
        for f in detail['problem']['problem_files']:
            download_file(PROBLEM_DIR, f['uuid'])

        for f in detail['submit_files']:
            download_file(SUBMIT_DIR, f['uuid'])

        os.chdir(BASE_PATH)

        possible_errors = []

        # evaluate with time limit
        process = subprocess.Popen(['/bin/bash', os.path.join(TESTCASE_DIR, judge_config['entry_file'])],
                stdout = subprocess.PIPE,
                stderr = subprocess.PIPE
                )
        
        if judge_config['time_limit'] != 0:
            try:
                out, err = process.communicate(timeout=judge_config['time_limit'])
            except subprocess.TimeoutExpired:
                process.kill()
                out, err = process.communicate()
                possible_errors.append("TIME_LIM_EXCEED")
        else:
            out, err = process.communicate()
        

        # push stdout & score to the server
        score_file_path = os.path.join(BASE_PATH, judge_config['final_score'])
        score = None
        if os.path.exists(score_file_path):
            with open(score_file_path, "r") as f:
                score = int(f.read())
        print("Final score: {}".format(score))

        if score is None:
            score = 0

        # Grab all logs
        if judge_config['submit_logs']:
            # out.read is expected to be bytes
            log_out = out.decode("utf8")
            log_err = err.decode("utf8")
        else:
            log_out = "Suppressed due to submit_logs in judge configurations"
            log_err = "Suppressed due to submit_logs in judge configurations"

        appdata = ""
        appdata_file_path = os.path.join(BASE_PATH, judge_config['appdata_path'])
        try:
            with open(appdata_file_path, "r") as f:
                appdata = f.read()
        except:
            appdata = "Error reading appdata ({}), traceback below\n{}".format(
                appdata_file_path, traceback.format_exc())


        possible_error_file_path = os.path.join(BASE_PATH, judge_config['possible_error_path'])
        try:
            with open(possible_error_file_path, "r") as f:
                possible_errors.append(f.read().strip())
        except:
            possible_errors.append("NA")

        # Post them back
        result = {
            'score': score,
            'success': True if score is not None else False,
            'log_out': log_out,
            'log_err': log_err,
            'appdata': appdata,
            # Sort out the most urgent, in this case the first
            'possible_failure': possible_errors[0] if len(possible_errors) > 0 else "NONE" 
        }

        return result


def judge(submission_detail, judger_config):
    """
    评测某个提交。生成若干SubmissionResult，之后Submission就会被更新。
    """
    try:
        detail = get_submission_detail(submission_id, testcase_id, submission_result_id, judge_config)
        result = prepare_and_run(detail, judge_config)
        push_result(result, submission_id, testcase_id, submission_result_id, judge_config)
        return True
    except:
        print("Unexpected error while processing {}-{} (result_id={}), traceback below:\n{}".format(
            submission_id, testcase_id, submission_result_id, traceback.format_exc()))
        return False