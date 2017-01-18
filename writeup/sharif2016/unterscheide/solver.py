# -*- coding: utf-8 -*-
from m1z0r3 import *
import os
import gmpy
import random
from Crypto.Cipher import AES

fenc = map(int,open('enc.txt','r').read().split('\n'))

q = fenc[1] - fenc[0] - 1
for i,x in enumerate(fenc):
  if i < 2:
    continue
  q = gcd(q,fenc[i]-fenc[0]-i)
print "[+] q",q

(p1,p2) = fermat((q-1)/2)

print "[+] p1,p2",p1,p2

rand = (fenc[0]-1) % q
print "[+] rand",rand

benc = []
for x in fenc:
  if pow((x-1-rand)/(rand*q),p1*2,q) == 1:
    benc.append("1")
  elif pow((x-1-rand)/(rand*q),p2*2,q) == 1:
    benc.append("0")
  rand += 1

benc = "".join(benc)
flag_enc = n2s(int(benc,2))

key = n2s(rand)
iv = key[16:32]
mode = AES.MODE_CBC
aes = AES.new(key[:16], mode, IV=iv)
flag = aes.decrypt(flag_enc)
print flag
# ** SharifCTF{10ED2D76BCC417D9C48BE67F6790AF70}**
