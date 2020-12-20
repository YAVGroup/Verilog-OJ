from judge.celery import app
from celery.utils.log import get_task_logger
import os, sys

import judge.executor.local
import judge.executor.docker

# To call:
# - run celery first (in the same folder with manage.py)
#   - celery -A judge worker -l INFO
# python3 manage.py shell
# >>> from judge.tasks import do_judge_task
# >>> do_judge_task.delay(1212)
# <AsyncResult: efdf51cb-148b-4796-a02b-817015b103df>
# >>> 

logger = get_task_logger(__name__)

@app.task
def do_judge_task(detail, judger_config):
    """
    Do judgement on submission with id given
    TODO: pass judger config struct
    """
    # todo: save result by calling POST on the model
    logger.info(
        "Called with submission_id={}, testcase_id={}, submission_result_id={}".format(
            detail['id'], 
            detail['testcase']['id'],
            detail['submission_result']['id']
        ))

    executor = None
    if judger_config['use_docker']:
        executor = judge.executor.docker.DockerExecutor
    else:
        executor = judge.executor.local.LocalExecutor

    inst = executor(detail, judger_config)
    inst.prepare()
    inst.run()
