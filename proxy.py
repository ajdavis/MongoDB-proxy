import traceback

import pymongo.errors
import mockupdb

# Assume MongoDB runs on localhost:27017, otherwise pass a URI to MongoClient().
client = pymongo.MongoClient()
# "Verbose" logs each message. Disable for speed.
server = mockupdb.MockupDB(
    auto_ismaster=True, request_timeout=9999999, port=5000, verbose=True)
server.run()

# "hello" is how clients detect if the server is part of a replica set, its
# wire protocol version, etc. I think we should fake the reply instead of
# proxying to avoid e.g. the client discovering MongoDB's IP address and
# connecting to it. Maybe this is unnecessary.
hello = client.admin.command("hello")  # Get MongoDB's reply to handshake command.
proxy_hello = {
    "setName": "mockupdb-replica-set",
    "setVersion": 1,
    "hosts": [server.address_string],
    "primary": server.address_string,
    "isWritablePrimary": True,
    "secondary": False,
    "maxBsonObjectSize": hello["maxBsonObjectSize"],
    "maxMessageSizeBytes": hello["maxMessageSizeBytes"],
    "maxWriteBatchSize": hello["maxWriteBatchSize"],
    "logicalSessionTimeoutMinutes": hello["logicalSessionTimeoutMinutes"],
    "minWireVersion": hello["minWireVersion"],
    "maxWireVersion": hello["maxWireVersion"],
}

print(f"Listening on {server.uri}")

# Process messages as they arrive. Single-threaded event loop.
for request in server:
    try:
        if request.command_name == "hello":
            request.reply(proxy_hello)
            continue

        # An example of command-specific processing.
        if request.command_name == "aggregate":
            print(f"Pipeline: {request['pipeline']}")  # Could edit the pipeline here.

        db_name = request["$db"]
        cmd = request.doc.copy()
        del cmd["$db"]
        try:
            reply = client.get_database(db_name).command(cmd)
        except pymongo.errors.OperationFailure as e:
            request.reply(e.details)  # Forward error message from MDB to client.
        else:
            request.reply(reply)
    except Exception as e:
        # Catch the error and keep serving. Control-C still kills me.
        traceback.print_exc()
