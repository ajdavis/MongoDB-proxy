# MongoDB proxy

An example of a proxy that receives MongoDB commands from a client over TCP-IP and forwards them
to a MongoDB server, then forwards MongoDB's replies to the client. This can be the basis of a
proxy that changes MongoDB's behavior by editing requests or replies. Slow and single-threaded.
Not for production use.

Built in Python using the [MockupDB](https://github.com/mongodb-labs/mongo-mockup-db) library.
