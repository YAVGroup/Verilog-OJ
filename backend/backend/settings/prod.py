from .base import *

import socket

REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.AutoSchema',
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'judge.judger_auth.JudgerAuthentication',
    ],
}

# Used by JudgerAuthentication, which sets auth to "Judger" and user to 
# django.contrib.auth.models.AnonymousUser.
# -- THIS SHOULD BE A SECRET! --
if 'VERILOG_OJ_JUDGER_SECRET' not in os.environ:
    raise Exception("Verilog OJ should have VERILOG_OJ_JUDGER_SECRET passed by envvars")

JUDGER_SECRET = os.environ['VERILOG_OJ_JUDGER_SECRET']

# Only IP in this range is allowed to be a valid judger in authentication
JUDGER_IP_WHITELIST = [
    '127.0.0.1',
    socket.gethostbyname("judgeworker")
]


# SECURITY WARNING: keep the secret key used in production secret!
if 'VERILOG_OJ_SECRET_KEY' not in os.environ:
    raise Exception("Verilog OJ should have VERILOG_OJ_SECRET_KEY passed by envvars")

SECRET_KEY = os.environ['VERILOG_OJ_SECRET_KEY']

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# Hmm, used for production debugging..
if 'VERILOG_OJ_PROD_DEBUG' in os.environ:
    DEBUG = True

if 'VERILOG_OJ_PUBLIC_HOST' not in os.environ:
    raise Exception("Verilog OJ should have VERILOG_OJ_PUBLIC_HOST passed by envvars")

ALLOWED_HOSTS = list(set([
    '127.0.0.1',
    'localhost',
    'backend',      # reference by hostname, used by judgeworker
    os.environ['VERILOG_OJ_PUBLIC_HOST']
]) | set(JUDGER_IP_WHITELIST))

# ---- Judger configurations ----

JUDGER_CONFIG = {
    'entry_file': './main.sh',             # entry file
    'final_score': './score.txt',          # the final score, in integer
    'submit_logs': True,
    'submit_appdata': True,
    'appdata_path': './appdata.txt',       # app data (if got)
    'possible_error_path': './possible_error.txt',           # The possible error collected
    'url_host': 'http://backend:8000/oj',  # here trailing / will affect performance, since
                                           # django will do 301 on this
    'judger_secret': JUDGER_SECRET,
    'use_docker': True,                    # True if run in docker, False otherwise
    'docker_image': 'judger-env:v1',
    'docker_judger_host_path': None,       # Assigned below
    'docker_host_dir': None,               # -v ${docker_judger_host_path}:${docker_host_dir}
    'docker_inside_dir': '/host_dir',       # -v ${docker_judger_host_path}/prob_id:/host_dir
    'max_time_limit': 60                   # second, this will override testcases whose value is greater
}

if JUDGER_CONFIG['use_docker']:
    if 'DOCKER_JUDGER_HOST_PATH' not in os.environ:
        raise Exception("Verilog OJ should have DOCKER_JUDGER_HOST_PATH passed by envvars")

    JUDGER_CONFIG['docker_judger_host_path'] = os.environ['DOCKER_JUDGER_HOST_PATH']

    if 'DOCKER_HOST_DIR' not in os.environ:
        raise Exception("Verilog OJ should have DOCKER_HOST_DIR passed by envvars")

    JUDGER_CONFIG['docker_host_dir'] = os.environ['DOCKER_HOST_DIR']

# ---- Celery configurations ----

if 'VERILOG_OJ_RABBITMQ_PASSWORD' not in os.environ:
    raise Exception("Verilog OJ should have VERILOG_OJ_RABBITMQ_PASSWORD passed by envvars")

BROKER_URL = 'amqp://user:' + os.environ['VERILOG_OJ_RABBITMQ_PASSWORD'] + '@mqserver:5672//'