# Issue #1 Domain Model TODO

[Issue #1: Python: Domain Modelと単体テストを実装する](https://github.com/Yutarotaro/ddd-learning-challenges/issues/1) の要件管理用チェックリスト。

## Value Object

- [x] `MemberId.generate()`でUUIDを生成できる
- [x] `ISBN`、`BookTitle`、`BookCopyId`、`MemberName`で空文字を拒否する
- [x] `ISBN`、`BookTitle`、`BookCopyId`、`MemberName`で空白だけの値を拒否する
- [x] `MemberName`の50文字上限を通常コンストラクタで保護する
- [ ] `LoanId`を実装する
- [ ] `LoanDate`、`DueDate`、`ReturnDate`を実装する
- [ ] `LoanPeriod`で貸出日と返却期限を表現する
- [ ] 貸出上限が1以上の整数であることを保証する
- [ ] 通常会員の貸出上限を3冊にする

## EntityとAggregate

- [x] `Book`を実装する
- [ ] `BookCopy`を生成時から有効な状態にする
- [ ] `Member`を生成時から有効な状態にする
- [ ] `Loan`を実装する
- [ ] `Member`をAggregate Rootとして所属する`Loan`を管理する
- [ ] `BookCopy`を独立したAggregate Rootとして貸出状態を管理する

## 貸出

- [ ] 貸出可能な`BookCopy`を借りると未返却の`Loan`が追加される
- [ ] 貸出成功時に`BookCopy`が貸出中になる
- [ ] 返却期限を貸出日の13日後にする
- [ ] 未返却の貸出が3件ある場合は4冊目を拒否する
- [x] 貸出中の`BookCopy`を拒否する
- [ ] 延滞中の未返却貸出がある場合は新規貸出を拒否する
- [ ] 同じ会員による同じ`BookCopy`の重複貸出を拒否する
- [ ] 貸出失敗時に`Member`と`BookCopy`の状態を変更しない

## 返却と延滞

- [ ] 返却時に`Loan`へ返却日を記録する
- [ ] 返却成功時に`BookCopy`を貸出可能に戻す
- [ ] 貸出日より前の返却を拒否する
- [ ] 返却済み`Loan`の二重返却を拒否する
- [ ] 返却失敗時に`Loan`と`BookCopy`の状態を変更しない
- [ ] 返却期限当日は延滞と判定しない
- [ ] 返却期限の翌日から延滞と判定する
- [ ] 返却済み`Loan`を延滞と判定しない

## Domain単体テスト

- [ ] Value Objectの正常値、空文字、空白、境界値をテストする
- [ ] 貸出成功をテストする
- [ ] 4冊目の貸出拒否をテストする
- [ ] 貸出中の蔵書の貸出拒否をテストする
- [ ] 延滞中の会員の貸出拒否をテストする
- [ ] 同じ蔵書の重複貸出拒否をテストする
- [ ] 返却成功をテストする
- [ ] 貸出日前の返却拒否をテストする
- [ ] 二重返却の拒否をテストする
- [ ] 返却期限当日と翌日の延滞境界をテストする
- [ ] 各失敗ケースで操作前後のAggregateの状態が同じことをテストする
- [ ] Pythonの全テストを実行して成功を確認する

## 完了前確認

- [ ] Domainが外部ライブラリ、環境変数、Infrastructureを参照していない
- [ ] Entity、Value Object、Aggregate Rootの判断をIssueへ記載する
- [ ] 操作失敗の表現方法をIssueへ記載する
