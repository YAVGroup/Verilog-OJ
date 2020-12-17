from .base import BaseExecutor

import logging, tempfile, os, subprocess, traceback

logger = logging.getLogger(__name__)

class LocalExecutor(BaseExecutor):
    def prepare(self):
        self.move_status("JUDGING")

    def run(self):
        
        with tempfile.TemporaryDirectory() as tmpdirname:
            TESTCASE_DIR, PROBLEM_DIR, SUBMIT_DIR = self.place_tree(tmpdirname)
            os.chdir(tmpdirname)

            possible_errors = []

            process = subprocess.Popen(
                ['/bin/bash', os.path.join(TESTCASE_DIR, self.judger_config['entry_file'])],
                stdout = subprocess.PIPE,
                stderr = subprocess.PIPE
                )
            
            if self.detail['time_limit'] != 0:
                try:
                    out, err = process.communicate(
                        timeout=self.judger_config['time_limit']
                    )
                except subprocess.TimeoutExpired:
                    process.kill()
                    out, err = process.communicate()
                    possible_errors.append('TIME_LIM_EXCEED')
            else:
                out, err = process.communicate()
            
            # Read score
            score_file_path = os.path.join(tmpdirname, self.judger_config['final_score'])
            score = None
            if os.path.exists(score_file_path):
                with open(score_file_path, "r") as f:
                    score = int(f.read())
            logger.info("Final score: {}".format(score))

            if score is None:
                score = 0

            # Grab all logs
            if self.judger_config['submit_logs']:
                # out.read is expected to be bytes
                log_out = out.decode("utf8")
                log_err = err.decode("utf8")
            else:
                log_out = "Suppressed due to submit_logs in judge configurations"
                log_err = "Suppressed due to submit_logs in judge configurations"

            appdata = ""
            appdata_file_path = os.path.join(tmpdirname, self.judger_config['appdata_path'])
            try:
                with open(appdata_file_path, "r") as f:
                    appdata = f.read()
            except:
                appdata = "Error reading appdata ({}), traceback below\n{}".format(
                    appdata_file_path, traceback.format_exc())


            possible_error_file_path = os.path.join(tmpdirname, self.judger_config['possible_error_path'])
            try:
                with open(possible_error_file_path, "r") as f:
                    possible_errors.append(f.read().strip())
            except:
                possible_errors.append("NA")

            self.patch_result({
                'grade': str(score),
                'log': "stderr:\n{}\n\nstdout:\n{}".format(
                    log_err, log_out),
                'status': 'DONE',
                'app_data': appdata if self.judger_config['submit_appdata'] else 'N/A',
                'possible_failure': possible_errors[0] if len(possible_errors) > 0 else "NONE"
            })

