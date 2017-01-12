# -*- coding: utf-8 -*-
import random
def modInv(a, m):
  g, x, y = egcd(a, m)
  if (g != 1):
    raise Exception("[-]No modular multiplicative inverse of %d under modulus %d" % (a, m))
  else:
    return x % m

def egcd(a, b):
  if (a == 0):
    return [b, 0, 1]
  else:
    g, y, x = egcd(b % a, a)
    return [g, x - (b // a) * y, y]

def brute(P,Q):
  """
  brute force attack
  @param  P Elliptic_Curve_point:base point
  @param  Q Elliptic_Curve_point:public key
  @return d secret key: Q = d*P
  """
  i = 1
  while P != Q:
    Q = Q - P
    i += 1
  return i

def baby_giant(P,Q,n):
  """
  baby step giant step method
  @param  P Elliptic_Curve_point:base point
  @param  Q Elliptic_Curve_point:public key
  @param  n Elliptic_Curve_Order:E.order()
  @return d secret key: Q = d*P
  """
  m = int(n**0.5)
  p = m*P
  glist = [Q - r*P for r in range(0,m)]
  for q in range(0,m):
    if q*p in glist:
      return m*q + glist.index(q*p)

def pollard_rho_method(P,Q,n):
  """
  pollard rho method
  @param  P Elliptic_Curve_point:base point
  @param  Q Elliptic_Curve_point:public key
  @param  n Elliptic_Curve_Order:E.order()
  @return d secret key: Q = d*P
  """
  def g(R):
    return Mod(R[0],m)

  def f(R):
    return g(R),R + M[g(R)]

  def pollard(P,Q):
    AB = [(1,1)]
    R = [P+Q]
    i = 0
    while True:
      idx,r = f(R[i])
      nAB = (Mod(AB[i][0]+ab[idx][0],n),Mod(AB[i][1]+ab[idx][1],n))
      if r in R:
        idx = R.index(r)
        if nAB[0] != AB[idx][0] and nAB[1] != AB[idx][1]:
          d = (nAB[0]-AB[idx][0])*modInv(int(AB[idx][1]-nAB[1]),n)
          return d
      R.append(r)
      AB.append(nAB)
      i += 1

  m = 20
  ab = [[random.randint(0,n),random.randint(0,n)] for x in range(m)]
  M = [ab[x][0]*P+ab[x][1]*Q for x in range(m)]
  return pollard(P,Q)

#=============
# test case 1
#=============
F.<a> = GF(229)
E = EllipticCurve(F,[1,44])
P = E([5,116])
Q = E([155,166])
n = E.order()

print "[+] brute",brute(P,Q)
"""
[+] brute 176

real    0m4.466s
user    0m1.562s
sys     0m1.179s
"""
print "[+] bsgs" ,baby_giant(P,Q,n)
"""
[+] bsgs 176

real    0m2.238s
user    0m1.426s
sys     0m0.834s
"""
print "[+] rho"  ,pollard_rho_method(P,Q,n)
"""
[+] rho 176

real    0m2.237s
user    0m1.434s
sys     0m0.824s
"""

#=============
# test case 2
#=============
F.<a> = GF(7654319)
E = EllipticCurve(F,[1234577,3213242])
P = E([5234568,2287747])
Q = E([2366653,1424308])
n = E.order()

print "[+] brute",brute(P,Q)
"""
[+] brute 1584718

real    1m57.437s
user    1m55.097s
sys     0m1.297s
"""
print "[+] bsgs" ,baby_giant(P,Q,n)
"""
[+] bsgs 1584718

real    0m21.262s
user    0m19.537s
sys     0m1.003s
"""
print "[+] rho"  ,pollard_rho_method(P,Q,n)
"""
[+] rho 1584718

real    0m48.260s
user    0m46.586s
sys     0m1.121s
"""
