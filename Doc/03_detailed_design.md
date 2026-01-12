# 詳細設計書（Yahooショッピング 商品検索・価格監視）

## 1. 概要
- 対象: Yahoo Shopping API（ItemSearch）を利用した商品検索・価格監視
- 実行方式: ローカルサーバ上で手動実行
- 出力: CSV

## 2. システム構成
### 2.1 コンポーネント
- フロントエンド: HTML/CSS
- バックエンド: Python
- 外部API: Yahoo Shopping API（ItemSearch）

### 2.2 処理フロー
1. ユーザーがカテゴリとキーワードを入力
2. バックエンドがAPIにリクエスト
3. レスポンスを整形しCSV生成
4. CSV保存と完了メッセージ表示
5. 実行ログ出力

## 3. ディレクトリ構成（案）
```
.
├── app/
│   ├── main.py
│   ├── api_client.py
│   ├── csv_writer.py
│   ├── logger.py
│   └── config.py
├── templates/
│   └── index.html
├── static/
│   └── style.css
├── output/
├── logs/
└── Doc/
    ├── 01_requirements.md
    ├── 02_specification.md
    └── 03_detailed_design.md
```

## 4. 画面設計
### 4.1 画面構成
- カテゴリ選択（セレクト）
- キーワード入力（テキスト）
- 実行ボタン
- 結果メッセージ表示
- 結果表（テーブル）

### 4.2 入力制御
- キーワード未入力時は送信不可
- カテゴリ未選択時は送信不可
- カテゴリ一覧は初期表示時にAPIから取得して表示

### 4.3 カテゴリ表示仕様（暫定）
- 表示名: `name`
- 内部ID: `id`
- 階層表示: フラット（親子階層は無視）
- 取得失敗時: 空のセレクトで表示し、エラーメッセージを出す

## 5. バックエンド設計
### 5.1 APIクライアント（api_client.py）
#### 役割
- Yahoo Shopping APIにリクエスト送信
- リトライ制御（最大2回）

#### 入力
- appid
- query
- category_id
- results（最大50）
- start（任意）
- sort（任意）

#### 出力
- レスポンスJSON（dict）

#### リトライ仕様
- 失敗時に最大2回リトライ
- リトライ間隔: 2秒（暫定）

### 5.2 CSV生成（csv_writer.py）
#### 役割
- APIレスポンスからCSVを作成・保存

#### 出力列（暫定）
- 取得日時
- 商品名
- 価格
- 商品URL
- ショップ名
- 画像URL
- 在庫状況
- レビュー件数
- レビュー平均
 - 列は任意（必要なものを選択可能）

#### ファイル名
- 形式: `yyyymmdd_hhmmss_itemsearch.csv`
- 保存先: `./output/`

### 5.3 ログ出力（logger.py）
#### 役割
- 実行ログの出力

#### 出力内容
- 実行開始/終了
- 入力パラメータ
- API結果（成功/失敗）
- エラーメッセージ

#### 保存先
- `./logs/`（日次追記）

#### 形式
- JSON

### 5.4 設定管理（config.py）
#### 管理項目
- appid（環境変数から取得）
- APIエンドポイント
- results上限
- ログ保存先
- CSV保存先

## 6. データ設計
### 6.1 内部データ構造
#### 商品情報（dict）
- name
- price
- url
- store_name
- image_url
- availability
- review_count
- review_rate

### 6.2 CSVマッピング
- APIレスポンスの該当項目をCSV列に変換

## 7. エラー処理
### 7.1 APIエラー
- HTTPエラー/タイムアウトはリトライ対象
- リトライ失敗時はエラーメッセージを表示し終了

### 7.2 入力エラー
- 未入力は画面側で防止
- バックエンドでも必須チェックを実施

## 8. 未確定事項
- CSV出力列の最終確定
- ログの出力形式（JSON化など）
