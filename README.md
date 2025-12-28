# 五目ならべ (Gomoku)

Python + Tkinterで実装された五目ならべゲームです。

## 機能

- 15x15のボード
- 2人対戦モード
- グラフィカルなGUIインターフェース
- 勝敗判定機能
- ゲームリセット機能

## 動作環境

- Docker + Docker Compose
- WSL2（Windows）またはLinux環境

## インストールと実行

### 1. リポジトリのクローン

```bash
git clone <repository-url>
cd gomoku
```

### 2. Dockerイメージのビルド

```bash
docker-compose build
```

### 3. ゲームの起動

```bash
docker-compose run --rm app python main.py
```

または、コンテナに入ってから実行：

```bash
docker-compose run --rm app bash
python main.py
```

## 遊び方

1. ゲームが起動すると、15x15の碁盤が表示されます
2. 黒石から始まり、交互に石を置きます
3. ボード上の交点をクリックして石を置きます
4. 縦、横、斜めのいずれかに5つ並べると勝利です
5. 「新しいゲーム」ボタンでゲームをリセットできます

## プロジェクト構造

```
gomoku/
├── Dockerfile              # Docker設定
├── docker-compose.yml      # Docker Compose設定
├── main.py                 # メインスクリプト
├── src/
│   ├── __init__.py
│   ├── gomoku_game.py      # ゲームロジック
│   └── gomoku_gui.py       # GUIインターフェース
├── README.md
└── LICENSE
```

## ライセンス

MIT License