# 8vana

The visualization tool of security incidents like retro games.

## インストール

### Pyxelのインストール

Pyxelをインストールするには、事前にPythonのバージョン3.7以降をインストールしておく必要があります。

```
$ pip install -U pyxel
```

### 8vanaのインストール

8vanaを任意のディレクトリに展開します。

```
$ git clone https://github.com/8vana/8vana.git
```

## 1vanaを起動する

```
$ cd 8vana/1vana
$ python3 ./8vana.py
```


## 1vanaのヘルプ

ヘルプを確認するには `-h` オプションを付けて実行します。

```
$ python3 ./8vana.py -h
usage: 8vana.py [-h] [-l]

1vana

optional arguments:
  -h, --help      show this help message and exit
  -l, --log_time  このオプションは、ログ再生機能で利用することを想定されており、ログファイル先頭のリソース（最も古いログ）から時刻を取得
                  し、開始時刻の基準値として利用します。このオプションを利用しない場合は、現在時刻が開始時刻として利用されます。
```


## 設定

動作設定は `env.py` で制御されています。
基本的な設定は以下の通りです。詳細は `env.py` を参照してください。

### NPUT_LOG
1vanaが参照するログファイルを指定します。デフォルトは `parser/log.json` です。

### LOG_POLLING_TIME
ログのアップデートを確認するタイミングを秒単位で指定します。デフォルトは `5` 秒です。

### LOG_HASH_ALGO
ログファイルの変更を検出するためのハッシュアルゴリズム。デフォルは `md5` です。

### FRAME_SECOND
何フレームで8vanaの時間を１秒進めるか指定する。デフォルトは `3` フレーム。
デフォルトの 30fps のときに FRAME_SECOND を 30 に設定すると実時間と同じスピードで描画される
つまり、同一条件のときに3を設定すると10倍のスピードで時間が進むことになる

### FRAME_SECOND_REAL
FRAME_SECOND_REAL は、実時間の1秒を検出するための設定。
fpsの設定に合わせて指定する。差分があると正しく1秒を検出できなくなるので注意。

### VISUALIZE_TIME_RANGE
デフォルトで8vanaは、現在時刻から前後30秒の情報を表示する。表示範囲を変更する場合にこの値を変更する。

### VISUALIZE_TIME_WAIT
8vana起動時に描画を開始するまでの待ち時間。ログから再生して描画する際に利用される。デフォルトは `5` 秒だが、この秒数は `FRAME_SECOND` の影響を受ける。

### hostdata

各ホストのモノリスで表示するアイコンや、モノリスを表示した際のアクションを設定する。
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

各設定はホスト単位で指定する必要がある。設定値の説明は以降に記載する。

### icon

iconには定義済みのicon名を指定することができる。現在利用できるのは以下の2種類のみ。

* unknown
* debian

これらの画像は、64x64pixに最適化されている。

なお、任意iconの画像は1vanaのApp関数内でimageloaderを利用して定義することで追加することができる。

1vanaにimageloaderでアイコン画像を追加する場合は、次のようにApp関数に追加する。同一の名前のiconに複数の画像を追加するとデフォルトでは8フレーム単位で切り替わる。

```
        self.actor["<任意の名前>"] = actor.Actor()
        self.actor["<任意の名前>"].imageload("<ファイルパス>")
        self.actor["<任意の名前>"].imageload("<ファイルパス>")
```

ただし、Pyxelではindexed colorのpng形式のみサポートされることに注意。24bitのpng画像は、添付のコンバーター `png_convert.py` を利用することで簡単に変換できる。

### action

actionに `zeijyaku` と設定されている場合、モノリスを開いて10フレーム経過してから20フレーム経過すまでの間に脆弱のアイコンが表示される。
現時点では演出用に利用できるのみの実験的な機能になっている。

## png_convert.pyについて

24bitのpngファイルをindexed colorのpng画像に変換するスクリプト。Pyxelのデフォルト設定で利用可能な16色のうちから近い色を検出して置換することができる。

### 利用方法

png_convert.pyを利用する場合は、以下のように利用する。

```
$ python3 png_convert.py <input file> <output file>
```

## パーサーについて

1vanaが読み込むファイルは `env.py` の `INPUT_LOG` で指定します。デフォルトは `parser/log.json` を読み込みます。

以下は、8vanaが読み込み可能なJSON形式の正規化されたログの例です。

```
[
  {
    "phase": "discover",
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
    "phase": "discover",
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


`phase`, `attack`, `time`, `from`, `to`, `note` は必須項目です。ただし、`note` の使われ方は各モードに依存するため、各モード毎の説明を確認してください。

各必須項目に設定可能な設定値は以下の通り。あなたが、独自ツールを8vanaで可視化する場合は、このルールに則ってパーサーを作る必要があります。

### phase

指定可能な値は以下の２つであり、文字列で指定します。この種別によって表示されるアイコンが変化します。

* attack
* discover

### attack

任意の名前を文字列で設定します。

### time

epoch秒（数値）でイベント発生時刻を設定します。

### from

接続元のIPv4アドレスを文字列で指定します。

### to

接続先のIPv4アドレスを文字列で指定します。

### 1vanaにおけるnoteの扱い

1vanaでは、noteに次の情報を載せることができます。

* option
* CVE

`option` には、補足的な説明事項をテキストデータとして格納できます。`CVE` には、関連するCVE番号を文字列として配列で保持することができます。


### 2vanaにおけるnoteの扱い


