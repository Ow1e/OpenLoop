"""
The Sapphire protocol, made for transmiting p2p data through OpenLoop Core servers
"""

from p2pnetwork.node import Node
import openloop.sapphire.package as package
from datetime import datetime
import logging

def example_check(auth):
    return True

def disable_check(auth):
    return False

class Sapphire(Node):
    def __init__(self, host, port, auth, check=example_check, id=None, callback=None, max_connections=0):
        super(Sapphire, self).__init__(host, port, id, callback, max_connections)
        self.pointer = None
        self.auth = auth
        self.pings = {}
        self.filters = {}
        self.authed = False
        self.check = check

    def outbound_node_connected(self, connected_node):
        self.pointer = connected_node
        signin = package.packet(package.SIGNIN, self.auth, {})
        self.send_to_node(connected_node, package.finalize(signin))

    def send_pointer(self, type, data):
        if not self.authed:
            logging.warning("Sending a message without a authentication welcome (SAPPHIRE_AUTH_TRUE)")
        self.send_to_node(self.pointer, package.finalize(package.packet(type, self.auth, data)))
        
    def node_message(self, connected_node, data):
        for i in data.get("packets", []):
            if self.check(package.getauth(i)):
                if self.debug:
                    print(i)
                if package.gettype(i)==package.SIGNIN:
                    self.send_to_node(
                        connected_node,
                        package.finalize(package.packet(
                                package.START_SEND, self.auth, {}
                        ))
                    )
                elif package.gettype(i)==package.START_SEND:
                    self.authed = True
                elif package.gettype(i)==package.PING and package.getdata(i)=="ping":
                    self.send_to_node(connected_node, package.finalize(package.packet("ping", self.auth, "pong")))
                else:
                    packet = i
                    if package.gettype(i) in self.filters:
                        for filter in self.filters[package.gettype(i)]:
                            fil = filter(packet)
                            if fil!=None:
                                packet = fil

                    if self.pointer!=None:
                        self.send_to_node(self.pointer, package.finalize(i))
