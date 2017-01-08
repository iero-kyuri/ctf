#!/usr/bin/python
# -*- coding:utf-8 -*-
import socket, struct, telnetlib

#=====================
# socket connection
#=====================
def sock(remoteip, remoteport):
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  s.connect((remoteip, remoteport))
  return s, s.makefile('rw', bufsize=0)

def read_until(f, delim='\n'):
  data = ''
  while not data.endswith(delim):
    data += f.read(1)
  return data

def shell(s):
  t = telnetlib.Telnet()
  t.sock = s
  t.interact()

def p32(a): return struct.pack("<I",a)
def u32(a): return struct.unpack("<I",a)[0]
def p64(a): return struct.pack("<Q",a)
def u64(a): return struct.unpack("<Q",a)[0]
