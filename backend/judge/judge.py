from submission.models import Submission, SubmissionResult
import re
import random
import string
import subprocess
import sys
import time
import filecmp


def generate_submit_zone():
    generated_name = "SUBMIT_ZONE_"
    generated_name += time.asctime().replace(' ', '-').replace(':', '')
    generated_name += ''.join(random.sample(string.ascii_letters +
                                            string.digits, 8))
    subprocess.run("mkdir " + generated_name, shell=False)
    return generated_name


def get_file(uuid):
    pass


def get_file_path(uuid):
    pass


def unzip_file(uuid, path):
    pass


def perform_judge(task_struct):
    task_file = get_file(task_struct.file.uuid)
    task_file_path = task_file.path
    task_file_name = task_file.name

    # Generate an empty directory
    submit_zone_path = generate_submit_zone()

    task_standard_output_path = get_file(task_struct.task_id.uuid).path
    task_submit_script_path = get_file(task_struct.script_uuid).path
    task_submit_script_name = get_file(task_struct.script_uuid).name

    # task_file_type - boolean type
    # True  - type = v
    # False - type = zip
    task_file_type = (task_file_name.find('.zip') is None)

    # Unzip or copy submission file to target directory
    if not task_file_type:
        unzip_file(task_file, submit_zone_path)
    else:
        try:
            subprocess.run("cp" + " {source_file} {target_path}".format(
                source_file=task_file_path, target_path=submit_zone_path), shell=False)
        except OSError as e:
            print("Failed to copy submission files: ", e, file=sys.stderr)

    # Copy standard output file to target directory
    try:
        subprocess.run("cp" + " {source_file} {target_path}".format(
            source_file=task_standard_output_path, target_path=submit_zone_path), shell=False)
    except OSError as e:
        print("Failed to copy standard output: ", e, file=sys.stderr)

    # Copy submit script to target directory
    try:
        subprocess.run("cp" + " {source_file} {target_path}".format(
            source_file=task_submit_script_path, target_path=submit_zone_path), shell=False)
    except OSError as e:
        print("Failed to copy submit script: ", e, file=sys.stderr)

    time_record = -1

    # Yosys to generate our output
    try:
        subprocess.run("bash " + " {script_name}".format(
            script_name=task_submit_script_name), shell=False)
    except OSError as e:
        print("Yosys Failed: ", e, file=sys.stderr)


def get_iverilog_output(problem_id):
    pass


def get_iverilog_script(problem_id):
    pass


def get_submit_file_test():
    pass


def perform_judge_iverilog_version(submission):
    submit_zone_path = generate_submit_zone()
    # submit_file = submission.submit_files
    submit_file = get_submit_file_test()

    # submit_problem = submission.problem

    # iverilog_output = get_iverilog_output(submit_problem.id)
    # iverilog_script = get_iverilog_script(submit_problem.id)

    iverilog_output = get_iverilog_output(1)
    iverilog_script = get_iverilog_script(1)

    try:
        subprocess.run("cp" + " {source_file} {target_path}".format(
            source_file=iverilog_output, target_path=submit_zone_path), shell=False)
    except OSError as e:
        print("Failed to copy standard output: ", e, file=sys.stderr)

    try:
        subprocess.run("cp" + " {source_file} {target_path}".format(
            source_file=iverilog_script, target_path=submit_zone_path), shell=False)
    except OSError as e:
        print("Failed to copy submit script: ", e, file=sys.stderr)

    try:
        subprocess.run("bash {script}".format(
            script=iverilog_script), shell=False)
    except OSError as e:
        print("Failed to execute submit script: ", e, file=sys.stderr)


def judge(submission_id):
    """
    评测某个提交。生成若干SubmissionResult，之后Submission就会被更新。
    """
    # TODO: 对某个提交进行评测
    # pass
    print("foo")
    return "good"
