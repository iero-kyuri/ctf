# vagrant環境を引っ越しした際のメモ
CTF環境をvagrantに(ほぼ)すべて置いてるので, 新しいPCに引っ越しする際のメモ

## 環境
移行元:mac
移行先:windows

## 移行元でやること
 - `vagrant package`
  - package.boxというものを作り, これを持っていけば基本的に終わる.  
 - package.box, Vagrantfile を転送
  - USBメモリでも, オンラインストレージでも, なんでも

## 移行先でやること
 - package.box, Vagrantfileを好きな場所に設置
 - virtualboxのインストール
  - https://www.virtualbox.org/
 - vagrantのインストール
  - http://www.vagrantup.com/
 - `vagrant box add BOX_NAME ./package.box`
  - BOX_NAME は好きな名前
 - VagrantfileのBOX_NAMEを編集
  - config.vm.box = "hoge"
  - なんか微妙に違う表記だった気もする

## 起動確認
```
vagrant up
vagrant ssh
```
ができればok.  
ただしwindowsではsshが面倒なのでteratermかなにかを使う.  

## ToDo
bash on windowsからvagrantが使えればスムーズにsshまでできそうだが, virtualboxがうまく動かずに断念中.

## reference
[vagrant + virtualboxで作ったRuby環境を他のPCに環境移行する方法](http://qiita.com/htk_jp/items/e7ab14238bb11057817e)
