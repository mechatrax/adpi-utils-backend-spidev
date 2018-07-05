adpi-utils-backend-spidev
=========================

SPI を利用して ADPi に搭載された ADC の操作を行うツール類を提供します。

## 提供ファイル
動作に必要な次のファイルがパッケージに含まれています。

* /lib/systemd/system/adpi-utils-backend-spidev.service  
  ADPi の初期化を行うサービスの設定ファイルです。

* /usr/lib/adpi-utils-backend-spidev/adpi-init.sh  
  起動時に ADPi の初期設定を行うファイルです。  

* /usr/lib/adpi-utils-backend-spidev/adpi-utils-backend-spidev.py  
  SPI を利用して ADPi の操作を行うスクリプトファイルです。

## 作成ファイル
  インストール時に次のファイルが作成されます。

* /usr/lib/adpi-utils/adpi-utils-backend  
  /usr/lib/adpi-utils-backend-spidev/adpi-utils-backend-spidev.py へのシンボリックリンクです。
