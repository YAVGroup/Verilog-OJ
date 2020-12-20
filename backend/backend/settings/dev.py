from .base import *

REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.AutoSchema',
    'DEFAULT_AUTHENTICATION_CLASSES': [

        # temporarily enable this to test api in django built-in coreapi docs
        # since SessionAuthentication checks for scrf_token, which the docs fail to 
        # give
        # TODO: comment on production
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'judge.judger_auth.JudgerAuthentication',
    ],
}

# Used by JudgerAuthentication, which sets auth to "Judger" and user to 
# django.contrib.auth.models.AnonymousUser.
# -- THIS SHOULD BE A SECRET! --
JUDGER_SECRET = 'c8fc82f3d6b6150692baaad61ae77abd29ab2d0379700443394cd41eca7ad5e2'

# Only IP in this range is allowed to be a valid judger in authentication
JUDGER_IP_WHITELIST = [
    '127.0.0.1'
]

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'xlb=+p_mb+z&=+4&++liz*ka_jc!ml8w#m+0jfbs0_8@4)s_w+'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# ---- Judger configurations ----

JUDGER_CONFIG = {
    'entry_file': './main.sh',             # entry file
    'final_score': './score.txt',          # the final score, in integer
    'submit_logs': True,
    'submit_appdata': True,
    'appdata_path': './appdata.txt',       # app data (if got)
    'possible_error_path': './possible_error.txt',           # The possible error collected
    'url_host': 'http://127.0.0.1:8000',   # here trailing / will affect performance, since
                                           # django will do 301 on this
    'judger_secret': JUDGER_SECRET,
    'use_docker': True,                    # True if run in docker, False otherwise
    'docker_image': 'judger-env:v1',
    'docker_judger_host_path': None,       # Assigned below
    'docker_host_dir': None,               # -v ${docker_judger_host_path}:${docker_host_dir}
    'docker_inside_dir': '/host_dir',      # -v ${docker_judger_host_path}/prob_id:/host_dir
    'max_time_limit': 10                   # second, this will override testcases whose value is greater
}

if JUDGER_CONFIG['use_docker']:
    if 'DOCKER_JUDGER_HOST_PATH' not in os.environ:
        raise Exception("Verilog OJ should have DOCKER_JUDGER_HOST_PATH passed by envvars")

    JUDGER_CONFIG['docker_judger_host_path'] = os.environ['DOCKER_JUDGER_HOST_PATH']

    if 'DOCKER_HOST_DIR' not in os.environ:
        raise Exception("Verilog OJ should have DOCKER_HOST_DIR passed by envvars")

    JUDGER_CONFIG['docker_host_dir'] = os.environ['DOCKER_HOST_DIR']

# ---- Celery configurations ----

BROKER_URL = 'amqp://guest:guest@localhost:5672//'