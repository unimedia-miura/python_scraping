# Python学習用プロジェクトです
==================

- BeautifulSoup というライブラリを用いて、Web スクレイピングを行っています。
- 以下の手順で処理しています。

1. 上場企業一覧ページを取得
2. 一覧ページで企業名,業種を取得
3. 一覧ページの各企業の詳細ページ（遷移先）を取得
4. 詳細ページで、企業HPのURL、本社所在地を取得
5. 企業HPのURLが"http://"から始まるものをdataオブジェクトにまとめる
6. excelファイルにdataを保存

- *実行時間がそこそこかかってしまう点が課題（10ページ分で約4分=> （非同期Verで）30秒ほどかかる）

- Google Colabでも実装済です（環境構築不要で実行できます） 以下にアクセスして、make_http_compnay_listを開き実行する。 https://drive.google.com/drive/folders/1FTnpzPIdHZXr6tTOyyQs0pnKr6MgCGVN
