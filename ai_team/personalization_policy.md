# Local Context and Personalization Policy

## 目的

各利用者のLocal Private Stateを他利用者や共有リポジトリへ混入させず、利用可能な場合だけUser-local Second Brainと個人設定を利用する。

## コンテキスト優先順位

判断時は次の順序を守る。

1. Current Explicit Request
2. Current Evidence（actual repository / code / data / configuration / runtime state / input）
3. User-local Second Brain
4. Shared AI Employee Core（Role / Skill / Workflow / Policy / canonical documentation）
5. General Model Knowledge

Second BrainとCurrent Evidenceが矛盾する場合はCurrent Evidenceを採用し、矛盾を未確認事項として残す。Current Explicit Requestに反する個人設定は適用しない。

## Local profileの解決

1. 明示的に渡された現在利用者のprofileを使う。
2. リポジトリ内の `.local/user_profile.yaml` が存在する場合だけ使う。
3. どちらもない場合は `profiles/current_user_profile.yaml` の匿名shared defaultを使い、個人属性を推測しない。

`.local/user_profile.yaml` はGit管理禁止である。他利用者のprofileを探索・参照・同期しない。

## User-local Second Brainの解決

1. Current Explicit Requestで指定されたrootを使う。
2. 現在のprocessで明示された `SECOND_BRAIN_ROOT` を使う。
3. `.local/second_brain.yaml` に現在利用者が設定したrootを使う。
4. いずれもない場合は利用しない。

Home directoryを無差別scanしない。rootの利用者所有が確認できない場合は参照しない。Second Brainが存在しない場合もAI社員チームはエラーにせずShared Coreへfallbackして動作する。

## PersonalizationとCapability Growthの分離

- 文体、詳しさ、利用者の好みはPersonalizationとしてのみ扱う。
- 個人の技術嗜好をUniversal SkillやCanonical Policyへ自動昇格しない。
- Second Brainの内容はRaw Evidenceとして共有・送信・commitしない。
- Canonical Growthへ使う場合は、個人情報を除いた独立Evidence、Before/After Eval、Independent Review、Celes Human Gateを別途要求する。

## 顧客向け成果物

依頼者profileと成果物の読み手を分ける。顧客の属性・案件情報をshared defaultへ書き戻さない。

## 参照

- `profiles/current_user_profile.yaml`
- `ai_team/obsidian_write_policy.md`
- `ai_team/governance/architecture_contract.yaml`
- `ai_team/governance/capability_growth_policy.yaml`
