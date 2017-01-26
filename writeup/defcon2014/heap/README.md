# heap

# Write-up
Dougle Lee mallocが実装された問題.  
最初に20個ほどmallocされ, 入力後にすべてfreeされていく.  
size=260で入力しろと言われるが, 普通にオーバーフロできる.

古いmallocなので, 古典的なUnlink Attackをするだけ.  
printf@pltを書き換えてret2shellcodeする.  

Unlink Attackの概要については[コチラ](https://github.com/iero-kyuri/ctf/blob/master/binary/unlink_attack.md)を参照.  

入力するchunkから3つ分のchunkに対して以下のようなことを行う.

## 1つ目のchunk
size=260とprintされるが, 厳密にはsize=264(chunkヘッダ含)のため, 256文字埋めるとこのchunkが埋まる. solver.py中では, 次のchunkのprev_sizeにあたる部分まで書き込むため"A"*260としている. 

## 2つ目のchunk
このchunkのfd,bkに相当する部分をいじる. まず, prev_sizeについては前のchunkがusedなため必要ない(既に書き込んである).   
sizeについては, このchunk全体のsizeを入れてやればよい. これはプログラムの出力したsizeを利用すればよい. ただし, 乱数でmallocしているが, malloc内部では8バイトアラインメントしているため同様にアラインメントし, 直前のchunkがusedなため最下位1bitをたててやる. なお, sizeにはchunkヘッダも含めるため, 最後に+8する必要がある.  

fdには, 書き換えたいメモリ - 8 を入れてやる. fd->bk = bk という処理が走るため-8バイトする必要がある.  
bkには, 書き込みたい値を入れてやればよい. ただし, bk->fd = fd という処理も走ることに注意が必要である. これについては後ほど触れる.  
あとのchunkの残り部分は適当に埋めてやる. sizeはわかっているため, 埋めるのは容易である. 

## 3つ目のchunk
2つ目のchunkはfreed chunkと偽装する必要があり, その偽装はこのchunkで行う.  
まずはprev_sizeに該当するメンバを埋める. これは2つ目のchunkのsizeで良い.  
次に, 3つ目のchunkのsizeを入れる. このとき, 2つ目のchunkをfreed chunkとするため, 最下位bitは立てないようにする.  
その後にシェルコードを埋め込んでおわり. (たぶん, シェルコードは1つ目のchunkに入れてもok)  

## シェルコードについて
unlinkの際の, bk->fd = fd という処理により, シェルコードの一部が書きかわってしまう.  
具体的には, bkがシェルコードの先頭を指しているため, 先頭から4バイトの位置が書きかわる.  
今回用いているシェルコードは以下の通りである.  
```
xor edx edx
push XXXXXXXX # このpushするものが書きかわる
pop edi
push "//sh"
push "/bin"
...
```
不要なゴミがpushされるので, 一旦edx以外の適当なレジスタにpopしてから改めてpushし直すことで/bin/shを作った.
