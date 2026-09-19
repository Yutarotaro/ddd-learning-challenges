# DDD Learning Challenges

Python と TypeScript で同じ題材を実装し、DDD と Clean Architecture を学ぶための課題リポジトリです。

## Challenge 01: 図書貸出

[課題ページ](./index.html)をブラウザで開き、ドメインモデル、ビジネスルール、受け入れ条件を確認して実装してください。

- 実装コード、DB設定、依存ライブラリは学習者が用意します。
- Python と TypeScript の両方で実装します。
- DynamoDB Local とローカル MySQL の2種類の Adapter を実装します。
- Domain と Application を変更せず、Infrastructure を差し替えられることを確認します。

詳細仕様は [`docs/specs/2026-09-19-library-lending-design.md`](./docs/specs/2026-09-19-library-lending-design.md) にあります。
