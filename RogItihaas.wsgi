import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/var/www/RogItihaas/")

from RogItihaas import app as application
application.secret_key = '@13@6$$#ddfccv'
