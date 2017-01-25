# pake (crypto 250?)

> see the pake.rb

# Write-up

PAKE(Password Authenticated Key Exchange)が実装されている.  
これは, パスワードベースのDH鍵共有のようなものであり, 具体的な計算はソースコードやコメント中のリンク先を見てもらいたい.  

まずやることとして, サーバに対してコネクションを2つ貼りPAKEを成立させる.  
すると, 各コネクションから同じ暗号文が返ってくることがわかる.(違ったらうまくできていない)  

次に, パスワードの1つ1つは1~16と総当たりできそうな数であることに注目する.  
最後の暗号文は, 具体的に以下のようにして求まる.  

```
flag_enc = flag ^ 0 ^ Round1_key ^ Round2_key ... ^ Round11_key
```

正しいPAKEが成立する場合, すべてのRoundでkeyが一致するためflag_encも等しくなる. 
1つのパスワードを総当たりによって求めたいとき, ある1Roundのみkeyが異なることになる.  
仮にRound1のkeyを総当たりしている場合, 最終的に以下のようなflag_enc'が双方から送られてくることになる.  
```
flag_enc'1 = X ^ Round1_key'1
flag_enc'2 = X ^ Round1_key'2
```

ただしXはRound1_key以外のxor結果である.  
ここで, Round1_key'1とRound1_key'2がそれぞれのbbの値と一致していた場合, flag_enc'1 ^ bb1とflag_enc'2 ^ bb2の値が一致する. この場合総当たりが成功している.  

つまり, 総当たりとしてw = pow(password,2,p)を送ってやればよい.  
このとき, サーバでは pow(w,b,p)が計算されるため, bbに等しい値がxorされるはずである.  
このようにして1つずつパスワードを求めていき, 最後は取得したパスワードを元にサーバと1対1でPAKEを行い復号するだけである.  

# flag
hitcon{73n_w34k_p455w0rd5_c0mb1n3d_4r3_571ll_wE4k_QQ}

# ToDo
Proof of Work ができない
