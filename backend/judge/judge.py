import tempfile
import os, sys
import subprocess
import requests
import traceback

judge_config = {
    'time_limit': 10 * 60 * 60,            # time limit in seconds, set to 0 if no limit
    'entry_file': './main.sh',             # entry file
    'final_score': './score.txt',          # the final score, in integer
    'submit_logs': True,
    'submit_appdata': True,
    'appdata_path': './appdata.txt',       # app data (if got)
    'possible_error_path': './possible_error.txt',           # The possible error collected
    'url_host': 'http://localhost:8000',   # here trailing / will affect performance, since
                                           # django will do 301 on this
    'judger_secret': 'c8fc82f3d6b6150692baaad61ae77abd29ab2d0379700443394cd41eca7ad5e2'
}

def get_submission_detail(submission_id, testcase_id, submission_result_id):

    with requests.Session() as sess:
        # Setup default options for auth
        sess.headers.update({'X-JudgerSecret': judge_config['judger_secret']})

        # Move status to JUDGING
        r = sess.patch("{}/api/submission-results/{}/".format(judge_config['url_host'], submission_result_id), data={
            'status': 'JUDGING'
        })
        print(r.content.decode("utf-8"))
        r.raise_for_status()

        # Example response for /api/submissions/2/:
        # {
        #     "id": 2,
        #     "results": [ ],
        #     "total_grade": 0,
        #     "judged": false,
        #     "submit_time": "14:41:14.400926",
        #     "problem": 1,
        #     "user": 1,
        #     "submit_files": [
        #         3
        #     ]
        # }

        s_resp = sess.get('{}/api/submissions/{}'.format(
                judge_config['url_host'], 
                submission_id)
            )
        s_resp.raise_for_status()
        print(s_resp.text)
        s_json = s_resp.json()

        # Example response for /api/problem-testcases/1
        # {
        #     "id": 1,
        #     "type": "SIM",
        #     "grade": 5,
        #     "problem": 1,
        #     "testcase_files": [
        #         4,
        #         5,
        #         6,
        #         7
        #     ]
        # }

        t_resp = sess.get('{}/api/problem-testcases/{}'.format(
                judge_config['url_host'], 
                testcase_id)
            )
        t_resp.raise_for_status()
        print(t_resp.text)
        t_json = t_resp.json()

        # Example response for /api/problems/1
        # {
        #     "id": 1,
        #     "testcases": [
        #         {
        #             "id": 1,
        #             "type": "SIM",
        #             "grade": 5,
        #             "problem": 1,
        #             "testcase_files": [
        #                 4,
        #                 5,
        #                 6,
        #                 7
        #             ]
        #         }
        #     ],
        #     "total_grade": 5,
        #     "name": "A decoder test",
        #     "create_time": "14:37:38.303324",
        #     "deadline_time": "14:31:00",
        #     "judge_files": [
        #         1
        #     ]
        # }

        p_resp = sess.get('{}/api/problems/{}'.format(
                judge_config['url_host'], 
                s_json['problem'])
            )
        p_resp.raise_for_status()
        print(p_resp.text)
        p_json = p_resp.json()

        return {
            'id': s_json['id'],
            'problem': {
                'id': s_json['problem'],
                'problem_files': [
                    {'uuid': str(k)} for k in p_json["judge_files"]
                ],
                'testcase_id': testcase_id
            },
            'user': {
                'id': s_json['user'],
                # TODO: fill this
                'student_id': "N/A"
            },
            # TODO: fill like this format 'submit_time': "20101001",
            'submit_time': s_json['submit_time'],
            'submit_files': [
                {'uuid': str(k)} for k in s_json["submit_files"]
            ],
            'testcase_files': [
                {'uuid': str(k)} for k in t_json["testcase_files"]
            ]
        }

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

def push_result(result, submission_id, testcase_id, submission_result_id):
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

def prepare_and_run(detail):
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


def judge(submission_id, testcase_id, submission_result_id):
    """
    评测某个提交。生成若干SubmissionResult，之后Submission就会被更新。
    """
    # TODO: 对某个提交进行评测
    # Query submission api for a json
    try:
        detail = get_submission_detail(submission_id, testcase_id, submission_result_id)
        result = prepare_and_run(detail)
        push_result(result, submission_id, testcase_id, submission_result_id)
        return True
    except:
        print("Unexpected error while processing {}-{} (result_id={}), traceback below:\n{}".format(
            submission_id, testcase_id, submission_result_id, traceback.format_exc()))
        return False