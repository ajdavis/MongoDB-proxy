# MongoDB proxy

An example of a proxy that receives MongoDB commands from a client over TCP-IP and forwards them
to a MongoDB server, then forwards MongoDB's replies to the client. This can be the basis of a
proxy that changes MongoDB's behavior by editing requests or replies. Slow and single-threaded.
Not for production use. Built in Python using the [MockupDB](https://github.com/mongodb-labs/mongo-mockup-db) library.

Install the packages in `requirements.txt`. Start a real MongoDB server on localhost on the default port of 27017. Then run `python3 proxy.py`. Install [mongosh](https://www.mongodb.com/docs/mongodb-shell/) and run `mongosh mongodb://localhost:5000` to connect to the proxy. Or in a separate Python interpreter:

```
from pymongo import *
client = MongoClient(port=5000)
client.db.collection.insert_one({})
print(list(client.db.collection.aggregate(pipeline=[])))
```
