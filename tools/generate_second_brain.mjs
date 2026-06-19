import fs from "node:fs";
import path from "node:path";

const defaultTargetRoot =
  "/Users/celesiizuka/Codex/CASA/second_brain/second_brain/data_engineer";
const targetRoot = path.resolve(process.argv[2] ?? defaultTargetRoot);

const managedMarker = "managed_by: engineering_knowledge_curator";
const created = [];
const updated = [];
const conflicts = [];

const sourceRoot = "/Users/celesiizuka/Codex/CASA/data_engineer";
const tmInput = `${sourceRoot}/input/トヨテック/TM東京_履歴データ設計_目的と課題.md`;
const tmOutput = `${sourceRoot}/output/トヨテック/20260614/TM東京_履歴データ設計_目的と課題`;
const cdvInput = `${sourceRoot}/input/トヨテック/ClouderaのDataVizに関する初学者への共有.md`;
const cdvOutput = `${sourceRoot}/output/トヨテック/20260615/ClouderaのDataVizに関する初学者への共有`;
const teamOutput = `${sourceRoot}/output`;

const requiredDirectories = [
  "00_MOC",
  "01_Projects",
  "02_Knowledge/data_engineering",
  "02_Knowledge/backend",
  "02_Knowledge/frontend",
  "02_Knowledge/cloud",
  "02_Knowledge/sre",
  "02_Knowledge/security",
  "02_Knowledge/qa",
  "02_Knowledge/ai_llm",
  "02_Knowledge/integration",
  "03_Patterns/architecture_patterns",
  "03_Patterns/db_design_patterns",
  "03_Patterns/api_design_patterns",
  "03_Patterns/data_pipeline_patterns",
  "03_Patterns/testing_patterns",
  "03_Patterns/operation_patterns",
  "04_Decision_Logs",
  "05_Troubleshooting/snowflake",
  "05_Troubleshooting/python",
  "05_Troubleshooting/api",
  "05_Troubleshooting/terraform",
  "05_Troubleshooting/ci_cd",
  "05_Troubleshooting/data_quality",
  "90_Templates",
  "99_Inbox",
];

function yamlList(values) {
  if (!values.length) return "[]";
  return `\n${values.map((value) => `  - ${JSON.stringify(value)}`).join("\n")}`;
}

function noteDateFromSources(source) {
  for (const value of source) {
    const match = String(value).match(/\/(20\d{2})(\d{2})(\d{2})\//);
    if (match) return `${match[1]}-${match[2]}-${match[3]}`;
  }
  return "2026-06-14";
}

function frontmatter({
  title,
  type,
  project = "",
  domain = "engineering",
  status = "active",
  source = [],
  tags = [],
  related = [],
}) {
  const noteDate = noteDateFromSources(source);
  return `---
title: ${JSON.stringify(title)}
type: ${JSON.stringify(type)}
project: ${JSON.stringify(project)}
domain: ${JSON.stringify(domain)}
status: ${JSON.stringify(status)}
created: ${JSON.stringify(noteDate)}
updated: ${JSON.stringify(noteDate)}
source: ${yamlList(source)}
tags: ${yamlList(tags)}
related: ${yamlList(related)}
managed_by: engineering_knowledge_curator
---`;
}

function note(metadata, body) {
  return `${frontmatter(metadata)}\n\n${body.trim()}\n`;
}

function writeManaged(relativePath, content) {
  const target = path.join(targetRoot, relativePath);
  fs.mkdirSync(path.dirname(target), { recursive: true });
  if (fs.existsSync(target)) {
    const current = fs.readFileSync(target, "utf8");
    if (!current.includes(managedMarker)) {
      conflicts.push(relativePath);
      return;
    }
    if (current === content) return;
    updated.push(relativePath);
  } else {
    created.push(relativePath);
  }
  fs.writeFileSync(target, content, "utf8");
}

for (const directory of requiredDirectories) {
  fs.mkdirSync(path.join(targetRoot, directory), { recursive: true });
}

const notes = new Map();

notes.set(
  "README.md",
  note(
    {
      title: "Engineering Second Brain",
      type: "index",
      source: [`${teamOutput}/execution_summary.md`, `${tmOutput}/execution_summary.md`],
      tags: ["engineering", "second-brain", "obsidian"],
      related: ["00_MOC/engineering_moc", "00_MOC/project_index"],
    },
    `# Engineering Second Brain

エンジニアチームの成果物を、案件の経緯と再利用できる知識に分けて保管する場所です。原文の保管庫ではありません。設計判断、前提、未解決事項、適用条件を短く整理し、必ず元成果物へ戻れるようにしています。

## 入口
- [[00_MOC/engineering_moc|Engineering MOC]]
- [[00_MOC/project_index|Project Index]]
- [[04_Decision_Logs/adr_index|ADR Index]]
- [[05_Troubleshooting/error_index|Troubleshooting Index]]

## 運用
- 案件の全体像は \`01_Projects\` に置く。
- 他案件でも使える内容だけを \`02_Knowledge\` と \`03_Patterns\` へ抽出する。
- 採用理由や見直し条件が重要な判断は \`04_Decision_Logs\` に残す。
- 実際に起きた不具合と再現・解決手順は \`05_Troubleshooting\` に残す。
- 未確認事項を確定知識として扱わない。条件付き承認は条件付きのまま記録する。`,
  ),
);

notes.set(
  "00_MOC/engineering_moc.md",
  note(
    {
      title: "Engineering MOC",
      type: "moc",
      tags: ["moc", "engineering"],
      related: [
        "00_MOC/project_index",
        "00_MOC/data_engineering_moc",
        "00_MOC/qa_sre_security_moc",
      ],
    },
    `# Engineering MOC

## Projects
- [[00_MOC/project_index|Project Index]]

## Domains
- [[00_MOC/data_engineering_moc|Data Engineering]]
- [[00_MOC/backend_moc|Backend]]
- [[00_MOC/frontend_moc|Frontend]]
- [[00_MOC/cloud_infra_moc|Cloud / Infrastructure]]
- [[00_MOC/ai_llm_moc|AI / LLM / Agent]]
- [[00_MOC/qa_sre_security_moc|QA / SRE / Security]]

## Decisions and Operations
- [[04_Decision_Logs/adr_index|ADR Index]]
- [[05_Troubleshooting/error_index|Troubleshooting Index]]`,
  ),
);

notes.set(
  "00_MOC/project_index.md",
  note(
    {
      title: "Project Index",
      type: "moc",
      tags: ["moc", "project"],
      related: ["00_MOC/engineering_moc"],
    },
    `# Project Index

## Active / Conditional
- [[01_Projects/TM東京_履歴データ設計/overview|TM東京 履歴データ設計]]: 構想は妥当。利益定義、観測範囲、車両照合ルールを決めてからMVPへ進む。
- [[01_Projects/Cloudera_DataViz_初学者教育/overview|Cloudera Data Visualization 初学者教育]]: 用意済みデータマートを使う半日MVPを推奨。実環境と権限の確認が必要。
- [[01_Projects/AIエンジニアチーム構築/overview|AIエンジニアチーム構築]]: 16ロールの責任分離と品質レビュー、第二の脳への知識化を整備。

## Statusの見方
- active: 現在運用または継続改善中
- conditional: 条件付き承認。未確認事項や実運用検証が残る
- archived: 終了。再開条件がある場合は案件ノートへ記載`,
  ),
);

notes.set(
  "00_MOC/data_engineering_moc.md",
  note(
    {
      title: "Data Engineering MOC",
      type: "moc",
      domain: "data_engineering",
      tags: ["moc", "data-engineering"],
      related: ["00_MOC/engineering_moc"],
    },
    `# Data Engineering MOC

## Project
- [[01_Projects/TM東京_履歴データ設計/overview|TM東京 履歴データ設計]]
- [[01_Projects/Cloudera_DataViz_初学者教育/overview|Cloudera Data Visualization 初学者教育]]

## Knowledge
- [[02_Knowledge/data_engineering/履歴データ設計の使い分け|履歴データ設計の使い分け]]
- [[02_Knowledge/data_engineering/車両個体IDと識別子クロスウォーク|車両個体IDと識別子クロスウォーク]]
- [[02_Knowledge/data_engineering/車両ライフサイクル利益モデル|車両ライフサイクル利益モデル]]
- [[02_Knowledge/data_engineering/観測可能範囲とデータ欠損の区別|観測可能範囲とデータ欠損の区別]]
- [[02_Knowledge/data_engineering/BI初学者教育ではデータマート実装と利用を分ける|BI初学者教育ではデータマート実装と利用を分ける]]

## Patterns
- [[03_Patterns/data_pipeline_patterns/Raw_Staging_Core_Martの責任分離|Raw / Staging / Core / Mart]]
- [[03_Patterns/data_pipeline_patterns/履歴方式選択パターン|履歴方式選択]]
- [[03_Patterns/db_design_patterns/識別子クロスウォークパターン|識別子クロスウォーク]]
- [[03_Patterns/testing_patterns/Source_Core_Mart照合パターン|Source / Core / Mart照合]]
- [[03_Patterns/operation_patterns/初学者ハンズオン教材の4点セット|初学者ハンズオン教材の4点セット]]`,
  ),
);

const simpleMocs = [
  [
    "00_MOC/backend_moc.md",
    "Backend MOC",
    "backend",
    `# Backend MOC

現時点では、Backend固有の再利用ノートはありません。案件成果物からAPI契約、認可、トランザクション、冪等性の具体的な知見が得られた時点で追加します。

- [[00_MOC/engineering_moc|Engineering MOC]]`,
  ],
  [
    "00_MOC/frontend_moc.md",
    "Frontend MOC",
    "frontend",
    `# Frontend MOC

現時点では、Frontend固有の再利用ノートはありません。画面状態、権限表示、アクセシビリティの実装・検証結果が出た時点で追加します。

- [[00_MOC/engineering_moc|Engineering MOC]]`,
  ],
  [
    "00_MOC/cloud_infra_moc.md",
    "Cloud Infrastructure MOC",
    "cloud",
    `# Cloud / Infrastructure MOC

現時点ではクラウド製品を確定していません。AzurePowerBIDBという名称だけから製品構成を推測せず、実環境の構成確認後にクラウド設計ノートを追加します。

- [[00_MOC/engineering_moc|Engineering MOC]]
- [[01_Projects/TM東京_履歴データ設計/risks_and_issues|TM東京の未確認事項]]`,
  ],
  [
    "00_MOC/ai_llm_moc.md",
    "AI LLM MOC",
    "ai_llm",
    `# AI / LLM / Agent MOC

## AI社員チーム
- [[01_Projects/AIエンジニアチーム構築/overview|AIエンジニアチーム構築]]
- [[02_Knowledge/ai_llm/AI社員チームの品質責任分離|AI社員チームの品質責任分離]]
- [[03_Patterns/operation_patterns/品質レビューと再作業ループ|品質レビューと再作業ループ]]
- [[04_Decision_Logs/ADR-20260614-最終品質責任を独立Reviewerへ集約する|最終品質責任の集約]]`,
  ],
  [
    "00_MOC/qa_sre_security_moc.md",
    "QA SRE Security MOC",
    "qa_sre_security",
    `# QA / SRE / Security MOC

## QA
- [[02_Knowledge/qa/データ基盤の品質ゲート|データ基盤の品質ゲート]]
- [[03_Patterns/testing_patterns/Source_Core_Mart照合パターン|Source / Core / Mart照合]]

## SRE
- [[02_Knowledge/sre/データパイプラインの再実行と監視|データパイプラインの再実行と監視]]

## Security
- [[02_Knowledge/security/車両識別子と顧客データの保護|車両識別子と顧客データの保護]]

## Governance
- [[03_Patterns/operation_patterns/品質レビューと再作業ループ|品質レビューと再作業ループ]]`,
  ],
];

for (const [file, title, domain, body] of simpleMocs) {
  notes.set(
    file,
    note({
      title,
      type: "moc",
      domain,
      tags: ["moc", domain],
      related: ["00_MOC/engineering_moc"],
    }, body),
  );
}

const tmProject = "TM東京_履歴データ設計";
const tmProjectBase = `01_Projects/${tmProject}`;
const tmSources = [
  tmInput,
  `${tmOutput}/エンジニアチーム総評.md`,
  `${tmOutput}/quality_review_report.md`,
  `${tmOutput}/questions.md`,
  `${tmOutput}/execution_summary.md`,
];

notes.set(
  `${tmProjectBase}/overview.md`,
  note(
    {
      title: "TM東京 履歴データ設計",
      type: "project",
      project: tmProject,
      domain: "data_engineering",
      status: "conditional",
      source: tmSources,
      tags: ["project", "toyotec", "vehicle-lifecycle", "data-platform"],
      related: [
        `${tmProjectBase}/decisions`,
        `${tmProjectBase}/risks_and_issues`,
        "00_MOC/data_engineering_moc",
      ],
    },
    `# TM東京 履歴データ設計

## 目的
TM東京と連携可能なシステムで観測できる範囲を対象に、車両1台ごとの販売、整備、下取、中古車販売などのイベントと、そこから生じた利益を説明できるようにする。

## 現在地
構想と課題設定は妥当です。ただし、まだ物理設計へ進む段階ではありません。利益の定義、車両同一性の判定、観測可能範囲が未確定で、実DDL、サンプルデータ、Power BIモデルも未確認です。品質判定はPASS_WITH_CONDITIONSです。

## いま優先すること
201テーブルを一律に履歴化するのではなく、代表的な1業務経路を選び、車両IDと直接粗利v1が実データで成立するかを確認します。

## 案件ノート
- [[${tmProjectBase}/decisions|Decisions]]
- [[${tmProjectBase}/architecture_summary|Architecture Summary]]
- [[${tmProjectBase}/implementation_summary|Implementation Summary]]
- [[${tmProjectBase}/test_summary|Test Summary]]
- [[${tmProjectBase}/risks_and_issues|Risks and Issues]]
- [[${tmProjectBase}/next_actions|Next Actions]]
- [[${tmProjectBase}/source_map|Source Map]]

## 関連知識
- [[02_Knowledge/data_engineering/車両個体IDと識別子クロスウォーク|車両個体IDと識別子クロスウォーク]]
- [[02_Knowledge/data_engineering/車両ライフサイクル利益モデル|車両ライフサイクル利益モデル]]
- [[02_Knowledge/data_engineering/観測可能範囲とデータ欠損の区別|観測可能範囲とデータ欠損の区別]]`,
  ),
);

notes.set(
  `${tmProjectBase}/decisions.md`,
  note(
    {
      title: "TM東京 履歴データ設計 Decisions",
      type: "decision_summary",
      project: tmProject,
      domain: "data_engineering",
      status: "conditional",
      source: tmSources,
      tags: ["decision", "vehicle-lifecycle", "mvp"],
      related: [
        `${tmProjectBase}/overview`,
        "04_Decision_Logs/ADR-20260614-車両利益MVPを全テーブル履歴化より先行する",
        "04_Decision_Logs/ADR-20260614-車両IDに識別子クロスウォークを採用する",
      ],
    },
    `# Decisions

## 採用した方針
1. 全201テーブルの詳細設計より、車両利益MVPを先行する。
2. MVPの利益は、車両・サービスへ直接ひも付く売上から直接原価、値引き、返品を引く「直接粗利v1」に絞る。
3. 登録番号を不変キーにせず、基盤内の車両個体IDと識別子クロスウォークで追跡する。
4. Raw、Staging、Core、Martの責任を分け、Power BI向け集計はMartに閉じ込める。
5. 業務有効時刻とシステム記録時刻を必要に応じて分け、訂正や遅延到着を再現できるようにする。

## まだ決めていないこと
- 代表業務経路
- 利益v1の正式な構成要素と責任者
- 車両照合の自動確定条件
- AzurePowerBIDBの製品構成と連携方式
- 成功基準となる照合率や金額許容差

未決事項は結論へ繰り上げず、[[${tmProjectBase}/risks_and_issues|Risks and Issues]]で管理します。`,
  ),
);

notes.set(
  `${tmProjectBase}/architecture_summary.md`,
  note(
    {
      title: "TM東京 履歴データ設計 Architecture Summary",
      type: "architecture",
      project: tmProject,
      domain: "data_engineering",
      status: "proposed",
      source: [tmInput, `${tmOutput}/エンジニアチーム総評.md`],
      tags: ["architecture", "raw", "staging", "core", "mart"],
      related: [
        `${tmProjectBase}/overview`,
        "03_Patterns/data_pipeline_patterns/Raw_Staging_Core_Martの責任分離",
      ],
    },
    `# Architecture Summary

## 推奨構成
- Raw: 取得元、取得日時、バッチIDを持たせ、原則上書きせず再処理可能にする。
- Staging: 型、コード、日付、重複、削除・取消表現を標準化し、品質エラーを隔離する。
- Core: 車両、識別子、イベント、利益構成要素を共通定義する。
- Mart: Power BIの用途別集計と、未照合・不足・未取得期間などの品質状態を提供する。

## 中心エンティティ
- vehicle_master
- vehicle_identifier_crosswalk
- vehicle_lifecycle_event
- vehicle_ownership_or_sales_episode
- vehicle_profit_component

## 注意
これは論理方針です。実DDL、クラウド構成、分散方式、パーティション方式は、増分量、更新・削除比率、取込可能時間、製品仕様を確認してから決めます。`,
  ),
);

notes.set(
  `${tmProjectBase}/implementation_summary.md`,
  note(
    {
      title: "TM東京 履歴データ設計 Implementation Summary",
      type: "implementation",
      project: tmProject,
      domain: "data_engineering",
      status: "not_started",
      source: [`${tmOutput}/execution_summary.md`, `${tmOutput}/quality_review_report.md`],
      tags: ["implementation", "not-started", "mvp"],
      related: [`${tmProjectBase}/next_actions`, `${tmProjectBase}/test_summary`],
    },
    `# Implementation Summary

現時点ではコード、DDL、dbtモデル、パイプライン、Power BIモデルの実装は行っていません。今回の成果は、設計着手前の論点整理とMVP方針です。

## 実装前に必要な入力
- MVP対象テーブルのDDLとサンプルデータ
- 主キー、業務キー、更新・削除仕様
- 全量・差分の連携方式
- Power BIの参照テーブルと集計ロジック
- 利益の業務定義と照合元

## 最初の実装単位
代表業務経路1つを対象に、RawからMartまでを細く通します。全体共通フレームワークは、この実装で成立したパターンを確認してから広げます。`,
  ),
);

notes.set(
  `${tmProjectBase}/test_summary.md`,
  note(
    {
      title: "TM東京 履歴データ設計 Test Summary",
      type: "test_summary",
      project: tmProject,
      domain: "qa",
      status: "planned",
      source: [`${tmOutput}/エンジニアチーム総評.md`, `${tmOutput}/quality_review_report.md`],
      tags: ["test", "data-quality", "reconciliation"],
      related: [
        `${tmProjectBase}/implementation_summary`,
        "03_Patterns/testing_patterns/Source_Core_Mart照合パターン",
      ],
    },
    `# Test Summary

実データテストは未実施です。設計時点で必要と判断したテストは次のとおりです。

- 車両ID重複、有効期間重複、孤立イベント
- 未照合、複数候補、誤統合候補
- 取消、訂正、削除、遅延到着の再現
- 同一バッチ再実行時の重複防止
- Source、Core、Martの件数・金額照合
- Power BIでの二重集計防止
- 車両別利益から根拠明細へのドリルバック

照合率や許容差は未設定です。実データを見ずに数値だけ決めない方が安全です。`,
  ),
);

notes.set(
  `${tmProjectBase}/risks_and_issues.md`,
  note(
    {
      title: "TM東京 履歴データ設計 Risks and Issues",
      type: "risk_register",
      project: tmProject,
      domain: "data_engineering",
      status: "open",
      source: [`${tmOutput}/questions.md`, `${tmOutput}/quality_review_report.md`],
      tags: ["risk", "open-question", "conditional"],
      related: [`${tmProjectBase}/next_actions`, `${tmProjectBase}/decisions`],
    },
    `# Risks and Issues

## 設計を止めるほど重要な未確定事項
- 利益に含める売上・費用、税区分、集計日付、責任者
- TM東京が観測できるライフサイクル範囲
- 車両IDの自動統合、手動確認、誤統合の分割ルール

## 実データ未確認
- DDL、サンプル、件数増分、更新・削除率
- 車台番号、登録番号、ソースキーの欠損・重複・変化
- Power BI参照テーブルと既存集計
- AzurePowerBIDBの実製品、接続、保持、SLA

## 運用・Security
- 未照合データの確認責任者が未定
- 車台番号、登録番号、顧客関係の公開範囲が未定
- バックフィル、誤統合修正、再実行のRunbookが未作成

品質判定はPASS_WITH_CONDITIONSです。これらを確定前の設計案として扱います。`,
  ),
);

notes.set(
  `${tmProjectBase}/next_actions.md`,
  note(
    {
      title: "TM東京 履歴データ設計 Next Actions",
      type: "action_plan",
      project: tmProject,
      domain: "data_engineering",
      status: "open",
      source: [`${tmOutput}/execution_summary.md`, `${tmOutput}/questions.md`],
      tags: ["next-action", "mvp", "data-profiling"],
      related: [`${tmProjectBase}/risks_and_issues`, `${tmProjectBase}/implementation_summary`],
    },
    `# Next Actions

1. 利益v1の定義と業務責任者を決める。
2. 観測可能なライフサイクル範囲を決める。
3. 201テーブルをMVP必須、将来、参照、ログ、一時、利用不明へ分類する。
4. 代表業務経路、店舗、期間、車種を選ぶ。
5. 対象テーブルのキー、粒度、更新、削除、時刻、金額をプロファイリングする。
6. 車両マスタと識別子クロスウォークの照合・分割ルールを設計する。
7. RawからMartまで最小構成を実装する。
8. 照合率、金額一致、訂正再現、再実行性、Power BI二重集計を検証する。

DDL作成を先行させず、1から5を先に済ませます。`,
  ),
);

notes.set(
  `${tmProjectBase}/source_map.md`,
  note(
    {
      title: "TM東京 履歴データ設計 Source Map",
      type: "source_map",
      project: tmProject,
      domain: "data_engineering",
      status: "active",
      source: tmSources,
      tags: ["source-map", "traceability"],
      related: [`${tmProjectBase}/overview`],
    },
    `# Source Map

| Source | Curated Notes | Extracted Content | Review Status | Notes |
|---|---|---|---|---|
| ${tmInput} | [[${tmProjectBase}/overview]], [[${tmProjectBase}/architecture_summary]] | 目的、201テーブル、車両利益、初期課題 | Input | 原資料 |
| ${tmOutput}/エンジニアチーム総評.md | [[${tmProjectBase}/decisions]], [[${tmProjectBase}/test_summary]], Knowledge / Pattern / ADR | 総評、設計課題、推奨構成、MVP | Reviewed | 主な抽出元 |
| ${tmOutput}/quality_review_report.md | [[${tmProjectBase}/overview]], [[${tmProjectBase}/risks_and_issues]] | PASS_WITH_CONDITIONS、未確認、判断事項 | Conditional | 判定状態を保持 |
| ${tmOutput}/questions.md | [[${tmProjectBase}/risks_and_issues]], [[${tmProjectBase}/next_actions]] | 優先確認事項 | Open | 未回答 |
| ${tmOutput}/execution_summary.md | [[${tmProjectBase}/implementation_summary]], [[${tmProjectBase}/next_actions]] | 実施範囲、未実装、次工程 | Complete | 2026-06-14時点 |

## 未反映
- 実DDL、サンプルデータ、Power BIモデルは提供されていないため、実装知識としては未反映です。

## 競合
- なし。

## 確認事項
- 利益定義、観測範囲、代表業務経路が確定したら、案件ノートとADRを更新します。`,
  ),
);

const teamProject = "AIエンジニアチーム構築";
const teamProjectBase = `01_Projects/${teamProject}`;
const teamSources = [
  `${teamOutput}/execution_summary.md`,
  `${teamOutput}/quality_review_report.md`,
  `${teamOutput}/finding_register.md`,
  `${sourceRoot}/ai_team/team_overview.md`,
  `${sourceRoot}/ai_team/review/review_policy.md`,
];

notes.set(
  `${teamProjectBase}/overview.md`,
  note(
    {
      title: "AIエンジニアチーム構築",
      type: "project",
      project: teamProject,
      domain: "ai_llm",
      status: "conditional",
      source: teamSources,
      tags: ["project", "ai-agent", "engineering-team", "quality"],
      related: [
        `${teamProjectBase}/decisions`,
        `${teamProjectBase}/risks_and_issues`,
        "00_MOC/ai_llm_moc",
      ],
    },
    `# AIエンジニアチーム構築

## 目的
入力課題を専門ロールが実務成果物へ変換し、専門レビュー、最終品質判定、セレス向け報告まで一貫して行うAI社員チームを作る。

## 現在地
PMO、実装系、Data、Cloud、SRE、Security、QA、LLM、DevEx、Integration、最終Quality Reviewerに、Engineering Knowledge Curatorを加えた16ロール構成です。リポジトリ検証は自動化されていますが、別実行コンテキストでの独立レビューと、複数案件での品質KPI蓄積は今後の課題です。

## 案件ノート
- [[${teamProjectBase}/decisions|Decisions]]
- [[${teamProjectBase}/architecture_summary|Architecture Summary]]
- [[${teamProjectBase}/implementation_summary|Implementation Summary]]
- [[${teamProjectBase}/test_summary|Test Summary]]
- [[${teamProjectBase}/risks_and_issues|Risks and Issues]]
- [[${teamProjectBase}/next_actions|Next Actions]]
- [[${teamProjectBase}/source_map|Source Map]]`,
  ),
);

notes.set(
  `${teamProjectBase}/decisions.md`,
  note(
    {
      title: "AIエンジニアチーム構築 Decisions",
      type: "decision_summary",
      project: teamProject,
      domain: "ai_llm",
      status: "active",
      source: teamSources,
      tags: ["decision", "quality-review", "knowledge-curation"],
      related: [
        "04_Decision_Logs/ADR-20260614-最終品質責任を独立Reviewerへ集約する",
        "03_Patterns/operation_patterns/品質レビューと再作業ループ",
      ],
    },
    `# Decisions

## 責任分離
- Producerは成果物と検証証跡を提出する。
- Specialist Reviewerは技術、QA、Security、SRE、Dataなどの担当観点を判定する。
- Deliverable Quality Reviewerは証跡を横断し、最終判定を出す。
- PMOは再作業を調整し、判定を改変せずセレスへ報告する。
- Knowledge CuratorはPASSまたはPASS_WITH_CONDITIONSの成果物を、判定状態と出典を保って第二の脳へ整理する。
- 高影響な例外承認、本番判断、契約、予算は人間が持つ。

## 判定
PASS、PASS_WITH_CONDITIONS、REWORK_REQUIRED、BLOCKEDの4段階とし、平均点よりP0、P1、必須証跡を優先します。

## Skill命名
Codex標準のハイフン形式を正規名とし、依頼書由来のアンダースコア形式はlegacy_idで保持します。`,
  ),
);

notes.set(
  `${teamProjectBase}/architecture_summary.md`,
  note(
    {
      title: "AIエンジニアチーム構築 Architecture Summary",
      type: "architecture",
      project: teamProject,
      domain: "ai_llm",
      status: "active",
      source: [`${sourceRoot}/ai_team/team_overview.md`, `${sourceRoot}/README.md`],
      tags: ["architecture", "agent-workflow", "skills"],
      related: [`${teamProjectBase}/overview`, `${teamProjectBase}/decisions`],
    },
    `# Architecture Summary

## 構成
- input: 課題、要件、コード、ログ、仕様
- output: 計画、成果物、質問、検証、品質レビュー、同期サマリー
- ai_team: ロール、ワークフロー、レビュー基準
- skills: Codex Skillと機械可読定義
- templates: 成果物とObsidianノートのテンプレート
- tools: 一括生成、リポジトリ検証、第二の脳生成・検証

## 標準フロー
PMOによる分類 → 専門ロールによる作成 → Specialist Review → Final Quality Verdict → PMO報告 → Knowledge Curatorによる知識化、の順です。

Knowledge CuratorはQuality Reviewerの代わりではありません。品質判定後に情報を整理する役割です。`,
  ),
);

notes.set(
  `${teamProjectBase}/implementation_summary.md`,
  note(
    {
      title: "AIエンジニアチーム構築 Implementation Summary",
      type: "implementation",
      project: teamProject,
      domain: "ai_llm",
      status: "active",
      source: [`${teamOutput}/execution_summary.md`, `${sourceRoot}/tools/generate_ai_team.mjs`],
      tags: ["implementation", "skill", "validator"],
      related: [`${teamProjectBase}/test_summary`, `${teamProjectBase}/source_map`],
    },
    `# Implementation Summary

ロール定義、Skill、YAML、ワークフロー、品質基準、テンプレートを、tools/generate_ai_team.mjsから一括生成する構成です。個別ファイルだけを直して定義がずれないよう、生成スクリプトを正本にしています。

Knowledge Curator向けには次を追加しました。
- AI Engineering Knowledge Curatorロール
- skill-engineering-knowledge-curator
- Engineering Knowledge Curation Workflow
- Obsidian用6テンプレート
- 第二の脳生成スクリプト
- frontmatter、MOC、内部リンク、source mapの検証スクリプト`,
  ),
);

notes.set(
  `${teamProjectBase}/test_summary.md`,
  note(
    {
      title: "AIエンジニアチーム構築 Test Summary",
      type: "test_summary",
      project: teamProject,
      domain: "qa",
      status: "active",
      source: [`${teamOutput}/validation_report.md`, `${sourceRoot}/tools/validate_repository.py`],
      tags: ["test", "validation", "skill"],
      related: [`${teamProjectBase}/risks_and_issues`],
    },
    `# Test Summary

## 自動検証
- 必須ファイルと見出し
- role / skill / workflow / templateの件数
- skill.yamlとagents/openai.yaml
- Codex公式Skill validator
- Reviewerの判定契約
- 第二の脳の必須構成、frontmatter、MOC、内部リンク、source map

## まだ未検証
- 別AI実行コンテキストでの独立レビュー
- 3件以上の実案件での検出率、再作業率、レビュー時間
- 既存の大規模Obsidian Vaultへ統合した場合の重複・競合運用`,
  ),
);

notes.set(
  `${teamProjectBase}/risks_and_issues.md`,
  note(
    {
      title: "AIエンジニアチーム構築 Risks and Issues",
      type: "risk_register",
      project: teamProject,
      domain: "ai_llm",
      status: "open",
      source: [`${teamOutput}/quality_review_report.md`, `${teamOutput}/finding_register.md`],
      tags: ["risk", "review-independence", "metrics"],
      related: [`${teamProjectBase}/next_actions`],
    },
    `# Risks and Issues

- 作成者とReviewerを同じAI実行コンテキストで動かすと、独立性が弱い。
- 実案件の検出率、誤検知、レビュー時間がまだ蓄積されていない。
- Skillを増やしすぎると、ロール選択と引き継ぎコストが上がる。
- 第二の脳に原文を複製すると、更新差分と正本が分からなくなる。
- 既存ノートを自動上書きすると、人間が加えた知見を失う可能性がある。

対策として、品質ReviewerとCuratorを分け、Curatorは管理対象ノートだけを更新し、非管理ノートとの競合は同期サマリーへ出します。`,
  ),
);

notes.set(
  `${teamProjectBase}/next_actions.md`,
  note(
    {
      title: "AIエンジニアチーム構築 Next Actions",
      type: "action_plan",
      project: teamProject,
      domain: "ai_llm",
      status: "open",
      source: [`${teamOutput}/execution_summary.md`, `${teamOutput}/quality_review_report.md`],
      tags: ["next-action", "forward-test", "metrics"],
      related: [`${teamProjectBase}/risks_and_issues`],
    },
    `# Next Actions

1. 次の実案件でProducerとQuality Reviewerを別実行コンテキストに分ける。
2. 3案件分のP1/P2反復テーマ、再作業回数、レビュー時間を記録する。
3. Knowledge Curatorの同期差分と競合件数を記録し、更新ルールを調整する。
4. 同じ指摘が続く場合は、個別対応ではなくProducer Skillかテンプレートを修正する。
5. クラウド、DWH、言語別の詳細Skillは、実需要が2件以上出てから分割を検討する。`,
  ),
);

notes.set(
  `${teamProjectBase}/source_map.md`,
  note(
    {
      title: "AIエンジニアチーム構築 Source Map",
      type: "source_map",
      project: teamProject,
      domain: "ai_llm",
      status: "active",
      source: teamSources,
      tags: ["source-map", "traceability"],
      related: [`${teamProjectBase}/overview`],
    },
    `# Source Map

| Source | Curated Notes | Extracted Content | Review Status | Notes |
|---|---|---|---|---|
| ${teamOutput}/execution_summary.md | [[${teamProjectBase}/overview]], [[${teamProjectBase}/implementation_summary]] | 構築内容、主要判断、残課題 | Conditional | 初期15ロール時点の記録 |
| ${teamOutput}/quality_review_report.md | [[${teamProjectBase}/risks_and_issues]], [[${teamProjectBase}/test_summary]] | 最終判定、独立性、未検証 | PASS_WITH_CONDITIONS | 判定状態を保持 |
| ${teamOutput}/finding_register.md | [[${teamProjectBase}/risks_and_issues]], [[${teamProjectBase}/next_actions]] | QR-001、QR-002 | Open | 継続追跡 |
| ${sourceRoot}/ai_team/team_overview.md | [[${teamProjectBase}/decisions]], [[${teamProjectBase}/architecture_summary]] | 責任分離、ロール選定 | Active | Knowledge Curator追加後 |
| ${sourceRoot}/ai_team/review/review_policy.md | [[02_Knowledge/ai_llm/AI社員チームの品質責任分離]], [[03_Patterns/operation_patterns/品質レビューと再作業ループ]] | 品質判定、再作業、報告 | Active | 共通ルール |

## 未反映
- 実案件3件分の品質メトリクスは未蓄積です。

## 競合
- なし。

## 確認事項
- グローバルSkillとしての配布範囲は未決です。`,
  ),
);

const cdvProject = "Cloudera_DataViz_初学者教育";
const cdvProjectBase = `01_Projects/${cdvProject}`;
const cdvSources = [
  cdvInput,
  `${cdvOutput}/エンジニアチーム総評.md`,
  `${cdvOutput}/quality_review_report.md`,
  `${cdvOutput}/questions.md`,
  `${cdvOutput}/execution_summary.md`,
];

notes.set(
  `${cdvProjectBase}/overview.md`,
  note(
    {
      title: "Cloudera Data Visualization 初学者教育",
      type: "project",
      project: cdvProject,
      domain: "data_engineering",
      status: "conditional",
      source: cdvSources,
      tags: ["project", "cloudera", "data-visualization", "training"],
      related: [
        `${cdvProjectBase}/decisions`,
        `${cdvProjectBase}/risks_and_issues`,
        "00_MOC/data_engineering_moc",
      ],
    },
    `# Cloudera Data Visualization 初学者教育

## 目的
BI初学者が、用意済みの小規模データマートを理解し、Cloudera Data Visualizationで基本Dashboardを作成し、事実・仮説・未確認事項を分けて説明できる状態を作る。

## 現在地
教育企画の方向性は妥当です。ただし、データマート実装からBI操作・解釈までを初回で扱うのは広すぎます。初回は半日ハンズオンへ絞り、SQL実装、複数Fact、権限、性能、運用は発展編へ分けます。

品質判定はPASS_WITH_CONDITIONSです。利用環境、製品リリース、権限、受講者、開催時間、実機所要時間が未確認です。

## 案件ノート
- [[${cdvProjectBase}/decisions|Decisions]]
- [[${cdvProjectBase}/architecture_summary|Education Architecture]]
- [[${cdvProjectBase}/implementation_summary|Material Summary]]
- [[${cdvProjectBase}/test_summary|Pilot and Acceptance]]
- [[${cdvProjectBase}/risks_and_issues|Risks and Issues]]
- [[${cdvProjectBase}/next_actions|Next Actions]]
- [[${cdvProjectBase}/source_map|Source Map]]`,
  ),
);

notes.set(
  `${cdvProjectBase}/decisions.md`,
  note(
    {
      title: "Cloudera Data Visualization 初学者教育 Decisions",
      type: "decision_summary",
      project: cdvProject,
      domain: "data_engineering",
      status: "proposed",
      source: cdvSources,
      tags: ["decision", "training", "mvp"],
      related: [
        `${cdvProjectBase}/overview`,
        "04_Decision_Logs/ADR-20260615-初回BI教育では用意済みデータマートを使う",
      ],
    },
    `# Decisions

## 採用する方針
1. 初回教育は、用意済みデータマートの理解、Visual作成、Dashboard作成、解釈までに絞る。
2. データマートのSQL実装、複数Fact、権限、性能、運用は発展編へ分ける。
3. 教材はスライド、ハンズオン、短いリファレンス、講師Runbookを組み合わせる。
4. 接続、Dataset、権限は講師側で事前準備する。
5. 架空の売上データを使い、顧客実データや個人情報を使わない。
6. 本番開催前に講師試行と3名程度のパイロットを行う。

## 未決事項
- 実環境の提供形態と製品リリース
- 受講者数、SQL経験、期待業務
- 半日1回か90分3回か
- Visual、Dashboard、Datasetの作成・保存権限`,
  ),
);

notes.set(
  `${cdvProjectBase}/architecture_summary.md`,
  note(
    {
      title: "Cloudera Data Visualization 初学者教育 Architecture Summary",
      type: "architecture",
      project: cdvProject,
      domain: "data_engineering",
      status: "proposed",
      source: [cdvInput, `${cdvOutput}/エンジニアチーム総評.md`],
      tags: ["curriculum", "dataset", "visual", "dashboard"],
      related: [
        `${cdvProjectBase}/decisions`,
        "02_Knowledge/data_engineering/BI初学者教育ではデータマート実装と利用を分ける",
      ],
    },
    `# Education Architecture

## 学習フロー
業務上の問い → 粒度と指標 → Dataset → Visual → Dashboard / Filter → 事実・仮説・未確認事項の説明。

## 半日MVP
- BIと可視化の基本: 25分
- サンプルデータマート確認: 30分
- Cloudera主要概念: 20分
- Visual作成: 50分
- Dashboard作成: 30分
- 読み解き・発表: 40分

## 共通題材
1営業日 × 1店舗 × 1商品カテゴリを粒度とする架空の日次売上Martを使い、KPI、売上推移、店舗比較、商品カテゴリ比較、期間・地域Filterを作る。

BI共通知識とCloudera固有操作を分けて管理し、製品更新時は操作手順だけを差し替えられるようにする。`,
  ),
);

notes.set(
  `${cdvProjectBase}/implementation_summary.md`,
  note(
    {
      title: "Cloudera Data Visualization 初学者教育 Material Summary",
      type: "implementation",
      project: cdvProject,
      domain: "data_engineering",
      status: "not_started",
      source: [`${cdvOutput}/エンジニアチーム総評.md`, `${cdvOutput}/execution_summary.md`],
      tags: ["material", "hands-on", "runbook"],
      related: [`${cdvProjectBase}/next_actions`, `${cdvProjectBase}/test_summary`],
    },
    `# Material Summary

現時点では教育方針と教材構成までで、スライド、サンプルデータ、Dataset、画面キャプチャ、ハンズオン手順は未作成です。

## 作成する教材
- 20から30枚の説明スライド
- 10から15ページの受講者向けハンズオン
- 3から5ページのクイックリファレンス
- 5ページ前後の講師Runbook
- サンプルデータ定義と期待集計値
- 1問から3問の確認課題

画面操作をスライドへ重複記載せず、変更が多い操作手順はハンズオン資料へ集約する。`,
  ),
);

notes.set(
  `${cdvProjectBase}/test_summary.md`,
  note(
    {
      title: "Cloudera Data Visualization 初学者教育 Pilot and Acceptance",
      type: "test_summary",
      project: cdvProject,
      domain: "qa",
      status: "planned",
      source: [`${cdvOutput}/エンジニアチーム総評.md`, `${cdvOutput}/quality_review_report.md`],
      tags: ["pilot", "acceptance", "training"],
      related: [`${cdvProjectBase}/implementation_summary`],
    },
    `# Pilot and Acceptance

## 受講者の完了条件
- Datasetを選び、DimensionとMeasureを区別できる。
- KPI、棒、折れ線を含む基本Visualを作成できる。
- Filterを設定し、VisualをDashboardへ配置できる。
- データの1行の粒度を説明できる。
- 事実2つ、仮説1つ、未確認事項1つを説明できる。
- 対象期間、集計単位、指標定義を説明できる。

## 実施前テスト
- 講師が全手順を実環境で通す。
- 期待集計値とVisualの数字を照合する。
- アカウント、Workspace、Dataset、保存、共有、同時接続を確認する。
- 3名程度でパイロットし、時間とつまずきを記録する。`,
  ),
);

notes.set(
  `${cdvProjectBase}/risks_and_issues.md`,
  note(
    {
      title: "Cloudera Data Visualization 初学者教育 Risks and Issues",
      type: "risk_register",
      project: cdvProject,
      domain: "data_engineering",
      status: "open",
      source: [`${cdvOutput}/questions.md`, `${cdvOutput}/quality_review_report.md`],
      tags: ["risk", "training", "environment"],
      related: [`${cdvProjectBase}/next_actions`],
    },
    `# Risks and Issues

- データマート実装とBI利用を同じ初回教育へ入れると時間不足になる。
- 実環境のリリース、提供形態、権限が不明で、画面教材が合わない可能性がある。
- 受講者のSQL経験と期待業務が不明で、難易度を固定できない。
- ハンズオンを実機で通しておらず、所要時間と同時接続負荷が不明。
- 操作完了だけを理解完了と判断する恐れがある。
- 顧客実データを使うと、権限と個人情報の問題が教育を複雑にする。

これらが解消するまで、本成果物は完成教材ではなく教育企画として扱う。`,
  ),
);

notes.set(
  `${cdvProjectBase}/next_actions.md`,
  note(
    {
      title: "Cloudera Data Visualization 初学者教育 Next Actions",
      type: "action_plan",
      project: cdvProject,
      domain: "data_engineering",
      status: "open",
      source: [`${cdvOutput}/questions.md`, `${cdvOutput}/execution_summary.md`],
      tags: ["next-action", "pilot", "material"],
      related: [`${cdvProjectBase}/risks_and_issues`],
    },
    `# Next Actions

1. 利用環境、製品リリース、受講者、時間、権限を確定する。
2. 架空売上データと期待集計値を作る。
3. 講師用のConnection、Dataset、Workspaceを準備する。
4. 講師がハンズオンを実機で通し、時間と失敗箇所を記録する。
5. スライド、受講者手順、クイックリファレンス、Runbookを作る。
6. 3名程度でパイロットし、削る内容と追加する内容を決める。
7. 本番開催後、発展編の必要性を判断する。`,
  ),
);

notes.set(
  `${cdvProjectBase}/source_map.md`,
  note(
    {
      title: "Cloudera Data Visualization 初学者教育 Source Map",
      type: "source_map",
      project: cdvProject,
      domain: "data_engineering",
      status: "active",
      source: cdvSources,
      tags: ["source-map", "traceability"],
      related: [`${cdvProjectBase}/overview`],
    },
    `# Source Map

| Source | Curated Notes | Extracted Content | Review Status | Notes |
|---|---|---|---|---|
| ${cdvInput} | [[${cdvProjectBase}/overview]], [[${cdvProjectBase}/architecture_summary]] | 教育目的、対象範囲、期待成果物 | Input | 企画依頼 |
| ${cdvOutput}/エンジニアチーム総評.md | 全案件ノート、Knowledge、Pattern、ADR | 評価、MVP、教材、ハンズオン、ロール見解 | Reviewed | 主な抽出元 |
| ${cdvOutput}/quality_review_report.md | [[${cdvProjectBase}/overview]], [[${cdvProjectBase}/risks_and_issues]] | PASS_WITH_CONDITIONS、指摘 | Conditional | 判定状態を保持 |
| ${cdvOutput}/questions.md | [[${cdvProjectBase}/risks_and_issues]], [[${cdvProjectBase}/next_actions]] | 環境、受講者、権限、開催条件 | Open | 未回答 |
| ${cdvOutput}/execution_summary.md | [[${cdvProjectBase}/implementation_summary]], [[${cdvProjectBase}/next_actions]] | 実施範囲、未作成物、次工程 | Complete | 2026-06-15時点 |

## 未反映
- 実環境の画面、サンプルデータ、Dataset、完成教材は未作成です。

## 競合
- なし。

## 確認事項
- 実環境と受講者条件が確定したら、教材構成と完了条件を更新します。`,
  ),
);

const knowledgeNotes = [
  [
    "02_Knowledge/data_engineering/履歴データ設計の使い分け.md",
    {
      title: "履歴データ設計の使い分け",
      type: "knowledge",
      domain: "data_engineering",
      source: [tmInput, `${tmOutput}/エンジニアチーム総評.md`],
      tags: ["history", "scd2", "event", "bitemporal"],
      related: [
        "03_Patterns/data_pipeline_patterns/履歴方式選択パターン",
        `${tmProjectBase}/architecture_summary`,
      ],
    },
    `# 履歴データ設計の使い分け

履歴方式は全テーブルで統一しません。データが何を表すかで分けます。

| 対象 | 基本方式 | 注意 |
|---|---|---|
| ログ | 追記型 | 重複、保持、機密情報 |
| 売上・明細 | Fact + 取消・訂正 | 上書きで過去を消さない |
| 状態変化する受注 | 最新 + 状態履歴 | 戻り遷移、遅延 |
| マスタ | SCD Type2または最新 + 履歴 | 期間重複、UNKNOWN |
| 対応表 | 有効期間付きBridge | 多対多、統合、分割 |
| 一時テーブル | 原則対象外 | 利用実態があれば再評価 |

過去訂正や遅延到着が重要な場合は、業務有効時刻とシステム記録時刻を分けます。SCD Type2だけで全部を表現しようとすると、取引訂正や取消が不自然になります。`,
  ],
  [
    "02_Knowledge/data_engineering/車両個体IDと識別子クロスウォーク.md",
    {
      title: "車両個体IDと識別子クロスウォーク",
      type: "knowledge",
      domain: "data_engineering",
      source: [`${tmOutput}/エンジニアチーム総評.md`],
      tags: ["identity-resolution", "crosswalk", "vehicle"],
      related: [
        "03_Patterns/db_design_patterns/識別子クロスウォークパターン",
        "04_Decision_Logs/ADR-20260614-車両IDに識別子クロスウォークを採用する",
      ],
    },
    `# 車両個体IDと識別子クロスウォーク

独自IDを追加するだけでは、同じ車両を正しく統合できません。必要なのは、不変の基盤内IDと、各システムの識別子を有効期間付きで対応させるクロスウォークです。

## 保持する情報
- source_system、source_vehicle_key
- identifier_type、identifier_value
- valid_from、valid_to
- match_method、match_confidence、review_status
- merge / splitの修正参照

登録番号は変わるため補助キーです。車台番号も品質検証なしに自動確定へ使いません。一致しないデータを無理に統合せず、未照合として残すことが重要です。`,
  ],
  [
    "02_Knowledge/data_engineering/車両ライフサイクル利益モデル.md",
    {
      title: "車両ライフサイクル利益モデル",
      type: "knowledge",
      domain: "data_engineering",
      status: "proposed",
      source: [`${tmOutput}/エンジニアチーム総評.md`],
      tags: ["profit", "vehicle-lifecycle", "fact-model"],
      related: [`${tmProjectBase}/decisions`, `${tmProjectBase}/risks_and_issues`],
    },
    `# 車両ライフサイクル利益モデル

MVPでは、車両やサービスへ直接ひも付く売上から、直接原価、値引き、返品を引く「直接粗利v1」から始めます。共通費や人件費配賦は、配賦ルールが合意できるまで別レイヤにします。

利益は集計値だけで持たず、vehicle_profit_componentとして根拠明細を保持します。金額種別、税区分、直接・配賦区分、会計日付、業務日付、ソース取引へ戻れることが必要です。

この定義は提案段階です。売上・費用の範囲、税込・税抜、集計日付、責任者が決まるまで確定知識として扱いません。`,
  ],
  [
    "02_Knowledge/data_engineering/観測可能範囲とデータ欠損の区別.md",
    {
      title: "観測可能範囲とデータ欠損の区別",
      type: "knowledge",
      domain: "data_engineering",
      source: [`${tmOutput}/エンジニアチーム総評.md`],
      tags: ["data-coverage", "missing-data", "semantics"],
      related: [`${tmProjectBase}/risks_and_issues`],
    },
    `# 観測可能範囲とデータ欠損の区別

「車の一生」のような長期概念を扱うとき、組織が観測できない期間をゼロや取引なしとして扱ってはいけません。

最低限、次を分けます。
- 取引が存在しない
- システムに記録されていない
- 外部で取引された
- 連携遅延またはデータ欠損

Martでもcoverage statusを見せ、利用者が数字の完全性を判断できるようにします。`,
  ],
  [
    "02_Knowledge/qa/データ基盤の品質ゲート.md",
    {
      title: "データ基盤の品質ゲート",
      type: "knowledge",
      domain: "qa",
      source: [`${tmOutput}/エンジニアチーム総評.md`],
      tags: ["quality-gate", "data-quality", "mvp"],
      related: [`${tmProjectBase}/test_summary`],
    },
    `# データ基盤の品質ゲート

設計や実装を先へ進める前に、Requirement Ready、Data Ready、Design Ready、Operableを分けて確認します。

- Requirement Ready: 目的、利益定義、観測範囲、MVP対象
- Data Ready: 粒度、キー、更新、削除、時刻、識別子品質、金額照合
- Design Ready: 車両マスタ、クロスウォーク、イベント、利益粒度、レイヤ責任
- Operable: 品質ルール、監視、再処理、未照合処理、公開権限

資料が読みやすいことと、実データで設計可能なことは別です。ゲートごとの証跡を残します。`,
  ],
  [
    "02_Knowledge/security/車両識別子と顧客データの保護.md",
    {
      title: "車両識別子と顧客データの保護",
      type: "knowledge",
      domain: "security",
      source: [`${tmOutput}/エンジニアチーム総評.md`],
      tags: ["security", "identifier", "pii"],
      related: ["00_MOC/qa_sre_security_moc"],
    },
    `# 車両識別子と顧客データの保護

車台番号、登録番号、所有・取引関係は、組み合わせによって個人や契約を特定し得ます。

Rawと利用Martの権限を分け、BI利用者へ不要な識別子を出しません。必要に応じてトークン化し、特権アクセスと照会を監査します。保持・削除期間は業務要件だけでなく、契約と社内データ分類に合わせて決めます。`,
  ],
  [
    "02_Knowledge/sre/データパイプラインの再実行と監視.md",
    {
      title: "データパイプラインの再実行と監視",
      type: "knowledge",
      domain: "sre",
      source: [`${tmOutput}/エンジニアチーム総評.md`],
      tags: ["sre", "reprocessing", "monitoring"],
      related: ["00_MOC/qa_sre_security_moc"],
    },
    `# データパイプラインの再実行と監視

ジョブの成功だけではデータ基盤の正常性を判断できません。鮮度、未取得、照合率、件数、金額不一致を監視します。

再実行では、同じ抽出範囲とバッチを識別でき、重複せず、どこまで反映したかを確認できることが必要です。バックフィル、誤統合修正、遅延到着、取消のRunbookを分けておくと、障害時の判断が速くなります。`,
  ],
  [
    "02_Knowledge/integration/差分連携で確認すること.md",
    {
      title: "差分連携で確認すること",
      type: "knowledge",
      domain: "integration",
      source: [`${tmOutput}/エンジニアチーム総評.md`],
      tags: ["integration", "incremental-load", "cdc"],
      related: ["03_Patterns/data_pipeline_patterns/履歴方式選択パターン"],
    },
    `# 差分連携で確認すること

更新日時だけの差分取得は、遅延更新、過去日付修正、削除を取りこぼすことがあります。

確認するものは、更新・削除・再送仕様、カーソルの信頼性、抽出境界、タイムゾーン、再取得方法、同一データの重複排除です。バッチID、抽出範囲、ソース件数、取込件数、隔離件数を残し、外部障害と内部変換エラーを分けます。`,
  ],
  [
    "02_Knowledge/data_engineering/BI初学者教育ではデータマート実装と利用を分ける.md",
    {
      title: "BI初学者教育ではデータマート実装と利用を分ける",
      type: "knowledge",
      domain: "data_engineering",
      source: [`${cdvOutput}/エンジニアチーム総評.md`],
      tags: ["bi", "training", "data-mart", "scope"],
      related: [
        `${cdvProjectBase}/decisions`,
        "04_Decision_Logs/ADR-20260615-初回BI教育では用意済みデータマートを使う",
      ],
    },
    `# BI初学者教育ではデータマート実装と利用を分ける

BI初学者に、RawデータからのMart実装、BI操作、Dashboard設計、データ解釈を同時に求めると、どの学習も浅くなります。

初回は用意済みMartを使い、粒度、Measure、Dimension、集計可否を理解してからVisualとDashboardを作ります。SQL、ETL、複数Fact、性能、権限は発展編へ分けます。

完了条件は画面完成ではなく、粒度と指標を説明し、事実・仮説・未確認事項を分けて話せることです。`,
  ],
  [
    "02_Knowledge/ai_llm/AI社員チームの品質責任分離.md",
    {
      title: "AI社員チームの品質責任分離",
      type: "knowledge",
      domain: "ai_llm",
      source: teamSources,
      tags: ["ai-agent", "quality", "responsibility"],
      related: [
        `${teamProjectBase}/decisions`,
        "04_Decision_Logs/ADR-20260614-最終品質責任を独立Reviewerへ集約する",
      ],
    },
    `# AI社員チームの品質責任分離

成果物の品質を作成者の自己確認だけに置くと、見落としと都合のよい解釈が残ります。

役割は、Produce、Specialist Review、Final Quality Verdict、Coordinate and Report、Curate and Reuse、Human Decisionに分けます。特に、Quality ReviewerとKnowledge Curatorを分けることが重要です。前者は品質判定、後者は承認済み成果物の再利用化を担い、判定を書き換えません。`,
  ],
];

for (const [file, metadata, body] of knowledgeNotes) {
  notes.set(file, note(metadata, body));
}

const patternNotes = [
  [
    "03_Patterns/data_pipeline_patterns/Raw_Staging_Core_Martの責任分離.md",
    "Raw Staging Core Martの責任分離",
    "data_engineering",
    [tmInput, `${tmOutput}/エンジニアチーム総評.md`],
    ["data-pipeline", "layered-architecture"],
    ["02_Knowledge/data_engineering/履歴データ設計の使い分け"],
    `# Raw / Staging / Core / Martの責任分離

## Pattern
- Rawは取得事実を保持し、再処理とソース差異調査を可能にする。
- Stagingはソース固有形式を標準化し、品質エラーを隔離する。
- Coreは業務上の共通定義と粒度を持つ。
- Martは利用用途に合わせて集計し、品質状態も見せる。

## 適用条件
複数ソース、訂正、再実行、BI利用があるデータ基盤。

## 避けること
Power BI都合をCoreへ直接持ち込むこと、Rawで業務定義を作ること、Martだけを正本にすること。`,
  ],
  [
    "03_Patterns/db_design_patterns/識別子クロスウォークパターン.md",
    "識別子クロスウォークパターン",
    "data_engineering",
    [`${tmOutput}/エンジニアチーム総評.md`],
    ["db-design", "identity-resolution"],
    ["02_Knowledge/data_engineering/車両個体IDと識別子クロスウォーク"],
    `# 識別子クロスウォークパターン

複数システムの識別子が変化・重複する対象を、基盤内の不変IDへ対応付けます。対応には有効期間、照合方法、確度、レビュー状態、統合・分割履歴を持たせます。

## 向くケース
車両、顧客、商品、拠点など、同一性が複数キーにまたがり、後から誤統合を修正する必要がある場合。

## 向かないケース
ソースの単一不変キーが契約として保証され、統合・分割が発生しない場合。`,
  ],
  [
    "03_Patterns/data_pipeline_patterns/履歴方式選択パターン.md",
    "履歴方式選択パターン",
    "data_engineering",
    [tmInput, `${tmOutput}/エンジニアチーム総評.md`],
    ["history", "scd2", "event-sourcing"],
    ["02_Knowledge/data_engineering/履歴データ設計の使い分け"],
    `# 履歴方式選択パターン

テーブル名ではなく、記録対象の性質で方式を選びます。

1. 事実が追加されるなら追記型。
2. 属性の有効期間が必要ならSCD Type2。
3. 状態遷移の順序が重要なら状態履歴。
4. 取引訂正があるなら元取引と取消・訂正を分ける。
5. 対応関係が変わるなら有効期間付きBridge。
6. 訂正前の見え方まで必要なら業務時刻と記録時刻を分ける。`,
  ],
  [
    "03_Patterns/testing_patterns/Source_Core_Mart照合パターン.md",
    "Source Core Mart照合パターン",
    "qa",
    [`${tmOutput}/エンジニアチーム総評.md`],
    ["testing", "reconciliation", "data-quality"],
    [`${tmProjectBase}/test_summary`],
    `# Source / Core / Mart照合パターン

データ変換の正しさを、件数だけでなく金額と除外理由まで含めて確認します。

## Check
- Source取得件数 = 正常取込 + 隔離 + 意図した除外
- Core金額 = Source金額を業務ルールで変換した結果
- Mart金額 = Coreから定義どおり集計した結果
- 未照合、取消、重複、遅延は別区分で説明可能

差分をゼロに見せるために未照合データを捨てないことが重要です。`,
  ],
  [
    "03_Patterns/operation_patterns/品質レビューと再作業ループ.md",
    "品質レビューと再作業ループ",
    "qa",
    [`${sourceRoot}/ai_team/review/review_policy.md`, `${teamOutput}/quality_review_report.md`],
    ["quality-review", "rework", "governance"],
    ["02_Knowledge/ai_llm/AI社員チームの品質責任分離"],
    `# 品質レビューと再作業ループ

Producerが成果物、差分、検証証跡、未実施事項を提出し、専門Reviewerが担当観点を判定します。Quality Reviewerは全証跡を横断してP0からP3を付け、PASS、PASS_WITH_CONDITIONS、REWORK_REQUIRED、BLOCKEDを判定します。

再作業ではFinding IDを維持し、修正内容ではなく修正証跡を確認します。PASS後はKnowledge Curatorが判断と未解決事項を第二の脳へ反映し、同じ指摘が続く場合はSkillやテンプレートを改善します。`,
  ],
  [
    "03_Patterns/operation_patterns/初学者ハンズオン教材の4点セット.md",
    "初学者ハンズオン教材の4点セット",
    "operation",
    [`${cdvOutput}/エンジニアチーム総評.md`],
    ["training", "hands-on", "documentation"],
    [`${cdvProjectBase}/implementation_summary`],
    `# 初学者ハンズオン教材の4点セット

## Pattern
初学者向けの製品教育は、スライド、受講者向けハンズオン、短いリファレンス、講師Runbookに分けます。

- スライド: 全体像と判断基準
- ハンズオン: 変更されやすい操作手順
- リファレンス: 用語と確認チェック
- Runbook: 環境確認、進行、つまずき対応

1つの巨大資料へまとめるより、役割ごとに分けた方が更新しやすく、講義と自習の両方へ使えます。初回は少人数で試行し、実際につまずいた箇所だけを補強します。`,
  ],
];

for (const [file, title, domain, source, tags, related, body] of patternNotes) {
  notes.set(file, note({
    title,
    type: "pattern",
    domain,
    source,
    tags,
    related,
  }, body));
}

notes.set(
  "04_Decision_Logs/adr_index.md",
  note(
    {
      title: "ADR Index",
      type: "moc",
      tags: ["adr", "decision"],
      related: ["00_MOC/engineering_moc"],
    },
    `# ADR Index

- [[04_Decision_Logs/ADR-20260614-車両利益MVPを全テーブル履歴化より先行する|車両利益MVPを先行する]]
- [[04_Decision_Logs/ADR-20260614-車両IDに識別子クロスウォークを採用する|車両IDに識別子クロスウォークを採用する]]
- [[04_Decision_Logs/ADR-20260615-初回BI教育では用意済みデータマートを使う|初回BI教育では用意済みデータマートを使う]]
- [[04_Decision_Logs/ADR-20260614-最終品質責任を独立Reviewerへ集約する|最終品質責任を独立Reviewerへ集約する]]`,
  ),
);

const adrNotes = [
  [
    "04_Decision_Logs/ADR-20260614-車両利益MVPを全テーブル履歴化より先行する.md",
    "ADR 車両利益MVPを全テーブル履歴化より先行する",
    tmProject,
    "data_engineering",
    [`${tmOutput}/エンジニアチーム総評.md`, `${tmOutput}/quality_review_report.md`],
    ["adr", "mvp", "scope"],
    [`${tmProjectBase}/decisions`],
    `# ADR: 車両利益MVPを全テーブル履歴化より先行する

## Context
201テーブル、約1.18億件がある一方、利益定義、車両ID、観測範囲、増分仕様が未確定です。

## Decision
全体はテーブル分類まで行い、詳細設計と実装は代表業務経路の車両利益MVPへ絞ります。

## Rationale
事業価値と技術リスクを早く検証でき、MVPで成立した方式だけを横展開できるためです。

## Consequences
全体標準の完成は後になります。MVP対象外のテーブルは分類と将来候補に留めます。

## Revisit Trigger
MVPで車両照合、金額照合、訂正、再実行が成立し、2つ目の業務経路へ展開するとき。`,
  ],
  [
    "04_Decision_Logs/ADR-20260614-車両IDに識別子クロスウォークを採用する.md",
    "ADR 車両IDに識別子クロスウォークを採用する",
    tmProject,
    "data_engineering",
    [`${tmOutput}/エンジニアチーム総評.md`],
    ["adr", "identity-resolution", "crosswalk"],
    [`${tmProjectBase}/decisions`],
    `# ADR: 車両IDに識別子クロスウォークを採用する

## Context
登録番号は変化し、車台番号も欠損、重複、反映遅延の可能性があります。

## Decision
基盤内のvehicle_lifecycle_idと、ソース識別子を有効期間付きで対応させるcrosswalkを採用します。

## Rationale
一致根拠、照合確度、手動確認、誤統合の分割を追跡できるためです。

## Consequences
照合ルールと例外運用が必要です。未照合を許容し、品質指標として可視化します。

## Revisit Trigger
ソース側で単一不変キーが契約として保証され、統合・分割が不要になったとき。`,
  ],
  [
    "04_Decision_Logs/ADR-20260615-初回BI教育では用意済みデータマートを使う.md",
    "ADR 初回BI教育では用意済みデータマートを使う",
    cdvProject,
    "data_engineering",
    [`${cdvOutput}/エンジニアチーム総評.md`, `${cdvOutput}/quality_review_report.md`],
    ["adr", "bi", "training", "mvp"],
    [`${cdvProjectBase}/decisions`],
    `# ADR: 初回BI教育では用意済みデータマートを使う

## Context
初学者向け教育に、データマートのSQL実装、BI操作、Dashboard設計、データ解釈をすべて含めると、半日や数回の教育では範囲が広すぎます。

## Decision
初回は講師が用意した小規模MartとDatasetを使い、粒度・指標の理解、Visual、Dashboard、解釈までを扱います。Mart実装、複数Fact、権限、性能、運用は発展編へ分けます。

## Rationale
受講者が1つの業務上の問いを最後まで通し、操作だけでなく数字の意味を説明できる状態を優先するためです。

## Consequences
初回だけではデータ提供側の実装スキルは身につきません。必要な受講者には別のデータマート設計・実装編を用意します。

## Revisit Trigger
受講者がData Engineer中心で、SQL経験と十分な教育時間が確保できる場合。`,
  ],
  [
    "04_Decision_Logs/ADR-20260614-最終品質責任を独立Reviewerへ集約する.md",
    "ADR 最終品質責任を独立Reviewerへ集約する",
    teamProject,
    "ai_llm",
    [`${sourceRoot}/ai_team/review/review_policy.md`, `${teamOutput}/quality_review_report.md`],
    ["adr", "quality-review", "ai-agent"],
    [`${teamProjectBase}/decisions`],
    `# ADR: 最終品質責任を独立Reviewerへ集約する

## Context
各AI社員が自己確認だけで完了すると、成果物間の矛盾や専門レビュー不足が残ります。

## Decision
専門Reviewerの判定を集約し、Deliverable Quality Reviewerが最終判定を行います。PMOは判定を変えずに報告します。

## Rationale
品質責任と進行責任を分け、P0・P1や未検証主張を平均点で埋もれさせないためです。

## Consequences
レビュー依頼と証跡作成の手間が増えます。同一AIコンテキストでは独立性が弱いため、重要案件は別実行に分けます。

## Revisit Trigger
3件以上の実績で、レビュー負荷が価値を上回る領域が明確になったとき。`,
  ],
];

for (const [file, title, project, domain, source, tags, related, body] of adrNotes) {
  notes.set(file, note({
    title,
    type: "adr",
    project,
    domain,
    status: "accepted",
    source,
    tags,
    related,
  }, body));
}

notes.set(
  "05_Troubleshooting/error_index.md",
  note(
    {
      title: "Troubleshooting Index",
      type: "moc",
      domain: "operations",
      tags: ["troubleshooting", "error"],
      related: ["00_MOC/engineering_moc"],
    },
    `# Troubleshooting Index

## Data Quality
- [[05_Troubleshooting/data_quality/車両誤統合を検知したとき|車両誤統合を検知したとき]]

## 未登録
Snowflake、Python、API、Terraform、CI/CDの実障害は、今回の成果物にはありません。起きていない問題を一般論だけでトラブルシュートへ登録せず、再現・原因・解決・検証が揃った時点で追加します。`,
  ),
);

notes.set(
  "05_Troubleshooting/data_quality/車両誤統合を検知したとき.md",
  note(
    {
      title: "車両誤統合を検知したとき",
      type: "troubleshooting",
      project: tmProject,
      domain: "data_quality",
      status: "proposed",
      source: [`${tmOutput}/エンジニアチーム総評.md`],
      tags: ["troubleshooting", "identity-resolution", "data-quality"],
      related: [
        "02_Knowledge/data_engineering/車両個体IDと識別子クロスウォーク",
        "03_Patterns/db_design_patterns/識別子クロスウォークパターン",
      ],
    },
    `# 車両誤統合を検知したとき

## 症状
同じvehicle_lifecycle_idに、同時期に成立しない識別子、所有、販売、入庫イベントが混在する。

## 確認
crosswalkのmatch_method、match_confidence、review_status、有効期間、元ソース行を確認します。登録番号だけの一致や、欠損補完による過剰一致がないかを見ます。

## 対応
自動統合を止め、該当レコードを要確認へ戻します。統合根拠を保持したままsplitし、影響するイベントと利益を再計算します。

## 検証
分割後の期間重複、孤立イベント、金額照合、Mart反映、Power BIキャッシュを確認します。

この手順は設計案で、実運用での検証前です。実障害が起きた際は、実行ログと所要時間を追記します。`,
  ),
);

const templateNotes = [
  [
    "90_Templates/project_note_template.md",
    "Project Note Template",
    "project",
    `# Project Overview

## 目的
## 現在地
## 主要成果物
## 主要な意思決定
## 未解決事項・リスク
## 次のアクション
## 関連ノート
## 参照元`,
  ],
  [
    "90_Templates/architecture_note_template.md",
    "Architecture Note Template",
    "architecture",
    `# Architecture Summary

## 目的と制約
## 構成
## データフロー
## 技術選定と理由
## 代替案
## 運用・Security・コスト
## 未確認事項
## 参照元`,
  ],
  [
    "90_Templates/decision_log_template.md",
    "Decision Log Template",
    "adr",
    `# ADR

## Context
## Decision
## Rationale
## Alternatives
## Consequences
## Revisit Trigger
## Evidence`,
  ],
  [
    "90_Templates/troubleshooting_template.md",
    "Troubleshooting Template",
    "troubleshooting",
    `# Troubleshooting

## 症状
## 影響
## 原因
## 確認手順
## 暫定対応
## 恒久対応
## 再発防止
## 検証結果
## 参照元`,
  ],
  [
    "90_Templates/learning_note_template.md",
    "Learning Note Template",
    "knowledge",
    `# Learning Note

## 要点
## 使える場面
## 適用条件
## 実務上の判断
## 失敗しやすい点
## 関連ノート
## 参照元`,
  ],
  [
    "90_Templates/source_map_template.md",
    "Source Map Template",
    "source_map",
    `# Source Map

| Source | Curated Notes | Extracted Content | Review Status | Notes |
|---|---|---|---|---|

## 未反映
## 競合
## 確認事項`,
  ],
];

for (const [file, title, type, body] of templateNotes) {
  notes.set(file, note({
    title,
    type,
    domain: "template",
    status: "template",
    tags: ["template", "obsidian"],
  }, body));
}

notes.set(
  "99_Inbox/unsorted.md",
  note(
    {
      title: "Unsorted Inbox",
      type: "inbox",
      status: "empty",
      tags: ["inbox"],
      related: ["00_MOC/engineering_moc"],
    },
    `# Unsorted Inbox

現在、未分類のメモはありません。

一時メモを置く場合も、出典、案件、確認状態だけは記録し、次回同期でProject、Knowledge、Pattern、ADR、Troubleshootingのいずれかへ移します。`,
  ),
);

for (const [relativePath, content] of notes) {
  writeManaged(relativePath, content);
}

console.log(JSON.stringify({
  target: targetRoot,
  notes: notes.size,
  created: created.length,
  updated: updated.length,
  conflicts,
}, null, 2));
