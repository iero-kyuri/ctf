# -*- coding: utf-8 -*- from m1z0r3 import *
from m1z0r3 import *
import os
import gmpy
import random
from Crypto.Cipher import AES

fenc = map(int,open('enc.txt','r').read().split('\n'))

#===============================
# q : prime
# q-1 % p1 == 0
# q-1 % p2 == 0
# p2 - p1 < 10**8
# h^(1023*p1*p2) mod q != 1
## a^(p-1) mod p == 1 より, q != 1023*p1*p2 + 1
#==============================

# flag_enc がわかればok
# randもわかるからkeyもわかって復号できる

# first = rand * (q * x + 1)
#       = rand * q * x + rand
# last  = (rand+382) * (q * y + 1)
#       = rand * (q * y + 1) + 382 * (q * y + 1)
#       = rand * q * y + rand + 382 * q * y + 382
# last - first = rand * q * y + 382 * q * y + 382 - rand * q * x
#              = rand * q * (y-x) + 382 * q * y + 382
#              = q * (rand+() + 382 *y) + 382
# last - first - 382 = rand * q * (y-x) + 382 * q * y
#                    = q * (rand*(y-x) + 382*y)

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
h = 2

benc = []
for x in fenc:
  tmp = (x - 1 - rand)/(rand*q)
  a = pow(tmp,p1*2,q)
  b = pow(tmp,p2*2,q)
  if a == 1:
    benc.append("1")
  elif b == 1:
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
