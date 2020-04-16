from judge.celery import app
from celery.utils.log import get_task_logger

from judge.judge import judge

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
def do_judge_task(submission_id):
    ''' Do judgement on submission with id given '''
    # todo: save result by calling POST on the model
    logger.info("do_judge_task() called!")
    return judge(submission_id)