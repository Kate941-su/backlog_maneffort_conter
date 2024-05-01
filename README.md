# 自動工数集計アプリケーション ver 0.1.0

## アプリの機能

月末に行う工数集計を自動で計算するアプリケーションです。

## アプリを使用するメリット

このアプリを使用することで月末の工数集計並びに月中の課題完了処理を、
月末にスクリプト１行で終わらせることができるため、各プロジェクトで工数削減が見込めます。また課題番号がソートされて出力されるため以前より見やすくなっております。

## アプリの使用方法

コマンドは macOS を想定して記述しています。

### パラメータの設定

このアプリは JSON ファイル(`params.json`)を読み込むことで以下の項目を設定します

- プロジェクト名(issue_name)
- プロジェクト ID(project_id)
- そのプロジェクトに参画するメンバーと保守対応履歴に記載する名前(name_dict)
- 工数集計をしたい月初(start_date)
- 工数集計をしたい月末(end_date)
- CSV ファイルをエクスポートしたいファイルのパス(output_path)

以下に`params.json`の設定例を掲載します。

```json
{
    "issue_name": "ISSUE_NAME",// 課題名
    "project_id" : "{ISSUE_ID}",// プロジェクトID
    "name_dict": // Backlog上の名前と工数に載せる名前の対応MAP
        {
            "北谷 海斗": "北谷",
        },
    "start_date": "2023/08/01",// 開始日付
    "end_date": "2023/08/31",// 終了日付
    "output_path": "./csv/TMD_SHARE_202308.csv",// 出力先のパス
    "start_from": "100"// 課題番号のオフセット
```

※ 上記のパラメータを正しく設定しなかった場合、Python がエラーを出力して終了します。

※ `start_date`,`end_date` は特別なことがない限り月初、月末で良いはずです。

※ プロジェクト ID の確認方法は以下のウェブサイトを参照してください
https://yatta47.hateblo.jp/entry/2017/07/08/130000

### 最初に使用するとき

1. Python を仮想環境を作成する
   以下のコマンドラインを使用して、仮想環境を作る

```
python3 -m venv venv
```

2. 仮想環境に入る

```
source venv/bin/activate
```

3. 必要なライブラリをインストール
   以下のコマンドを使用して、必要なライブラリをインストールする

```
pip install -r requirements.txt
```

### 二回目以降の使用

1. 仮想環境に入る

```
source venv/bin/activate
```

2. json ファイルの中身を書き換える

```json
    "issue_name": "ISSUE_NAME",// 課題名
    "project_id" : "{ISSUE_ID}",// プロジェクトID
    "name_dict": // Backlog上の名前と工数に載せる名前の対応MAP
        {
            "北谷 海斗": "北谷",
        },
    "start_date": "20YY/MM/01",// 工数を集計する月に変更
    "end_date": "20YY/MM/DD",// 終了日付
    "output_path": "./csv/TMD_SHARE_YYYYMM.csv",// 出力先のパス
    "start_from": "1"// 課題番号のオフセット。通常は1よい。

```

3. `main.py` があるディレクトリでスクリプトを実行する

```
python3 main.py
```

4. 正常に終了したら仮想環境から抜ける

```
deactivate
```

## 出力内容

### ファイル

工数集計結果 : .csv

### ターミナル

- 進捗表示（%表記）
- ※要確認課題リスト

#### ※要確認課題リスト

```
('You should check this issue yourself below 👇. Because It has posibility to '
 'miss out some issue production time')
```

要確認課題リストは手動で CSV ファイルに書き込まなければならない可能性がある課題の一覧です。

この表示の下に表示される課題の一覧が要確認リストです。

`None`の場合は確認する必要はありません。要確認リストは Backlog API の仕様上コメントが 100 件までしか取得できないことからこのリストが必要になりました。このリストに記載されている課題は目視で工数チェックをする必要があります。
