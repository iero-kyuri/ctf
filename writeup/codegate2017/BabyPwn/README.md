# 下調べ
つなぐとこんな感じ

```
▒▒▒▒▒▒▒C▒O▒D▒E▒G▒A▒T▒E▒2▒0▒1▒7▒▒▒▒▒▒▒
▒▒▒▒▒▒▒B▒A▒B▒Y▒P▒W▒N▒!▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒
▒▒▒▒▒▒▒G▒O▒O▒D▒L▒U▒C▒K▒~▒!▒▒▒▒▒▒▒▒▒▒▒
===============================
1. Echo
2. Reverse Echo
3. Exit
===============================
Select menu > 
```

それぞれの動きは書いてある通りで, 1は入力したものをそのまま出力し, 2はreverseして出力する.  
checksec結果は以下の通り.  

```
gdb-peda$ checksec
CANARY    : ENABLED
FORTIFY   : disabled
NX        : ENABLED
PIE       : disabled
RELRO     : Partial
```

また, fork-sever型である.  
個人的にfork-server型の問題を解いたのははじめてだったので, メモがてら後ほどまとめる.  
# vulnerability
入力を100文字うけつけているが, たくさん入力するとcanaryが破壊されることからバッファオーバーフローできることがわかる.  
なのでスタックの状況を見てみると, オフセット40からcanary, 56からmainのreturn addressをoverwriteできることがわかる.  

# exploit
canaryのnullバイトまでを潰すように入力することでcanaryを出力させることでリークできる.  
同様に, stackにつまれているアドレスを出力させることでstackのアドレスもリークできる.  
fork-server型であることからこの辺の値はずっと同じであるため, 1回の接続で1個リークすればよい.  
あとはsystemにret2pltしてシェルをとるだけ.  

# fork-server
はじめて触れたので個人的メモ.  
gdbでデバッグする際は, set follow-fork-mode child とすることで子プロセスを追いかけてくれる.  
これをした状態でacceptまで進めて, ncすればデバッグ可能.  
ついでに, alarmが邪魔なときは deactive alarm を入れとくといいかもしれない.

# FLAG

```
$ python solver.py
[+] canary cc781900
[+] arg addr ffca6f34
[+] exit
 ls
babypwn
flag
cat flag

Time Out!
FLAG{Good_Job~!Y0u_@re_Very__G@@d!!!!!!^.^}
exit
*** Connection closed by remote host ***
```
