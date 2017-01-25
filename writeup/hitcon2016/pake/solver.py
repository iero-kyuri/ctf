# -*- coding: utf-8 -*-
from m1z0r3 import *
from hashlib import sha512

def hash(n):
  return int(sha512(str(n)).hexdigest(),16)

ip = "localhost"
port = 4444

p = 285370232948523998980902649176998223002378361587332218493775786752826166161423082436982297888443231240619463576886971476889906175870272573060319231258784649665194518832695848032181036303102119334432612172767710672560390596241136280678425624046988433310588364872005613290545811367950034187020564546262381876467
passwords = [None] * 11
for i in range(11):
  for x in range(17): 
    s1,f1 = sock(ip,port)
    s2,f2 = sock(ip,port)
    for j in range(11):
      read_until(f1,"Server send ")
      read_until(f2,"Server send ")
      a = int(read_until(f1)[:-1])
      b = int(read_until(f2)[:-1])

      if i != j:
        s1.send(str(b)+"\n")
        s2.send(str(a)+"\n")
      else:
        test_password = pow(hash(x),2,p)
        s1.send(str(test_password)+"\n")
        s2.send(str(test_password)+"\n")
        a1 = hash(a)
        b1 = hash(b)

    read_until(f1,"Flag is (of course after encryption :D): ")
    read_until(f2,"Flag is (of course after encryption :D): ")
    r1 = int(read_until(f1)[:-1])
    r2 = int(read_until(f2)[:-1])

    if r1 ^ a1 == r2 ^ b1:
      print "[+] found!!"
      print "password",i,"is",x
      passwords[i] = x
      break

print "[+] brute force done"
print "[+] password is",passwords
s1.close()
s2.close()

s,f = sock(ip,port)
read_until(f) # p = %d
key = 0
for i in range(11):
  read_until(f) # Round %d
  read_until(f,"Server send ") # Server send %d
  a = int(read_until(f)[:-1])
  s.send(str(pow(hash(passwords[i]),2,p))+"\n")
  key ^= hash(a)
read_until(f,"Flag is (of course after encryption :D): ")
flag = int(read_until(f)[:-1])
print "[+] key",key
flag ^= key
print "[+] flag",flag
print n2s(flag)
