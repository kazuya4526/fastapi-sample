## FastAPIお試し

### 起動方法

- DBの設定
  - 任意のDBを立ち上げ、下記DDLを適用する。※例としてpostgresqlを使用しているが、[db_config.py](./src/config/db_config.py)の7行目の記載を変えることで（恐らく）どのDBでも対応可能。
    - [create_table_download_user.sql](./create_table_download_user.sql)
- 環境情報の設定
  1. [.env.example](./.env.example)を同階層にコピーする。
  2. 1.を`.env`にリネームする。
  3. 2.の各変数の値を設定する。
- venv導入～FastAPI起動
  1. ターミナルを立ち上げ、プロジェクトのルートディレクトリに移動
  2. ```python -m venv venv``` を実行し、venv作成する。
  3. ```venv\Scripts\activate``` を実行し、venvに入る。
  4. ```pip install -r requirement.txt``` を実行し、必要なライブラリをダウンロードする。 
  5. ```uvicorn main:app --reload``` を実行し、FastAPIサーバを起動する。
  6. ブラウザで[http://localhost:8000/docs]にアクセスし、APIドキュメントが表示されればOK。

### ディレクトリ構成

- src
  - config: 各種設定
    - auth_config.py: OAUTH2.0用設定
    - db_config: SQLAlchemy設定
    - config.py: 環境ごとに変わる変数を管理（.envと合わせて使用）
  - dao: DAOクラスを格納
  - ep: APIエンドポイント。MVCのController
  - model: Modelクラスを格納
    - entities.py: SQLAlchemy用のModel設定。
- .env.example: 環境ごとに変えたい変数を管理する「.env」ファイルの元ネタ。当ファイルをコピー、リネームして使用する。
- main.py: FastAPIのメインクラス。全体の設定と、APIのルーティングを行う。
  