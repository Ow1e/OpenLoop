"""
Saphhire tools for making node.py look nice
"""

def packet(name, auth, data):
    return {
        "PACKET": name,
        "DATA": data,
        "AUTH": auth
    }

def finalize(*args):
    arr = []
    for i in args: arr.append(i)
    return {
        "packets": arr
    }

def gettype(packet):
    return packet["PACKET"]

def getdata(packet):
    return packet["DATA"]

def getauth(packet):
    return packet["AUTH"]

SIGNIN = "SAPPHIRE_SIGNIN" # Send to for clearence for the client
START_SEND = "SAPPHIRE_AUTH_TRUE" # For returning clearence from host
PING = "ping"