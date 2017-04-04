## Distributed Health App

## Setup

```
$ virtualenv flask
$ source flask/bin/activate
$ pip install -r requirements
```

### Start Server

```
$ ./run.py
```

### Interact with Server

```
$ import requests
$ requests.post('http://127.0.0.1:5000/update', data = {'key':'value'})
```
