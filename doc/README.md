## Distributed Health App

Project for CSCI 5673

Our application anonymizes this data and uses it to match people with similar health conditions together. Our design uses a Hybrid P2P approach to enable the peers to discover each other through data correlation techniques. These peers can share their health statistics for anonymous comparisons. We also allow them to form groups to allow messaging or group broadcasts.

## Local Setup

```
$ virtualenv flask
$ source flask/bin/activate
$ pip install -r requirements.txt
```

### Start Server

Start the Flask server in the virtual environment

```
$ ./run.py
```

### Start Client

Start the application client

```
$ ./client.py
```

## Cluster Setup

Running this application with a Streaming Spark for large scale data processing requires that the Flask Server and Storm Master be on the same machine. Complete Java implementation for Spark is included in a tar file

The Storm Implementation is at https://github.com/ReedAnders/nearest_vector
