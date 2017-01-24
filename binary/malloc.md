# Overview
heap問を解くにあたり, まずは一番基本となるmalloc/freeのメモリ管理についての個人的メモ.  
何か違ってたら教えてください.  

# arena
mallocによってheap領域からメモリが確保されるが, どこから確保するかなどを管理している機構がarena.  
data領域に存在する.  
main_arenaというものがデフォルトで定義されており, 他のarenaは必要に応じて作成される.
main_arenaだけ知っておけばおそらく大丈夫なのでここではmain_arenaに絞って話しを進める.  
arenaはmalloc_state構造体の変数として定義されているが, そのうち重要なメンバを以下にまとめる. (ここは随時追加予定)  

```
struct malloc_state{
  INTERNAL_SIZE_T max_fast;
  mfastbinptr fastbins[NFASTBINS];
  mchunkptr top;
  mchunkptr bins[NBINS * 2];
}
``` 

### max_fast
後述のfastbinsに登録するメモリの最大サイズ.

### fastbins
小さい要求メモリに対して, 素早くメモリ確保をできるように用意されたchunkのリストヘッダの配列. 単方向リスト.

### top
次にmallocが呼ばれた際に, おそらく返すことになるであろうchunkのポインタ.  
厳密には, max_fast以上mmap_threshold以下の要求サイズで, かつunsorted_chunksから適切なsizeのchunkが見つからなかったときにここからchunkを切り出す.(?)

### bins
max_fastよりも大きいサイズのchunkを登録するリストヘッダの配列.  
NBINS=128であり, リストヘッダはfd,bkで1組のため128個のリストヘッダからなる配列.  
ヘッダ0は空.  
ヘッダ1(index=2,3)はunsorted chunkとして使われる. fastbins対象でないchunkは解放時に一旦ここに登録され, 次にmallocが呼ばれた際にここに登録されたchunkが確保対象でないとなった段階でbinsに登録される. これは, 同じサイズのメモリ確保が発生しやすいという特性を活かし, 効率を上げるための仕組み. LIFO.(キャッシュの局所参照性. malloc動画の47分前後参照.)  
ヘッダ2(index=4,5)からが通常のchunk登録用. ヘッダ64以上はサイズの大きいchunk(512B以上)登録用. chunkのサイズによってindexを変える. size * 8 = indexとなるように登録される.  
size<=512 ... small bin  
size> 512 ... large bin  


# chunk
mallocした際に確保されるメモリの塊.  
以下のような構造体がchunkヘッダとして定義される.

```
struct malloc_chunk {
  INTERNAL_SIZE_T      prev_size;
  INTERNAL_SIZE_T      size; 
  struct malloc_chunk* fd; 
  struct malloc_chunk* bk;
```
 
### prev_size
**メモリ上で**直前のchunkのsize.  
ただし, 直前のchunkがfreeな場合のみ格納される.
 
### size
ヘッダも含めた自信のchunk全体のsize.  
mallocによりメモリが確保される際, 8バイトアラインメントされるため, sizeの下位3bitは必ず0になる. そこで, 下位3bitはそれぞれ以下のような特別な意味のフラグである.  

```
下位1bit目：PREV_INUSE (直前のchunkが使用中)
下位2bit目：IS_MMAPED (mmapにより確保されたchunk)
下位3bit目：NON_MAIN_ARENA (main_arena以外のarenaから確保されたchunk)
```

### fd,bk
未使用のchunkでありbinsに登録されている場合, そのリンクリストの前後の要素へのポインタが格納される. リンクリストの最初, 最後はそれぞれmain_arenaへのポインタとなるが, binsのアドレスではなくその8バイト前となる. これは, chunkとして見た場合, fd,bkメンバが先頭から8バイトの位置にあるためである.  
未使用chunkであるということは, **メモリ上で**直後のchunkにはprev_sizeが存在する.
使用中のchunkには存在しない.  

# Refernce
- [malloc(3)のメモリ管理構造](http://www.valinux.co.jp/technologylibrary/document/linux/malloc0001/)
- [The 67th Yokohama kernel reading party](https://www.youtube.com/watch?v=0-vWT-t0UHg)

