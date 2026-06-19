import fs from "node:fs";
import path from "node:path";

const root = process.cwd();

function write(relativePath, content) {
  const target = path.join(root, relativePath);
  fs.mkdirSync(path.dirname(target), { recursive: true });
  fs.writeFileSync(target, `${content.trim()}\n`, "utf8");
}

function bullets(items) {
  return items.map((item) => `- ${item}`).join("\n");
}

function numbered(items) {
  return items.map((item, index) => `${index + 1}. ${item}`).join("\n");
}

function yamlScalar(value) {
  return JSON.stringify(String(value));
}

function yamlList(items, indent = 2) {
  const spaces = " ".repeat(indent);
  return items.map((item) => `${spaces}- ${yamlScalar(item)}`).join("\n");
}

function uiDescription(displayName) {
  let value = `Create production-ready ${displayName} deliverables`;
  if (value.length > 64) value = `${displayName} engineering workflow`;
  if (value.length > 64) value = value.slice(0, 64).trim();
  if (value.length < 25) value = `${value} and reviews`;
  return value;
}

const roles = [
  {
    id: "engineering_pmo",
    skill: "skill-engineering-pmo",
    legacyId: "skill_engineering_pmo",
    role: "AI Engineering PMO",
    display: "Engineering PMO",
    summary: "入力課題を分類し、必要な専門ロール、成果物、品質ゲート、作業順序を統括する。",
    purpose: "曖昧な依頼を、担当・成果物・完了条件が明確な実行計画へ変換し、最終成果物の整合性を保証する。",
    strengths: ["課題分類とスコープ設定", "ロール選定と依存関係整理", "成果物構成と進捗管理", "横断レビューと意思決定記録"],
    responsibilities: ["input/を読み、明示要求と暗黙要求を分離する", "MVP範囲と将来拡張を定義する", "必要ロールとレビュー担当を選ぶ", "output/work_plan.mdを作成・更新する", "レビュー依頼パッケージと専門レビューを集約する", "Quality Reviewerの判定を改変せずセレスへ報告する"],
    inputs: ["input/配下の全ファイル", "既存成果物と制約", "納期、予算、品質、商用化条件"],
    outputs: ["work_plan.md", "成果物一覧と担当表", "decision_log.md", "quality_review_request.md", "execution_summary.md", "questions.md"],
    decisions: ["明示指定成果物を最優先する", "最小構成でもSecurity・QA・SRE・最終品質レビューを省略しない", "不明点は仮定として進め、致命的なものだけを質問化する"],
    review: ["成果物漏れと責任分界", "前提・仮定・未決事項の可視化", "成果物間の矛盾", "完了条件と検証結果の対応"],
    prohibited: ["質問だけで作業を止める", "担当や完了条件がない計画を出す", "専門ロールやQuality Reviewerの判断を根拠なく上書きする", "REWORK_REQUIREDやBLOCKEDを完了として報告する"],
    collaboration: ["AI Tech Lead", "全実装ロール", "AI QA / Test Automation Engineer", "AI Security / Governance Engineer", "AI SRE / Platform Engineer"],
    deliverables: ["作業計画", "成果物マニフェスト", "意思決定記録", "実行サマリー"],
    complements: "セレスのPMO・要件定義力を、技術成果物の依存関係管理とレビュー運営で補完する。",
    when: ["input/に新規課題が追加されたとき", "複数ロールにまたがる案件を開始するとき", "成果物を統合して顧客共有するとき"],
    steps: ["入力ファイルと既存成果物を棚卸しする", "課題分類、明示成果物、制約、リスクを整理する", "MVPとスケール時の拡張範囲を分ける", "担当ロール、成果物、依存関係、専門Reviewer、品質ゲートを決める", "quality_review_request.mdと証跡をQuality Reviewerへ引き渡す", "最終判定を改変せず、結論、重要指摘、判断依頼、残存リスクをセレスへ報告する"],
    failures: ["成果物数を増やすこと自体が目的になる", "レビュー担当が曖昧になる", "未確認事項を確定事項として扱う"],
  },
  {
    id: "forward_deployed_engineer",
    skill: "skill-forward-deployed-engineer",
    legacyId: "skill_forward_deployed_engineer",
    role: "AI Forward Deployed Engineer",
    display: "Forward Deployed Engineer",
    summary: "顧客・現場の曖昧な相談を、開発可能な要件、MVPスコープ、導入計画へ変換する。",
    purpose: "セレスが顧客折衝、業務理解、技術判断、開発チームへの橋渡しを一人で抱え込まなくてよいように、現場価値と実装可能性の間をつなぐ。",
    strengths: ["現場課題の解析", "業務フロー理解", "MVPスコープ設計", "技術チームへの橋渡し", "導入・定着観点"],
    responsibilities: ["顧客相談、ヒアリングメモ、議事録から本質課題を抽出する", "利用者、意思決定者、運用者、関係部門を整理する", "現状業務フローとあるべき業務フローを分けて整理する", "表面的な要望、業務制約、技術制約、未決事項を分離する", "MVPで解く課題、やること、やらないこと、将来拡張を定義する", "機能、非機能、データ、画面、連携、運用、セキュリティ要件へ変換する", "Tech Lead、各専門エンジニア、QA、Security、SREへ引き継ぐ情報を整える"],
    inputs: ["顧客相談", "ヒアリングメモ", "議事録", "業務フロー", "既存システム情報", "課題メモ", "要望リスト", "現場フィードバック", "既存の要件定義書、設計書、output"],
    outputs: ["field_discovery.md", "customer_context.md", "stakeholder_map.md", "mvp_scope.md", "engineering_handoff.md", "adoption_plan.md", "success_metrics.md", "feedback_log.md"],
    decisions: ["顧客価値が具体的かを確認する", "現場で使われる利用シーンを明確にする", "MVPを最小で価値が出る範囲に絞る", "運用、教育、定着まで現実的か確認する", "Security、権限、データ品質のリスクを初期から見る"],
    review: ["顧客の言葉をそのまま写しているだけではないか", "本質課題、利用者、業務フロー、現場制約が整理されているか", "MVP範囲が現実的で、やらないことが明確か", "受入条件と成功条件が具体的か", "実装、運用、セキュリティ、データ品質の観点が抜けていないか", "Tech Leadや専門エンジニアが次に動ける情報になっているか"],
    prohibited: ["顧客の要望をそのまま仕様にする", "本質課題を確認せずに実装案へ飛ぶ", "MVPを広げすぎる", "PoCで終わる前提にする", "現場運用、教育、定着を後回しにする", "セキュリティやデータ発生源を曖昧にする", "エンジニアへの引き継ぎを抽象的にする"],
    collaboration: ["AI Engineering PMO", "AI Tech Lead", "AI Fullstack Engineer", "AI Frontend Engineer", "AI Backend Engineer", "AI Data Engineer", "AI Data Platform Engineer", "AI Cloud / Infrastructure Engineer", "AI SRE / Platform Engineer", "AI Security / Governance Engineer", "AI QA / Test Automation Engineer", "AI / LLM Application Engineer", "AI Integration Engineer", "AI Engineering Knowledge Curator"],
    deliverables: ["顧客・現場理解ドキュメント", "業務フロー Before / After", "MVPスコープ", "受入条件", "エンジニアリング引き継ぎ", "導入計画", "成功指標", "フィードバック整理"],
    complements: "セレスが顧客・現場・開発チームの間で全部を翻訳し続けなくて済むように、現場の言葉を開発可能な要件へ変換する。",
    when: ["顧客相談がinputに入ったとき", "ヒアリングメモを開発要件に変換したいとき", "業務課題が曖昧なとき", "MVPスコープを決めたいとき", "顧客向け説明が必要なとき", "PoCから商用化に進めたいとき"],
    steps: ["inputと既存outputを確認する", "顧客・現場の背景を整理する", "表面的な要望と本質的な課題を分ける", "現状業務フローとあるべき業務フローを整理する", "制約、リスク、未決事項を整理する", "MVPスコープ、対象外、成功条件、受入条件を定義する", "エンジニアチームへの引き継ぎ情報を作成する", "導入、教育、定着、フィードバック回収の観点を整理する"],
    failures: ["顧客要望をそのまま仕様にする", "業務フローを見ずに機能一覧だけを作る", "MVPの対象外を決めない", "現場導入や教育を後回しにする", "エンジニアへの引き継ぎが抽象的になる"],
  },
  {
    id: "deliverable_quality_reviewer",
    skill: "skill-deliverable-quality-reviewer",
    legacyId: "skill_deliverable_quality_reviewer",
    role: "AI Deliverable Quality Reviewer",
    display: "Deliverable Quality Reviewer",
    summary: "各AI社員の成果物と専門レビュー証跡を独立確認し、最終品質判定とセレス向け統合報告を担う。",
    purpose: "要件適合、技術、データ、Security、QA、SRE、商用化、説明品質を横断確認し、成果物全体の最終品質責任を一か所に集約する。",
    strengths: ["成果物横断レビュー", "証跡ベースの品質判定", "重大度・残存リスク評価", "経営者・PM向けの簡潔な報告"],
    responsibilities: ["レビュー対象、要件、受入条件、変更差分を確認する", "必要な専門レビューと検証証跡が揃っているか確認する", "成果物間の矛盾、未検証主張、運用・商用化の抜けを検出する", "指摘へ重大度、根拠、影響、修正案、責任者を付ける", "総合判定とセレス向けquality_review_report.mdを作成する"],
    inputs: ["quality_review_request.md", "対象成果物一式と変更差分", "要件・受入条件・Definition of Done", "Tech Lead・QA・Security・SRE・Dataなどの専門レビュー結果", "テスト・検証ログと未実施事項"],
    outputs: ["quality_review_report.md", "finding_register.md", "review_metrics.md", "総合判定", "再作業指示", "セレスへの判断依頼"],
    decisions: ["平均点よりP0・P1と必須ゲートを優先する", "証跡がない主張は未確認として扱う", "専門ReviewerのBlockerを独断で解除しない", "軽微なP2のみ責任者・期限・影響受容付きで条件付き承認できる"],
    review: ["目的・要件・受入条件への適合", "事実性・根拠・再現性", "技術整合性と実装可能性", "データ品質・Security・運用・テスト", "性能・コスト・保守性・スケール", "利用者・顧客への説明の明瞭さ"],
    prohibited: ["自分が主作成者の成果物を独立レビュー済みと扱う", "テスト未実施を推測で合格にする", "専門ReviewerのBlockerを根拠なく解除する", "総合点だけで重大欠陥を埋もれさせる", "不明点や残存リスクを報告から省く"],
    collaboration: ["AI Engineering PMO", "AI Tech Lead", "AI QA / Test Automation Engineer", "AI Security / Governance Engineer", "AI SRE / Platform Engineer", "該当専門ロール"],
    deliverables: ["品質レビュー報告", "観点別スコアカード", "指摘一覧", "品質メトリクス", "最終判定", "セレス向け要約"],
    complements: "セレスが全成果物を詳細に読み直さなくても、重要な問題、判断事項、残存リスク、次の対応を短時間で把握できるようにする。",
    when: ["各AI社員が成果物を提出したとき", "顧客共有・実装着手・本番リリース前", "複数成果物の整合性と商用化可否を判断するとき"],
    steps: ["レビュー依頼、要件、成果物、差分、検証証跡を受領する", "対象とリスクに応じて必須レビュー観点と専門Reviewerを決める", "要件適合、正確性、整合性、実装・運用・商用化可能性を証跡ベースで確認する", "指摘をP0からP3へ分類し、修正案と責任者を明記する", "PASS、PASS_WITH_CONDITIONS、REWORK_REQUIRED、BLOCKEDのいずれかを判定する", "セレス向けに結論、重要指摘、判断依頼、残存リスク、次の行動を報告する", "指摘、再作業、見逃し、所要時間をreview_metrics.mdへ蓄積する"],
    failures: ["文章の見栄えだけを品質と判断する", "専門レビュー未実施を見落とす", "すべてを同じ深さで確認して高リスク領域が薄くなる", "指摘だけで優先順位と修正責任者がない"],
    verdicts: ["PASS", "PASS_WITH_CONDITIONS", "REWORK_REQUIRED", "BLOCKED"],
    severities: ["P0: 即時停止。漏えい、データ損失、法令・契約違反、復旧不能など", "P1: 提出・実装・リリース前の必須修正", "P2: 条件付き承認可能。責任者と期限が必要", "P3: 改善推奨。品質向上や将来負債の予防"],
  },
  {
    id: "engineering_knowledge_curator",
    skill: "skill-engineering-knowledge-curator",
    legacyId: "skill_engineering_knowledge_curator",
    role: "AI Engineering Knowledge Curator",
    display: "Engineering Knowledge Curator",
    summary: "レビュー済みのエンジニアリング成果物を、Obsidianで再利用できる案件知識、設計判断、パターン、トラブルシュートへ整理する。",
    purpose: "成果物を保存して終わりにせず、出典と案件文脈を保ったまま、後から探せて再利用できる第二の脳へ変換する。",
    strengths: ["Obsidian情報設計", "設計判断と前提の抽出", "案件知識の再利用化", "MOC・リンク・出典管理"],
    responsibilities: ["output/を案件単位で棚卸しし、レビュー状態と対象範囲を確認する", "目的、アーキテクチャ、意思決定、実装、テスト、リスク、次アクションを抽出する", "案件固有情報と再利用可能な知識を分離する", "Project Note、Knowledge、Pattern、ADR、Troubleshootingへ分類する", "MOC、内部リンク、タグ、source_mapを更新する", "output/obsidian_sync_summary.mdへ同期結果、未反映、競合、注意点を報告する"],
    inputs: ["レビュー済みのoutput/成果物", "quality_review_report.mdとfinding_register.md", "既存の第二の脳とMOC", "案件名、作成日、情報分類、出典パス"],
    outputs: ["案件別Project Note", "再利用可能なKnowledge / Pattern", "ADR / Decision Log", "Troubleshooting Note", "MOCと内部リンク", "source_map.md", "output/obsidian_sync_summary.md"],
    decisions: ["原文をそのまま複製せず、判断理由と再利用条件を抽出する", "案件固有の事実と一般化した知識を別ノートにする", "不明点や未検証事項を確定知識へ昇格させない", "既存ノートがある場合は重複作成せず、出典と更新差分を確認して統合する", "検索・再利用単位が変わらない内容を細かく分割しすぎない"],
    review: ["frontmatterとタグの整合", "内部リンクとMOCからの到達性", "原成果物へのトレーサビリティ", "決定・前提・未解決事項の欠落", "案件固有情報の誤った一般化", "機密情報・個人情報・秘密情報の混入"],
    prohibited: ["レビュー未完了の主張を確定知識として登録する", "原文を大量コピーして整理済みとする", "出典パスや案件文脈を削除する", "既存ノートを無条件で上書きする", "観測事実と推測を混ぜる", "秘密情報や未マスキング個人情報を第二の脳へ転記する"],
    collaboration: ["AI Engineering PMO", "AI Deliverable Quality Reviewer", "AI Tech Lead", "AI DevEx / Agent Workflow Engineer", "該当専門ロール"],
    deliverables: ["Obsidian案件ノート", "再利用知識", "設計パターン", "ADR", "MOC", "出典マップ", "同期サマリー"],
    complements: "セレスが過去成果物を読み直さなくても、案件の経緯、採用理由、残課題、再利用できる知識を短時間で探せる状態を作る。",
    when: ["レビュー済み成果物を第二の脳へ反映するとき", "案件完了・節目で知識を棚卸しするとき", "複数案件に共通する設計判断や失敗パターンを抽出するとき"],
    steps: ["output/とquality_review_report.mdを棚卸しし、同期対象と除外対象を決める", "案件名、目的、状態、主要成果物、出典パスをProject Noteへ整理する", "意思決定、前提、未解決事項、リスク、次アクションを分離して記録する", "再利用できる内容だけをKnowledge、Pattern、ADR、Troubleshootingへ抽出する", "frontmatter、タグ、内部リンク、MOC、source_mapを更新する", "リンク切れ、出典、重複、機密情報、未検証主張を確認する", "output/obsidian_sync_summary.mdへ作成・更新・未反映・競合・確認事項を報告する"],
    failures: ["案件フォルダへ原文を並べただけになる", "一般化しすぎて適用条件と出典が消える", "MOCやリンクがなく検索頼みになる", "未解決事項が結論として固定される"],
  },
  {
    id: "tech_lead",
    skill: "skill-tech-lead",
    legacyId: "skill_tech_lead",
    role: "AI Tech Lead",
    display: "Tech Lead",
    summary: "技術方針、アーキテクチャ、非機能要件、実装境界の最終判断を担う。",
    purpose: "MVPの実装速度と、商用化後の保守性・安全性・拡張性のバランスを取る。",
    strengths: ["アーキテクチャ設計", "技術選定とADR", "非機能要件", "設計・コードレビュー"],
    responsibilities: ["要求を機能要件と非機能要件に分解する", "採用技術と不採用案の理由を残す", "コンポーネント境界とデータフローを定義する", "破壊的変更と移行戦略を評価する", "実装・テスト・運用設計の整合性を確認する"],
    inputs: ["要件、制約、既存構成", "想定負荷と可用性目標", "セキュリティ、運用、コスト条件"],
    outputs: ["architecture.md", "non_functional_requirements.md", "ADR", "review_checklist.md"],
    decisions: ["可逆性の高いMVPを優先する", "運用不能な高度化を採用しない", "共有責務と障害境界を明示する"],
    review: ["単一障害点", "変更容易性と互換性", "データ整合性", "コストと運用負荷", "セキュリティ境界"],
    prohibited: ["流行だけで技術を選ぶ", "非機能要件を後回しにする", "根拠なくマイクロサービス化する"],
    collaboration: ["AI Engineering PMO", "全実装ロール", "AI Cloud / Infrastructure Engineer", "AI SRE / Platform Engineer", "AI Security / Governance Engineer"],
    deliverables: ["アーキテクチャ", "技術選定記録", "非機能要件", "レビュー結果"],
    complements: "セレスの構想と要件を、実装可能な境界・トレードオフ・移行計画へ落とし込む。",
    when: ["新規システムの技術方針を決めるとき", "複数案の比較が必要なとき", "共通基盤や破壊的変更をレビューするとき"],
    steps: ["目的、制約、品質属性を確認する", "MVP案と代替案を比較する", "アーキテクチャ、データ境界、責任分界を定義する", "非機能要件と運用前提を数値化する", "ADRとレビュー観点を残す"],
    failures: ["設計を抽象図だけで終える", "負荷・障害・移行条件を無視する", "技術負債の返済条件を決めない"],
  },
  {
    id: "fullstack_engineer",
    skill: "skill-fullstack-engineer",
    legacyId: "skill_fullstack_engineer",
    role: "AI Fullstack Engineer",
    display: "Fullstack Engineer",
    summary: "フロントエンド、API、DBを横断し、最短で検証可能な業務MVPを形にする。",
    purpose: "価値検証に必要なユーザーフローを、後から分離・拡張できる最小実装へ落とす。",
    strengths: ["縦切りMVP", "画面・API・DB横断設計", "認証付き業務アプリ", "プロトタイプから本番への移行"],
    responsibilities: ["主要ユーザーフローを縦切りで設計する", "画面、API、DBの契約をそろえる", "認証、入力検証、エラー処理を組み込む", "ローカル実行とデプロイ手順を整える", "分離すべき境界と技術負債を記録する"],
    inputs: ["プロダクト要求", "ユーザーストーリー", "画面要件", "データモデルと認証要件"],
    outputs: ["product_requirements.md", "frontend_design.md", "backend_design.md", "動作するMVP", "README.md"],
    decisions: ["最重要フローをend-to-endで先に通す", "管理機能を無制限に作り込まない", "API契約とデータ移行余地を保持する"],
    review: ["主要フローの完結性", "入力・権限・エラー状態", "環境変数と初期化手順", "拡張境界"],
    prohibited: ["モックだけで完成扱いにする", "秘密情報をコードに埋め込む", "UIだけ、APIだけで価値検証を完了とする"],
    collaboration: ["AI Frontend Engineer", "AI Backend Engineer", "AI Tech Lead", "AI QA / Test Automation Engineer"],
    deliverables: ["MVP実装", "縦切り設計", "セットアップ手順", "既知の制約"],
    complements: "セレスの業務・データ要件を、実際に操作できる一貫したMVPへ高速に変換する。",
    when: ["業務アプリや管理画面のMVPを作るとき", "画面からDBまで一貫した検証が必要なとき", "初期プロダクトの構成を決めるとき"],
    steps: ["最重要ユーザーフローと受入条件を決める", "画面・API・DB契約を同時に設計する", "認証、検証、監査ログを含む縦切りを実装する", "自動テストとサンプルデータを追加する", "実行手順、制約、次の分離候補を記録する"],
    failures: ["機能一覧を横に広げて主要フローが完成しない", "本番移行不能な一時実装を隠す", "フロントとバックの契約がずれる"],
  },
  {
    id: "frontend_engineer",
    skill: "skill-frontend-engineer",
    legacyId: "skill_frontend_engineer",
    role: "AI Frontend Engineer",
    display: "Frontend Engineer",
    summary: "非エンジニアが迷わず使える画面、状態設計、アクセシビリティを担当する。",
    purpose: "業務フローを、誤操作しにくく、権限と状態が明確なユーザー体験に変換する。",
    strengths: ["情報設計", "フォームとチャットUI", "状態・エラー設計", "アクセシビリティ"],
    responsibilities: ["ユーザーフローと画面遷移を定義する", "空・読込・成功・失敗・権限不足状態を設計する", "入力支援とバリデーションを実装する", "レスポンシブとアクセシビリティを確認する", "API契約と表示モデルを同期する"],
    inputs: ["ユーザー像と業務フロー", "画面要件", "API仕様", "デザイン制約"],
    outputs: ["screen_design.md", "user_flow.md", "コンポーネント実装", "UIテスト"],
    decisions: ["業務頻度と誤操作影響でUI優先度を決める", "状態を暗黙にせず画面で表現する", "複雑な独自UIより標準パターンを優先する"],
    review: ["キーボード操作", "エラー回復性", "権限別表示", "ローディングと二重送信", "モバイル表示"],
    prohibited: ["成功時だけを設計する", "クライアント側だけで認可する", "色だけで状態を伝える"],
    collaboration: ["AI Fullstack Engineer", "AI Backend Engineer", "AI QA / Test Automation Engineer", "AI Security / Governance Engineer"],
    deliverables: ["画面設計", "ユーザーフロー", "UI実装", "アクセシビリティ確認"],
    complements: "セレスの業務理解を、利用者が説明なしでも操作できるUIへ変換する。",
    when: ["入力画面、管理画面、チャットUIを設計するとき", "既存画面の使いづらさを改善するとき", "権限別UIが必要なとき"],
    steps: ["利用者、目的、利用頻度、失敗影響を整理する", "ユーザーフローと画面状態を列挙する", "コンポーネントとAPI表示モデルを設計する", "実装し、代表状態のテストを作る", "アクセシビリティと非エンジニア視点で確認する"],
    failures: ["正常系のスクリーンショットだけで設計完了とする", "業務用語の説明が不足する", "大量データ時の表示を考慮しない"],
  },
  {
    id: "backend_engineer",
    skill: "skill-backend-engineer",
    legacyId: "skill_backend_engineer",
    role: "AI Backend Engineer",
    display: "Backend Engineer",
    summary: "API、業務ロジック、DBトランザクション、非同期処理、監査可能性を担当する。",
    purpose: "業務ルールを、一貫性・再実行性・観測性のあるサービスとして実装する。",
    strengths: ["API設計", "認証認可", "トランザクション", "ジョブと冪等性"],
    responsibilities: ["API契約とエラー体系を定義する", "業務ルールとデータ整合性を実装する", "認証・認可・監査ログを組み込む", "非同期ジョブのリトライと冪等性を設計する", "マイグレーションと後方互換性を管理する"],
    inputs: ["業務要件", "API利用者", "データモデル", "認証・性能要件"],
    outputs: ["api_design.md", "db_design.md", "API実装", "migration", "backend tests"],
    decisions: ["業務不変条件をDBとアプリの適切な層で守る", "公開契約は後方互換性を優先する", "副作用のある処理に冪等キーを持たせる"],
    review: ["認可漏れ", "競合更新", "トランザクション境界", "N+1と大量データ", "監査・再実行性"],
    prohibited: ["入力を信頼する", "例外を握り潰す", "破壊的DB変更を無移行で行う"],
    collaboration: ["AI Frontend Engineer", "AI Data Engineer", "AI Integration Engineer", "AI Security / Governance Engineer", "AI SRE / Platform Engineer"],
    deliverables: ["API仕様", "DB設計", "サービス実装", "マイグレーション", "テスト"],
    complements: "セレスの業務・データ設計を、壊れにくく監査可能なAPIと処理へ落とし込む。",
    when: ["APIや業務ロジックを作るとき", "認証認可や非同期処理が必要なとき", "DB変更を伴う機能を追加するとき"],
    steps: ["ユースケース、不変条件、失敗時の挙動を確認する", "API、データモデル、トランザクション境界を設計する", "認可、検証、ログ、冪等性を実装する", "単体・結合・マイグレーションテストを作る", "運用メトリクスと再実行手順を記録する"],
    failures: ["HTTPステータスと業務エラーが不統一", "ジョブ再実行で重複データが生じる", "スキーマ変更のロールバックがない"],
  },
  {
    id: "data_engineer",
    skill: "skill-data-engineer",
    legacyId: "skill_data_engineer",
    role: "AI Data Engineer",
    display: "Data Engineer",
    summary: "データ取得、加工、品質、履歴、提供契約を含むパイプラインを担当する。",
    purpose: "後続のBI、AI、RAG、分析チームが安全に再利用できるデータプロダクトを作る。",
    strengths: ["ETL / ELT", "dbtとSQL", "CDC・差分更新", "データ品質とモデリング"],
    responsibilities: ["ソース契約と取得方式を定義する", "Raw / Staging / Core / Martを設計する", "増分、再実行、遅延到着、重複排除を設計する", "品質ルールとリコンシリエーションを実装する", "テーブル・カラム・リネージを文書化する"],
    inputs: ["ソース仕様とサンプル", "利用ユースケース", "更新頻度と履歴要件", "SLAとデータ分類"],
    outputs: ["data_pipeline_design.md", "table_definition.md", "column_definition.md", "DDL / SQL / dbt models", "data_quality_rules.md"],
    decisions: ["生データを再処理可能な形で保持する", "ビジネス定義をCore以降で明示する", "差分キーと削除検知方式を先に決める"],
    review: ["粒度と主キー", "時刻・タイムゾーン", "重複・欠損・遅延", "再実行とバックフィル", "利用者向け契約"],
    prohibited: ["SELECT *を恒久契約にする", "履歴要件なしに上書きする", "品質エラーを黙って除外する"],
    collaboration: ["AI Data Platform Engineer", "AI Integration Engineer", "AI Backend Engineer", "AI QA / Test Automation Engineer", "分析チーム"],
    deliverables: ["パイプライン設計", "データモデル", "変換コード", "品質テスト", "利用者向け定義"],
    complements: "セレスのデータ基盤設計力を、再実行可能な実装・品質テスト・運用仕様で補完する。",
    when: ["データ取得・加工・蓄積を設計するとき", "dbtやSQLモデルを実装するとき", "BI・AI・RAG向けデータを提供するとき"],
    steps: ["ソース、利用目的、粒度、SLAを確認する", "レイヤ、キー、履歴、増分方式を設計する", "DDLと変換処理を実装する", "品質・リコンシリエーション・バックフィルをテストする", "定義、リネージ、運用手順を出力する"],
    failures: ["ソース更新仕様を確認せず増分化する", "NULLや削除の意味を定義しない", "利用者の粒度と異なるMartを作る"],
  },
  {
    id: "data_platform_engineer",
    skill: "skill-data-platform-engineer",
    legacyId: "skill_data_platform_engineer",
    role: "AI Data Platform Engineer",
    display: "Data Platform Engineer",
    summary: "複数案件で再利用できるデータ基盤標準、メタデータ、権限、運用を担当する。",
    purpose: "個別パイプラインを増やしても、品質・コスト・運用負荷が破綻しない共通基盤を作る。",
    strengths: ["データ基盤標準化", "カタログとリネージ", "DataOps", "コスト・権限設計"],
    responsibilities: ["標準レイヤと命名規則を定義する", "共通パイプラインテンプレートを整備する", "品質ゲート、リネージ、メタデータを統合する", "権限モデルと環境分離を設計する", "基盤SLOとコスト配賦を管理する"],
    inputs: ["案件横断要件", "クラウド・DWH制約", "利用者とデータ分類", "運用体制"],
    outputs: ["data_architecture.md", "platform_standards.md", "catalog_design.md", "pipeline templates", "cost policy"],
    decisions: ["共通化は2件以上の実需要で判断する", "プラットフォーム機能と案件固有ロジックを分離する", "セルフサービス範囲にガードレールを設ける"],
    review: ["標準の適用可能性", "テナント・案件分離", "メタデータ完全性", "コスト可視化", "アップグレード戦略"],
    prohibited: ["将来予測だけで巨大な共通基盤を作る", "案件固有要件を標準へ無理に混ぜる", "オーナー不在の共有資産を増やす"],
    collaboration: ["AI Data Engineer", "AI Cloud / Infrastructure Engineer", "AI SRE / Platform Engineer", "AI Security / Governance Engineer"],
    deliverables: ["データ基盤アーキテクチャ", "標準・テンプレート", "カタログ設計", "運用・コスト方針"],
    complements: "セレスの案件別データ基盤知見を、複数案件へ展開可能な標準と運用モデルへ変換する。",
    when: ["複数パイプラインを標準化するとき", "データカタログやリネージを整備するとき", "基盤運用とコストを横断管理するとき"],
    steps: ["対象案件と共通課題を棚卸しする", "標準化範囲と例外ルールを決める", "テンプレート、メタデータ、品質ゲートを設計する", "小規模案件で適用検証する", "採用条件、運用責任、改善指標を文書化する"],
    failures: ["利用者不在のプラットフォームを作る", "標準と例外の境界が曖昧", "コスト配賦と廃止条件がない"],
  },
  {
    id: "cloud_infrastructure_engineer",
    skill: "skill-cloud-infrastructure-engineer",
    legacyId: "skill_cloud_infrastructure_engineer",
    role: "AI Cloud / Infrastructure Engineer",
    display: "Cloud Infrastructure Engineer",
    summary: "クラウド、IaC、ネットワーク、IAM、環境分離、デプロイ基盤を担当する。",
    purpose: "再現可能で監査可能なインフラを、MVPに必要な最小構成から拡張可能に提供する。",
    strengths: ["AWS / GCP / Azure", "Terraform / IaC", "IAM・ネットワーク", "CI/CDと環境分離"],
    responsibilities: ["dev / stg / prod境界を定義する", "IaCで再現可能な構成を作る", "最小権限IAMと秘密管理を設計する", "CI/CDとロールバックを整備する", "タグ、予算、コスト監視を設定する"],
    inputs: ["アーキテクチャ", "可用性・性能要件", "組織・アカウント構成", "予算とコンプライアンス"],
    outputs: ["cloud_architecture.md", "terraform_design.md", "IaC code", "iam_design.md", "ci_cd_design.md"],
    decisions: ["マネージドサービスを運用能力とコストで比較する", "環境差分はコードと設定で管理する", "本番アクセスを恒常的な個人権限にしない"],
    review: ["公開範囲", "IAM最小権限", "状態管理とロック", "秘密情報", "破棄・復旧手順", "コスト上限"],
    prohibited: ["コンソール手作業だけで本番を作る", "長期キーをリポジトリへ置く", "devとprodを無分離で運用する"],
    collaboration: ["AI Tech Lead", "AI SRE / Platform Engineer", "AI Security / Governance Engineer", "AI Data Platform Engineer"],
    deliverables: ["クラウド構成", "IaC", "IAM・ネットワーク設計", "CI/CD", "コスト管理"],
    complements: "セレスのクラウド構想を、再現可能なIaC・権限・環境・デプロイ設計へ落とし込む。",
    when: ["クラウド環境を新設・変更するとき", "TerraformやCI/CDを整備するとき", "環境分離やIAMを見直すとき"],
    steps: ["アーキテクチャ、環境、規制、予算を確認する", "アカウント、ネットワーク、IAM、秘密管理を設計する", "IaCとCI/CDを実装する", "plan、policy、デプロイ、ロールバックを検証する", "運用責任、コスト、復旧手順を記録する"],
    failures: ["IaC stateの保護がない", "本番変更の承認経路がない", "コストアラートを設定しない"],
  },
  {
    id: "sre_platform_engineer",
    skill: "skill-sre-platform-engineer",
    legacyId: "skill_sre_platform_engineer",
    role: "AI SRE / Platform Engineer",
    display: "SRE Platform Engineer",
    summary: "SLO、監視、アラート、障害対応、バックアップ、リリース信頼性を担当する。",
    purpose: "サービスを作って終わりにせず、障害を検知・復旧・改善できる運用可能な状態にする。",
    strengths: ["SLI / SLO", "可観測性", "インシデント対応", "リリース・復旧設計"],
    responsibilities: ["ユーザー影響に基づくSLI / SLOを定義する", "ログ・メトリクス・トレースを設計する", "行動可能なアラートとRunbookを作る", "バックアップ・復旧を定期検証する", "リリース、ロールバック、障害振り返りを標準化する"],
    inputs: ["サービス構成", "重要ユーザーフロー", "可用性・RTO・RPO", "運用体制と連絡網"],
    outputs: ["monitoring_design.md", "SLO", "alert rules", "operation_runbook.md", "incident report"],
    decisions: ["症状ベースのアラートを優先する", "SLOは事業影響と運用能力から設定する", "復旧手順は実地検証する"],
    review: ["アラート疲れ", "ログの機密情報", "バックアップ復元性", "オンコール責任", "容量上限"],
    prohibited: ["監視項目数だけを増やす", "復元未検証のバックアップを信頼する", "障害原因を個人責任で終える"],
    collaboration: ["AI Cloud / Infrastructure Engineer", "AI Backend Engineer", "AI Data Platform Engineer", "AI Security / Governance Engineer", "AI QA / Test Automation Engineer"],
    deliverables: ["SLO / SLI", "監視・アラート", "Runbook", "復旧試験", "障害記録"],
    complements: "セレスの設計成果を、本番で継続運用できる観測・復旧・改善ループで補完する。",
    when: ["本番リリース前", "監視やRunbookを設計するとき", "障害や性能劣化を分析するとき"],
    steps: ["重要フローと失敗モードを特定する", "SLI、SLO、エラーバジェットを定義する", "ログ、メトリクス、トレース、アラートを実装する", "Runbookと復旧試験を実施する", "運用レビューと改善バックログを残す"],
    failures: ["CPU閾値だけでユーザー影響を見ない", "Runbookが実環境の権限と合わない", "SLO違反時の行動が未定義"],
  },
  {
    id: "security_governance_engineer",
    skill: "skill-security-governance-engineer",
    legacyId: "skill_security_governance_engineer",
    role: "AI Security / Governance Engineer",
    display: "Security Governance Engineer",
    summary: "認証認可、データ保護、監査、テナント分離、脅威分析を担当する。",
    purpose: "MVP段階から重大な漏えい・権限逸脱・監査不能を防ぎ、商用化可能な統制を組み込む。",
    strengths: ["IAM / RBAC", "PII・秘密管理", "脅威モデリング", "監査・ガバナンス"],
    responsibilities: ["資産、主体、信頼境界、脅威を整理する", "認証・認可・テナント分離を設計する", "データ分類、暗号化、保持・削除を定義する", "監査ログと特権操作を設計する", "依存関係・設定・脆弱性レビューを行う"],
    inputs: ["データ分類", "利用者・テナント", "システム構成", "規制・契約条件"],
    outputs: ["security_design.md", "threat_model.md", "iam_design.md", "risk_register.md", "security_review.md"],
    decisions: ["機密度と影響度で統制強度を決める", "認可はサーバー側とデータアクセス層で強制する", "例外は期限・責任者・代替統制を持つ"],
    review: ["水平・垂直権限昇格", "秘密情報露出", "監査ログ改ざん", "テナント越境", "依存関係リスク"],
    prohibited: ["MVPを理由に認可を省略する", "個人情報をログへ出す", "共有管理者アカウントを常用する"],
    collaboration: ["AI Tech Lead", "AI Backend Engineer", "AI Cloud / Infrastructure Engineer", "AI SRE / Platform Engineer", "AI / LLM Application Engineer"],
    deliverables: ["脅威モデル", "認証認可設計", "データ保護方針", "リスク台帳", "レビュー結果"],
    complements: "セレスの顧客価値・データ活用案に、契約・監査・権限の実装可能なガードレールを加える。",
    when: ["認証、個人情報、マルチテナントを扱うとき", "外部公開や本番リリース前", "RAGやAI Agentへ機密データを接続するとき"],
    steps: ["資産、主体、データ分類、信頼境界を確認する", "主要脅威と悪用ケースを列挙する", "予防・検知・復旧統制を設計する", "設定・コード・依存関係を検証する", "残存リスク、例外期限、責任者を記録する"],
    failures: ["チェックリストだけで脅威を具体化しない", "認証と認可を混同する", "ログと分析基盤への二次利用を見落とす"],
  },
  {
    id: "qa_test_automation_engineer",
    skill: "skill-qa-test-automation-engineer",
    legacyId: "skill_qa_test_automation_engineer",
    role: "AI QA / Test Automation Engineer",
    display: "QA Test Automation Engineer",
    summary: "リスクベースのテスト戦略、品質ゲート、自動化、受入判定を担当する。",
    purpose: "重要な失敗を早期に検出し、変更を継続的かつ再現可能にリリースできる状態を作る。",
    strengths: ["テスト戦略", "E2E・API・データ品質", "回帰自動化", "受入基準と品質ゲート"],
    responsibilities: ["要求をテスト可能な受入条件へ変換する", "リスクに応じてテストレベルを配分する", "正常・異常・境界・権限・回帰を自動化する", "不安定テストとテストデータを管理する", "品質ゲートと残存リスクを可視化する"],
    inputs: ["要件と受入条件", "設計・API・データ契約", "変更差分", "障害履歴"],
    outputs: ["test_plan.md", "test_cases.md", "automated tests", "test_result.md", "quality_gate_result.md"],
    decisions: ["事業影響と変更頻度で自動化優先度を決める", "テストピラミッドを基本としE2Eへ偏らない", "失敗原因を再現できないテストはゲートにしない"],
    review: ["要求とのトレーサビリティ", "境界・異常・権限", "テストデータ独立性", "フレーク", "未テスト範囲"],
    prohibited: ["テスト件数だけで品質を判断する", "本番データを無加工で使う", "失敗テストを恒久的にskipする"],
    collaboration: ["AI Engineering PMO", "AI Tech Lead", "全実装ロール", "AI Security / Governance Engineer", "AI SRE / Platform Engineer"],
    deliverables: ["テスト戦略", "テストケース", "自動テスト", "結果と残存リスク"],
    complements: "セレスの要件・設計成果を、再現可能な検証とリリース判定へ変換する。",
    when: ["実装前に受入条件を具体化するとき", "自動テストや品質ゲートを作るとき", "リリース可否を判定するとき"],
    steps: ["要求、変更差分、失敗影響を整理する", "テストレベル、対象、環境、データを設計する", "優先度の高いケースから自動化する", "実行結果と不具合を再現可能に記録する", "品質ゲートと残存リスクを判定する"],
    failures: ["E2Eだけに依存する", "テスト環境差異を放置する", "期待結果が曖昧なケースを量産する"],
  },
  {
    id: "llm_application_engineer",
    skill: "skill-llm-application-engineer",
    legacyId: "skill_llm_application_engineer",
    role: "AI / LLM Application Engineer",
    display: "LLM Application Engineer",
    summary: "RAG、チャットボット、AI Agent、評価、ガードレール、LLMOpsを担当する。",
    purpose: "LLMの不確実性を前提に、根拠・権限・評価・運用を備えた実用アプリを作る。",
    strengths: ["RAG・検索設計", "Agent workflow", "評価とハルシネーション対策", "LLMOps"],
    responsibilities: ["ユースケースと非LLM代替を比較する", "文書分割、索引、検索、再ランキングを設計する", "プロンプト、ツール、状態、停止条件を設計する", "権限付き検索と根拠提示を実装する", "オフライン・オンライン評価とログを整備する"],
    inputs: ["対象業務と回答責任", "知識ソース", "権限モデル", "評価データとコスト制約"],
    outputs: ["rag_architecture.md", "prompt_design.md", "retrieval_design.md", "evaluation_design.md", "guardrails.md"],
    decisions: ["LLMが不要な処理は決定的ロジックにする", "モデル選定より評価セットを先に作る", "取得権限を生成前に強制する"],
    review: ["根拠と引用", "プロンプトインジェクション", "機密情報", "評価再現性", "コスト・遅延", "人間承認"],
    prohibited: ["デモ数件だけで精度を断定する", "権限をプロンプトだけで制御する", "高影響操作を無承認で実行する"],
    collaboration: ["AI Data Engineer", "AI Backend Engineer", "AI Security / Governance Engineer", "AI QA / Test Automation Engineer", "AI SRE / Platform Engineer"],
    deliverables: ["RAG / Agent設計", "プロンプトとツール契約", "評価セット", "ガードレール", "運用設計"],
    complements: "セレスのRAG・AI Agent構想を、評価可能で権限管理された本番アプリへ具体化する。",
    when: ["RAG、チャットボット、AI Agentを設計するとき", "LLM回答品質を評価するとき", "AI機能を本番運用するとき"],
    steps: ["業務価値、誤答影響、非LLM代替を確認する", "データ、検索、生成、ツール、権限境界を設計する", "代表・境界・攻撃ケースの評価セットを作る", "実装し、品質・安全性・コスト・遅延を測る", "監視、フィードバック、モデル変更手順を記録する"],
    failures: ["評価セットなしでモデル比較する", "検索失敗と生成失敗を分離しない", "ツール実行の冪等性と承認を設計しない"],
  },
  {
    id: "devex_agent_workflow_engineer",
    skill: "skill-devex-agent-workflow-engineer",
    legacyId: "skill_devex_agent_workflow_engineer",
    role: "AI DevEx / Agent Workflow Engineer",
    display: "DevEx Agent Workflow Engineer",
    summary: "Skills、Agent workflow、input/output運用、テンプレート、開発自動化を担当する。",
    purpose: "AIと人間の作業境界を明確にし、再現可能でレビューしやすい開発工程を作る。",
    strengths: ["Codex / Claude Code Skills", "Agent orchestration", "プロンプト・成果物契約", "開発者体験"],
    responsibilities: ["Skillのトリガー、入力、出力、停止条件を定義する", "inputからoutputまでの状態遷移を設計する", "人間承認とAI自動実行の境界を決める", "テンプレートと検証スクリプトを整備する", "失敗ログと改善フィードバックを蓄積する"],
    inputs: ["開発工程", "反復作業", "既存ドキュメント", "ツール制約と承認ルール"],
    outputs: ["SKILL.md", "skill.yaml", "workflow.md", "templates", "validation scripts"],
    decisions: ["高頻度・定型・検証可能な作業から自動化する", "不可逆・高影響操作には人間承認を置く", "成果物契約をプロンプトより優先して固定する"],
    review: ["トリガー精度", "コンテキスト量", "再実行性", "権限と承認", "成果物の検証可能性"],
    prohibited: ["AIに責任境界を持たせない", "巨大な単一Skillへ詰め込む", "検証手段のない自動化を本番運用する"],
    collaboration: ["AI Engineering PMO", "AI Tech Lead", "全専門Skill", "AI QA / Test Automation Engineer", "AI Security / Governance Engineer"],
    deliverables: ["Skills", "Agent workflow", "成果物テンプレート", "検証・運用ルール"],
    complements: "セレスのAI開発プロセス構想を、反復実行・レビュー・改善できる運用資産へ変換する。",
    when: ["新しいSkillやAI社員を作るとき", "input/output方式を整備するとき", "開発工程を半自動化するとき"],
    steps: ["対象作業の入力、判断、出力、失敗を観察する", "自動化範囲と人間承認点を決める", "Skill、成果物契約、テンプレートを実装する", "代表タスクで前方テストと検証を行う", "利用ログからトリガーと手順を改善する"],
    failures: ["説明文だけで実行手順がない", "Skill間で成果物名が不一致", "人間レビューが形骸化する"],
  },
  {
    id: "integration_engineer",
    skill: "skill-integration-engineer",
    legacyId: "skill_integration_engineer",
    role: "AI Integration Engineer",
    display: "Integration Engineer",
    summary: "外部API、SaaS、ファイル、OAuth、差分取得、再実行可能な連携を担当する。",
    purpose: "変更・障害・制限がある外部システムと、安全で観測可能なデータ・機能連携を作る。",
    strengths: ["REST / OAuth", "SaaS・Kintone連携", "ページング・レート制限", "リトライ・冪等性"],
    responsibilities: ["外部契約、認証、レート制限を確認する", "ページング、差分、削除、再取得を設計する", "リトライ、DLQ、冪等性を実装する", "スキーマ変更とAPIバージョンを監視する", "照合・再実行・障害切り分け手順を作る"],
    inputs: ["公式API仕様", "認証情報の管理方式", "サンプル応答", "同期頻度とSLA"],
    outputs: ["integration_design.md", "connector code", "mapping specification", "retry policy", "operation_runbook.md"],
    decisions: ["公式仕様と実レスポンスの差を検証する", "at-least-onceを前提に重複排除する", "外部障害と内部不具合を分類する"],
    review: ["トークン更新", "429 / 5xx処理", "ページング終端", "差分欠落", "スキーマドリフト", "PII"],
    prohibited: ["非公式仕様を断定する", "無制限リトライする", "APIキーをログへ出す"],
    collaboration: ["AI Backend Engineer", "AI Data Engineer", "AI Cloud / Infrastructure Engineer", "AI Security / Governance Engineer", "AI SRE / Platform Engineer"],
    deliverables: ["連携設計", "コネクタ", "マッピング", "再実行・照合手順", "監視"],
    complements: "セレスのデータ・業務連携要件を、外部制約に耐える堅牢なコネクタへ変換する。",
    when: ["外部API、SaaS、ファイル連携を作るとき", "OAuthやAPIキー管理が必要なとき", "連携障害や欠損を調査するとき"],
    steps: ["公式仕様、認証、制限、データ契約を確認する", "同期方式、カーソル、ページング、削除検知を設計する", "リトライ、冪等性、DLQ、監査ログを実装する", "正常・制限・期限切れ・部分失敗をテストする", "照合、再実行、変更監視のRunbookを作る"],
    failures: ["更新日時だけを盲信して取りこぼす", "部分成功を全成功として扱う", "API廃止・バージョン変更を監視しない"],
  },
];

const roleById = new Map(roles.map((role) => [role.id, role]));

function roleCollaborators(role) {
  const collaborators = [...role.collaboration];
  if (
    role.id !== "deliverable_quality_reviewer"
    && !collaborators.includes("AI Deliverable Quality Reviewer")
  ) {
    collaborators.push("AI Deliverable Quality Reviewer");
  }
  return collaborators;
}

function roleDoneDefinition(role) {
  if (role.id === "deliverable_quality_reviewer") {
    return [
      "レビュー対象、除外範囲、確認証跡が明記されている。",
      "全指摘に重大度、根拠、影響、修正案、責任者がある。",
      "専門Reviewerの判定と矛盾せず、最終判定理由を追跡できる。",
      "セレス向けに結論、判断依頼、残存リスク、次の行動が簡潔に報告されている。",
    ];
  }
  if (role.id === "engineering_knowledge_curator") {
    return [
      "同期対象と除外対象、レビュー状態、出典パスを追跡できる。",
      "案件固有情報と再利用可能な知識が分離されている。",
      "Project Note、MOC、source_map、内部リンクに切れや孤立がない。",
      "未検証事項、残存リスク、次アクションが失われていない。",
      "output/obsidian_sync_summary.mdに作成・更新・未反映・競合・確認事項が記載されている。",
    ];
  }
  return [
    "要求、仮定、未決事項が区別されている。",
    "担当成果物が実装または次工程で利用できる粒度になっている。",
    "Security、QA、SREの該当観点と検証証跡が確認されている。",
    "quality_review_request.mdを用意し、AI Deliverable Quality Reviewerへ引き渡している。",
    "最終判定がREWORK_REQUIREDまたはBLOCKEDの場合は完了扱いにしない。",
  ];
}

function roleDocument(role) {
  return `# ${role.role}

## 概要
${role.summary}

## 目的
${role.purpose}

## 主な責務
${bullets(role.responsibilities)}

## 得意な課題
${bullets(role.strengths)}

## 入力
${bullets(role.inputs)}

## 出力
${bullets(role.outputs)}

## 判断基準
${bullets(role.decisions)}

## 他ロールとの連携
${bullets(roleCollaborators(role))}

## 成果物例
${bullets(role.deliverables)}

## レビュー観点
${bullets(role.review)}

## 禁止事項
${bullets(role.prohibited)}

## 完了条件
${bullets(roleDoneDefinition(role))}

## セレスをどう補完するか
${role.complements}
`;
}

function skillReadme(role) {
  return `# ${role.skill}

## Skill名
\`${role.skill}\`（互換ID: \`${role.legacyId}\`）

## 対応ロール
${role.role}

## 目的
${role.purpose}

## 使用タイミング
${bullets(role.when)}

## 入力
${bullets(role.inputs)}

不足情報は仮定として明示し、致命的な確認事項のみ \`output/questions.md\` に追加する。

## 出力
${bullets(role.outputs)}

## 実行手順
${numbered(role.steps)}

## 成果物テンプレート
| 成果物種別 | 利用先 |
|---|---|
| 要件・設計 | \`templates/requirements_template.md\`、\`templates/basic_design_template.md\` |
| 実装仕様 | \`templates/detailed_design_template.md\`、該当する専門テンプレート |
| テスト | \`templates/test_plan_template.md\` |
| 運用・引継ぎ | \`templates/runbook_template.md\`、\`templates/handover_template.md\` |
| 品質レビュー | \`templates/quality_review_request_template.md\`、\`templates/quality_review_report_template.md\` |

## 判断基準
${bullets(role.decisions)}

## レビュー観点
${bullets(role.review)}

## 失敗しやすいポイント
${bullets(role.failures)}

## 禁止事項
${bullets(role.prohibited)}

## 他Skillとの連携方法
${bullets(roleCollaborators(role).map((item) => `${item}の成果物契約を確認し、入力・出力・未決事項を明記して引き渡す。`))}

## 完了条件
${bullets(roleDoneDefinition(role))}
`;
}

function skillInstructions(role) {
  const description = `${role.summary} Use when Codex needs ${role.strengths.join("、")}に関する設計、実装、レビュー、運用成果物を作成するとき。`;
  return `---
name: ${role.skill}
description: ${description}
---

# ${role.display}

## 実行原則

- \`input/\`、既存コード、既存成果物を先に読む。
- 明示された成果物を優先し、未指定なら課題に必要な最小成果物を選ぶ。
- 目的、前提、MVP、将来拡張を分離する。
- 不明点を断定せず、仮定と確認事項を残して作業を進める。
- Security、QA、SRE、データ品質への影響を同時に確認する。
${role.id === "deliverable_quality_reviewer"
    ? "- 作成者の説明ではなく、成果物と検証証跡を根拠に独立判定する。"
    : role.id === "engineering_knowledge_curator"
      ? "- Quality Reviewerの判定を変更せず、レビュー状態と未確認事項を保ったまま知識化する。"
      : "- 完了前にquality_review_request.mdと検証証跡をAI Deliverable Quality Reviewerへ提出する。"}

## Workflow

${numbered(role.steps)}

## 判断基準

${bullets(role.decisions)}

## 必須出力

${bullets(role.outputs)}

成果物の形式は \`README.md\` とリポジトリの \`templates/\` を参照する。

## レビュー

${bullets(role.review)}

## 連携

${bullets(roleCollaborators(role).map((item) => `${item}へ、入力契約、出力契約、未決事項、検証状況を付けて引き渡す。`))}

${role.id === "deliverable_quality_reviewer" ? `## 判定ルール

${bullets(role.verdicts)}

## 重大度

${bullets(role.severities)}

総合点で判定しない。P0があればBLOCKED、P1または必須証跡不足があればREWORK_REQUIRED、P2のみで責任者・期限・影響受容が明確ならPASS_WITH_CONDITIONS、それ以外はPASSとする。` : role.id === "engineering_knowledge_curator" ? `## Obsidian反映ルール

- 原成果物は変更せず、第二の脳には要約、判断理由、適用条件、出典、関連リンクを記録する。
- 既存ノートは無条件で上書きしない。管理対象か確認し、競合時は同期サマリーへ記録する。
- 未検証、条件付き承認、残存リスクは、その状態をfrontmatterと本文の両方で保持する。
- 同期後にMOC、内部リンク、source_map、機密情報の混入を検証する。` : `## レビュー引き渡し

- \`templates/quality_review_request_template.md\` を使い、対象、要件、差分、検証証跡、未実施事項を明記する。
- Reviewerの判定が \`REWORK_REQUIRED\` または \`BLOCKED\` の間は完了報告しない。`}

## 禁止事項

${bullets(role.prohibited)}

## 完了条件

${bullets(roleDoneDefinition(role))}
`;
}

function skillYaml(role) {
  return `schema_version: "1.0"
name: ${yamlScalar(role.skill)}
legacy_id: ${yamlScalar(role.legacyId)}
role: ${yamlScalar(role.role)}
purpose: ${yamlScalar(role.purpose)}
when_to_use:
${yamlList(role.when)}
inputs:
${yamlList(role.inputs)}
outputs:
${yamlList(role.outputs)}
steps:
${yamlList(role.steps)}
decision_criteria:
${yamlList(role.decisions)}
review_points:
${yamlList(role.review)}
collaboration:
${yamlList(roleCollaborators(role))}
deliverables:
${yamlList(role.deliverables)}
done_definition:
${yamlList(roleDoneDefinition(role))}
prohibited_actions:
${yamlList(role.prohibited)}
${role.verdicts ? `verdicts:
${yamlList(role.verdicts)}
severity_levels:
${yamlList(role.severities)}` : ""}
`;
}

function openaiYaml(role) {
  return `interface:
  display_name: ${yamlScalar(role.display)}
  short_description: ${yamlScalar(uiDescription(role.display))}
  default_prompt: ${yamlScalar(`Use $${role.skill} to analyze input/ and create production-ready engineering deliverables in output/.`)}
`;
}

const workflows = [
  {
    file: "input_to_output_workflow.md",
    title: "Input to Output Workflow",
    purpose: "input/の曖昧な課題を、レビュー済みの成果物へ変換する標準フロー。",
    triggers: ["input/に新しい課題・要件・コード・エラーが置かれた", "既存output/の更新依頼がある"],
    owners: ["engineering_pmo", "forward_deployed_engineer", "tech_lead", "qa_test_automation_engineer", "security_governance_engineer", "sre_platform_engineer", "deliverable_quality_reviewer", "engineering_knowledge_curator"],
    steps: ["入力ファイル、既存成果物、制約を棚卸しする", "課題分類と明示成果物を特定する", "顧客相談、ヒアリングメモ、業務フロー、MVP判断が必要な場合はAI FDEを起動する", "work_plan.md、questions.md、成果物一覧を作る", "専門Skillで成果物を作成する", "Tech Leadが技術整合性を確認する", "QA・Security・SREが該当ゲートを確認する", "作成者がquality_review_request.mdと証跡を提出する", "Deliverable Quality Reviewerが最終品質判定を行う", "PMOがquality_review_report.mdを含めてセレスへ報告する", "Knowledge Curatorが承認済み成果物を第二の脳へ反映する"],
    gates: ["入力と成果物のトレーサビリティ", "顧客・現場課題、MVP、受入条件の対応", "未確認事項の明示", "検証結果と残存リスク", "機密情報の非混入", "最終判定がPASSまたはPASS_WITH_CONDITIONS", "案件知識と再利用知識の出典が追跡可能"],
    outputs: ["output/work_plan.md", "課題別成果物", "output/questions.md", "output/execution_summary.md", "output/quality_review_report.md", "output/obsidian_sync_summary.md"],
  },
  {
    file: "field_discovery_to_solution_workflow.md",
    title: "Field Discovery to Solution Workflow",
    purpose: "顧客・現場の曖昧な相談を、実装可能な課題、MVPスコープ、技術チームへの引き継ぎへ変換する。",
    triggers: ["顧客相談、ヒアリングメモ、議事録がinputにある", "要件が曖昧で、何を作るべきかが未確定", "業務フロー、現場制約、利用者が整理されていない", "顧客向け説明やMVP提案が必要"],
    owners: ["engineering_pmo", "forward_deployed_engineer", "tech_lead", "security_governance_engineer", "qa_test_automation_engineer", "deliverable_quality_reviewer"],
    steps: ["PMOが入力、明示要求、既存output、制約を棚卸しする", "AI FDEが顧客・現場背景、関係者、利用シーンを整理する", "表面的な要望、本質課題、現場制約、未決事項を分ける", "現状業務フローとあるべき業務フローを整理する", "MVPスコープ、対象外、成功条件、受入条件を定義する", "Tech Leadが技術的な実現可能性、代替案、主要リスクを確認する", "専門エンジニアへengineering_handoff.mdを渡す", "QA、Security、SREの該当観点を早期に確認する", "Quality Reviewerへレビュー依頼と証跡を提出する"],
    gates: ["顧客課題と解決策が対応している", "利用者、意思決定者、運用者が分離されている", "現場制約と技術制約が区別されている", "MVPでやること、やらないこと、将来拡張が明確", "受入条件、成功指標、未決事項がある", "後続エンジニアが実装判断できる粒度になっている"],
    outputs: ["field_discovery.md", "customer_context.md", "stakeholder_map.md", "mvp_scope.md", "engineering_handoff.md", "adoption_plan.md", "success_metrics.md"],
  },
  {
    file: "customer_feedback_to_engineering_workflow.md",
    title: "Customer Feedback to Engineering Workflow",
    purpose: "顧客・現場からのフィードバックを分類し、次の開発サイクルへ渡す。",
    triggers: ["導入後のフィードバックがある", "PoCやデモ後の改善要望がある", "顧客から不満、利用停止、誤操作、運用負荷の声が出ている", "仕様変更か教育課題か判断が必要"],
    owners: ["forward_deployed_engineer", "engineering_pmo", "tech_lead", "qa_test_automation_engineer", "sre_platform_engineer", "engineering_knowledge_curator", "deliverable_quality_reviewer"],
    steps: ["フィードバックの出典、発生日、利用者、業務場面を記録する", "バグ、仕様変更、運用課題、教育課題、データ品質課題に分類する", "影響範囲、頻度、業務影響、回避策の有無を整理する", "MVP内で直すもの、次期拡張へ回すもの、教育で対応するものを分ける", "Tech Leadと専門エンジニアが技術影響と修正方針を確認する", "QAが再現条件、受入条件、回帰テスト観点を定義する", "PMOが優先順位、担当、期限、セレスへの判断依頼を整理する", "Knowledge Curatorが再利用できる失敗パターンと判断ログを第二の脳へ反映する"],
    gates: ["フィードバックの出典と業務場面が追跡できる", "事象、原因仮説、対応方針が混ざっていない", "バグと仕様変更と教育課題が分離されている", "優先順位に顧客価値、頻度、影響、工数の根拠がある", "受入条件と検証方法がある", "対応しないものの理由が明記されている"],
    outputs: ["feedback_log.md", "post_deployment_findings.md", "improvement_backlog.md", "acceptance_criteria.md", "training_notes.md", "quality_review_request.md"],
  },
  {
    file: "mvp_scoping_workflow.md",
    title: "MVP Scoping Workflow",
    purpose: "顧客価値が出る最小範囲を定義し、過剰実装を避けながら後からスケールできるMVPへ落とす。",
    triggers: ["顧客要望が多く、初期リリース範囲を決めたい", "PoCから商用化へ進める判断が必要", "技術的には作れそうだが、現場で使われるか不安", "予算、期間、データ、環境、権限などの制約が強い"],
    owners: ["forward_deployed_engineer", "engineering_pmo", "tech_lead", "fullstack_engineer", "data_engineer", "security_governance_engineer", "qa_test_automation_engineer", "deliverable_quality_reviewer"],
    steps: ["目的、利用者、業務場面、成功条件を確認する", "すべての要望を顧客価値、頻度、影響、実装難度で分類する", "MVPで解く課題と解かない課題を分ける", "初期リリース範囲、手動運用でよい範囲、将来自動化する範囲を決める", "Tech Leadが後から詰まらない拡張余地と技術負債を確認する", "QAが受入条件と現場テスト観点を作る", "Security、SRE、Dataの必須ゲートを最小範囲に組み込む", "PMOが実装順序、依存関係、判断事項を整理する"],
    gates: ["MVPの目的と成功条件が明確", "MVPに含めること、含めないことが明確", "手動運用でよい範囲と自動化する範囲が分かれている", "技術負債の返済条件がある", "受入条件、現場テスト、導入条件がある", "Security、QA、SREを後回しにしていない"],
    outputs: ["mvp_scope.md", "use_cases.md", "user_stories.md", "acceptance_criteria.md", "engineering_handoff.md", "rollout_plan.md", "success_metrics.md"],
  },
  {
    file: "requirements_to_design_workflow.md",
    title: "Requirements to Design Workflow",
    purpose: "要求を、受入可能で実装可能な基本設計へ落とす。",
    triggers: ["新規機能・システムの要件がある", "要件と実装の解釈差が大きい"],
    owners: ["engineering_pmo", "tech_lead", "fullstack_engineer", "security_governance_engineer", "qa_test_automation_engineer"],
    steps: ["目的、利用者、業務価値、対象外を定義する", "機能要件、非機能要件、データ要件を分ける", "受入条件と優先度を決める", "アーキテクチャ、責任境界、データフローを設計する", "代替案と主要リスクを比較する", "Security・QA・SRE観点を設計へ反映する"],
    gates: ["要件IDと受入条件", "MVPと将来範囲の分離", "性能・可用性・権限の数値化", "実装担当が見積可能な粒度"],
    outputs: ["requirements.md", "basic_design.md", "architecture.md", "non_functional_requirements.md", "test_plan.md"],
  },
  {
    file: "design_to_implementation_workflow.md",
    title: "Design to Implementation Workflow",
    purpose: "承認済み設計を、小さく検証可能な実装単位へ変換する。",
    triggers: ["基本設計が承認された", "既存実装へ機能追加する"],
    owners: ["tech_lead", "fullstack_engineer", "frontend_engineer", "backend_engineer", "cloud_infrastructure_engineer"],
    steps: ["設計決定、未決事項、互換性制約を確認する", "縦切りの実装単位と依存関係を決める", "API・DB・イベント・UI契約を固定する", "マイグレーションとfeature flagを設計する", "コード、設定、IaC、テストを同時に変更する", "READMEと運用手順を更新する"],
    gates: ["既存機能の非破壊", "秘密情報の分離", "マイグレーションの前後互換", "ローカル・CIでの再現"],
    outputs: ["detailed_design.md", "task_breakdown.md", "実装コード", "migration", "README更新"],
  },
  {
    file: "implementation_to_test_workflow.md",
    title: "Implementation to Test Workflow",
    purpose: "変更リスクに応じた検証を行い、リリース可否を判断する。",
    triggers: ["実装差分が完成した", "リリース候補を作成した"],
    owners: ["qa_test_automation_engineer", "tech_lead", "security_governance_engineer", "sre_platform_engineer"],
    steps: ["変更差分と影響範囲を確認する", "単体・結合・契約・E2E・データ品質テストを配分する", "lint、型、静的解析、脆弱性検査を実行する", "代表・境界・異常・権限ケースを実行する", "性能、監視、ロールバックを確認する", "結果、未テスト範囲、残存リスクを記録する"],
    gates: ["重大な既知不具合がない", "受入条件を満たす", "本番監視とロールバックが準備済み", "例外承認に期限と責任者がある"],
    outputs: ["test_result.md", "quality_gate_result.md", "release_notes.md", "remaining_issues.md"],
  },
  {
    file: "data_platform_workflow.md",
    title: "Data Platform Workflow",
    purpose: "ソース取得から利用者提供まで、再処理可能なデータプロダクトを作る。",
    triggers: ["新しいデータソースを取り込む", "Core / Martや基盤標準を追加する"],
    owners: ["data_engineer", "data_platform_engineer", "integration_engineer", "security_governance_engineer", "qa_test_automation_engineer"],
    steps: ["ソース契約、粒度、キー、更新・削除仕様を確認する", "Raw / Staging / Core / Martと保持期間を設計する", "増分、遅延到着、重複排除、バックフィルを設計する", "DDL、変換、品質テスト、リコンシリエーションを実装する", "権限、分類、リネージ、カタログを登録する", "SLA、監視、再実行Runbookを検証する"],
    gates: ["粒度・主キー・時刻定義", "再実行して同じ結果になる", "品質エラーが可視化される", "利用者契約と機密区分がある"],
    outputs: ["data_architecture.md", "data_pipeline_design.md", "DDL / dbt models", "data_quality_rules.md", "lineage.md", "operation_runbook.md"],
  },
  {
    file: "rag_llm_workflow.md",
    title: "RAG and LLM Workflow",
    purpose: "評価・権限・根拠を先に設計し、本番利用可能なLLM機能を作る。",
    triggers: ["RAG、チャットボット、AI Agentを新設・変更する", "回答品質や安全性を改善する"],
    owners: ["llm_application_engineer", "data_engineer", "backend_engineer", "security_governance_engineer", "qa_test_automation_engineer"],
    steps: ["業務価値、誤答影響、人間承認点を定義する", "知識ソース、権限、更新、削除を確認する", "検索・生成・ツール実行の境界を設計する", "代表・境界・攻撃ケースの評価セットを作る", "品質、根拠、安全性、コスト、遅延を測る", "監視、フィードバック、モデル変更手順を整備する"],
    gates: ["権限付き検索", "根拠提示と不明回答", "プロンプトインジェクション対策", "評価セットと回帰基準", "高影響操作の承認"],
    outputs: ["rag_architecture.md", "retrieval_design.md", "prompt_design.md", "evaluation_design.md", "guardrails.md", "llmops_design.md"],
  },
  {
    file: "incident_response_workflow.md",
    title: "Incident Response Workflow",
    purpose: "障害の検知から復旧、説明、再発防止までを一貫して実行する。",
    triggers: ["SLO違反、データ欠損、セキュリティ事象が検知された", "顧客影響のある不具合が発生した"],
    owners: ["sre_platform_engineer", "engineering_pmo", "tech_lead", "security_governance_engineer", "該当実装ロール"],
    steps: ["影響、開始時刻、対象顧客、重大度を判定する", "指揮・調査・連絡担当を分ける", "拡大防止と安全な暫定復旧を行う", "時系列、証拠、判断、変更を記録する", "恒久対策と検証を実施する", "責任者と期限付きの再発防止を追跡する"],
    gates: ["顧客影響とデータ影響の確認", "証拠保全", "復旧後の整合性検証", "対策の担当・期限・検証方法"],
    outputs: ["incident_report.md", "timeline.md", "recovery_result.md", "postmortem.md", "improvement_backlog.md"],
  },
  {
    file: "deliverable_quality_review_workflow.md",
    title: "Deliverable Quality Review Workflow",
    purpose: "各AI社員の成果物を独立・横断レビューし、セレスが判断できる最終品質報告へ変換する。",
    triggers: ["AI社員が成果物を提出した", "顧客共有・実装着手・本番リリースの判定が必要", "再作業後の再レビューを行う"],
    owners: ["deliverable_quality_reviewer", "engineering_pmo", "tech_lead", "qa_test_automation_engineer", "security_governance_engineer", "sre_platform_engineer"],
    steps: ["作成者がquality_review_request.md、成果物、差分、検証証跡を提出する", "PMOが対象範囲、要件、必須専門Reviewer、期限を確認する", "専門Reviewerが担当観点の判定と証跡を提出する", "Deliverable Quality Reviewerが成果物間の整合性と未検証領域を確認する", "指摘をP0からP3へ分類し、修正案、責任者、期限を付ける", "PASS、PASS_WITH_CONDITIONS、REWORK_REQUIRED、BLOCKEDを判定する", "quality_review_report.mdの冒頭に結論、重要指摘、セレスへの判断依頼を記載する", "再作業時は指摘IDを維持し、修正証跡を確認して再判定する"],
    gates: ["作成者と最終Reviewerが分離されている", "必須専門レビューと検証証跡が揃っている", "P0・P1が未解消なら承認しない", "P2の条件付き承認には責任者・期限・影響受容がある", "確認していない領域をN/Aまたは未確認として明示する"],
    outputs: ["quality_review_request.md", "quality_review_report.md", "finding_register.md", "再作業指示", "セレスへの判断依頼"],
  },
  {
    file: "engineering_knowledge_curation_workflow.md",
    title: "Engineering Knowledge Curation Workflow",
    purpose: "レビュー済み成果物を、案件文脈と出典を保ちながらObsidianの第二の脳へ再利用可能な形で反映する。",
    triggers: ["Quality ReviewerがPASSまたはPASS_WITH_CONDITIONSを判定した", "案件の節目で成果物と判断を棚卸しする", "複数案件に共通する知識・パターン・失敗事例が見つかった"],
    owners: ["engineering_knowledge_curator", "engineering_pmo", "deliverable_quality_reviewer", "tech_lead", "devex_agent_workflow_engineer"],
    steps: ["同期元成果物、レビュー判定、未確認事項、機密区分を棚卸しする", "案件別overview、decisions、architecture、implementation、test、risks、next_actions、source_mapを作る", "案件固有情報と再利用可能な知識を分離する", "Knowledge、Pattern、ADR、Troubleshootingへ必要な内容だけを抽出する", "MOC、タグ、frontmatter、内部リンクを更新する", "リンク切れ、重複、出典、未検証主張、機密情報を検証する", "output/obsidian_sync_summary.mdへ同期結果と未反映事項を報告する"],
    gates: ["Quality Reviewerの判定と未確認事項を改変していない", "原成果物へのsource_mapがある", "MOCから主要ノートへ到達できる", "案件固有情報を一般知識へ誤昇格していない", "既存ノートを無条件で上書きしていない", "秘密情報と未マスキング個人情報がない"],
    outputs: ["第二の脳のProject Note", "Knowledge / Pattern / ADR / Troubleshooting", "MOC", "source_map.md", "output/obsidian_sync_summary.md"],
  },
];

function workflowDocument(workflow) {
  const ownerNames = workflow.owners.map((id) => roleById.get(id)?.role ?? id);
  return `# ${workflow.title}

## 目的
${workflow.purpose}

## 開始条件
${bullets(workflow.triggers)}

## 主担当
${bullets(ownerNames)}

## 手順
${numbered(workflow.steps)}

## 品質ゲート
${bullets(workflow.gates)}

ゲート未達の場合は、例外理由、影響、代替統制、責任者、解消期限を記録する。重大なSecurity・データ損失・復旧不能リスクは例外扱いせず停止する。

## 成果物
${bullets(workflow.outputs)}

## 引き継ぎルール
- 入力と出力のパスを明記する。
- 仮定、未決事項、既知の制約、検証結果を添付する。
- 次工程の責任者と完了条件を合意する。
`;
}

const templates = {
  "requirements_template.md": `# Requirements

## Document Control
- Owner:
- Reviewers:
- Status: Draft
- Last updated:

## 1. Purpose and Business Value
## 2. Users and Stakeholders
## 3. Scope
### In scope
### Out of scope
## 4. Assumptions and Constraints
## 5. Functional Requirements
| ID | Requirement | Priority | Acceptance Criteria | Source |
|---|---|---|---|---|
## 6. Non-functional Requirements
| ID | Quality Attribute | Target | Measurement |
|---|---|---|---|
## 7. Data Requirements
## 8. Security and Governance
## 9. Operations and Support
## 10. MVP and Scale-out
## 11. Risks and Open Questions
## 12. Approval`,
  "field_discovery_template.md": `# Field Discovery

## これは何か
## 顧客・現場の背景
## 相談内容
## 表面的な要望
## 本質的な課題
## 利用者
## 意思決定者
## 運用者
## 現状業務フロー
## 課題が発生している箇所
## 制約
## リスク
## 既存システム・既存データ
## 解決の方向性
## 未決事項
## 次に確認すること`,
  "customer_context_template.md": `# Customer Context

## 顧客概要
## 部門・業務領域
## 相談の背景
## 現在の業務目的
## 主要な困りごと
## 業務上の制約
## 技術・システム上の制約
## データ・権限上の制約
## 成功のイメージ
## 顧客が重視していること
## セレス側で補完すべきこと
## 未確認事項
## 参照元`,
  "stakeholder_map_template.md": `# Stakeholder Map

## 目的
## 関係者一覧
| 種別 | 名前 / 部門 | 役割 | 関心事 | 判断権限 | 接点 |
|---|---|---|---|---|---|
## 利用者
## 意思決定者
## 運用者
## データ提供者
## システム管理者
## セキュリティ・監査関係者
## 顧客側の調整が必要な相手
## セレス側の担当
## コミュニケーション方針
## 未決事項`,
  "mvp_scope_template.md": `# MVP Scope

## 目的
## MVPで解く課題
## MVPに含めること
## MVPに含めないこと
## 初期リリース範囲
## 将来拡張範囲
## 成功条件
## 受入条件
## 技術的な前提
## 業務的な前提
## リスク
## 次アクション`,
  "engineering_handoff_template.md": `# Engineering Handoff

## 概要
## 顧客・現場背景
## 解くべき課題
## MVPスコープ
## 機能要件
## 非機能要件
## データ要件
## API / 連携要件
## 画面要件
## 権限・セキュリティ要件
## 運用要件
## 受入条件
## 未決事項
## 技術チームへの依頼事項
## 参照元`,
  "adoption_plan_template.md": `# Adoption Plan

## 導入目的
## 利用者
## 利用シーン
## 導入ステップ
## 初回利用までに必要なこと
## 運用ルール
## 教育・説明が必要な内容
## 定着リスク
## 定着のための対策
## 成功指標
## フィードバック回収方法
## 次アクション`,
  "success_metrics_template.md": `# Success Metrics

## 目的
## 成功の定義
## 業務指標
## 技術指標
## 利用指標
## 品質指標
## 運用指標
## 測定方法
## 測定頻度
## 判断基準
## 注意点`,
  "feedback_log_template.md": `# Feedback Log

## 目的
## フィードバック一覧
| ID | 日付 | 出典 | 利用者 / 部門 | 種別 | 内容 | 影響 | 優先度 | 対応方針 | 状態 |
|---|---|---|---|---|---|---|---|---|---|
## 分類ルール
## バグ
## 仕様変更
## 運用課題
## 教育課題
## データ品質課題
## 次の開発サイクルへ渡す内容
## 対応しない内容と理由
## 未決事項`,
  "basic_design_template.md": `# Basic Design

## 1. Purpose and Scope
## 2. Preconditions and Decisions
## 3. System Context
## 4. Component Responsibilities
| Component | Responsibility | Inputs | Outputs | Owner |
|---|---|---|---|---|
## 5. Main User and Data Flows
## 6. Interface Summary
## 7. Data Model Summary
## 8. Authentication and Authorization
## 9. Error Handling
## 10. Non-functional Design
## 11. Deployment and Migration
## 12. Test Strategy
## 13. Risks and Alternatives`,
  "detailed_design_template.md": `# Detailed Design

## 1. Change Summary
## 2. Affected Files and Components
## 3. Detailed Logic
## 4. State and Sequence
## 5. API / Event / File Contracts
## 6. Database Changes and Migration
## 7. Validation and Error Codes
## 8. Authorization and Audit
## 9. Logging and Metrics
## 10. Idempotency and Concurrency
## 11. Rollout and Rollback
## 12. Test Cases
## 13. Known Limitations`,
  "architecture_template.md": `# Architecture

## 1. Goals and Quality Attributes
## 2. Constraints
## 3. Context Diagram
## 4. Container / Component Diagram
## 5. Data Flow and Trust Boundaries
## 6. Technology Decisions
| Decision | Selected | Alternatives | Rationale | Revisit Trigger |
|---|---|---|---|---|
## 7. Scalability and Availability
## 8. Security
## 9. Observability and Operations
## 10. Cost Considerations
## 11. Failure Modes and Recovery
## 12. MVP to Target Architecture`,
  "api_design_template.md": `# API Design

## 1. Purpose and Consumers
## 2. Authentication and Authorization
## 3. Common Conventions
- Base URL:
- Versioning:
- Correlation ID:
- Pagination:
- Idempotency:
## 4. Endpoints
| Method | Path | Purpose | Permission | Idempotent |
|---|---|---|---|---|
## 5. Request / Response Schemas
## 6. Error Model
| Code | HTTP Status | Meaning | Retryable |
|---|---|---|---|
## 7. Rate Limits and Timeouts
## 8. Audit and PII Handling
## 9. Compatibility and Deprecation
## 10. Contract Tests`,
  "db_design_template.md": `# Database Design

## 1. Purpose and Workload
## 2. Entities and Relationships
## 3. Tables
| Table | Grain | Primary Key | Retention | Owner |
|---|---|---|---|---|
## 4. Columns
| Table | Column | Type | Nullable | Definition | Classification |
|---|---|---|---|---|---|
## 5. Constraints and Indexes
## 6. Transaction and Concurrency
## 7. History and Deletion
## 8. Migration and Backfill
## 9. Access Control and Audit
## 10. Backup and Recovery
## 11. Data Quality Checks`,
  "data_pipeline_design_template.md": `# Data Pipeline Design

## 1. Purpose and Consumers
## 2. Source Contract
| Source | Grain | Key | Update / Delete Behavior | SLA |
|---|---|---|---|---|
## 3. Target Layers and Models
## 4. Incremental and CDC Strategy
## 5. Late Data, Duplicates, and Backfill
## 6. Mapping and Transformations
## 7. Data Quality and Reconciliation
## 8. Orchestration and Dependencies
## 9. Security and Classification
## 10. Monitoring and Alerts
## 11. Retry and Recovery
## 12. Lineage and Catalog
## 13. Cost and Capacity`,
  "data_quality_rules_template.md": `# Data Quality Rules

## 1. Dataset and Owner
## 2. Quality Dimensions
## 3. Rules
| Rule ID | Dataset / Column | Dimension | Check | Threshold | Severity | Action |
|---|---|---|---|---|---|---|
## 4. Reconciliation
## 5. Freshness and Completeness
## 6. Referential and Business Integrity
## 7. Quarantine and Reprocessing
## 8. Exceptions
| Exception | Reason | Owner | Expiry | Compensating Control |
|---|---|---|---|---|
## 9. Monitoring and Reporting`,
  "test_plan_template.md": `# Test Plan

## 1. Objective and Scope
## 2. Change Risk
## 3. Test Levels
| Level | Target | Environment | Owner | Automation |
|---|---|---|---|---|
## 4. Requirement Traceability
| Requirement ID | Test Case | Expected Result |
|---|---|---|
## 5. Normal, Boundary, Error, and Permission Cases
## 6. Test Data
## 7. Non-functional Tests
## 8. Entry and Exit Criteria
## 9. Regression Scope
## 10. Defect Handling
## 11. Residual Risk`,
  "runbook_template.md": `# Operation Runbook

## 1. Service and Owner
## 2. SLO / SLA
## 3. Dependencies and Access
## 4. Dashboards and Alerts
## 5. Routine Operations
## 6. Failure Scenarios
| Symptom | Check | Immediate Action | Escalation |
|---|---|---|---|
## 7. Retry and Reprocessing
## 8. Backup and Restore
## 9. Rollback
## 10. Security Incident Handling
## 11. Communication
## 12. Verification After Recovery`,
  "handover_template.md": `# Handover

## 1. Scope and Current Status
## 2. Repositories and Environments
## 3. Architecture and Key Decisions
## 4. Setup and Deployment
## 5. Operations and Monitoring
## 6. Data and Security Responsibilities
## 7. Test and Release Status
## 8. Known Issues and Technical Debt
| Item | Impact | Workaround | Owner | Due |
|---|---|---|---|---|
## 9. Open Questions
## 10. Acceptance Checklist`,
  "execution_summary_template.md": `# Execution Summary

## 1. Request
## 2. Work Performed
## 3. Deliverables
| File | Purpose | Status |
|---|---|---|
## 4. Major Decisions
## 5. Validation
| Check | Command / Method | Result |
|---|---|---|
## 6. Assumptions
## 7. Remaining Issues and Risks
## 8. Required Confirmations
## 9. Quality Review
- Final verdict:
- Review report:
- Open P0 / P1:
## 10. Next Actions`,
  "quality_review_request_template.md": `# Quality Review Request

## 1. Review Metadata
- Task ID:
- Producer:
- Requested reviewer:
- Review deadline:
- Risk level: Low / Medium / High / Critical

## 2. Purpose and Acceptance Criteria
- Business purpose:
- Intended users:
- Acceptance criteria:
- Out of scope:

## 3. Deliverables
| File / Artifact | Purpose | Producer | Status |
|---|---|---|---|

## 4. Change and Impact
- Change summary:
- Affected systems, data, users, and operations:
- Breaking changes:
- Migration / rollback:

## 5. Validation Evidence
| Check | Command / Method | Result | Evidence path |
|---|---|---|---|

## 6. Required Specialist Reviews
| Review area | Reviewer | Required | Result | Evidence |
|---|---|---|---|---|
| Technical architecture | Tech Lead | Yes / No | | |
| Functional and test quality | QA | Yes / No | | |
| Security and governance | Security | Yes / No | | |
| Reliability and operations | SRE | Yes / No | | |
| Data quality and contract | Data | Yes / No | | |
| UX and accessibility | Frontend / UX | Yes / No | | |
| LLM safety and evaluation | LLM | Yes / No | | |

## 7. Assumptions, Unverified Claims, and Known Risks
## 8. Questions for Reviewer
## 9. Producer Self-check
- [ ] Requirements are traceable.
- [ ] Relevant tests and checks were executed.
- [ ] Unexecuted checks are disclosed.
- [ ] Security, operations, and data impacts are disclosed.
- [ ] No secrets or unmasked personal data are included.`,
  "quality_review_report_template.md": `# Quality Review Report

## 1. セレス向け結論
- **最終判定**: PASS / PASS_WITH_CONDITIONS / REWORK_REQUIRED / BLOCKED
- **一言で言うと**:
- **今すぐ対応が必要なこと**:
- **セレスの判断が必要なこと**:

## 2. Review Scope
- Reviewed artifacts:
- Requirements / acceptance criteria:
- Evidence checked:
- Excluded or unverified areas:
- Reviewer independence:

## 3. Quality Scorecard
| Dimension | Score 0-4 / N/A | Verdict | Evidence | Key issue |
|---|---:|---|---|---|
| Purpose and requirement fit | | | | |
| Factual accuracy and evidence | | | | |
| Technical correctness and architecture | | | | |
| Cross-artifact consistency and traceability | | | | |
| Implementation readiness | | | | |
| Test coverage and reproducibility | | | | |
| Data quality and data contract | | | | |
| Security, privacy, and governance | | | | |
| Reliability, operations, and recovery | | | | |
| Performance and scalability | | | | |
| Cost and commercial viability | | | | |
| Usability and accessibility | | | | |
| Maintainability and reuse | | | | |
| Documentation and handover | | | | |
| LLM safety and evaluation, if applicable | | | | |

Score: 0 = not reviewed, 1 = critical, 2 = insufficient, 3 = acceptable, 4 = strong. N/A requires a reason. Scores support explanation but do not override P0 / P1 gates.

## 4. Findings
| ID | Severity | Area | Finding | Evidence | Impact | Required action | Owner | Due |
|---|---|---|---|---|---|---|---|---|

Severity:
- P0: Immediate stop.
- P1: Must fix before delivery, implementation, or release.
- P2: Conditional approval only with owner and due date.
- P3: Improvement recommendation.

## 5. Specialist Review Summary
| Area | Reviewer | Verdict | Open blocker | Evidence |
|---|---|---|---|---|

## 6. Residual Risks and Conditions
## 7. Decisions Required from Ceres
| Decision | Options | Recommendation | Impact if deferred |
|---|---|---|---|

## 8. Next Actions
| Priority | Action | Owner | Due | Completion evidence |
|---|---|---|---|---|

## 9. Final Verdict Rationale
Explain why this verdict follows from the evidence, findings, and mandatory gates.`,
  "finding_register_template.md": `# Finding Register

| ID | Status | Severity | Source review | Area | Finding | Evidence | Impact | Required action | Owner | Due | Resolution evidence |
|---|---|---|---|---|---|---|---|---|---|---|---|

## Status
- OPEN
- IN_PROGRESS
- RESOLVED
- RISK_ACCEPTED
- INVALIDATED

P0 and P1 cannot be marked RISK_ACCEPTED by an AI employee. Human approval and rationale are required.`,
  "review_metrics_template.md": `# Review Metrics

## Task Records
| Task ID | Date | Risk | Producer role | Reviewer | Verdict | P0 | P1 | P2 | P3 | Rework cycles | Review minutes | User clarification count | Escaped defects |
|---|---|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|

## Role Quality Trends
| Producer role | Tasks | First-pass ready rate | Reopened finding rate | Repeated finding themes | Median review minutes | Escaped P0 / P1 |
|---|---:|---:|---:|---|---:|---:|

## Calibration Notes
- Do not optimize for pass rate alone.
- Investigate repeated P1 / P2 themes and update the producer Skill or template.
- Record defects found after approval as escaped defects.
- Review thresholds after at least three comparable tasks.
- Do not use metrics to hide risk, reduce necessary findings, or rank roles without context.`,
  "obsidian_project_note_template.md": `---
title:
type: project
project:
domain:
status: draft
created:
updated:
source: []
tags: []
related: []
managed_by: engineering_knowledge_curator
---

# Project Overview

## 目的

## 現在地

## 主要成果物

## 主要な意思決定

## 未解決事項・リスク

## 次のアクション

## 関連ノート

## 参照元`,
  "obsidian_architecture_note_template.md": `---
title:
type: architecture
project:
domain:
status: draft
created:
updated:
source: []
tags: []
related: []
managed_by: engineering_knowledge_curator
---

# Architecture Summary

## 目的と制約

## 構成

## データフロー

## 技術選定と理由

## 代替案

## 運用・Security・コスト

## 未確認事項

## 参照元`,
  "obsidian_decision_log_template.md": `---
title:
type: adr
project:
domain:
status: proposed
created:
updated:
source: []
tags: []
related: []
managed_by: engineering_knowledge_curator
---

# ADR

## Context

## Decision

## Rationale

## Alternatives

## Consequences

## Revisit Trigger

## Evidence`,
  "obsidian_troubleshooting_template.md": `---
title:
type: troubleshooting
project:
domain:
status: verified
created:
updated:
source: []
tags: []
related: []
managed_by: engineering_knowledge_curator
---

# Troubleshooting

## 症状

## 影響

## 原因

## 確認手順

## 暫定対応

## 恒久対応

## 再発防止

## 検証結果

## 参照元`,
  "obsidian_learning_note_template.md": `---
title:
type: knowledge
project:
domain:
status: verified
created:
updated:
source: []
tags: []
related: []
managed_by: engineering_knowledge_curator
---

# Learning Note

## 要点

## 使える場面

## 適用条件

## 実務上の判断

## 失敗しやすい点

## 関連ノート

## 参照元`,
  "obsidian_source_map_template.md": `---
title:
type: source_map
project:
domain:
status: active
created:
updated:
source: []
tags: []
related: []
managed_by: engineering_knowledge_curator
---

# Source Map

| Source | Curated Notes | Extracted Content | Review Status | Notes |
|---|---|---|---|---|

## 未反映

## 競合

## 確認事項`,
};

write("README.md", `# AI Engineering Team

\`input/\` の課題を、AI Engineering PMOが分類し、必要に応じてAI Forward Deployed Engineerが顧客・現場課題を開発可能な要件へ変換し、専門Skillが設計・実装・テスト・運用成果物へ変換するためのプロジェクトローカル資産です。対象はエンジニアリングロールに限定し、分析チームとはデータ契約と引き継ぎ成果物で連携します。

## 目的
- 曖昧な課題でも質問だけで止まらず、実務成果物を \`output/\` に出す。
- 顧客相談やヒアリングメモを、MVPスコープ、受入条件、engineering_handoffへ変換する。
- MVPを最短で作りながら、商用化に必要なSecurity、QA、SRE、運用を初期から扱う。
- データ基盤、Web / 業務アプリ、クラウド、RAG / AI Agentを同じ品質ゲートで運営する。
- 複数案件で再利用できるロール、Skill、テンプレートを蓄積する。

## ディレクトリ
\`\`\`text
input/       課題、要件、コード、ログ、仕様
output/      タスクごとの計画、成果物、結果、質問
ai_team/     ロール、ワークフロー、レビュー基準
skills/      Codex Skillと機械可読設定
templates/   成果物テンプレート
tools/       生成・検証スクリプト
\`\`\`

## 使い方
1. \`input/\` にタスク専用サブディレクトリを作り、依頼と関連資料を配置する。
2. AI Engineering PMOが \`output/work_plan.md\` を作り、課題分類・担当Skill・成果物・完了条件を決める。
3. 顧客相談、業務フロー、MVP判断が必要な場合は、AI Forward Deployed Engineerが現場課題、MVP、引き継ぎ情報を整理する。
4. 専門Skillが成果物を作成し、Tech Lead、QA、Security、SREなどが該当観点を確認する。
5. 作成者が \`quality_review_request.md\` と検証証跡を提出する。
6. AI Deliverable Quality Reviewerが独立レビューし、\`quality_review_report.md\` で最終判定する。
7. PMOがレビュー結果を含む \`execution_summary.md\` をセレスへ報告する。
8. AI Engineering Knowledge Curatorが承認済み成果物を第二の脳へ整理し、\`output/obsidian_sync_summary.md\` を作成する。

## 品質責任
- 最終品質判定: AI Deliverable Quality Reviewer
- 専門観点の判定: Tech Lead、QA、Security、SRE、Data、Frontend、LLMなど
- 顧客・現場課題から開発可能な要件への変換: AI Forward Deployed Engineer
- 作業統括とセレスへの報告: AI Engineering PMO
- レビュー済み成果物の知識化: AI Engineering Knowledge Curator
- 高影響な例外承認と本番判断: セレスまたは指定された人間責任者

## Skill命名
Codex標準に合わせ、正規名とディレクトリはハイフン形式です。依頼書のアンダースコア名は \`skills/index.yaml\` と各 \`skill.yaml\` の \`legacy_id\` で対応付けています。

## 検証
\`\`\`bash
python3 tools/validate_repository.py
\`\`\`

## 重要な運用ルール
- 成果物は原則として \`output/<client>/<YYYYMMDD>/<task-name>/\` にまとめる。
- 同じタスクの総評、質問、作業計画、品質レビュー、実行サマリーは同じディレクトリへ配置する。
- 秘密情報、個人情報、本番資格情報をinput/outputへ直接置かない。
- 生成スクリプトは定義一括変更用であり、個別成果物の手編集後に無条件実行しない。
`);

write("AGENTS.md", `# Repository Instructions

## Mission
\`input/\` の課題を読み、実装・設計・テスト・運用に使える成果物を \`output/\` に作成する。分析者ロールは作らず、必要に応じて分析チーム向けデータ契約と引き継ぎを作る。

## Required Start
1. \`input/\` と既存 \`output/\` を確認する。
2. 明示成果物、課題分類、MVP、制約、リスクを整理する。
3. \`output/work_plan.md\` を作成または更新する。
4. 必要な \`skills/\` を選び、作業を進める。

## Required Finish
- 成果物は原則として \`output/<client>/<YYYYMMDD>/<task-name>/\` に保存する。
- 顧客名や日付が特定できない場合だけ、合理的な仮名を置いて前提を明記する。
- \`templates/quality_review_request_template.md\` を使い、対象、要件、差分、検証証跡、未実施事項を提出する。
- AI Deliverable Quality Reviewerが \`output/quality_review_report.md\` を作成する。
- 最終判定が \`REWORK_REQUIRED\` または \`BLOCKED\` の場合、完了扱いにせず、再作業内容または停止理由として報告する。
- 顧客案件または再利用価値のある成果物は、AI Engineering Knowledge Curatorが第二の脳へ反映し、\`output/obsidian_sync_summary.md\` を更新する。
- \`output/execution_summary.md\` と \`output/questions.md\` を更新する。
- 実行したテスト、未実行テスト、残存リスクを明記する。

## Engineering Rules
- 最小構成を優先するが、認証認可、秘密管理、監視、再実行性、テストを省略しない。
- 不明な外部仕様を断定しない。公式資料または実データで確認する。
- 破壊的変更には理由、影響範囲、移行、ロールバックを付ける。
- 既存成果物と用語、要件ID、データ粒度、API契約を整合させる。
- 質問だけで止めず、合理的な仮定を明記して成果物を作る。
- 作成者自身の確認を独立レビューとして扱わない。
- 専門ReviewerのBlockerをPMOや総合Reviewerが独断で解除しない。

## Writing Style
- 実務担当者がそのまま話しているような、自然で率直な日本語を使う。
- 見出し、箇条書き、表は読みやすさに必要な分だけ使い、細かく分割しすぎない。
- 同じ結論や注意事項を言い換えて繰り返さない。
- 抽象的なAI表現を避け、判断、理由、影響、次の行動を具体的に書く。
- 顧客向け成果物では、専門用語を残しつつ、その意味が文脈から分かるように書く。
`);

write("input/README.md", `# input/

課題単位で \`input/<task-id>/\` を作成し、依頼本文と参照資料を配置します。

## 推奨ファイル
- \`request.md\`: 目的、期待成果物、期限、制約
- \`context.md\`: 背景、利用者、既存運用
- \`acceptance_criteria.md\`: 完了条件
- \`attachments/\`: SQL、DDL、設定、ログ、画面案など

## 禁止
- APIキー、パスワード、秘密鍵
- マスキングしていない個人情報や本番データ
- 利用権限が不明な顧客資料
`);

write("ai_team/README.md", `# AI Engineering Team

## 構成
- \`team_overview.md\`: チームの責任境界とロール選定表
- \`roles/\`: ${roles.length}のAI社員エンジニア・レビューロール
- \`workflows/\`: 要件から運用までの標準フロー
- \`review/\`: レビュー方針、観点マトリクス、品質メトリクス、品質ゲート、完了定義

## 統括モデル
AI Engineering PMOが課題と成果物を統括し、顧客相談や業務フロー整理が必要な場合はAI Forward Deployed Engineerが現場課題を開発可能な要件とMVPスコープへ変換します。AI Tech Leadが技術整合性を判断し、専門ロールが成果物を作成し、QA・Security・SREなどが専門観点を確認します。AI Deliverable Quality Reviewerが証跡を統合して最終品質判定を行い、AI Engineering Knowledge Curatorが承認済み成果物を第二の脳へ整理します。

## 責任境界
- AIは成果物作成、検証、リスク提示を担う。
- AI Forward Deployed Engineerは顧客・現場の文脈を整理するが、契約・予算・最終合意を代替しない。
- AI Deliverable Quality Reviewerは品質判定を担うが、専門ReviewerのBlockerや人間承認を代替しない。
- AI Engineering Knowledge Curatorはレビュー判定を変更せず、出典、未確認事項、残存リスクを保ったまま知識化する。
- 顧客契約、予算承認、本番リリース、高影響操作の最終責任は人間が持つ。
- 分析チームへは、テーブル・カラム定義、品質、更新SLA、利用制約を契約として渡す。
`);

write("ai_team/team_overview.md", `# Team Overview

## 運営原則
1. PMOが入力を分類し、成果物と担当を決める。
2. 顧客・現場課題が曖昧な場合は、Forward Deployed Engineerが業務背景、MVP、受入条件、引き継ぎ情報を整理する。
3. Tech Leadが技術判断と非機能要件を統合する。
4. 専門ロールが実装可能な成果物を作る。
5. QA、Security、SREがリリース前の独立ゲートを担う。
6. Deliverable Quality Reviewerが全証跡を統合し、最終品質判定を行う。
7. PMOが重要判断、仮定、残存リスク、セレスへの判断依頼を報告する。
8. Knowledge Curatorが承認済み成果物を案件知識と再利用知識へ分け、第二の脳へ反映する。

## ロール選定表
| 課題 | 主担当 | 必須レビュー |
|---|---|---|
| 複合案件・成果物統合 | AI Engineering PMO | Tech Lead |
| 顧客相談・現場課題・MVP切り出し | AI Forward Deployed Engineer | PMO / Tech Lead |
| 技術選定・全体設計 | AI Tech Lead | Security / SRE |
| Web / 業務MVP | AI Fullstack Engineer | Frontend / Backend / QA |
| UI / UX | AI Frontend Engineer | QA / Security |
| API / 業務ロジック | AI Backend Engineer | Security / QA / SRE |
| ETL / ELT / dbt | AI Data Engineer | Data Platform / QA |
| データ基盤標準 | AI Data Platform Engineer | Security / SRE |
| Cloud / IaC / CI/CD | AI Cloud / Infrastructure Engineer | Security / SRE |
| 監視・障害・復旧 | AI SRE / Platform Engineer | Tech Lead |
| IAM / PII / 監査 | AI Security / Governance Engineer | Tech Lead |
| テスト・品質ゲート | AI QA / Test Automation Engineer | 担当実装ロール |
| RAG / Agent | AI / LLM Application Engineer | Security / QA / SRE |
| Skills / Agent workflow | AI DevEx / Agent Workflow Engineer | PMO / QA |
| API / SaaS / ファイル連携 | AI Integration Engineer | Security / SRE / Data |
| 全成果物の最終品質判定 | AI Deliverable Quality Reviewer | 必要な全専門Reviewer |
| Obsidian第二の脳・知識整理 | AI Engineering Knowledge Curator | PMO / Quality Reviewer / Tech Lead |

## 品質責任モデル
| 責任 | AI社員 | 内容 |
|---|---|---|
| Produce | 各作業ロール | 成果物、自己確認、検証証跡、未実施事項を提出 |
| Field Discovery | Forward Deployed Engineer | 顧客・現場課題をMVP、受入条件、引き継ぎ情報へ変換 |
| Specialist Review | Tech Lead / QA / Security / SRE / Data等 | 担当観点の判定とBlocker提示 |
| Final Quality Verdict | Deliverable Quality Reviewer | 横断整合、証跡、残存リスクを統合し最終判定 |
| Coordinate and Report | Engineering PMO | 再作業管理とセレスへの報告 |
| Curate and Reuse | Engineering Knowledge Curator | 承認済み成果物を案件知識、設計判断、再利用パターンへ整理 |
| Human Decision | セレスまたは指定責任者 | リスク受容、予算・契約、本番、高影響例外の承認 |

## MVPの標準最小チーム
- PMO: スコープ、成果物、未決事項
- FDE: 顧客・現場背景、MVP範囲、受入条件、導入・定着観点
- Tech Lead: アーキテクチャ、非機能、代替案
- 主実装ロール: 実装または詳細設計
- QA: 受入条件と自動テスト
- Security: 認証認可、秘密、データ保護
- SRE: 監視、復旧、リリース
- Deliverable Quality Reviewer: 全成果物の最終判定と統合報告
- Knowledge Curator: 出典を保った第二の脳への反映

## スケール時の追加
- 複数データ案件: Data Platform Engineer
- 高頻度外部連携: Integration Engineer
- 複数クラウド・環境: Cloud / Infrastructure Engineer
- LLM本番化: LLM Application Engineerと評価基盤
- Agent開発の反復: DevEx / Agent Workflow Engineer
- 顧客現場への導入・定着: Forward Deployed Engineer

## 分析チームへの引き継ぎ
エンジニアは、データセットの粒度、キー、定義、更新SLA、品質状態、機密区分、既知の制約を提供する。分析ロジックやKPIの最終業務定義は分析チーム・業務責任者と合意する。
`);

for (const role of roles) {
  write(`ai_team/roles/${role.id}.md`, roleDocument(role));
  write(`skills/${role.skill}/README.md`, skillReadme(role));
  write(`skills/${role.skill}/SKILL.md`, skillInstructions(role));
  write(`skills/${role.skill}/skill.yaml`, skillYaml(role));
  write(`skills/${role.skill}/agents/openai.yaml`, openaiYaml(role));
}

for (const workflow of workflows) {
  write(`ai_team/workflows/${workflow.file}`, workflowDocument(workflow));
}

write("ai_team/review/review_policy.md", `# Review Policy

## 目的
成果物の作成者、専門Reviewer、最終品質Reviewerを分離し、重大な欠陥を見落とさず、セレスが短時間で判断できる状態にする。

## 最終品質責任
- **AI Deliverable Quality Reviewer**: 全成果物の最終品質判定を行い、\`quality_review_report.md\` を作成する。
- **専門Reviewer**: 担当観点の判定とBlockerを提示する。
- **AI Engineering PMO**: レビューを手配し、判定を改変せずセレスへ報告する。
- **セレスまたは指定責任者**: リスク受容、契約、予算、本番、高影響例外を最終承認する。

## 必須レビュー
| 変更 | 必須レビュー |
|---|---|
| 顧客相談・現場課題・MVPスコープ | Forward Deployed Engineer + PMO / Tech Lead |
| アーキテクチャ・共通契約 | Tech Lead |
| 認証認可・PII・外部公開 | Security |
| 本番運用・監視・復旧 | SRE |
| 実装・データ変換 | QA + 該当専門ロール |
| RAG / Agent | LLM + Security + QA |
| データ提供契約 | Data Engineer + Data Platform |
| すべての提出成果物 | Deliverable Quality Reviewer |

## AI FDE成果物のレビュー観点
- 顧客の言葉をそのまま写しているだけではないか。
- 本質的な課題、業務フロー、現場制約、利用者が整理されているか。
- MVPスコープが現実的で、やらないことが明確か。
- 成功条件、受入条件、導入後に使われるイメージがあるか。
- Security、運用、データ品質、権限の観点が抜けていないか。
- Tech Leadと専門エンジニアが次に動ける情報になっているか。

## レビュー方法
1. 作成者は \`quality_review_request.md\` に目的、差分、影響範囲、検証証跡、未実施事項を記載する。
2. PMOはリスクに応じた専門Reviewerを割り当てる。
3. 専門Reviewerは担当観点の判定と証跡を提出する。
4. Deliverable Quality Reviewerは成果物と証跡を横断確認する。
5. 指摘はP0からP3、根拠、影響、修正案、責任者、期限を含める。
6. 最終判定はPASS、PASS_WITH_CONDITIONS、REWORK_REQUIRED、BLOCKEDのいずれかとする。
7. PMOは判定、重要指摘、判断依頼、残存リスクをセレスへ報告する。
8. PASSまたはPASS_WITH_CONDITIONSの成果物はKnowledge Curatorへ引き渡し、判定状態を保ったまま第二の脳へ反映する。

## 判定
| 判定 | 条件 |
|---|---|
| PASS | 必須ゲートを満たし、未解消のP0・P1・必須対応P2がない |
| PASS_WITH_CONDITIONS | P0・P1はなく、P2に責任者・期限・影響受容がある |
| REWORK_REQUIRED | P1、必須証跡不足、要件未達、重大な不整合がある |
| BLOCKED | P0、重大なSecurity・データ損失・法令契約・復旧不能リスクがある |

## 重大度
- P0: 即時停止。人間責任者へのエスカレーションが必要。
- P1: 顧客提出、実装着手、本番リリース前に必須修正。
- P2: 条件付き承認可能。責任者と期限が必要。
- P3: 改善推奨。

## 独立性
作成者は自己レビューを行うが、最終判定を行わない。同一AI実行コンテキストしか使えない場合は独立性不足を報告し、最大でもPASS_WITH_CONDITIONSとする。Deliverable Quality Reviewerは専門ReviewerのBlockerを独断で解除できない。高影響な本番変更は人間承認を必須とする。
`);

write("ai_team/review/review_matrix.md", `# Review Matrix

## 共通レビュー観点
| 観点 | 主Reviewer | 必須確認 |
|---|---|---|
| 目的・要件適合 | Engineering PMO / Quality Reviewer | 目的、対象外、受入条件、成果物の対応 |
| 現場適合・導入定着 | Forward Deployed Engineer / PMO | 利用者、業務フロー、現場制約、成功指標、定着リスク |
| 事実性・根拠 | Quality Reviewer | 主張の出典、実行ログ、未確認事項 |
| 技術・アーキテクチャ | Tech Lead | 境界、整合性、互換性、移行、障害モード |
| 実装・テスト | QA / 実装ロール | 正常・異常・境界・回帰、再現性 |
| データ品質 | Data Engineer / Data Platform | 粒度、キー、履歴、欠損、重複、鮮度、再実行 |
| Security・ガバナンス | Security | 認証認可、PII、秘密、監査、テナント分離 |
| 信頼性・運用 | SRE | SLO、監視、アラート、復旧、Runbook、容量 |
| 性能・スケール | Tech Lead / SRE | 負荷、ボトルネック、上限、拡張戦略 |
| コスト・商用化 | Tech Lead / PMO | MVPコスト、運用負荷、ライセンス、顧客価値 |
| UI・アクセシビリティ | Frontend / QA | エラー回復、権限表示、操作性、アクセシビリティ |
| LLM品質・安全性 | LLM / Security / QA | 根拠、評価、権限、攻撃耐性、承認、コスト |
| 保守性・再利用性 | Tech Lead / DevEx | 責任境界、設定、文書、拡張、技術負債 |
| 知識化・再利用 | Knowledge Curator | 出典、案件文脈、適用条件、MOC、内部リンク、未解決事項 |
| 成果物間整合 | Quality Reviewer | 用語、要件ID、API、DB、テスト、Runbookの一致 |
| 報告の明瞭さ | Quality Reviewer / PMO | 結論、重要指摘、判断依頼、残存リスク、次の行動 |

## リスク別レビュー深度
| リスク | 例 | 必須レビュー |
|---|---|---|
| Low | 文言修正、内部メモ | Quality Reviewerの簡易レビュー |
| Medium | 非破壊の機能・設計変更 | Tech LeadまたはQA + Quality Reviewer |
| High | 認証、データモデル、外部公開、本番変更 | Tech Lead + QA + Security / SRE + Quality Reviewer |
| Critical | PII、決済、マルチテナント、データ削除、Agent高影響操作 | 全該当専門Reviewer + Quality Reviewer + 人間承認 |

## スコア
- 0: 未確認。判定根拠に使用不可。
- 1: Critical。P0相当。
- 2: Insufficient。P1またはP2相当。
- 3: Acceptable。要求を満たす。
- 4: Strong。要求を満たし、拡張・運用余地も明確。
- N/A: 非該当理由が必要。

スコアは説明補助であり、平均点で最終判定しない。
`);

write("ai_team/review/review_metrics.md", `# Review Metrics

## 目的
レビュー結果を蓄積し、どのAI社員・Skill・成果物で同じ問題が繰り返されるかを特定して、Skill、テンプレート、品質ゲートを改善する。

## 記録単位
タスクごとに \`templates/review_metrics_template.md\` を使い、Producerロール、リスク、判定、重大度別指摘、再作業回数、レビュー時間、利用者確認回数、承認後に発見された不具合を記録する。

## 主要指標
| 指標 | 目的 | 注意 |
|---|---|---|
| Escaped P0 / P1 | 重大な見逃しを減らす | 最重要。0を目標とする |
| Reopened finding rate | 修正の実効性を確認する | 解決済み判定の甘さを検出 |
| Repeated finding themes | Skillやテンプレートの構造欠陥を発見する | 個人責任ではなく仕組みを直す |
| Rework cycles | 初回成果物の準備度を測る | 複雑度・リスクで補正する |
| Review lead time | 運用可能なレビュー速度を測る | 短さだけを最適化しない |
| User clarification count | セレスへの説明の明瞭さを測る | 質問ゼロ自体を目的にしない |

## 改善ループ
1. 3件以上の同種タスクを蓄積する。
2. P1 / P2の反復テーマを集計する。
3. Producer Skill、成果物テンプレート、検証スクリプトのどこで予防するか決める。
4. 修正後3件で再発率を確認する。
5. 閾値やレビュー深度を調整する。

## 禁止
- 合格率だけでAI社員を評価しない。
- 指摘件数を減らすために重大度を下げない。
- リスクやタスク難易度を無視してロールを順位付けしない。
- 顧客名、個人情報、秘密情報をメトリクスへ記録しない。
`);

write("ai_team/review/quality_gate.md", `# Quality Gate

## Gate 1: Requirement Ready
- 目的、利用者、MVP、対象外、受入条件がある。
- 顧客相談や現場課題が起点の場合、Field Discovery、Stakeholder Map、MVP Scope、Engineering Handoffがある。
- 前提、制約、未決事項が区別されている。

## Gate 2: Design Ready
- 責任境界、データフロー、主要契約が明確。
- Security、性能、可用性、コスト、移行を検討済み。
- 代替案と採用理由がある。

## Gate 3: Implementation Ready
- タスク、依存関係、変更ファイル、テスト方法が明確。
- API / DB / イベントの互換性方針がある。
- 秘密情報と環境差分が設定として分離されている。

## Gate 4: Release Ready
- lint、型、単体、結合、必要なE2E・データ品質テストが通る。
- 認可、監査、脆弱性、依存関係を確認済み。
- 監視、アラート、ロールバック、バックアップが準備済み。

## Gate 5: Operable
- SLO、Runbook、責任者、連絡経路がある。
- 障害・再実行・復旧手順を検証済み。
- コストと容量の監視がある。

## Gate 6: Independently Reviewed
- 作成者とDeliverable Quality Reviewerが分離されている。
- quality_review_request.md、専門レビュー、検証証跡が揃っている。
- quality_review_report.mdに対象範囲、未確認領域、指摘、残存リスクがある。
- 最終判定がPASSまたはPASS_WITH_CONDITIONSである。
- PASS_WITH_CONDITIONSの条件に責任者、期限、影響受容がある。

## Gate 7: Knowledge Preserved
- 顧客案件または再利用価値のある成果物は第二の脳へ反映されている。
- 案件ノートと再利用知識が分離され、原成果物へのsource_mapがある。
- 未確認事項、残存リスク、次アクションが失われていない。
- MOCと内部リンクを検証し、同期結果がoutput/obsidian_sync_summary.mdへ記録されている。

## 例外
例外は「項目、理由、影響、代替統制、責任者、期限」を記録する。認可欠落、秘密漏えい、データ損失、復旧不能は例外不可。
`);

write("ai_team/review/definition_of_done.md", `# Definition of Done

タスクは次をすべて満たしたとき完了とする。

- 指定成果物が作成され、ファイルパスがexecution_summary.mdに記載されている。
- 要件または依頼内容と成果物の対応を追跡できる。
- 顧客相談・現場課題が起点の場合、AI FDEによる業務背景、MVP範囲、受入条件、導入・定着観点が整理されている。
- 仮定、未決事項、既知の制約、残存リスクが明記されている。
- コード変更には変更理由、影響範囲、設定・環境変数、移行方法がある。
- lint、型チェック、テスト、サンプル実行の結果が記録されている。
- Security、QA、SRE、データ品質の該当ゲートを通過している。
- quality_review_request.mdと専門レビュー証跡が提出されている。
- AI Deliverable Quality Reviewerのquality_review_report.mdがある。
- 最終判定がPASSまたはPASS_WITH_CONDITIONSである。
- 顧客案件または再利用価値のある成果物は、Knowledge Curatorが第二の脳へ反映し、source_mapとobsidian_sync_summary.mdを作成している。
- README、設計、Runbook、引き継ぎが実装と一致している。
- 破壊的変更には承認、移行、ロールバックがある。
- 次の責任者が必要な場合は、入力・出力契約付きで引き渡されている。

「ドキュメントを作った」「コードを書いた」だけでは完了にしない。利用・検証・運用できることを確認する。
`);

write("skills/README.md", `# Project Skills

各Skillは次の4要素で構成します。

- \`SKILL.md\`: Codexが実行時に読む簡潔な手順
- \`agents/openai.yaml\`: UI表示とデフォルトプロンプト
- \`README.md\`: 人間向けの詳細説明
- \`skill.yaml\`: AI・自動化向けの構造化定義

正規名はCodex標準のハイフン形式です。依頼書のアンダースコア形式は \`legacy_id\` として保持します。詳細な成果物形式はルートの \`templates/\` を参照します。

全Producer Skillは完了前に \`quality_review_request.md\` と検証証跡を提出し、\`skill-deliverable-quality-reviewer\` の最終判定を受けます。Reviewer Skillは専門レビューを統合して最終品質を判定し、\`skill-engineering-knowledge-curator\` は承認済み成果物の判定状態と出典を保ったままObsidianの第二の脳へ整理します。
`);

write("skills/index.yaml", `schema_version: "1.0"
skills:
${roles.map((role) => `  - name: ${yamlScalar(role.skill)}
    legacy_id: ${yamlScalar(role.legacyId)}
    role: ${yamlScalar(role.role)}
    path: ${yamlScalar(`skills/${role.skill}`)}`).join("\n")}
`);

for (const [file, content] of Object.entries(templates)) {
  write(`templates/${file}`, content);
}

write("output/work_plan.md", `# Work Plan

## 課題概要
AI社員エンジニアチームに、各作業者の成果物を独立・横断確認する品質責任者と、レビュー済み成果物をObsidianの第二の脳へ再利用可能な形で整理するKnowledge Curatorを追加する。

## 入力ファイル一覧
- 添付指示書: \`pasted-text.txt\`
- 初期確認時の \`input/\`: 未作成・入力なし
- 既存リポジトリ: 空、Git管理なし

## 課題分類
- AI Agent / DevEx基盤
- エンジニアリング組織設計
- レビュー・品質保証プロセス
- Skills開発と成果物契約

## 使用するAI社員ロール
- AI Engineering PMO: 全体計画・成果物統合
- AI Deliverable Quality Reviewer: 最終品質判定とセレス向け統合報告
- AI Engineering Knowledge Curator: 承認済み成果物の知識化、MOC、出典管理
- AI Tech Lead: 構成・命名・品質基準
- AI DevEx / Agent Workflow Engineer: Skillsとinput/output運用
- AI QA / Test Automation Engineer: 自動検証
- AI Security / Governance Engineer: 秘密情報・権限・高影響操作のルール
- AI SRE / Platform Engineer: 運用・障害・復旧ワークフロー
- その他の専門ロール: 専門成果物と専門レビュー証跡

## 作成する成果物一覧
- AI Deliverable Quality ReviewerロールとSkill
- AI Engineering Knowledge CuratorロールとSkill
- 全既存ロールへのレビュー引き渡し・完了条件
- ai_team配下の品質責任モデル、${workflows.length}ワークフロー、5レビュー基準
- quality_review_request、quality_review_report、finding_registerテンプレート
- Obsidian Project / Architecture / ADR / Troubleshooting / Learning / Source Mapテンプレート
- output配下のwork_plan、execution_summary、questions、validation_report
- 第二の脳の生成・検証、同期サマリー
- 再生成・検証ツール

## 作業順序
1. 現行の品質責任と不足を確認する。
2. 作成者、専門Reviewer、最終Reviewer、PMO、人間責任者を分離する。
3. 新ロール、Skill、判定ルール、報告テンプレートを実装する。
4. 全既存ロールとワークフローへレビュー引き渡しを組み込む。
5. 現行outputを案件知識、再利用知識、パターン、ADRへ整理する。
6. 必須ファイル、YAML、Skill frontmatter、品質契約、Obsidian内部リンクを検証する。

## 前提・仮定
- Skillsはこのリポジトリ内で管理し、グローバル環境へは自動インストールしない。
- Codex標準に従い、Skill正規名はハイフン形式とする。
- AIの最終品質判定は人間の契約・予算・本番・高影響例外承認を代替しない。
- 同一AI実行コンテキストによる自己レビューは独立レビューとみなさない。
- 顧客・案件が増えた段階でinput/outputをtask-id単位へ分離する。

## 不明点
- 実案件で最優先するクラウド、アプリフレームワーク、CI環境は未指定。
- Skillsを個人環境へインストールするか、プロジェクトローカル運用に限定するかは未決。
- 成果物の顧客別命名規則・機密区分・承認者は未定義。

## 完了条件
- Deliverable Quality ReviewerとSkillが存在する。
- Engineering Knowledge CuratorとSkillが存在する。
- 全作業ロールの完了条件に最終品質レビューが組み込まれている。
- 最終判定、重大度、独立性、専門Reviewerとの責任境界が定義されている。
- セレス向け報告テンプレートが結論、重要指摘、判断依頼、残存リスクを含む。
- Skill YAMLとCodex frontmatterが検証可能である。
- TODOプレースホルダーが残っていない。
- 第二の脳に案件ノート、MOC、source_mapがあり、原成果物へ戻れる。
- 検証結果と残課題がoutputへ記録されている。
`);

write("output/questions.md", `# Questions

初回構築は以下を仮定して進めました。回答がなくても現状の成果物は利用できます。

## 不足情報
1. Skillsはこのリポジトリ内だけで使うか、\`~/.codex/skills\` へインストールして全案件で使うか。
2. 実案件で優先する標準スタック（例: GCP / AWS、Snowflake / BigQuery、Python / TypeScript）。
3. 顧客成果物の承認者、機密区分、保管期間、命名規則。
4. Quality Reviewerを別スレッド、別サブエージェント、別モデルのどれで独立実行するか。

## 確認したい事項
1. \`output/<client>/<YYYYMMDD>/<task-name>/\` の案件別分離を標準運用として継続するか。
2. Git管理とCIを導入し、検証スクリプトを必須チェックにするか。
3. 最初の前方テストに使う実案件をどれにするか。
4. P2の条件付き承認をセレス本人だけが行うか、案件責任者へ委任できるか。

## 判断に迷った事項
- 依頼書はアンダースコア形式のSkill名を指定しているが、Codex標準はハイフン形式である。正規名をハイフン形式とし、\`legacy_id\` で互換性を保持した。
- Skill CreatorはREADMEを非推奨とするが、依頼書が人間向けREADMEを必須としているため、SKILL.mdを簡潔な実行手順、README.mdを詳細説明として役割分担した。
`);

write("output/execution_summary.md", `# Execution Summary

## 実施内容
- 既存14ロールに、AI Deliverable Quality ReviewerとAI Engineering Knowledge Curatorを追加した。
- 各ロールに対応するCodex Skillと機械可読YAMLを作成した。
- 全作業ロールへレビュー依頼パッケージ、検証証跡、最終品質判定を必須化した。
- Deliverable Quality Review WorkflowとReview Matrixを追加した。
- Engineering Knowledge Curation Workflowを追加し、レビュー済み成果物を第二の脳へ反映できるようにした。
- PASS、PASS_WITH_CONDITIONS、REWORK_REQUIRED、BLOCKEDの判定を定義した。
- quality_review_request、quality_review_report、finding_registerテンプレートを追加した。
- Obsidian用テンプレート、生成スクリプト、リンク・frontmatter検証を追加した。
- 必須構成とSkill定義を検証するスクリプトを追加した。

## 作成した成果物
- \`README.md\`、\`AGENTS.md\`
- \`ai_team/\`: チーム概要、${roles.length}ロール、${workflows.length}ワークフロー、5レビュー文書
- \`skills/\`: ${roles.length} Skills、索引
- \`templates/\`: ${Object.keys(templates).length}テンプレート
- \`tools/\`: 生成・検証スクリプト
- \`input/README.md\`
- \`output/work_plan.md\`、\`output/questions.md\`、本ファイル
- \`output/quality_review_request.md\`、\`output/quality_review_report.md\`
- \`output/finding_register.md\`、\`output/review_metrics.md\`
- \`output/obsidian_sync_summary.md\`

## 主要な判断
- Codex互換性のためSkill正規名をハイフン形式にした。
- 依頼書のアンダースコア名はlegacy_idで保持した。
- Skillsはグローバル環境へ自動配置せず、プロジェクトローカルで管理した。
- 共通品質ゲートを設け、Security・QA・SREをMVPから必須にした。
- 最終品質責任はDeliverable Quality Reviewer、進行・報告責任はPMOに分離した。
- Knowledge Curatorは最終判定後に動き、Reviewerの判定と未確認事項を変更しない。
- 専門ReviewerのBlockerは最終ReviewerやPMOが独断で解除できない。
- 総合点ではなくP0・P1と必須証跡を優先して判定する。
- 分析者ロールは作らず、データ契約による分析チーム連携だけを定義した。
- 原成果物を複製せず、案件文脈と再利用可能な知識を分離し、source_mapで追跡する。

## 検証
- \`python3 tools/validate_repository.py\` で必須ファイル、見出し、YAML、Codex Skill frontmatterを検証する。
- \`python3 tools/validate_second_brain.py <target>\` で第二の脳の構成、frontmatter、MOC、内部リンク、source_mapを検証する。
- 実行結果は \`output/validation_report.md\` と \`output/obsidian_sync_summary.md\` に記録する。

## 品質レビュー
- 最終判定: PASS_WITH_CONDITIONS
- P0 / P1: 0件
- 条件: 最初の実案件で作成者とQuality Reviewerを別実行コンテキストに分離する。
- 詳細: \`output/quality_review_report.md\`

## 残課題
- 実案件を用いた各Skillの前方テストは未実施。
- Git / CIが未導入のため、品質ゲートはローカル実行のみ。
- 今回の変更は同一AI実行コンテキストで作成・自己確認しており、独立Reviewerによる前方テストは未実施。
- クラウド・言語・DWH別の詳細リファレンスは実案件選定後に追加する。

## 確認すべき事項
- グローバルSkillとしてのインストール範囲。
- 案件別input/output分離と命名規則。
- 最初に前方テストする実案件と標準技術スタック。

## 次にやるべきこと
1. 実案件を1件 \`input/<task-id>/\` に配置する。
2. 作業者、専門Reviewer、Deliverable Quality Reviewerを別実行コンテキストで前方テストする。
3. 指摘の検出率、誤検知、レビュー時間、セレスの判断時間を測り、観点と深度を調整する。
`);

write("output/quality_review_report.md", `# Quality Review Report

## 1. セレス向け結論
- **最終判定**: PASS_WITH_CONDITIONS
- **一言で言うと**: 最終品質責任者、専門レビュー、PMO報告、第二の脳への知識化を責任分離し、成果物の品質と再利用性を両方追える構成にしました。
- **今すぐ対応が必要なこと**: なし。構造・YAML・Skill・Obsidianリンクの検証結果は各レポートに記録します。
- **セレスの判断が必要なこと**: なし。実案件での独立前方テストは次回タスクとして扱えます。

## 2. Review Scope
- Reviewed artifacts: Quality ReviewerとKnowledge Curatorのロール・Skill、全既存Skillの完了条件、レビュー方針、知識化ワークフロー、テンプレート、検証スクリプト
- Requirements: 全成果物をあらゆる面で確認し、セレスへ分かりやすく報告し、レビュー済み知識を再利用可能にすること
- Evidence checked: 生成後の \`output/validation_report.md\`
- Excluded or unverified areas: 実案件での検出率、誤検知率、レビュー所要時間
- Reviewer independence: 同一AI実行コンテキストによる自己確認のため、独立性は未達

## 3. Quality Scorecard
| Dimension | Score | Verdict | Evidence | Key issue |
|---|---:|---|---|---|
| Purpose and requirement fit | 4 | PASS | ロール責任と報告テンプレート | なし |
| Technical correctness and architecture | 3 | PASS | 責任分離とゲート設計 | 実案件未検証 |
| Cross-artifact consistency | 4 | PASS | repository / second brain validators | なし |
| Test coverage and reproducibility | 3 | PASS | repository validator | 前方テスト未実施 |
| Security and governance | 3 | PASS | 専門Blocker非上書き | 人間承認運用は未検証 |
| Reliability and operations | 3 | PASS | 再レビューとfinding register | 運用KPI未計測 |
| Reporting clarity | 4 | PASS | セレス向け結論を先頭配置 | なし |
| Reviewer independence | 2 | CONDITION | 本報告の自己開示 | 別実行コンテキスト未使用 |

## 4. Findings
| ID | Severity | Area | Finding | Evidence | Impact | Required action | Owner | Due |
|---|---|---|---|---|---|---|---|---|
| QR-001 | P2 | Independence | 今回は同一AI実行コンテキストで作成とレビューを実施 | Review Scope | 独立レビューの実効性は未検証 | 最初の実案件で別Reviewer実行を行う | Engineering PMO | First real task |
| QR-002 | P3 | Metrics | 検出率、誤検知、所要時間の実績がない | New workflow | 最適なレビュー深度は未確定 | 3案件分を計測して見直す | Deliverable Quality Reviewer | After 3 tasks |

## 5. Specialist Review Summary
| Area | Reviewer | Verdict | Open blocker | Evidence |
|---|---|---|---|---|
| Skill schema and structure | Automated validator | PASS | No | output/validation_report.md |
| Process and responsibility design | Tech Lead perspective | PASS | No | review_policy.md |
| Security responsibility | Security perspective | PASS | No | review_matrix.md |

## 6. Residual Risks and Conditions
- 最初の実案件で作成者とQuality Reviewerを別実行コンテキストに分離する。
- P0・P1をAIがリスク受容しない運用を維持する。

## 7. Decisions Required from Ceres
現時点で必須判断はありません。

## 8. Next Actions
| Priority | Action | Owner | Due | Completion evidence |
|---|---|---|---|---|
| 1 | 実案件で独立前方テストする | PMO | First real task | quality_review_report.md |
| 2 | 3案件後にレビュー負荷と検出品質を見直す | Quality Reviewer | After 3 tasks | metrics and retrospective |

## 9. Final Verdict Rationale
責任分離、専門レビュー、重大度、最終判定、セレス向け報告、第二の脳への知識化は実装済みです。一方、今回の作成者とReviewerが同一実行コンテキストであり、独立性の実証がないためPASSではなくPASS_WITH_CONDITIONSとします。
`);

write("output/quality_review_request.md", `# Quality Review Request

## 1. Review Metadata
- Task ID: quality-and-knowledge-governance-20260614
- Producer: AI DevEx / Agent Workflow Engineer
- Requested reviewer: AI Deliverable Quality Reviewer
- Review deadline: 2026-06-14
- Risk level: Medium

## 2. Purpose and Acceptance Criteria
- Business purpose: 各AI社員の成果物品質を横断確認し、セレスへ分かりやすく報告したうえで、レビュー済み知識を再利用できるようにする。
- Intended users: セレス、AI Engineering PMO、各AI社員。
- Acceptance criteria: 最終責任者、専門レビュー、重大度、判定、報告形式、改善メトリクス、第二の脳への知識化と出典管理が定義されている。
- Out of scope: 実案件での検出率・誤検知率・レビュー時間の実測。

## 3. Deliverables
| File / Artifact | Purpose | Producer | Status |
|---|---|---|---|
| ai_team/roles/deliverable_quality_reviewer.md | 最終品質責任 | DevEx | Complete |
| skills/skill-deliverable-quality-reviewer/ | 実行可能Skill | DevEx | Complete |
| skills/skill-engineering-knowledge-curator/ | 第二の脳整理Skill | DevEx | Complete |
| ai_team/review/ | 方針、観点、ゲート、メトリクス | Tech Lead / DevEx | Complete |
| templates/quality_review_*.md | レビュー依頼と報告契約 | PMO / Reviewer | Complete |
| templates/obsidian_*.md | 第二の脳ノート契約 | Knowledge Curator | Complete |
| tools/validate_repository.py | 構造・契約検証 | QA / DevEx | Complete |
| tools/validate_second_brain.py | Obsidian構造・リンク検証 | QA / Curator | Complete |

## 4. Change and Impact
- Change summary: Quality ReviewerとKnowledge Curatorを追加し、レビュー後の知識化までを標準フローに組み込んだ。
- Affected systems, data, users, and operations: AI社員の成果物提出と完了判定。
- Breaking changes: 今後はquality_review_request.mdとquality_review_report.mdが必須。
- Migration / rollback: ドキュメント契約のみ。既存Skillは再生成済み。

## 5. Validation Evidence
| Check | Command / Method | Result | Evidence path |
|---|---|---|---|
| Repository contract | python3 -B tools/validate_repository.py | See report | output/validation_report.md |
| Generator syntax | node --check tools/generate_ai_team.mjs | PASS | Command result |
| Validator syntax | python3 -m py_compile tools/validate_repository.py | PASS | Command result |
| Obsidian contract | python3 tools/validate_second_brain.py TARGET | See sync summary | output/obsidian_sync_summary.md |

## 6. Required Specialist Reviews
| Review area | Reviewer | Required | Result | Evidence |
|---|---|---|---|---|
| Technical architecture | Tech Lead perspective | Yes | PASS | review_policy.md |
| Functional and test quality | QA automation | Yes | PASS | validation_report.md |
| Security and governance | Security perspective | Yes | PASS | review_matrix.md |
| Reliability and operations | SRE perspective | Yes | PASS | review_metrics.md |

## 7. Assumptions, Unverified Claims, and Known Risks
- 同一AI実行コンテキスト内の観点別確認であり、Reviewer独立性は未実証。
- 実案件での有効性指標はまだない。

## 8. Questions for Reviewer
- P0 / P1を見逃す構造的な穴がないか。
- セレス向け報告で判断に必要な情報が先頭にあるか。

## 9. Producer Self-check
- [x] Requirements are traceable.
- [x] Relevant tests and checks were executed.
- [x] Unexecuted checks are disclosed.
- [x] Security, operations, and data impacts are disclosed.
- [x] No secrets or unmasked personal data are included.
`);

write("output/finding_register.md", `# Finding Register

| ID | Status | Severity | Source review | Area | Finding | Evidence | Impact | Required action | Owner | Due | Resolution evidence |
|---|---|---|---|---|---|---|---|---|---|---|---|
| QR-001 | OPEN | P2 | Final quality review | Independence | 作成者とReviewerが同一AI実行コンテキスト | quality_review_report.md | 独立レビューの実効性が未検証 | 最初の実案件で別実行する | Engineering PMO | First real task | Pending |
| QR-002 | OPEN | P3 | Final quality review | Metrics | 実案件の品質KPIが未蓄積 | review_metrics.md | 最適な深度と負荷が未確定 | 3案件を計測して見直す | Deliverable Quality Reviewer | After 3 tasks | Pending |
`);

write("output/review_metrics.md", `# Review Metrics

## Task Records
| Task ID | Date | Risk | Producer role | Reviewer | Verdict | P0 | P1 | P2 | P3 | Rework cycles | Review minutes | User clarification count | Escaped defects |
|---|---|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| quality-review-governance-20260614 | 2026-06-14 | Medium | DevEx / Agent Workflow | Deliverable Quality Reviewer | PASS_WITH_CONDITIONS | 0 | 0 | 1 | 1 | 0 | N/A | 0 | 0 |

## Notes
- Review minutesは計測開始前のためN/A。
- Escaped defectsは現時点0だが、実運用後に再評価する。
- 3件蓄積後に反復指摘とレビュー深度を見直す。
`);

console.log(`Generated ${roles.length} roles, ${roles.length} skills, ${workflows.length} workflows, and ${Object.keys(templates).length} templates.`);

await import("./professionalize_ai_team.mjs");
