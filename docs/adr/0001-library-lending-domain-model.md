# ADR 0001: 図書貸出ドメインモデルの集約境界と操作責務

- Status: Accepted
- Date: 2026-09-19
- Related: [Issue #1](https://github.com/Yutarotaro/ddd-learning-challenges/issues/1)

## Context

図書貸出ドメインでは、会員ごとの貸出上限、同一蔵書の重複貸出、延滞中の新規貸出停止、返却時の貸出と蔵書の同時変更をDomain自身が保護する必要がある。

一方で、`Member`、`Loan`、`BookCopy`をすべて独立したAggregate Rootにすると、会員に属する複数の貸出を横断した判定がApplicationへ漏れる。反対に、すべてを1つのAggregateに含めると、蔵書の独立したライフサイクルと永続化境界が失われる。

また、DomainからRepositoryを呼び出すと、ビジネスルールと永続化の調整が混ざる。貸出・返却の操作では、Domainの整合性を守りながら、別Aggregateの取得と保存をUse Caseへ委ねる境界が必要である。

## Decision

### 1. Aggregate境界

`Member`をAggregate Rootとし、その会員に属する`Loan`を内部Entityとして管理する。

```text
Member Aggregate
└── Member（Aggregate Root）
    └── Loan[]（内部Entity）
```

`BookCopy`は、貸出可能または貸出中という状態を管理する独立したAggregate Rootとする。

```text
BookCopy Aggregate
└── BookCopy（Aggregate Root）
```

`Loan`は`LoanId`で識別されるEntityだが、独立したAggregate Rootにはしない。`LoanRepository`は作らず、`MemberRepository`がLoanを含むMember Aggregate全体を保存・復元する。

### 2. Aggregate間の参照

`Loan`は`BookCopy`オブジェクトを保持せず、`BookCopyId`で参照する。`BookCopy`は現在の`LoanId`を保持しない。

```text
Member 1 *-- 0..* Loan
Loan   * --> 1 BookCopy : BookCopyId
```

これにより、`Member`と`BookCopy`のAggregate境界を維持し、相互参照による状態同期を避ける。

`Loan`の`MemberId`は、貸出が属する会員を示す属性として保持する。Member Aggregate内では所属関係と重複するが、永続化データやドメインイベントで貸出の所属を明示できる。

### 3. 貸出操作

貸出操作の入口は`Member.borrow(book_copy, loan_date)`とする。

`Member`は自身が保持するLoan一覧を使用して、次の不変条件を検証する。

- 未返却の貸出が貸出上限未満である
- 延滞中の未返却Loanがない
- 同じ`BookCopy`の未返却Loanがない
- 渡された`BookCopy`が貸出可能である

すべての検証が成功した後、`Loan.start()`で新しいLoanを生成してMemberへ追加し、`BookCopy.lend()`で蔵書を貸出中にする。

`Loan.start()`は新規貸出用のFactory Methodとする。`Loan.__init__`も不変条件を検証し、Factory以外の生成経路やRepositoryからの復元でも不正なLoanを保持できないようにする。

### 4. 返却操作

外部からUse Caseへ渡す入力は、`MemberId`、`LoanId`、返却日とする。Use CaseはMemberから返却対象Loanの`BookCopyId`を取得し、BookCopy Repositoryから対応するBookCopyを取得する。

Domain操作の入口は`Member.return_book(book_copy, loan_id, return_date)`とする。

`Member`は次の内容を状態変更前に検証する。

- LoanがMemberに属する
- Loanが未返却である
- 返却日が貸出日以降である
- Loanの`BookCopyId`と渡されたBookCopyのIDが一致する
- BookCopyが貸出中である

すべての検証が成功した後、Loanへ返却日を記録し、BookCopyを貸出可能に戻す。

BookCopyを引数として受け取るのは、DomainからRepositoryを参照せず、1回のDomain操作でLoanとBookCopyの状態を変更するためである。IDの一致確認は、誤ったBookCopyを返却状態へ変更しないための不変条件とする。

### 5. Use Caseの責務

Use Caseは次を担当する。

1. RepositoryからMemberとBookCopyを取得する
2. `Member.borrow()`または`Member.return_book()`を呼び出す
3. 変更されたMemberとBookCopyを保存する
4. 永続化時のトランザクションを管理する

EntityやDomain ServiceからRepositoryを呼び出さない。DomainはApplication、Infrastructure、DB、SDK、ORM、環境変数へ依存しない。

### 6. Loanの状態と日付

Domain内の日付は、時刻を含まない暦日を表す`datetime.date`に統一する。文字列との変換はApplicationまたはInfrastructureの境界で行う。

`LoanPeriod`はValue Objectとし、貸出日を保持して返却期限を貸出日の13日後として導出する。

Loanの永続的な状態は、未返却と返却済みの2つとする。

- `returned_at is None`: 未返却
- `returned_at is not None`: 返却済み

延滞は保存する状態ではなく、未返却であり、かつ判定日が返却期限より後である場合に導出する。

- `LoanPeriod.is_past_due(on_date)`: 判定日が期限を過ぎている
- `Loan.is_overdue(on_date)`: 未返却かつ期限を過ぎている
- `Loan.was_returned_late`: 期限後に返却された

返却期限当日は延滞とせず、翌日から延滞とする。

### 7. コードの配置

ファイルは`entity.py`、`aggregate.py`のようなDDD上の役割ではなく、ドメイン用語を基準に分割する。

```text
domain/
├── member.py
├── loan.py
├── book.py
├── book_copy.py
└── errors.py
```

Value Objectは、最も関係が深いドメイン概念と同じファイルへ置く。複数の概念で共有され、独立したルールを持つ型だけを共通モジュールへ分離する。

## Alternatives Considered

### Loanを独立したAggregate Rootにする

採用しない。会員の貸出上限、延滞、重複貸出を判定するために複数Loanの検索が必要となり、Member Aggregateだけで不変条件を保護できない。

### BookCopyに現在のLoanIdを保持する

採用しない。LoanとBookCopyの相互参照が生まれ、Loanの`BookCopyId`、BookCopyの`LoanId`、BookCopyの貸出状態を同期する必要がある。現在の要件ではBookCopyは貸出可否だけを知れば責務を果たせる。

### MemberからRepositoryを呼び出してBookCopyを取得する

採用しない。Domain Entityが永続化へ依存し、単体テストと責務の分離が悪化する。取得と保存はUse Caseが担当する。

### 返却時にLoanだけを先に変更する

採用しない。BookCopyの取得または状態変更に失敗すると、Loanは返却済みだがBookCopyは貸出中という不整合な状態になる。状態変更前に両Aggregateを揃え、1回のDomain操作で検証・変更する。

### LoanDate、DueDate、ReturnDateをすべて独自クラスにする

現時点では採用しない。個別の日付に独自の制約がないため、標準の`datetime.date`を使用する。日付間のドメインルールは`LoanPeriod`と`Loan`へ置く。

### Domain Serviceへ貸出・返却処理を置く

現時点では採用しない。貸出上限、延滞、重複貸出はMemberが保持するLoan一覧から判断できるため、Member Aggregate Rootの振る舞いとして自然である。将来、図書館カレンダーや会員区分など、どのEntityにも自然に属さない規則が追加された場合はDomain Serviceを再検討する。

## Consequences

### Positive

- Memberだけで会員単位の貸出不変条件を保護できる
- BookCopyは自身の貸出状態だけに集中できる
- DomainをRepositoryやDBから分離できる
- 貸出・返却の失敗時に、MemberとBookCopyの状態を変更しない実装が可能になる
- Use Caseの入力とDomainメソッドの引数を分離できる
- 日付と延滞の境界条件を明示的にテストできる

### Negative

- 貸出・返却ではMemberとBookCopyの2つのAggregateを取得・保存する必要がある
- 永続化時の原子性をApplicationとInfrastructureで保証する必要がある
- 返却時にLoanとBookCopyのID一致を検証する必要がある
- Member AggregateのLoan件数が増える場合は、読み込み量やAggregate境界を再検討する必要がある

## Validation

次の単体テストでDecisionを検証する。

- 貸出成功時にMemberへLoanが追加され、BookCopyが貸出中になる
- 貸出上限、貸出中、延滞中、重複貸出の失敗時に両Aggregateが変化しない
- 返却成功時にLoanへ返却日が記録され、BookCopyが貸出可能になる
- 貸出日前返却、二重返却、LoanとBookCopyの不一致の失敗時に両Aggregateが変化しない
- 返却期限当日は延滞ではなく、翌日は延滞になる
- 返却済みLoanは判定日が期限より後でも延滞にならない
