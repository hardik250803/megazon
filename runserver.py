"""
This script runs the PRML application using a development server.
"""

from os import environ
from PRML import app

if __name__ == '__main__':
    HOST = environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(environ.get('SERVER_PORT', '4785'))
    except ValueError:
        PORT = 4785
    app.run(HOST, PORT)
