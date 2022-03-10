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
import sys

try:
    1/0
except Exception as e:
    print(traceback.format_exc())
```
