# AI Engineering Team

セレスのためのAI社員エンジニアチーム。単なる作業代行ではなく、プロフェッショナルとして意見、設計、実装、検証を行う。

## 使い方
1. `input/` に依頼、資料、コード、エラー、顧客メモを置く。
2. `ai_team/request_mode_policy.md` に従い依頼タイプを分類する。
3. `ai_team/role_scope_matrix.md` に従い担当Roleを選ぶ。
4. 成果物を `output/<client>/<YYYYMMDD>/<task-name>/` または `output/` に作る。
5. `ai_team/review/professional_quality_gate.md` とQuality Reviewerで最終確認する。

## 4つのProfessional Mode
- Professional Opinion Mode: プロとして意見する。
- Professional Design Mode: プロとして設計する。
- Professional Implementation Mode: プロとして実装する。
- Professional Verification Mode: プロとして検証する。

## 主要ドキュメント
- `ai_team/professional_standards.md`
- `ai_team/professional_only_policy.md`
- `ai_team/role_scope_matrix.md`
- `ai_team/request_mode_policy.md`
- `ai_team/handoff_policy.md`
- `ai_team/professional_response_templates.md`
- `ai_team/review/professional_quality_gate.md`

## 検証
```bash
python3 tools/validate_repository.py
```
