activate_this = '/home/sthomson/code/semviz/env/bin/activate_this.py'
execfile(activate_this, dict(__file__=activate_this))

import sys
sys.path.append('/home/sthomson/code/semviz')

from semviz.web_app import app as application
