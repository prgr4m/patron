#!/path/to/python/bin/python

# edit this file appropriately to match destination environment
# optional path to your local python site-packages folder
import sys
sys.path.insert(0, '/path/to/python/lib/python_version/site-packages')

from flup.server.fcgi import WSGIServer
from {{cookiecutter.project_name}} import create_app

class ScriptNameStripper(object):
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        environ['SCRIPT_NAME'] = ''
        return self.app(environ, start_response)

created_app = create_app('production')
app = ScriptNameStripper(created_app)

if __name__ == '__main__':
    WSGIServer(app).run()


