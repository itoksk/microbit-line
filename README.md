# micro:bit Workshop Materials

このリポジトリは、micro:bit を使ったライントレースとカーリングのワークショップを実施するための教材一式をまとめたものです。授業ドキュメント、サンプルコード、Google Apps Script を利用した結果集計フロー、配布用ファイルが含まれています。

## コンテンツ一覧

| ファイル | 概要 |
| --- | --- |
| `lesson-microbit-line.html` | ライントレース上級編の授業資料（micro:bit Python Editor 前提）。センサー調整→条件分岐→ライン追従→無線応用まで段階的に体験し、クリア報告フォームで進捗を共有できます。理想の直進速度探し・閾値調整・ログの取り方といった実験プロセスを大切にしています。 |
| `lesson-microbit-curling.html` | カーリング初級編の授業資料（MakeCode ブロック前提）。シーケンス制御を信号機で体験→MakeCodeで仮想カーリング→対戦＆ランキング記録の流れ。チームロール（ストラテジスト／プログラマ／テスト係）を回しながら、順番設計と振り返りを重視しています。 |
| `lesson-python-basics.html` | Python の基礎復習資料。授業で出てきた構文（変数・条件分岐・ループ・関数など）を micro:bit と通常 Python の双方向で確認し、学び直しに使えるサンプルと練習課題を整理しました。 |
| `実際にはGoogleドライブに入っているプログラム/` | 授業で配布するモジュール (`haizen.py` など) を格納。micro:bit Python Editor で読み込んで利用します。 |

## レッスン設計のポイント

- **生徒が迷わない導入**
  - カーリング初級編は MakeCode でブロックを並べるところから入ることで、コードに不慣れな生徒でも順序づくりを体験できます。
  - ライントレース上級編ではセンサー値の測定・ノートへの記録を徹底し、実験と調整のサイクルを意識させます。

- **役割リレーと協働学習**
  - カーリングはストラテジスト（戦略係）、プログラマ、テスト担当をローテーションし、同じ問題でも異なる視点を持てるよう設計。
  - ライントレースではハドルタイムを用意し、他班との閾値や速度の共有を推奨しています。

- **ハマりどころの先回り**
  - シーケンス制御では「順番が崩れると危険」という実例（信号機・自動ドア・洗濯機など）を押さえ、順序設計の重要性を実感させます。
  - ライントレースは「まっすぐ進まない」「黒線で止まらない」といった典型的なトラブルをヒントカードにまとめ、原因究明と対策をすぐ参照できるようにしています。

- **成果の可視化と称賛**
  - 進捗フォーム（ライン）／対戦結果フォーム（カーリング）を整備し、Google Apps Script でリアルタイムにランキング・最新ログを表示。誰がどこまで到達したかをクラス全体で共有できます。
  - 表示は「勝ち点」「得失点差」「直近のメモ」など、生徒が工夫を語り合える情報を重視しています。

## 事前準備

1. **micro:bit と周辺機材**
   - micro:bit 本体 + USB ケーブル
   - RoboBase LineSensor ボード（左右モーター付き）
   - 授業資料で参照するコース PDF を印刷（必要に応じて）

2. **micro:bit Python Editor (ラインレース用)**
   - <https://python.microbit.org/v/3> を開く
   - `実際にはGoogleドライブに入っているプログラム/haizen.py` を読み込む
   - `lesson-microbit-line.html` に記載されたコードを段階的に貼り付けて保存・転送

3. **MakeCode (カーリング用)**
   - シーケンス制御の導入では空の MakeCode プロジェクトを使用（<https://makecode.microbit.org/?lang=ja>）
   - カーリング本編はサンプルプロジェクト URL から開始（資料内に記載）

4. **Google Apps Script / スプレッドシート**
   - 対戦結果、進捗報告を記録するための Web アプリを Apps Script で作成
   - スクリプトは README 末尾のコードを貼り付け、ウェブアプリとして公開
   - デプロイ URL を各 HTML の `SCRIPT_URL` / `MATCH_SCRIPT_URL` に設定

## Google Apps Script（対戦・進捗記録API）

以下のコードを Google Apps Script に貼り付け、`matches` シート（ヘッダーは `timestamp|matchId|teamA|teamB|scoreA|scoreB|winner|loser|notes`）を自動生成できるようにします。リポジトリで使用している最新のデプロイ URL は `lesson-microbit-curling.html` の `MATCH_SCRIPT_URL` に記載されています。

```javascript
const SHEET_NAME = 'matches';
const SPREADSHEET_ID = '';      // 既存のスプレッドシートを使う場合はIDを指定
const CACHE_DURATION = 60;      // ランキングキャッシュの秒数
const HEADERS = [
  'timestamp', 'matchId', 'teamA', 'teamB', 'scoreA', 'scoreB', 'winner', 'loser', 'notes',
];

function doPost(e) {
  try {
    const params = e && e.parameter ? e.parameter : {};
    const teamA = (params.teamA || '').trim();
    const teamB = (params.teamB || '').trim();
    const scoreA = Number.parseInt(params.scoreA, 10);
    const scoreB = Number.parseInt(params.scoreB, 10);
    const notes  = (params.notes || '').trim();

    if (!teamA || !teamB || Number.isNaN(scoreA) || Number.isNaN(scoreB)) {
      return json({ status: 'error', message: 'teamA/teamB/scoreA/scoreB を確認してください。' });
    }

    const winner = scoreA === scoreB ? 'draw' : (scoreA > scoreB ? teamA : teamB);
    const loser  = scoreA === scoreB ? ''     : (scoreA > scoreB ? teamB : teamA);

    const lock = LockService.getScriptLock();
    lock.tryLock(5000);

    const sheet = getSheet();
    ensureHeader(sheet);

    const ts = new Date();
    const matchId = makeMatchId(ts);
    sheet.appendRow([
      ts, matchId, teamA, teamB, scoreA, scoreB, winner, loser, notes,
    ]);

    lock.releaseLock();
    clearRankingCache();

    return json({
      status: 'success',
      message: '記録しました！',
      ranking: buildRanking(),
      recentMatches: getRecentMatches(),
    });
  } catch (err) {
    return json({ status: 'error', message: String(err) });
  }
}

function doGet(e) {
  try {
    const action = ((e && e.parameter && e.parameter.action) || '').toLowerCase();
    if (action === 'ranking') {
      return json({
        status: 'success',
        ranking: buildRanking(),
        recentMatches: getRecentMatches(),
      });
    }
    return json({ status: 'error', message: 'action=ranking を指定してください。' });
  } catch (err) {
    return json({ status: 'error', message: String(err) });
  }
}

function doOptions() {
  return ContentService.createTextOutput('ok');
}

function json(obj) {
  return ContentService
    .createTextOutput(JSON.stringify(obj))
    .setMimeType(ContentService.MimeType.JSON);
}

function buildRanking() {
  const cache = CacheService.getScriptCache();
  const hit = cache.get('ranking');
  if (hit) return JSON.parse(hit);

  const sheet = getSheet();
  ensureHeader(sheet);
  const values = safeGetValues(sheet);
  const header = values.shift();
  const idx = indexOf(header);

  const stats = {};
  values.forEach(row => {
    const ta = String(row[idx.teamA] || '').trim();
    const tb = String(row[idx.teamB] || '').trim();
    if (!ta || !tb) return;

    const sa = Number(row[idx.scoreA] || 0);
    const sb = Number(row[idx.scoreB] || 0);

    ensureTeam(stats, ta);
    ensureTeam(stats, tb);

    stats[ta].pointsFor     += sa;
    stats[ta].pointsAgainst += sb;
    stats[tb].pointsFor     += sb;
    stats[tb].pointsAgainst += sa;

    if (sa === sb) {
      stats[ta].draws++; stats[tb].draws++;
    } else if (sa > sb) {
      stats[ta].wins++;  stats[tb].losses++;
    } else {
      stats[tb].wins++;  stats[ta].losses++;
    }
    stats[ta].matchCount++; stats[tb].matchCount++;
  });

  const ranking = Object.keys(stats).map(team => {
    const r = stats[team];
    const diff = r.pointsFor - r.pointsAgainst;
    const points = r.wins * 3 + r.draws;
    return {
      team,
      matches: r.matchCount,
      wins: r.wins,
      draws: r.draws,
      losses: r.losses,
      pointsFor: r.pointsFor,
      pointsAgainst: r.pointsAgainst,
      diff,
      points,
    };
  }).sort((a, b) => (
    b.points - a.points
      || b.diff - a.diff
      || b.pointsFor - a.pointsFor
      || a.team.localeCompare(b.team)
  ));

  cache.put('ranking', JSON.stringify(ranking), CACHE_DURATION);
  return ranking;
}

function getRecentMatches(limit = 10) {
  const sheet = getSheet();
  ensureHeader(sheet);
  const values = safeGetValues(sheet);
  const header = values.shift();
  const idx = indexOf(header);

  const rows = values.slice(-limit).reverse();
  return rows.map(r => ({
    timestamp: formatDate(r[idx.timestamp]),
    matchId: r[idx.matchId] || '',
    teamA: r[idx.teamA],
    teamB: r[idx.teamB],
    scoreA: r[idx.scoreA],
    scoreB: r[idx.scoreB],
    winner: r[idx.winner],
    loser: r[idx.loser],
    notes: r[idx.notes] || '',
  }));
}

function getSheet() {
  const ss = SPREADSHEET_ID
    ? SpreadsheetApp.openById(SPREADSHEET_ID)
    : SpreadsheetApp.getActiveSpreadsheet();

  if (!ss) {
    const created = SpreadsheetApp.create('matches-data');
    return initAndGetSheet(created);
  }

  let sheet = ss.getSheetByName(SHEET_NAME);
  if (!sheet) {
    sheet = ss.insertSheet(SHEET_NAME);
  }
  return sheet;
}

function initAndGetSheet(ss) {
  const sheet = ss.getSheetByName(SHEET_NAME) || ss.insertSheet(SHEET_NAME);
  ensureHeader(sheet);
  return sheet;
}

function ensureHeader(sheet) {
  const lastColumn = sheet.getLastColumn();
  const headerNow = lastColumn ? sheet.getRange(1, 1, 1, lastColumn).getValues()[0] : [];
  const needs = HEADERS.some((h, i) => headerNow[i] !== h) || headerNow.length !== HEADERS.length;

  if (needs) {
    sheet.clear();
    sheet.getRange(1, 1, 1, HEADERS.length).setValues([HEADERS]);
    sheet.setFrozenRows(1);
    sheet.autoResizeColumns(1, HEADERS.length);
  }
}

function indexOf(header) {
  const map = {};
  header.forEach((name, i) => { map[name] = i; });
  return {
    timestamp: map.timestamp,
    matchId:   map.matchId,
    teamA:     map.teamA,
    teamB:     map.teamB,
    scoreA:    map.scoreA,
    scoreB:    map.scoreB,
    winner:    map.winner,
    loser:     map.loser,
    notes:     map.notes,
  };
}

function ensureTeam(stats, team) {
  if (!stats[team]) {
    stats[team] = {
      matchCount: 0,
      wins: 0,
      draws: 0,
      losses: 0,
      pointsFor: 0,
      pointsAgainst: 0,
    };
  }
}

function formatDate(value) {
  if (!value) return '';
  return Utilities.formatDate(new Date(value), Session.getScriptTimeZone(), 'yyyy/MM/dd HH:mm');
}

function safeGetValues(sheet) {
  const lastRow = sheet.getLastRow();
  const lastCol = Math.max(sheet.getLastColumn(), HEADERS.length);
  if (lastRow < 1) return [HEADERS.slice()];
  return sheet.getRange(1, 1, lastRow, lastCol).getValues();
}

function clearRankingCache() {
  CacheService.getScriptCache().remove('ranking');
}

function makeMatchId(ts) {
  const t = Utilities.formatDate(ts, Session.getScriptTimeZone(), 'yyyyMMdd-HHmmss');
  return `${t}-${Utilities.getUuid().slice(0, 8)}`;
}
```

### 公開手順

1. Apps Script に上記を貼り付けて保存
2. 「デプロイ」→「新しいデプロイ」→「種類: ウェブアプリ」
3. 実行するユーザー: **自分** / アクセスできるユーザー: **全員（匿名含む）**
4. 発行された URL を `lesson-microbit-curling.html` の `MATCH_SCRIPT_URL` に設定（進捗フォームを使う場合は `lesson-microbit-line.html` の `SCRIPT_URL` にも設定）

## 運用のヒント

- MakeCode や micro:bit Python Editor の準備は授業開始前に行い、生徒がすぐコードを改造できる状態にしておくとスムーズです。
- ランキング用スプレッドシートは教師用にバックアップをつくり、Apps Script の実行アカウントで編集権限を確保してください。
- `実際にはGoogleドライブに入っているプログラム/` に授業で配布する追加モジュールやサンプルコードをまとめておくと、生徒の環境差異が減ります。
- HTML 資料はブラウザで開くだけで利用できるため、タブレットや Chromebook からでも閲覧可能です。

以上のセットアップで、ライントレース上級編・カーリング初級編・Python 基礎復習という 3 本立てのカリキュラムを一貫して実施できます。授業中に得られた記録はスプレッドシートに集約されるため、振り返りレポートや評価にも活用可能です。
