import argparse
import xmlrpc.client
import xmlrpc.server

serverId = 0
basePort = 9000


class KVSRPCServer:
    # TODO: You need to implement details for these functions.

    def __init__(self):
        self.kvs = dict()

    ## put: Insert a new-key-value pair or updates an existing
    ## one with new one if the same key already exists.
    def put(self, key, value):
        self.kvs[key] = value
        return "SUCCESS: SERVER PUT"
        # return "[Server " + str(serverId) + "] Receive a put request: " + "Key = " + str(key) + ", Val = " + str(value)

    ## get: Get the value associated with the given key.
    def get(self, key):
        ret = self.kvs.get(key, "ERR_KEY")
        if ret == "ERR_KEY":
            return "ERR_KEY"
        return str(key) + ":" + str(ret)

    ## printKVPairs: Print all the key-value pairs at this server.
    def printKVPairs(self):
        ret = ""
        for key in self.kvs:
            ret += str(key) + ":" + str(self.kvs[key]) + "\n"
        return ret
    
    ## catchup: This function makes a request to a server 
    ## in the membership to get the new server up to date.
    def catchup(self):
        ret = ""
        for key in self.kvs:
            ret += 1
        return self.kvs
        #return "SUCCESS: SERVER CAUGHT UP"
    
    ## shutdownServer: Terminate the server itself normally.
    def shutdownServer(self):
        return "[Server " + str(serverId) + "] Receive a request for a normal shutdown"

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = '''To be added.''')

    parser.add_argument('-i', '--id', nargs=1, type=int, metavar='I',
                        help='Server id (required)', dest='serverId', required=True)

    args = parser.parse_args()

    serverId = args.serverId[0]

    server = xmlrpc.server.SimpleXMLRPCServer(("localhost", basePort + serverId))
    server.register_instance(KVSRPCServer())

    server.serve_forever()
