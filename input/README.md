# Input Directory

このディレクトリには、エンジニアチームへ渡す依頼、顧客資料、分析対象メモ、設計相談メモを配置する。

## 配置ルール

- 顧客名または案件名ごとにサブディレクトリを作る。
- 元資料はなるべくそのまま残し、必要に応じてエンジニアチーム向けに要約・再構成した `.md` を追加する。
- 機密情報、個人情報、認証情報、APIキー、接続情報は入れない。
- 出力成果物は `output/<client>/<YYYYMMDD>/<task-name>/` 配下に作成する。

## 例

- `input/example-client/data-platform-catchup-request.md`
- `input/example-project/system-design-review.md`

このREADMEだけが共有用scaffoldであり、`input/` 配下の実案件名・顧客名・資料はGit管理しない。
