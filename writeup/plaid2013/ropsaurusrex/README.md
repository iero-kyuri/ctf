# ropsaurusrex

> ROP ROP ROP ROP ROP ROP ROP

# Write-up
入力を求められて, 何か入力するとWINと表示されて終わるプログラム.  
明らかなBOF脆弱性があり, 適当にpattern文字列を突っ込むとoffset 140でEIPが奪えることがわかる.  
checksecの結果は以下の通り.  
```
CANARY    : disabled
FORTIFY   : disabled
NX        : ENABLED
PIE       : disabled
RELRO     : disabled
```

NXbitがたっているのでret2shellcodeはできないが, 問題名的にも明らかにROPをすることを考える.  
まずはlibcのアドレスをリークする必要があるが, これは_libc_start_mainあたりのgotをwriteしてやればよい. この際, writeからのreturn addressをmainの最初にしてやれば再び入力待ちの状態にもっていける.  

リークしたlibcのアドレスから, system関数と"/bin/sh"という文字列のアドレスを計算して, あとはret2libcするだけでおわり.  
なお"/bin/sh"が与えられたlibcにあることも確認済み.
