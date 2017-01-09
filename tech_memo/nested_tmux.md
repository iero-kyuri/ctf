# nested tmux
ターミナル(tmux) -> vagrant -> ubuntu  
という作業環境において,リモートでtmuxを使おうとするとローカルのtmuxと競合してうまく動かない問題.  

## solution
```:.tmux.conf
bind-key b send-prefix
```

## usage
ローカルもリモートもprefixはC-bとしたとき,  
C-b b %  
とすれば縦分割をしてやることができる.

# reference
[tmux nested tmux (tmux の中で tmux) を使う設定(備忘録)](http://blog.ccm-lulu.com/2013/02/tmux-nested-tmux-tmux-tmux.html)
[Practical Tmux](https://mutelight.org/practical-tmux)
