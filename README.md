# 8vana: The visualization tool of security incidents like retro games.

 ![8vana_logo](./images/8vana_logo_github.jpg)  

English page is coming soon!!  

## 概要
我々は”**セキュリティのインシデントをリアルタイムにレトロゲーム風に可視化**”するツール「**8vana**(ハチバーナ)」を開発しました。セキュリティインシデントを可視化するツールは既に幾つも存在しますが、「UIが馴染まない」「ハイスペックな動作環境が必要」「費用が高い」などのハードルが往々にしてあるため、誰でも気軽に扱えるツールは多くはありませんでした。  

そこで、我々の8vanaは”**会いに行けるインシデント可視化ツール**”をコンセプトに、UIとエンジンをレトロゲーム風にすることで「**ユーザフレンドリーなUI**」と「**低スペックでも動作可能**」を実現、そして「**OSSとして公開**」することで、誰でも気軽にお使い頂ける多くの工夫を行いました。我々は、8vanaを世界中の多くの方々に使っていただき、インシデント・レスポンスの裾野を広げ、**世の中のインシデント対処に少しでも多く貢献する**ことを目指しています。  

なお、8vanaはインシデントを可視化できるという特性上、あなたがお使いの**Offensiveツールの挙動や攻撃シミュレーションをも可視化**できます。すなわち、あなたの**ツールデモやCTF、サイバーセキュリティ演習などで8vanaを使う**ことができ、これにより素晴らしいアイキャッチ効果を得ることも可能です。  

 ![8vana_overview](./images/8vana_overview.png)  

## システム構成
 ![](./images/design.png)  

## インストール手順

### Pyxelのインストール
Pyxelをインストールするには、事前にPythonのバージョン3.7以降をインストールしておく必要があります。  

```
$ pip install -U pyxel
```

### 8vanaのインストール
8vanaを本リポジトリからCloneし、任意のディレクトリに展開します。  

```
$ git clone https://github.com/8vana/8vana.git
```

## 使用方法
8vanaは、外部の監視ツールが出力した（セキュリティ・インシデントを含む）ログファイルを8vana形式のログに正規化する「**Ultimate Log Parser**」と「**レンダリングエンジン**」から構成されます。また、レンダリングエンジンは、現在2つのレンダリングモード（1vana、2vana）が実装済みです。  

 * Ultimate Log Parser  
 外部監視ツールが出力したログを8vanaに最適化されたログ形式に正規化するパーサー。  

 * 1vana  
 計算され尽くしたUIを備え、サイバーな雰囲気を感じることができるレンダリングモード。  

 * 2vana  
 某戦車RPG風のUIを備え、攻撃者と監視対象システムが相対しているような雰囲気を
醸し出すレンダリングモード。  

以下、各機能の使用方法を解説します。  

### Ultimate Log Parser
#### Ultimate Log Parserを起動する
```
$ cd 8vana
$ python3 ./Ultimate_Log_parser.py
```

Ultimate Log Parserが起動されると、予め設定された監視対象ログを定期的にチェックし、ログを8vanaに最適化されたJSON形式に変換して新たに保存します。以下にJSON形式に変換されたログの一例を示します。  

```
[
  {
    "phase": "Discover",
    "attack": "nmap",
    "time": 1555784308.0,
    "from": "172.31.200.91",
    "to": "172.31.101.30",
    "note": {
      "option": "",
      "CVE": [
        "N/A"
      ]
    }
  },
  {
    "phase": "Discover",
    "attack": "nmap",
    "time": 1555784308.0,
    "from": "172.31.200.91",
    "to": "172.31.101.30",
    "note": {
      "option": "",
      "CVE": [
        "N/A"
      ]
    }
  }
]
```

本ログの要素、`phase`, `attack`, `time`, `from`, `to`, `note` は必須項目であり、監視対象ログにこれらの情報が含まれない場合は、イベントを描画することができません。  

ただし、`note` の使われ方は各モードに依存するため、各モード毎の説明を確認してください。  

各必須項目に設定可能な設定値は以下の通りです。  
あなたが、独自ツールを8vanaで可視化する場合は、このルールに則ってパーサーを作成する必要があります。  

#### 各要素の解説および取得方法
##### phase
イベントの種別（偵察行為or攻撃行為）を表します。  
現在指定可能な値は以下の２つであり、文字列で指定します。この種別によって描画されるアイコンが変化します。  

* Attack
* Discover または Discovery

監視対象ログからイベント種別を抽出する場合は、Ultimate Log Parserの設定ファイル（`config.ini`）の下記項目を監視対象ログの形式に合わせて変更します。  

```
[LogParser]
...snip...
phase_regex        : \sPhase\:\[(.*)\],\sAction\:
...snip...
```

正規表現で指定します。  
監視対象ログが下記形式であった場合、イベント種別として「`Discovery`」が取得されます。  

```
INFO,2019/09/21 16:46:32 [Out] Phase:[Discovery], Action:[Nmap], Note:[Get target information], To:[192.168.220.129], From:[GyoiThon] [gyoithon.py]
```

##### attack
具体的なイベントの事象を表します。  

監視対象ログから具体的なイベントの事象を抽出する場合は、Ultimate Log Parserの設定ファイル（`config.ini`）の下記項目を監視対象ログの形式に合わせて変更します。  

```
[LogParser]
...snip...
action_regex       : \sAction\:\[(.*)\],\sNote\:
...snip...
```

正規表現で指定します。  
監視対象ログが下記形式であった場合、イベント事象として「`Nmap`」が取得されます。  

```
INFO,2019/09/21 16:46:32 [Out] Phase:[Discovery], Action:[Nmap], Note:[Get target information], To:[192.168.220.129], From:[GyoiThon] [gyoithon.py]
```

##### time
イベント発生時刻（epoch秒）を表します。  

監視対象ログからイベント発生時刻を抽出する場合は、Ultimate Log Parserの設定ファイル（`config.ini`）の下記項目を監視対象ログの形式に合わせて変更します。  

```
[LogParser]
...snip...
date_regex         : ,(\d{4}/\d{2}/\d{2}\s\d{2}\:\d{2}\:\d{2})
...snip...
```

正規表現で指定します。  
監視対象ログが下記形式であった場合、イベント発生時刻として「`1569051992.0`」が取得されます（`2019/09/21 16:46:32`をepoch秒に変換した値）。  

```
INFO,2019/09/21 16:46:32 [Out] Phase:[Discovery], Action:[Nmap], Note:[Get target information], To:[192.168.220.129], From:[GyoiThon] [gyoithon.py]
```

##### from
接続元のIPv4アドレスまたはホスト名を文字列で表します。  

監視対象ログから接続元を抽出する場合は、Ultimate Log Parserの設定ファイル（`config.ini`）の下記項目を監視対象ログの形式に合わせて変更します。  

```
[LogParser]
...snip...
from_regex         : \sFrom\:\[(.*)\]\s\[.*\][\r\n]
...snip...
```

正規表現で指定します。  
監視対象ログが下記形式であった場合、接続元として「`GyoiThon`」が取得されます。  

```
INFO,2019/09/21 16:46:32 [Out] Phase:[Discovery], Action:[Nmap], Note:[Get target information], To:[192.168.220.129], From:[GyoiThon] [gyoithon.py]
```

##### to
接続先のIPv4アドレスまたはホスト名で表します。  

監視対象ログから接続先を抽出する場合は、Ultimate Log Parserの設定ファイル（`config.ini`）の下記項目を監視対象ログの形式に合わせて変更します。  

```
[LogParser]
...snip...
to_regex           : \sTo\:\[(.*)\],\sFrom\:
...snip...
```

正規表現で指定します。  
監視対象ログが下記形式であった場合、接続先として「`192.168.220.129`」が取得されます。  

```
INFO,2019/09/21 16:46:32 [Out] Phase:[Discovery], Action:[Nmap], Note:[Get target information], To:[192.168.220.129], From:[GyoiThon] [gyoithon.py]
```

##### note
イベントの付加情報を表します。  

監視対象ログから付加情報を抽出する場合は、Ultimate Log Parserの設定ファイル（`config.ini`）の下記項目を監視対象ログの形式に合わせて変更します。  

```
[LogParser]
...snip...
note_regex         : \sNote\:\[(.*)\],\sTo\:
...snip...
```

正規表現で指定します。  
監視対象ログが下記形式であった場合、付加情報として「`Get target information`」が取得されます。  

```
INFO,2019/09/21 16:46:32 [Out] Phase:[Discovery], Action:[Nmap], Note:[Get target information], To:[192.168.220.129], From:[GyoiThon] [gyoithon.py]
```

 * 1vanaにおけるnoteの扱い  
 1vanaでは、noteに次の情報を載せることができます。  
   * option  
   * CVE  

 `option` には、補足的な説明事項をテキストデータとして格納できます。  
 `CVE` には、関連するCVE番号を文字列として配列で保持することができます。  

#### その他の設定
Ultimate Log Parserのログの監視時間間隔やログのPathを変更したい場合は、以下の値を変更します。  

```
[Common]
...snip...
watch_period    : 5
...snip...

[LogParser]
origin_log_path    : origin_logs
origin_log_file    : gyoithon.log
converted_log_path : converted_logs
converted_log_file : 8vana_input.json
...snip...
```

 * `watch_period`  
 ログの監視時間間隔（単位は秒）です。  
 最小設定値は`5秒`となり、これより小さい値に設定した場合は強制的に5秒に設定されます。  

 * `origin_log_path`  
 監視対象ログのPathです。  
 デフォルトは `origin_logs` です。連携する外部ツールに合わせて変更します。  

 * `converted_log_file`  
 監視対象ログのファイル名です。  
 デフォルトは `gyoithon.log` です。連携する外部ツールに合わせて変更します。  

 * `converted_log_path`  
 8vana形式のJSONファイルを出力するPathです。  
 デフォルトは `converted_logs` です。  

 * `converted_log_file`  
 8vana形式のJSONファイル名です。  
 デフォルトは `8vana_input.json` です。  

### 1vana
 ![](./images/1vana_explanation.png)    

#### 1vanaを起動する

```
$ cd 8vana/1vana
$ python3 ./8vana.py
```

#### 1vanaのヘルプ
1vanaのヘルプを確認するには `-h` オプションを付けて実行します。  

```
$ python3 ./1vana.py -h
usage: 1vana.py [-h] [-l]

1vana

optional arguments:
  -h, --help      show this help message and exit
  -l, --log_time  このオプションは、ログ再生機能で利用することを想定されており、ログファイル先頭のリソース（最も古いログ）から時刻を取得
                  し、開始時刻の基準値として利用します。このオプションを利用しない場合は、現在時刻が開始時刻として利用されます。
```

#### 1vanaのコンフィグ
動作設定は `env.py` で制御されています。  
基本的な設定は以下の通りです。詳細は `env.py` を参照してください。  

##### NPUT_LOG
1vanaが参照するログファイルを指定します。デフォルトは `converted_logs/8vana_input.json` です。  

##### LOG_POLLING_TIME
ログのアップデートを確認するタイミングを秒単位で指定します。デフォルトは `5` 秒です。  

##### LOG_HASH_ALGO
ログファイルの変更を検出するためのハッシュアルゴリズム。デフォルは `md5` です。  

##### FRAME_SECOND
何フレームで1vanaの時間を１秒進めるか指定します。デフォルトは `3` フレームです。  
デフォルトの`30fps`の時に`FRAME_SECOND`を`30`に設定すると、実時間と同じスピードで描画されます。つまり、同一条件の時に`3`を設定すると、10倍のスピードで時間が進むことになります。  

##### FRAME_SECOND_REAL
FRAME_SECOND_REAL は、実時間の1秒を検出するための設定です。  
fpsの設定に合わせて指定します。差分があると正しく1秒を検出できなくなるので注意が必要です。  

##### VISUALIZE_TIME_RANGE
デフォルトで1vanaは、現在時刻から前後30秒の情報を表示します。  
表示範囲を変更する場合にこの値を変更する。  

##### VISUALIZE_TIME_WAIT
1vana起動時に描画を開始するまでの待ち時間です。  
ログから再生して描画する際に利用されます。デフォルトは`5`秒ですが、この秒数は `FRAME_SECOND`の影響を受けます。  

##### hostdata
各ホストのモノリスで表示するアイコンや、モノリスを表示した際のアクションを設定します。  
フォーマットは以下の通り。  

```
hostdata = {
    'default': {
        'icon': 'unknown',
        'action': None,
    },
    '172.31.101.30': {
        'icon': 'debian',
        'action': 'zeijyaku',
    },
```

各設定はホスト単位で指定する必要があります。  
設定値の説明は以降に記載します。  

###### icon
iconには定義済みのicon名を指定することができます。  
現在利用できるのは以下の2種類のみ。  

 * unknown  
 * debian  

これらの画像は、64x64pixに最適化されています。  

なお、任意iconの画像は、1vanaのApp関数内でimageloaderを利用して定義することで追加することができます。  

1vanaにimageloaderでアイコン画像を追加する場合は、次のようにApp関数に追加します。  
同一の名前のiconに複数の画像を追加すると、デフォルトでは8フレーム単位で切り替わります。  

```
        self.actor["<任意の名前>"] = actor.Actor()
        self.actor["<任意の名前>"].imageload("<ファイルパス>")
        self.actor["<任意の名前>"].imageload("<ファイルパス>")
```

ただし、Pyxelではindexed colorのpng形式のみサポートされることに注意が必要です。  
24bitのpng画像は、添付のコンバーター「`png_convert.py`」を利用することで簡単に変換できます。  

###### action
actionに `zeijyaku` と設定されている場合、モノリスを開いて10フレーム経過してから20フレーム経過すまでの間に脆弱のアイコンが表示されます。  
現時点では、演出用に利用できるのみの実験的な機能になっている。  

### 2vana
 ![](./images/2vana_explanation.png)    

#### 2vanaを起動する
```
$ cd 8vana/2vana
$ python3 ./2vana.py
```

#### 2vanaのコンフィグ
2vanaの動作は `2vana/config.ini` で設定できます。  
基本的な設定値を以下に示します。  

##### 攻撃元ホスト（War Tank）の設定
監視対象ホストに偵察行為や攻撃行為を行う攻撃元ホストを指定します。  
IPアドレスまたは任意のホスト名を設定することができます。  

 * War Tankが1ホストの場合（IPアドレス表記）  
 ```
 [Attacker]
 attackers : 192.168.220.129
 ```

 * War Tankが1ホストの場合（ホスト名表記）  
 ```
 [Attacker]
 attackers : GyoiThon
 ```

 * War Tankが4ホストの場合  
 アットマーク区切りで各ホストを記述します。  
 ```
 [Attacker]
 attackers : 192.168.220.129@192.168.220.130@GyoiThon@192.168.220.132
 ```

なお、War Tankの数は**最大で4台**です。  
5台以上のホストを記述した場合、**5台目以降は無視**されますのでご注意ください。  

##### 監視対象ホストの設定
監視対象ホストを指定します。  
IPアドレスまたは任意のホスト名を設定することができます。  

 * 監視対象ホストが1ホストの場合（IPアドレス表記）  
 ```
 [Target]
 targets   : 192.168.184.155
 ```

 * 監視対象ホストが1ホストの場合（ホスト名表記）  
 ```
 [Target]
 targets   : Metasploitable3
 ```

 * 監視対象ホストが3ホストの場合  
 アットマーク区切りで各ホストを記述します。  
 ```
 [Target]
 targets   : 192.168.184.155@192.168.184.129@Metasploitable3
 ```

なお、監視対象ホストの数は**最大で12台**です。  
13台以上のホストを記述した場合、**13台目以降は無視**されますのでご注意ください。  

##### ログ関連の設定
2vanaは、ログパーサーが生成したJSON形式のログファイルからイベントを取り込み、描画します。  
ログの監視時間間隔やログのPathを変更したい場合は、以下の値を変更します。  

```
[LogParser]
watch_period       : 3
converted_log_path : converted_logs
converted_log_file : 8vana_input.json
```

 * `watch_period`  
 ログの監視時間間隔（単位は秒）です。  
 最小設定値は1秒となり、これより小さい値に設定した場合は強制的に1秒に設定されます。  

 * `converted_log_path`  
 監視対象ログのPathです。  
 デフォルトは `converted_logs` です。  

 * `converted_log_file`  
 監視対象ログのファイル名です。  
 デフォルトは `8vana_input.json` です。  

### ユーティリティーツール
#### 画像コンバーター「png_convert.py」
24bitのpngファイルをindexed colorのpng画像に変換するスクリプトです。  
Pyxelのデフォルト設定で利用可能な16色のうちから、最も近い色を検出して置換することができます。  

##### 使用方法
png_convert.pyを利用する場合は、以下のように利用します。  
※png_convert.py自体はcommonディレクトリ配下に配置されています。  

```
$ cd common/png_convert
$ python3 png_convert.py <input file> <output file>
```

## 動作環境

## ライセンス
[Apache License 2.0](LICENSE)  

## 連絡先
