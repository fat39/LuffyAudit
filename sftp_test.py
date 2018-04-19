# -*- coding:utf-8 -*-

import paramiko

t = paramiko.Transport(("1.1.1.40",22))
t.connect(username="root",
          password="toor", )
sftp = paramiko.SFTPClient.from_transport(t)


try:
    sftp.stat("/tmp/2.txt")
    sftp.get("/tmp/2.txt","1.txt")
except:
    pass
print("haha")
t.close()