#!/usr/bin/env python3

import os, sys

class UUIDNotInFileMap(Exception):
    pass

class JudgerTester:
    def __init__(self):
        # inject in, this assumes judge.py is in ../
        BASE_PATH = os.path.realpath(os.path.join(os.path.realpath(__file__), "../"))
        print("BASE_PATH: {}".format(BASE_PATH))

        # cases
        sys.path.append(os.path.join(BASE_PATH, "./cases"))

        # the judge.py
        sys.path.append(os.path.join(BASE_PATH, "../"))


    def run_case(self, case_name):
        # import config
        cfg_inst = __import__(case_name)
        
        # mock objects
        def mock_download_file(path, uuid):
            if uuid not in cfg_inst.config['file_map']:
                raise UUIDNotInFileMap("UUID {} not in file_map".format(uuid))

            filename = cfg_inst.config['file_map'][uuid]['filename']
            content = cfg_inst.config['file_map'][uuid]['content']

            # the path shall exist
            real_fp = os.path.realpath(os.path.join(path, filename))
            with open(real_fp, "wb") as f:
                f.write(content)
            
            print("Wriiten {}/".format(real_fp))
            
        def mock_get_submission_detail(submission_id, testcase_id):
            return cfg_inst.config['submission_detail'].copy()
        
        def mock_push_result(result, submission_id, testcase_id):
            print("Result: {}".format(result))
        
        # inject in, this assumes judge.py is in ../
        BASE_PATH = os.path.join(os.path.realpath(__file__), "../")
        sys.path.append(BASE_PATH)

        import judge
        judge.push_result = mock_push_result
        judge.get_submission_detail = mock_get_submission_detail
        judge.download_file = mock_download_file

        judge.judge(cfg_inst.config['submission_id'], cfg_inst.config['testcase_id'])

if __name__ == '__main__':
    a = JudgerTester()
    a.run_case("icarus_wave_cmp")