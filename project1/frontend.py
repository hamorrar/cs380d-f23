import xmlrpc.client
import xmlrpc.server
from socketserver import ThreadingMixIn
from xmlrpc.server import SimpleXMLRPCServer
from readerwriterlock import rwlock
import socket
from threading import Lock
from time import sleep

kvsServers = dict()
baseAddr = "http://localhost:"
baseServerPort = 9000

lock = Lock()

class SimpleThreadedXMLRPCServer(ThreadingMixIn, SimpleXMLRPCServer):
        pass

class FrontendRPCServer:
    ## put: This function routes requests from clients to proper
    ## servers that are responsible for inserting a new key-value
    ## pair or updating an existing one.
    def put(self, key, value):
        with lock:
            deleteserver = []
            for id in kvsServers:
                print("FE PUT KEY SERVERS: ", kvsServers)
                try:
                    kvsServers[id].put(key, value)
                except:
                    deleteserver.append(id)
            for s in deleteserver:
                kvsServers.pop(s)
        return "SUCCESS: FE PUT"

    ## get: This function routes requests from clients to proper
    ## servers that are responsible for getting the value
    ## associated with the given key.
    def get(self, key):
        with lock:
            deleteserver = []
            for id in kvsServers:
                try:
                    ret = kvsServers[id].get(key)
                    break
                except:
                    deleteserver.append(id)
            for s in deleteserver:
                kvsServers.pop(s)
        return ret

    ## printKVPairs: This function routes requests to servers
    ## matched with the given serverIds.
    def printKVPairs(self, serverId):
        with lock:
            try:
                ret = kvsServers[serverId].printKVPairs()
            except:
                return "ERR_NOEXIST"
        return ret

    ## addServer: This function registers a new server with the
    ## serverId to the cluster membership.
    def addServer(self, serverId):
        with lock:
            deadservers = []
            if len(kvsServers) > 0:
                for id in kvsServers:
                    kvsServers[serverId] = xmlrpc.client.ServerProxy(baseAddr + str(baseServerPort + serverId))
                    try:
                        kvsFromMember = kvsServers[id].printKVPairs()
                    
                        for kvp in kvsFromMember.splitlines():
                            sp = kvp.split(":")
                            key = sp[0]
                            val = sp[1]

                            # new one could crash/fail while being added
                            try:
                                kvsServers[serverId].put(key, val)
                            except:
                                kvsServers.pop(serverId)
                    except:
                        deadservers.append(id)
                        continue
                    #this breaks out of the outer for loop - if previous stuff is all good, dont need to loop again to reupdate
                    break
            else:
                kvsServers[serverId] = xmlrpc.client.ServerProxy(baseAddr + str(baseServerPort + serverId))
            for s in deadservers:
                kvsServers.pop(s)
        return "SUCCESS: FE ADD SERVER"

    ## listServer: This function prints out a list of servers that
    ## are currently active/alive inside the cluster.
    def listServer(self):
        with lock:
            if(len(kvsServers) == 0):
                return "ERR_NOSERVERS"
            ret = ""
            serverList = []
            deleteservers = []
            for serverId, rpcHandle in kvsServers.items():
                try:
                    rpcHandle.heart()
                    serverList.append(serverId)
                except:
                    deleteservers.append(serverId)
            for s in deleteservers:
                kvsServers.pop(s)
            for s in serverList:
                ret += str(s) + ","
            return ret[:-1]

    ## shutdownServer: This function routes the shutdown request to
    ## a server matched with the specified serverId to let the corresponding
    ## server terminate normally.
    def shutdownServer(self, serverId):
        with lock:
            kvsServers[serverId].shutdownServer()
            kvsServers.pop(serverId)

server = SimpleThreadedXMLRPCServer(("localhost", 8001))
socket.setdefaulttimeout(3)
server.register_instance(FrontendRPCServer())

server.serve_forever()
