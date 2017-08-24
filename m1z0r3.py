# -*- coding:utf-8 -*-
import socket, struct, telnetlib
import gmpy
import string
import itertools
from PIL import Image
from tqdm import tqdm
from fractions import gcd, Fraction
from Crypto.Util.number import bytes_to_long
from Crypto.Util.number import long_to_bytes
from Crypto.PublicKey import RSA
from steganography.steganography import Steganography

#===========
# shellcode
#===========
shellcode_x86 = "\x31\xd2\x52\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x52\x53\x89\xe1\x8d\x42\x0b\xcd\x80"
unlink_shellcode_x86 = "\x31\xd2\x52\x68\x2f\x2f\x73\x68\x5f\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x52\x53\x89\xe1\x8d\x42\x0b\xcd\x80"
shellcode_x64 = "\x48\x31\xd2\x52\x48\xb8\x2f\x62\x69\x6e\x2f\x2f\x73\x68\x50\x48\x89\xe7\x52\x57\x48\x89\xe6\x48\x8d\x42\x3b\x0f\x05"
jmp_shellcode_x64 = "\xeb\x06\x00\x00\x00\x00\x00\x00\x48\x31\xd2\x52\x48\xb8\x2f\x62\x69\x6e\x2f\x2f\x73\x68\x50\x48\x89\xe7\x52\x57\x48\x89\xe6\x48\x8d\x42\x3b\x0f\x05"


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
def n2s(n):
  return long_to_bytes(n)

def s2n(s):
  return bytes_to_long(s)

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

def openssl_public_read(fname):
  with open(fname,'r') as f:
    key = RSA.importKey(f.read())
  return key

def chinese_remainder(n, a):
  sum = 0
  prod = reduce(lambda a, b: a*b, n)
  for n_i, a_i in zip(n, a):
    p = prod / n_i
    sum += a_i * mul_inv(p, n_i) * p
  return sum % prod

def mul_inv(a, b):
  b0 = b
  x0, x1 = 0, 1
  if b == 1: return 1
  while a > 1:
    q = a / b
    a, b = b, a%b
    x0, x1 = x1 - q * x0, x0
  if x1 < 0: 
    x1 += b0
  return x1

def continued_fraction(n,d):
  cf = []
  while d:
    q = n//d
    cf.append(q)
    n,d = d,n-d*q
  return cf

def convergents_of_contfrac(cf):
  n0, n1 = cf[0], cf[0]*cf[1]+1
  d0, d1 = 1, cf[1]
  yield (n0,d0)
  yield (n1,d1)
  for i in xrange(2,len(cf)):
    n2,d2 = cf[i]*n1+n0, cf[i]*d1+d0
    yield (n2,d2)
    n0,n1 = n1,n2
    d0,d1 = d1,d2

def int_sqrt(n):
  def f(prev):
    while True:
      m = (prev + n/prev)/2
      if m >= prev:
        return prev
      prev = m
  return f(n)
 
def xor(a,b):
  r = ""
  for x,y in zip(a,b):
    r += chr(ord(x)^ord(y))
  return r

def pad(m,block_size = 16):
  return m + (chr(block_size - len(m) % block_size) * (block_size - len(m) % block_size))

def unpad(m):
  return m[:-ord(m[-1])]

def int_sqrt(n):
	def f(prev):
		while True:
			m = (prev + n/prev)/2
			if m >= prev:
				return prev
			prev = m
	return f(n)

def fermat(n):
	x = int_sqrt(n) + 1
	y = int_sqrt(x*x - n)
	while True:
		w = x*x - n -y*y
		if w == 0:
			return (x-y,x+y)
		elif w > 0:
			y = y+1
		else:
			x = x+1
			y = int_sqrt(x*x-n)

#============
# RSA cipher
#============
def rsa(p,q,e=65537):
  """
  RSA Cipher
  @param  p int: prime number1
  @param  q int: prime number2
  @param  e int: public exponent
  @return d int: secret key
  """
  phi = (p-1) * (q-1)
  return modInv(e,phi)

def common(c1, c2, e1, e2, n):
  """
  Common Modulus Attack
  @param  c int: cipher
  @param  e int: public exponent
  @param  n int: modulus
  @return m int: plain text
  """
  gcd, s1, s2 = gmpy.gcdext(e1, e2)
  if s1 < 0:
    s1 = -s1
    c1 = gmpy.invert(c1, n)
  elif s2 < 0:
    s2 = -s2
    c2 = gmpy.invert(c2, n)
  v = pow(c1, s1, n)
  w = pow(c2, s2, n)
  m = (v * w) % n
  return m
 
def wiener(e,n):
  """
  Wiener's Attack
  @param  e int: public exponent
  @param  n int: modulus
  @return d int: private key
  """
  cf = continued_fraction(e,n)
  convergents = convergents_of_contfrac(cf)
  for k,d in convergents:
    if k == 0:
      continue
    phi, rem = divmod(e*d-1,k)
    if rem != 0:
      continue
    s = n-phi+1
    D = s*s - 4*n
    if D>0 and gmpy.is_square(D):
      return d

def hastad(c,n):
  """
  Hastad's Broacast Attack
  @param  c lst: cipher text
  @param  n lst: modulus
  @return m int: plain text
  """
  e = len(n)
  crt = chinese_remainder(n,c)
  return int(gmpy.mpz(crt).root(e)[0].digits())

#============
# morse code
#============
TABLE={'A':'.-','B':'-...','C':'-.-.','D':'-..','E':'.','F':'..-.','G':'--.','H':'....','I':'..','J':'.---','K':'-.-','L':'.-..','M':'--','N':'-.','O':'---','P':'.--.','Q':'--.-','R':'.-.','S':'...','T':'-','U':'..-','V':'...-','W':'.--','X':'-..-','Y':'-.--','Z':'--..','1':'.----','2':'..---','3':'...--','4':'....-','5':'.....','6':'-....','7':'--...','8':'---..','9':'----.','0':'-----','.':'.-.-.-',',':'--..--',':':'---...','?':'..--..',"'":'.----.','-':'-....-','(':'-.--.',')':'-.--.-','/':'-..-.','=':'-...-','+':'.-.-.','"':'.-..-.','@':'.--.-.'}
RTABLE = dict(map(lambda(k,v):(v,k), TABLE.items()))
def morse_encode(s):
  return ' '.join(map((lambda x: TABLE[x]), list(s.upper())))
def morse_decode(s):
  return ''.join(map((lambda x: RTABLE[x]), s.split(" ")))

#=======
# rot n
#=======
def caesar(text,key=13):
  low = string.ascii_lowercase
  up = string.ascii_uppercase
  ret = ""
  for c in text:
    if c in low:
      ret += low[(low.index(c)+key)%len(low)]
    elif c in up:
      ret += up[(up.index(c)+key)%len(up)]
    else:
      ret += c
  return ret

#===============
# Steganography
#===============
def steg_solve(fname):
  solve1 = Steganography.decode(fname)
  im = Image.open(fname)
  width,height = im.size
  secretdata = ''
  for y in range(height):
    for x in range(width):
      (r,g,b) = im.getpixel((x,y))
      secretdata += str(r&1) + str(g&1) + str(b&1)
  solve2 = "".join([chr(int(secretdata[i:i+8],2)) for i in range(0,len(secretdata),8)])
  return (solve1,solve2)

#=============
# brute force
#=============
printable = string.letters + string.digits + string.punctuation

def printable_generator(n):
  for s in printable,repeat=n):
    yield s
