# https://www.learndatasci.com/tutorials/how-stream-text-data-twitch-sockets-python/
import socket
import numpy as np
import time
from params import CONST
from time_statistics import time_statistics


def event_loop():
    print("Going into while loop" + 3*"\n")
    while True:
        resp: str = sock.recv(byte_size).decode('utf-8')

        if resp.startswith('PING'):
            sock.send("PONG\n".encode('utf-8'))
            if verbose > 0: print("Sent twitch a pong")
        elif len(resp) > 0:
            map_out = list(map(lambda x: x.startswith(f":{p.target}!"), resp.split("\n")))
            if any(map_out): # Found user
                
                if t is not None: # Append time
                    dt = time.time() - t
                    t = time.time()
                    T.append(dt)
                    if verbose > 0: print(f"logged delta = {dt:.3f} s")
                else: # Validate user 
                    counter += 1
                    if counter > n_validation_msgs:
                        print("Initialized timer")
                        t = time.time()

                if (verbose > 1) and (len(T) % 10 == 0) and (len(T) > 0):
                    np_T = np.array(T)
                    print(f"mean = {np_T.mean():.3f} s, std = {np_T.std(ddof=0):.3f} s")


if __name__ == "__main__":

    # Internal variables
    byte_size = 2048
    n_validation_msgs = 5
    counter = 0
    p = CONST()
    T = []
    t = None
    verbose = 0 # 0 = no, 1 = delta & PONG, 2 = mu & std

    # Establish socket
    sock = socket.socket()
    sock.connect((p.server, p.port))
    sock.send(f"PASS {p.token}\n".encode('utf-8'))
    sock.send(f"NICK {p.nickname}\n".encode('utf-8'))
    sock.send(f"JOIN {p.channel}\n".encode('utf-8'))

    time.sleep(5)

    try:
        event_loop()
    except KeyboardInterrupt:
        time_statistics(T)