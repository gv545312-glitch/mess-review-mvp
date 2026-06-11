import serverless_wsgi
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app import app

def handler(event, context):
    return serverless_wsgi.handle_request(app, event, context)
