adpi-utils-backend-spidev
=========================

SPI を利用して ADPi に搭載された ADC の操作を行うツール類を提供します。

## 提供ファイル
次のファイルがパッケージに含まれています。

### /lib/udev/rules.d/85-adpi-utils-backend-spidev.rules  
ADPi のデバイスを定義した設定ファイルです。

### /lib/systemd/system/adpi-utils-backend-spidev-init<span>@</span>.service  
ADPi の初期化を行うサービスの設定ファイルです。

### /usr/lib/adpi-utils-backend-spidev/adpi-init.sh  
起動時に ADPi の初期設定を行うファイルです。

### /usr/lib/adpi-utils-backend-spidev/adpi-utils-backend-spidev.py  
SPI を利用して ADPi の操作を行うスクリプトファイルです。

### /usr/share/doc/adpi-utils-backend-spidev/changelog.gz
パッケージの変更履歴を記録したファイルです。

### /usr/share/doc/adpi-utils-backend-spidev/copyright
著作権とライセンスを記載したファイルです。

## 作成ファイル
インストール時に次のファイルが作成されます。

### /usr/lib/adpi-utils/adpi-utils-backend  
/usr/lib/adpi-utils-backend-spidev/adpi-utils-backend-spidev.py へのシンボリックリンクです。
