from .base import *

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    # SQLite
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
    # MySQL
    # 'default': {
    #     'ENGINE': 'django.db.backends.mysql',
    #     'NAME': 'VerilogOJ',
    #     'USER':'mysql',
    #     'PASSWORD':'mysql',
    #     'HOST':'localhost',
    #     'PORT':'',
    # }
}

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
    '127.0.0.1'
]


# SECURITY WARNING: keep the secret key used in production secret!
if 'VERILOG_OJ_SECRET_KEY' not in os.environ:
    raise Exception("Verilog OJ should have VERILOG_OJ_SECRET_KEY passed by envvars")

SECRET_KEY = os.environ['VERILOG_OJ_SECRET_KEY']

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = [
    '127.0.0.1'
]