import os

if os.environ.get('VERILOG_OJ_DEV', 'FALSE') == 'TRUE':
   from .dev import *
else:
   from .prod import *