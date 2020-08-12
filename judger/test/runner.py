#!/usr/bin/env python3

import os, sys
import argparse
import base64

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

    def fold_case(self, case_name, testcase_files, problem_files, submit_files):
        """Fold a given testcase into Python config"""

        BASE_PATH = os.path.realpath(os.path.join(os.path.realpath(__file__), "../"))
        print("BASE_PATH: {}".format(BASE_PATH))

        # checking for conflict
        dest_py = os.path.join(BASE_PATH, "./cases/", "{}.py".format(case_name))
        if os.path.exists(dest_py):
            print("File {} already exists, abort".format(dest_py))
            return 1

        cur_uuid = 0
        uuid_tab = {}

        def legalize(filename):
            # TODO: process more generally
            # we allow only C-index names for now
            filename = filename.replace(".", "_")
            filename = filename.replace(" ", "_")
            return filename

        # A bit ugly here, TODO: improve coding style
        for i in testcase_files:
            content = None
            with open(i, "r") as f:
                content = f.read()
            assert(content is not None)
            
            uuid_tab[cur_uuid] = {
                "filename": os.path.basename(i),
                "content": content.encode("utf8"),
                "belong": "testcase"
            }
            cur_uuid += 1
        
        for i in problem_files:
            content = None
            with open(i, "r") as f:
                content = f.read()
            assert(content is not None)
            
            uuid_tab[cur_uuid] = {
                "filename": os.path.basename(i),
                "content": content.encode("utf8"),
                "belong": "problem"
            }
            cur_uuid += 1
        
        for i in submit_files:
            content = None
            with open(i, "r") as f:
                content = f.read()
            assert(content is not None)
            
            uuid_tab[cur_uuid] = {
                "filename": os.path.basename(i),
                "content": content.encode("utf8"),
                "belong": "submit"
            }
            cur_uuid += 1

        with open(dest_py, "w") as f:

            # writing config struct

            config = {
                'submission_id': 0,
                'testcase_id': 0,
                'submission_detail': {
                    'id': 0,
                    'problem': {
                        'id': 0,
                        'problem_files': [
                            {'uuid': str(k)} for k, v in uuid_tab.items() if v["belong"] == "problem"
                        ],
                        'testcase_id': 0
                    },
                    'user': {
                        'id': 0,
                        'student_id': "PB17000232"
                    },
                    'submit_time': "20101001",
                    'submit_files': [
                        {'uuid': str(k)} for k, v in uuid_tab.items() if v["belong"] == "submit"
                    ],
                    'testcase_files': [
                        {'uuid': str(k)} for k, v in uuid_tab.items() if v["belong"] == "testcase"
                    ]
                },
                'file_map': {
                    str(k): {
                        "filename": v["filename"],
                        "content": v["content"]
                    } for k, v in uuid_tab.items()
                }
            }

            f.write("config={}".format(str(config)))

        print("Written {}".format(dest_py))



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
            
        def mock_get_submission_detail(submission_id, testcase_id, submission_result_id):
            return cfg_inst.config['submission_detail'].copy()
        
        def mock_push_result(result, submission_id, testcase_id, submission_result_id):
            print("Result: {}".format(result))
        
        # inject in, this assumes judge.py is in ../
        BASE_PATH = os.path.join(os.path.realpath(__file__), "../")
        sys.path.append(BASE_PATH)

        import judge
        judge.push_result = mock_push_result
        judge.get_submission_detail = mock_get_submission_detail
        judge.download_file = mock_download_file

        # 1 stands for the submission result id, useless here
        judge.judge(cfg_inst.config['submission_id'], cfg_inst.config['testcase_id'], 1)

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

def fold(args):
    print("Running subcommand fold with name={}, testcase_files={}, problem_files={} and submit_files={}".format(
        args.name, args.testcase_files, args.problem_files, args.submit_files
    ))

    testcase_files = args.testcase_files.split(";")
    problem_files = args.problem_files.split(";")
    submit_files = args.submit_files.split(";")

    inst = JudgerTester()
    inst.fold_case(args.name, testcase_files, problem_files, submit_files)

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

    fold_parser = subparsers.add_parser('fold', help="Fold files into a given testcase")
    fold_parser.add_argument("name", help="name of the testcase")
    fold_parser.add_argument("testcase_files", help="files for testcase, separated with ; (eg. a.v;b.v)")
    fold_parser.add_argument("problem_files", help="files for problem, separated with ; (eg. a.v;b.v)")
    fold_parser.add_argument("submit_files", help="files for submit, separated with ; (eg. a.v;b.v)")
    fold_parser.set_defaults(func=fold)

    args = parser.parse_args()
    # https://docs.python.org/3/library/argparse.html#argparse.ArgumentParser.add_subparsers
    
    # Fix "AttributeError" bug when no arguments are given
    # ref: https://stackoverflow.com/questions/48648036/python-argparse-args-has-no-attribute-func
    #args.func(args)

    try:
        func = args.func
    except AttributeError:
        parser.error("too few arguments")
    func(args)

if __name__ == '__main__':
    main()
    # a = JudgerTester()
    # a.run_case("icarus_wave_cmp")