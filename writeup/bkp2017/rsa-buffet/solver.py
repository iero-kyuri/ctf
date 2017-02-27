from m1z0r3 import *
from Crypto.Cipher import PKCS1_OAEP, AES
from secretsharing import PlaintextToHexSecretSharer as SS
import functools

def decrypt(p,q,c):
  msg_header = c[:512]
  msg_iv = c[512:528]
  msg_body = c[528:]
  e = 65537
  d = rsa(p,q)
  private_key = RSA.construct(map(long,(p*q, e, d)))
  symmetric_key = PKCS1_OAEP.new(private_key).decrypt(msg_header)
  if len(symmetric_key) != 32:
    return None
  return AES.new(symmetric_key,mode=AES.MODE_CFB,IV=msg_iv).decrypt(msg_body)

n = []
c = []
for i in range(10):
  n.append(openssl_public_read('key-'+str(i)+'.pem').n)
for i in range(1,6):
  with open('ciphertext-'+str(i)+'.bin') as f:
    c.append(f.read())

x = []
y = []
z = []

# key-2.pem, ciphertext-1.bin
p = 2758599203
q = n[2] // p
m = decrypt(p,q,c[0])
x.append(m.split('\n')[1])
y.append(m.split('\n')[2])
z.append(m.split('\n')[3])
print m
"""
Congratulations, you decrypted a ciphertext!  One down, two to go :)
1-32a1cd9f414f14cff6685879444acbe41e5dba6574a072cace6e8d0eb338ad64910897369b7589e6a408c861c8e708f60fbbbe91953d4a73bcf1df11e1ecaa2885bed1e5a772bfed42d776a9
1-e0c113fa1ebea9318dd413bf28308707fd660a5d1417fbc7da72416c8baaa5bf628f11c660dcee518134353e6ff8d37c
1-1b8b6c4e3145a96b1b0031f63521c8df58713c4d6d737039b0f1c0750e16e1579340cfc5dadef4e96d6b95ecf89f52b8136ae657c9c32e96bf4384e18bd8190546ff5102cd006be5e1580053
1-c332b8b93a914532a2dab045ea52b86d4d3950a990b5fc5e041dce9be1fd3912f9978cad009320e18f4383ca71d9d79114c9816b5f950305a6dd19c9f458695d52
"""

# key-0.pem & key-6.pem, ciphertext-3.bin
p = gcd(n[0],n[6])
q = n[0] // p
m = decrypt(p,q,c[2])
x.append(m.split('\n')[1])
y.append(m.split('\n')[2])
z.append(m.split('\n')[3])
print m
"""
Congratulations, you decrypted a ciphertext!  One down, two to go :)
3-17e568ddc3ed3e6fe330ca47a2b27a2707edd0e0839df59fe9114fe6c08c6fc1ac1c3c8d9ab3cf7860dac103dff464d4c215e197b54f0cb46993912c3d0220a3eb1b80adf33ee2cc59b0372c
3-b69efb4f9c5205175a4c9afb9d3c7bef728d9fb6c9cc1241411b31d4bd18744660391a330cefa8a86af8d2b80c881cfa
3-572e70c5acfbe8b4c2cbd47217477d217da88c256ff2586af6a18391972c258bbea6143e7cd2ff6d39393efeb64d51d9318a2c337e50e2d764a42173bc3a1d5c7c8f24b64043daf5d2a8e9f4
3-e9e6850880eb0a44d36fe9f2e5a458c6da3977b7fcd285afa27e9bfc116b1408570991504116b81864b03a7060bfd5d3fb6e007bb346f276d749befd545d1489c4
"""

# key-1.pem, ciphertext-5.bin
(p,q) = fermat(n[1])
m = decrypt(p,q,c[4])
x.append(m.split('\n')[1])
y.append(m.split('\n')[2])
z.append(m.split('\n')[3])
print m
"""
Congratulations, you decrypted a ciphertext!  One down, two to go :)
5-7d29041c468b680fcff93c16011a2869f17de75b929b787503b412becde0321ec72fe1e499f2150a1dacb9a5f701c0b37470049dd560cef5163543469817971f50782f763f0b05ab7088f7ae
5-a7a1e271cf263279cece532b540545fa539b0f3650e2929163b02ee5459debdc53c1e07149eb2153015bb5c88e6270e8
5-149480c5c75cbe320564adfa432ac8ea241e048ed39c8bc6be14ca80c392487f43a7882075d785d62cb314ea6c89a6b5f28adfa56ec481e124567b88241de2a6cabcc7ec9de3acac8be5375b
5-7285289084282d559573f68eef10191091d76d6670014202670651f867cd2bc8640a86eef1c1e482affc7ae801fa446956c2186972fb6b7bac88c91d050c9d3cca
"""

print SS.recover_secret(x)
print SS.recover_secret(y)
print SS.recover_secret(z)
# FLAG{ndQzjRpnSP60NgWET6jX}
