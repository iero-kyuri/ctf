# -*- coding:utf-8 -*-
import socket, struct, telnetlib
from fractions import *

#============================
# socket connection template
#============================
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

#===================
# standard function
#===================
def egcd(a, b):
 if (a == 0):
     return [b, 0, 1]
 else:
     g, y, x = egcd(b % a, a)
     return [g, x - (b // a) * y, y]

def modInv(a, m):
 g, x, y = egcd(a, m)
 if (g != 1):
     raise Exception("[-]No modular multiplicative inverse of %d under modulus %d" % (a, m))
 else:
     return x % m

def continued_fractions(n,e):
  cf = [0]
  while e != 0:
    cf.append(int(n/e))
    N = n
    n = e
    e = N%e
  return cf
 
def calcKD(cf):
  kd = list()
  for i in range(1,len(cf)+1):
    tmp = Fraction(0)
    for j in cf[1:i][::-1]:
      tmp = 1/(tmp+j)
      kd.append((tmp.numerator,tmp.denominator))
  return kd
 
def int_sqrt(n):
  def f(prev):
    while True:
      m = (prev + n/prev)/2
      if m >= prev:
        return prev
      prev = m
  return f(n)
 
def calcPQ(a,b):
  if a*a < 4*b or a < 0:
    return None
  c = int_sqrt(a*a-4*b)
  p = (a + c) /2
  q = (a - c) /2
  if p + q == a and p * q == b:
    return (p,q)
  else:
    return None

#============
# RSA cipher
#============
def common(c, e, n):
  """
  Common Modulus Attack
  @param  c lst: cipher
  @param  e lst: public exponent
  @param  n int: modulus
  @return m int: plain text
  """
  for i,e_a in enumerate(e):
    for j,e_b in enumerate(e[i:]):
      if gcd(e_a,e_b) == 1:
        break
    else:
      continue
    break
  a = egcd(e_a,e_b)
  c1 = c[i]
  c2 = c[j]
  if a[1] < 0:
    m = (pow(modInv(c1,n),a[1]*-1,n) * pow(c2,a[2],n)) % n
  elif a[2] < 0:
    m = (pow(c1,a[1],n) * pow(modInv(c2,n),a[2]*-1,n)) % n
  return m
 
def wiener(n,e):
  """
  Wiener's Attack
  @param  n int: modulus
  @param  e int: public exponent
  @return (p,q) tpl: prime numbers
  """
  kd = calcKD(continued_fractions(n,e))
  for (k,d) in kd:
    if k == 0:
      continue
    if (e*d-1) % k != 0:
      continue
    phin = (e*d-1) / k
    if phin >= n:
      continue
    ans = calcPQ(n-phin+1,n)
    if not ans is None:
      return (ans[0],ans[1])
  return None
