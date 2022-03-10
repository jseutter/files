# Python

## Print certificates path in Python
### if using Requests
python -c "import certifi; print(certifi.where())"
### if using old stuff
python -c "import ssl; print(ssl.get_default_verify_paths())"

## Adding a custom cert to Certifi (for Requests)
https://incognitjoe.github.io/adding-certs-to-requests.html

## Printing exception tracebacks
```
import traceback

try:
    1/0
except Exception as e:
    print(traceback.format_exc())
```

## Logging everything that the requests module sees
```
import requests

import logging
import contextlib
try:
    from http.client import HTTPConnection # py3
except ImportError:
    from httplib import HTTPConnection # py2

def debug_requests_on():
    '''Switches on logging of the requests module.'''
    HTTPConnection.debuglevel = 1

    logging.basicConfig()
    logging.getLogger().setLevel(logging.DEBUG)
    requests_log = logging.getLogger("requests.packages.urllib3")
    requests_log.setLevel(logging.DEBUG)
    requests_log.propagate = True

def debug_requests_off():
    '''Switches off logging of the requests module, might be some side-effects'''
    HTTPConnection.debuglevel = 0

    root_logger = logging.getLogger()
    root_logger.setLevel(logging.WARNING)
    root_logger.handlers = []
    requests_log = logging.getLogger("requests.packages.urllib3")
    requests_log.setLevel(logging.WARNING)
    requests_log.propagate = False

@contextlib.contextmanager
def debug_requests():
    '''Use with 'with'!'''
    debug_requests_on()
    yield
    debug_requests_off()

debug_requests_on()
requests.get('http://google.com')
```
