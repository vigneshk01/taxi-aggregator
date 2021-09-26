#flaskapp.wsgi
import sys
sys.path.insert(0, '/var/www/html/flaskapp/GitpayUp')

from api import app as application

