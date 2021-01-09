import os, sys, socket
import cryptography, hashlib, rsa
import pickle
from cryptography.fernet import Fernet


class TA():

    def __init__(self):
        self.RSU0 = ""      # OK
        self.IDta = Fernet.generate_key()
        self.private = ""
        self.shared = ""

    def __str__(self):
        return "__TA class__"

    def __del__(self):
        del self
    ############################## getters
    def get_RSU0(self):
        return self.RSU0

    def get_IDta(self):
        return self.IDta

    def get_private(self):
        return self.private

    def get_shared(self):
        return self.shared

    ############################## setters
    def set_RSU0(self, tmp):
        if tmp != self.RSU0:
            self.RSU0 = tmp

    def set_IDta(self, tmp):
        if tmp != self.IDta:
            self.IDta = tmp

    def set_private(self, tmp):
        if tmp != self.private:
            self.private = tmp

    def set_shared(self, tmp):
        if tmp != self.shared:
            self.shared = tmp

    ####################################################### functions
    def refresh(self):
        # key = Fernet.generate_key()
        # public and private key
        public, private = rsa.newkeys(512)
        # generate shared key

        shared = Fernet.generate_key()

        return [public, shared, private]

    def cupdate(self):
        return self.refresh()

    def sign(self, cupdate):
        # hashed = []
        # for h in cupdate:
        #     tmp = "{}".format(h)
        #     hashed.append()
        hashed = [hashlib.sha256("{}".format(h).encode()).hexdigest() for h in cupdate]
        return hashed


if __name__ == '__main__':

    ta = TA()
    host = "127.0.0.1"
    port = 12345
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    s.listen(5)
    print("Server launched ...")

    while True:
        conn, addr = s.accept()
        print('Connected by', addr)
        data = conn.recv(1024)
        if not data: break
        print("======= data = ", data.decode())
        tmp = ta.cupdate()
        signed = ta.sign(tmp)
        final = tmp
        for sign in signed:
            final.append(sign)
        final.append(ta.IDta)
        data = pickle.dumps(final)

        conn.sendall(data)
        print("=================================================")
        ta.set_RSU0(tmp[0])
        ta.set_shared(tmp[1])
        ta.set_private(tmp[2])
        conn.close()
