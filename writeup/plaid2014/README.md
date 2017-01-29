# ezhp

> Luckily when you travel back in time, you still get to use all your knowledge from the present. With that knowledge in hand, breaking into this service (at 54.81.149.239:9174) owned by The Plague shouldn't be hard at all.
> 
> Hint: the heap allocator is really, really bad.

# Write-up
自作のメモリアロケータが実装されたnoteアプリっぽいやつ. 以下メニュー.  
```
1 to add a note.
2 to remove a note.
3 to change a note.
4 to print a note.
5 to print.
```
1でメモリ確保, 2で解放, 3で書き込み, 4で表示, 5で終了というわかりやすい構成.  
適当に確保してheapを確認すると, 1つのchunkは以下の構成になっていることがわかる.  
```
size:(最下位bitが自身のuse判定?)
fd
bk
user_area
```
また, メモリ確保時と書き込み時の両方でsizeが入力できることから, 試しに書き込み時に大きなsizeを指定するとオーバーフローすることがわかる.  

このことから, fd bkを上書きしてunlink attackすることを考える. putsのgotをoverwriteしてheap中に用意したshellcodeに飛ばす.  
しかし, ASLRが有効であるためheapのアドレスを特定する必要がある.  
これに関しては残りの機能であるprintを使う.  
書き込む際にfd bkを上書きせずにギリギリまで書き込んでからprintすることでfd bkがわかる. このbkを見ればshellcodeの置かれたアドレスがわかる.
