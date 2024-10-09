# MongoDB Change Stream Experiments

Two sample apps for working with MongoDB change streams.

## app.py

This will generate some random data and write to a MongoDB collection. It writes one entry every minute.

## change.py

This will listen to the change stream of the collection and print out the changes.
