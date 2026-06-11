import json
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

def handler(event, context):
    try:
        import serverless_wsgi
        from app import app
        return serverless_wsgi.handle_request(app, event, context)
    except Exception as e:
        return {
            "statusCode": 500,
            "body": str(e)
        }
