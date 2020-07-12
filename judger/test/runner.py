#!/usr/bin/env python3

import os, sys
import argparse

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

    def unfold_case(self, case_name, folder):
        """Extract a given case into folder"""
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
            
            print("Written {}/".format(real_fp))
        
        BASE_PATH = folder
        TESTCASE_DIR = os.path.join(BASE_PATH, "./testcase")
        PROBLEM_DIR = os.path.join(BASE_PATH, "./problem")
        SUBMIT_DIR = os.path.join(BASE_PATH, "./submit")

        os.mkdir(TESTCASE_DIR)
        os.mkdir(PROBLEM_DIR)
        os.mkdir(SUBMIT_DIR)

        # download all contents in place
        for f in cfg_inst.config['submission_detail']['testcase_files']:
            mock_download_file(TESTCASE_DIR, f['uuid'])
        
        for f in cfg_inst.config['submission_detail']['problem']['problem_files']:
            mock_download_file(PROBLEM_DIR, f['uuid'])

        for f in cfg_inst.config['submission_detail']['submit_files']:
            mock_download_file(SUBMIT_DIR, f['uuid'])

        
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
            
            print("Written {}/".format(real_fp))
            
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

def run(args):
    print("Running subcommand run with name={}".format(args.name))
    inst = JudgerTester()
    inst.run_case(args.name)

def unfold(args):
    print("Running subcommand unfold with name={} and folder={}".format(args.name, args.folder))
    inst = JudgerTester()
    if not os.path.exists(args.folder):
        os.makedirs(args.folder)
    inst.unfold_case(args.name, args.folder)

def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(title="Subcommands")

    run_parser = subparsers.add_parser('run', help="run testcase(s)")
    run_parser.add_argument("name", help="name of the testcase")
    run_parser.set_defaults(func=run)

    unfold_parser = subparsers.add_parser('unfold', help="Extract files from a given testcase")
    unfold_parser.add_argument("name", help="name of the testcase")
    unfold_parser.add_argument("folder", help="path to the folder to be extracted to")
    unfold_parser.set_defaults(func=unfold)

    args = parser.parse_args()
    # https://docs.python.org/3/library/argparse.html#argparse.ArgumentParser.add_subparsers
    args.func(args)

if __name__ == '__main__':
    main()
    # a = JudgerTester()
    # a.run_case("icarus_wave_cmp")