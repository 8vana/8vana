# default setting

INPUT_LOG        = "../converted_logs/8vana_input.json"
LOG_POLLING_TIME = 5
LOG_HASH_ALGO    = 'md5'

# ログウィンドウ向けセッティング（各種表示位置を設定）
LOG_AREA_X       = 52
LOG_AREA_Y       = 184
LOG_FRAME_X1     = 48
LOG_FRAME_Y1     = 175
LOG_FRAME_X2     = 246
LOG_FRAME_Y2     = 232
LOG_MAX_LINE     = 7

# モノリス向けセッティング（各種表示位置を設定）
MONOLITH_X1               = 48
MONOLITH_Y1               = 92
MONOLITH_X2               = 204
MONOLITH_Y2               = 224
MONOLITH_MARGIN_LEFT      = 4
MONOLITH_MARGIN_TOP       = 4
MONOLITH_TITLE_LENGTH     = 6

# モノリスのサイズを画面サイズの割合で指定します
MONOLITH_WIDTH  = 0.6
MONOLITH_HEIGHT = 0.8

# モノリス向けセッティング（ログのページ移動量を設定）
## <- をクリックしたときの移動量
MONOLITH_PREVIOUS_AMOUNT1 = 10
## << をクリックしたときの移動量
MONOLITH_PREVIOUS_AMOUNT2 = 100
## -> をクリックしたときの移動量
MONOLITH_NEXT_AMOUNT1     = 10
## >> をクリックしたときの移動量
MONOLITH_NEXT_AMOUNT2     = 100


# 時刻表示セッティング（表示位置を設定）
TIME_AREA_X          = 120
TIME_AREA_Y          = 245

# 何フレームで１秒進むかを指定する
# デフォルトの 30fps のときに FRAME_SECOND を 30 に設定すると実時間と同じスピードで描画される
# つまり、同一条件のときに3を設定すると10倍のスピードで時間が進むことになる
# FRAME_SECOND_REAL は、fpsの設定に合わせて指定すること。※差分があると正しく1秒を検出できなくなる。
FRAME_SECOND         = 3
FRAME_SECOND_REAL    = 30

# 描画するログの範囲を指定
VISUALIZE_TIME_RANGE = 30
VISUALIZE_TIME_WAIT  = 5

# 各ホスト毎の表示設定です
hostdata = {
    'default': {
        'icon': 'unknown',
        'action': None,
    },
    '172.31.101.30': {
        'icon': 'debian',
        'action': 'zeijyaku',
    },
    '172.31.102.30': {
        'icon': 'debian',
        'action': 'zeijyaku',
    },
    '172.31.103.30': {
        'icon': 'debian',
        'action': 'zeijyaku',
    },
    '172.31.104.30': {
        'icon': 'debian',
        'action': 'zeijyaku',
    },
    '172.31.105.30': {
        'icon': 'debian',
        'action': 'zeijyaku',
    },
    '172.31.106.30': {
        'icon': 'debian',
        'action': 'zeijyaku',
    },
    '172.31.107.30': {
        'icon': 'debian',
        'action': 'zeijyaku',
    },
    '172.31.108.30': {
        'icon': 'debian',
        'action': 'zeijyaku',
    },
    '172.31.109.30': {
        'icon': 'debian',
        'action': 'zeijyaku',
    },
    '172.31.110.30': {
        'icon': 'debian',
        'action': 'zeijyaku',
    },
}





# 以降は1vanaのデフォルト設定です
# 通常は変更しません
WINDOW_WIDTH  = 255
WINDOW_HEIGHT = 255
NETMAP_OBJ_WIDTH = 15  # 1 charactor 5pix
NETMAP_OBJ_HEIGHT = 8
NETMAP_OBJ_MARGIN_TOP = 8
NETMAP_OBJ_MARGIN_DOWN = 10
NETMAP_OBJ_MARGIN_RIGHT = 2
NETMAP_BASE_X = 8
NETMAP_BASE_Y = 4
CHAR_WIDTH    = 5
CHAR_HEIGHT   = 7

WORLDMAP = 0
CLASS_A  = 1
CLASS_B  = 2
CLASS_C  = 3
HOST     = 4
VIEW_MONOLITH = 4

# move speed
MOVE_X = 8
MOVE_Y = 8

# object grow speed
GROW_X = 8
GROW_Y = 8

# icon action wait
ICON_ACTION_WAIT = 8


# color http://tkitao.hatenablog.com/entry/2017/01/26/193908
BLACK = 0
DARK_BLUE = 1
DARK_PURPLE = 2
DARK_GREEN = 3
BROWN = 4
DARK_GRAY = 5
LIGHT_GRAY = 6
WHITE = 7
RED = 8
ORANGE = 9
YELLOW = 10
GREEN = 11
BLUE = 12
INDIGO = 13
PINK = 14
PEACH = 15

LEVEL_1 = RED
LEVEL_2 = PINK
LEVEL_3 = ORANGE
LEVEL_4 = BLUE
LEVEL_5 = LIGHT_GRAY
