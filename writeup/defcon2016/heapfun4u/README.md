# heapfun4u

> Guess what, it is a heap bug.
> file heapfun4u_873c6d81dd688c9057d5b229cf80579e.quals.shallweplayaga.me:3957

# Write-up
(しばらく解けなくてwrite upしたので自力で解いたのは途中まで)  
NXbitが有効な実行ファイル.  
実際に動かしてみると, メモリ確保/解放/書き込みが可能であり, Nice guyという謎の機能もあることがわかる. 確保したメモリ領域やNice guyによりstackと思われるアドレスは出力される.  
中身を見てみると, 独自のメモリアロケータが実装されている.  
確保されるchunkの構造を把握するためにAlloc/Freeを繰り返していると, だいたい以下の構造になっていることがわかる.  

```
Size(8byte):chunk_size. malloc_chunk同様下位3bitは特殊な用途と思われる. 最下位bitは自身のuseフラグ.  
Data:ユーザの使うdata領域.  
bk:free時のみ存在. free_listの前のchunk.  
fd:free時のみ存在. free_listの次のchunk.
```

freeなchunkをまとめておくfree_listが存在していると思われる.  
chunkをfreeするたびにこのlistに入れていき, 割りあてるときはこのlistを最後に追加した要素から順に見ていってsizeが合えば割りあてる(?)  

## Vulnerability
適当に動かしていると, 解放したメモリにも書き込み可能なUse-After-Free脆弱性があることがすぐにわかる.  
これにより, free_chunkに存在するbk,fdをoverwriteすることが可能.  
その後unlink処理を走らせれば, 任意のアドレスを任意の値で書き換えることができる.  

## exploit
メモリアロケータによって確保される領域は実行可能であることから, ここにシェルコードを置いたchunkを作り, そこにRIPを飛ばすことを考える. また, Nice guyによってstackのアドレスがわかることから, main関数からのreturn addressが格納されたアドレスも計算できる. したがって, unlinkによってreturn addressを書き換えてシェルコードへ飛ばす.  
通常のmalloc/freeでは, free_chunk直下のchunkをfreeするときにunlink処理が走るが, 今回のアロケータではおそらく異なる.(?)  
だが, free_listを持っていることから, listの中央あたりにあるchunkをallocしようとすればlistから外す処理が入ると思われるため, それを利用してunlink attackを行う.  
今回用いた具体的なchunkの構造は以下のようになる.  

```
# [U] = use, [F] = free  
chunk1(128):[U], shellcode
chunk2(64):[F], fd/bk overwrite
chunk3(32):[U]
chunk4(32):[F], dummy chunk
chunk5(32):[U]
```

まず, chunk2のbkはshellcodeを指すように, fdはchunk4のdata部分を指すようにoverwriteする.  
chunk4のdata部分には, [main関数からのreturn address - 自身のアドレス + 8]を入れておく. これは, unlink処理の際に以下のような処理が入るためである.  
```
chunk2->fd + chunk2->fd->size - 8 = chunk2->bk
```
data部分にdummyのchunk_hdrを作ることでunlink処理でうまく書き換えられるようにする. 

この状態でfree_listは以下のようになっている.  
```
mmap_chunk -> chunk2 -> chunk4
```
つまり, chunk2をallocする処理を入れればunlinkされるため, size=64でallocをする.  
これでmain関数からのreturn addressを書き換えることができたため, あとはexitをすればシェルがとれる.  

## shell code
なお, unlinkの際に以下のような処理も入る.  
```
chunk2->bk + chunk2->bk->size = chunk2->fd
```
つまり, シェルコードの先頭8byteが数値として見たときに小さな値をとっている必要がある.  
そこで, jmp命令(\xeb)を用いたshellcodeを使った.(通常のshellcodeの先頭に, 6ワード分jmpさせる命令とNULLバイトを入れただけ)

## solver
[solver.py](https://github.com/iero-kyuri/ctf/blob/master/writeup/defcon2016/heapfun4u/solver.py)
