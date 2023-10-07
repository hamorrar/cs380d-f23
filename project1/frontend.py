import xmlrpc.client
import xmlrpc.server
from socketserver import ThreadingMixIn
from xmlrpc.server import SimpleXMLRPCServer
import random
from readerwriterlock import rwlock
import socket
from time import sleep

kvsServers = dict()
baseAddr = "http://localhost:"
baseServerPort = 9000

rw = rwlock.RWLockFair()
# rlock = rw.gen_rlock()
# wlock = rw.gen_wlock()

class SimpleThreadedXMLRPCServer(ThreadingMixIn, SimpleXMLRPCServer):
        pass

class FrontendRPCServer:
    # TODO: You need to implement details for these functions.

    ## put: This function routes requests from clients to proper
    ## servers that are responsible for inserting a new key-value
    ## pair or updating an existing one.
    def put(self, key, value):
        with rw.gen_wlock():
            problem = None
            for id in kvsServers:
                try:
                    problem = id
                    ret = kvsServers[id].put(key, value)
                except:
                    kvsServers.pop(problem)
        return "SUCCESS: FE PUT"

    ## get: This function routes requests from clients to proper
    ## servers that are responsible for getting the value
    ## associated with the given key.
    def get(self, key):
            serverId = key % len(kvsServers)
            return kvsServers[serverId].get(key)

    ## printKVPairs: This function routes requests to servers
    ## matched with the given serverIds.
    def printKVPairs(self, serverId):
        return kvsServers[serverId].printKVPairs()

    ## addServer: This function registers a new server with the
    ## serverId to the cluster membership.
    def addServer(self, serverId):
        with rw.gen_wlock():
            if len(kvsServers) > 0:
                firstID = random.choice(list(kvsServers.keys()))
                # print(firstID)
                kvsServers[serverId] = xmlrpc.client.ServerProxy(baseAddr + str(baseServerPort + serverId))

                kvsFromMember = kvsServers[firstID].printKVPairs()
                
                for kvp in kvsFromMember.splitlines():
                    sp = kvp.split(":")
                    key = sp[0]
                    val = sp[1]

                    kvsServers[serverId].put(key, val)
                
            else:
                kvsServers[serverId] = xmlrpc.client.ServerProxy(baseAddr + str(baseServerPort + serverId))
        return "SUCCESS: FE ADD SERVER"

    ## listServer: This function prints out a list of servers that
    ## are currently active/alive inside the cluster.
    def listServer(self):
        serverList = []
        for serverId, rpcHandle in kvsServers.items():
            try:
                rpcHandle.heart()
            except:
                continue
            serverList.append(serverId)
        return serverList

    ## shutdownServer: This function routes the shutdown request to
    ## a server matched with the specified serverId to let the corresponding
    ## server terminate normally.
    def shutdownServer(self, serverId):
        result = kvsServers[serverId].shutdownServer()
        kvsServers.pop(serverId)
        return result

server = SimpleThreadedXMLRPCServer(("localhost", 8001))
socket.setdefaulttimeout(3)
server.register_instance(FrontendRPCServer())

server.serve_forever()
