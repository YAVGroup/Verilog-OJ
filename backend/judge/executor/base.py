import os
import requests

import logging

logger = logging.getLogger(__name__)

class BaseExecutor:
    def __init__(self, detail, judger_config):
        """ see build_judge_detail and JUDGER_CONFIG for more info """
        self.judger_config = judger_config
        self.detail = detail
    
    def download_file(self, path, uuid):
        # Download file and store it in path (a dir)
        r_file = requests.get('{}/api/files/{}'.format(
            self.judger_config['url_host'],
            uuid
        ), headers={'X-JudgerSecret': self.judger_config['judger_secret']})

        r_file.raise_for_status()
        # Filename obtained from Content-Disposition, e.g.
        # Content-Disposition: attachment; filename="decoder_ref.v"
        filename = r_file.headers.get('content-disposition')
        filename = filename[filename.find("filename=") + 10 : -1]

        with open(os.path.join(path, filename), "wb") as f:
            f.write(r_file.content)
    
    def place_tree(self, base_dir):
        """Place like this:
        /submit
        /problem
        /testcase
        """
        TESTCASE_DIR = os.path.join(base_dir, "./testcase")
        PROBLEM_DIR = os.path.join(base_dir, "./problem")
        SUBMIT_DIR = os.path.join(base_dir, "./submit")

        os.mkdir(TESTCASE_DIR)
        os.mkdir(PROBLEM_DIR)
        os.mkdir(SUBMIT_DIR)

        # download all contents in place
        for uuid in self.detail['testcase']['testcase_files']:
            self.download_file(TESTCASE_DIR, uuid)
        
        for uuid in self.detail['problem']['judge_files']:
            self.download_file(PROBLEM_DIR, uuid)

        for uuid in self.detail['submit_files']:
            self.download_file(SUBMIT_DIR, uuid)
        
        return (TESTCASE_DIR, PROBLEM_DIR, SUBMIT_DIR)

    def move_status(self, status_msg):
        return self.patch_result(
            {
                'status': status_msg
            }
        )

    def patch_result(self, data):
        with requests.Session() as sess:
            sess.headers.update({'X-JudgerSecret': self.judger_config['judger_secret']})

            # NOTE: when app_data == '', the requests library will probably
            # ignore sending it (?)
            url = f"{self.judger_config['url_host']}/api/submission-results/{self.detail['submission_result']['id']}/"
            r = sess.patch(url, data=data)

            try:
                r.raise_for_status()
            except:
                logger.error(
                    f"Error patching {url}: code={r.status_code}, text={r.text}"
                )
                raise Exception("Bad response code")

        return True

    def prepare(self):
        """ Called first """
        raise NotImplementedError("You are expected to implement this")

    def run(self):
        """ Called after """
        raise NotImplementedError("You are expected to implement this")