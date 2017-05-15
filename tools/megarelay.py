import socket
import select
import os
import sys
import time

megarelay = sys.modules[__name__]
history = []
sockets = []
sockets2 = []
connid = 1
backlog = []

def get_prev_timestamp():
    if len(backlog) == 0:
        megarelay.basis_time = time.monotonic()
        return basis_time
    return basis_time + sum([i[-1] for i in backlog])
                
def main():
    megarelay.bind = socket.socket()
    bind.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
    bind.bind(('0.0.0.0',445))
    bind.listen(25)
    sockets2.append(bind)
    while True:
        readers, _, _ = select.select(sockets2,[],[],0)
        if bind in readers:
            print("Accepting a connection")
            accepted = bind.accept()
            out = socket.socket()
            out.connect(('172.16.99.2',445))
            sockets.append({"socket" : accepted[0], "addr" : accepted[1], "out" : out, "stream" : connid})
            backlog.append(("connect",connid,time.monotonic() - get_prev_timestamp()))
            megarelay.connid+=1
            sockets2.append(accepted[0])
            sockets2.append(out)
        for i in readers:
            if i is bind:
                continue
            b = [j for j in sockets if j['socket'] is i]
            if b:
                b = b[0]
                try:
                    data = b['socket'].recv(1500)
                except ConnectionResetError:
                    data = b''
                if data == b'':
                    backlog.append(("close", b['stream'], time.monotonic() - get_prev_timestamp()))
                    print("Closing from left, ",b['stream'])
                    b['out'].close()
                    sockets2.remove(b['out'])
                    sockets2.remove(b['socket'])
                    continue
                b['out'].send(data)
                backlog.append(("send", b['stream'], data, time.monotonic() - get_prev_timestamp()))
                print("Sending from left", b['stream'], data)
            else:
                b = [j for j in sockets if j['out'] is i][0]
                try:
                    data = b['out'].recv(1500)
                except ConnectionResetError:
                    data = b''
                if data == b'':
                    print("Closing from right, ", b['stream'])
                    b['socket'].close()
                    sockets2.remove(b['out'])
                    sockets2.remove(b['socket'])
                    continue
                b['socket'].send(data)
                backlog.append(('recv', b['stream'], time.monotonic() - get_prev_timestamp()))
                print("Sending from right", b['stream'])

if __name__ == "__main__":
    main()
