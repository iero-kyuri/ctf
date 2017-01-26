# About
ここでは, 古いmalloc/freeに対してのUnlink Attackについて述べる.  
[mallocの説明](https://github.com/iero-kyuri/ctf/blob/master/binary/malloc.md)で, mallocによって確保されるchunkの構造について述べた.  
Unlink Attackとは, ヒープオーバーフローにとってchunkメンバのfd,bkを書き換えてしまう攻撃である.  

# Unlink
確保済みのchunkをfreeするとき, メモリ上で直後のchunkがfree済みの場合は以下のようにunlinkと呼ばれる機能が起こる. ただし, P,P2は以下のように配置されているとする. 
```
|------|
|  P   |
|(used)|
|------|
|  P2  |
|(free)|
|------|
```
今P2はarenaのbinsにリンクリストとして繋がれている. リンクを表すのはP2->fd,P2->bkメンバである.  
Pをfreeするとき, メモリのフラグメントを防ぐためにPとP2をまとめて1つのchunkとしつつリンクリストを以下のように更新する.  
```
P2->fd->bk = P2->bk
P2->bk->fd = P2->fd
```

# Unlink Attack
Pへの入力によってヒープオーバーフローを起こし, P2を上書きできる状況を考える. すると, P2->fd, P2->bkも上書きできる.  
このときPをfreeすることでunlinkが発生すると, 書き換えたfd, bkの指すアドレスを書き換えることができる.  
これによりwritableな領域なら任意の箇所を書き換えることができてしまう攻撃.  

# 具体例
- [DEF CON 2014 heap - writeup](https://github.com/iero-kyuri/ctf/tree/master/writeup/defcon2014/heap)

# ToDo
- unsafe unlink attack
- fastbins unlink attack
