# gdb-peda install
gdb-pedaをインストールした際のメモ.

## install
```
apt-get install binutils python2.7 perl socat git build-essential gdb gdbserver
git clone https://github.com/longld/peda.git ~/peda
echo source ~/peda/peda.py >> ~/.gdbinit
```
gdbを起動して, gdb-peda$ となりカラフルならok.

## エラーが起こる場合
おそらくgdbのバージョンが原因?  
一度gdbを削除して入れ直したら解決した.
```
sudo rm -r /usr/local/bin/gdb
sudo apt-get install gdb
```
