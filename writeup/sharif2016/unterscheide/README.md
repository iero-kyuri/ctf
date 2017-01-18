# Unterscheide(Crypto 200)

>See the attachment

# Write-up
与えられたencrypt.pyを読むと, flagをCBCモードのAESで暗号化した後に1bitずつ独自の方法で暗号化したものがenc.txtであることがわかる.  
このとき, bencとrandがわかればAESの復号ができflagが得られる.  
  
まずは, 未知数であるq,p1,p2,hについて, assertから以下のことが言える.  

- qは素数である
- q-1はp1,p2をともに因数に持つ
- p1,p2の差は10^8以下
- pow(h,1023*p1*p2,q) != 1

また, enc.txtの任意の2行の差をとったものから行数の差を引いたものがqの倍数となることが式展開をするとわかる.  
```
i行目:x * q * (rand + i) + (rand + i) + 1
j行目:y * q * (rand + j) + (rand + j) + 1
j行目 - i行目 = (y-x) * q * rand + y*q*j - x*q*i + (j-i)
j行目 - i行目 - (j-i) = q * ((y-x)*rand + y*j - x*i)
```  
このような計算をしたものを複数用意しgcdをとってやればqが導出できる.  
  
次に, q-1を素因数分解してやることでp1,p2が求まる.  
q-1は偶数のため2を因数に持つことがすぐにわかる.  
また, 条件よりp1,p2の差が比較的小さいことがわかっているため,(q-1)/2をフェルマー法により素因数分解することができる.  
さらに, enc.txtの1行目は x * q * rand + rand + 1となっているため, 1を引いてからqで割った余りを求めることでrandも導出することができる.  
  
以上より, q,p1,p2,randを求めることができた.  

一般にフェルマーの小定理より, qが素数であるとき以下のことが言える.  

> pow(a,q-1,q) == 1

今回の問題では, q-1 = 2 * p1 * p2であるから, pow(a,2 * p1 * p2,q) == 1 となる.  
つまり, pow(pow(h,r * r * p1,q),p2 * 2,q) == 1,pow(pow(h,s * s * p2,q),p1 * 2,q) == 1 となる.  
求めたパラメータから各行のpow()の値は計算できるので, p1とp2どちらを用いて上記の計算を行ったときに値が1になるかを調べることで, 元のbitが0か1かを判定することができる.  
  
bencが復元できたら後はrandからkeyを作ってAESの復号をすることでflagを得る.

# Other write-up

- [https://shiho-elliptic.tumblr.com/](https://shiho-elliptic.tumblr.com/)
- [https://galhacktictrendsetters.wordpress.com/2016/12/20/sharifctf-7-unterscheide/](https://galhacktictrendsetters.wordpress.com/2016/12/20/sharifctf-7-unterscheide/)

