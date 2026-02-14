# Upbit Trading Bot (OpenClaw A-Plan) 🚀

이 프로젝트는 **OpenClaw** 환경에 최적화된 업비트 자동 매매 엔진입니다. **A-Plan(Single-Run)** 아키텍처를 채택하여 높은 안정성과 리소스 효율성을 제공합니다.

## ✨ 주요 특징

- **A-Plan 아키텍처**: 무한 루프 없이 Cron 스케줄러에 의해 5분마다 1회 실행되는 단일 실행 모델.
- **OpenClaw Tool 통합**: 직접적인 HTTP 호출이나 FS 입출력 없이 OpenClaw가 제공하는 전용 도구(Market, Trading, Storage)를 통해 동작.
- **상태 기반 관리**: Storage/KV를 활용하여 각 마켓별 포지션 상태를 독립적으로 관리하고 중복 주문을 방지.
- **분산 락킹**: `lock:monitor_once` 키를 사용하여 Cron 실행이 겹치는 것을 방지.
- **데이터 쿼리 커맨드**: 실시간 시세, 보유 자산, 계좌 평가액 등을 즉시 조회할 수 있는 전용 명령어 지원.
- **진단 로그**: 실행 결과에 상세 진단 로그(`logs`)를 포함하여 전략 미발생 사유 등을 투명하게 확인 가능.

## 📁 디렉토리 구조

```text
skill.js                # CLI 엔트리포인트 & 커맨드 러너
handlers/
  monitorOnce.js        # 메인 매매 사이클 오케스트리에이터
repo/
  positionsRepo.js      # Storage 기반 포지션 상태 관리
domain/
  strategies.js         # 변동성 돌파 전략 수식 (Pure Logic)
  riskManager.js        # 계좌 잔고 및 주문 가능 여부 검증
adapters/
  execution.js          # OpenClaw Tools 래퍼 레이어
services/
  orderService.js       # 매수/매도 주문 실행 서비스
utils/
  log.js                # 인메모리 로그 버퍼 유틸리티
  time.js               # 시간 포맷 및 설정 파싱 유틸리티
SKILL.md                # OpenClaw 스킬 명세 및 메타데이터
```

## 🚀 실행 및 관리

### CLI 사용법

모든 실행은 `skill.js`를 통해 이루어지며, 출력은 항상 단일 라인 JSON 형식을 유지합니다.

```bash
# 메인 매매 사이클 실행 (Cron 스케줄러가 호출)
node skill.js monitor_once

# 실시간 시세 조회
node skill.js price KRW-BTC

# 보유 자산 목록 조회
node skill.js holdings

# 총 자산 평가액(KRW 취합) 조회
node skill.js assets

# 도움말 확인
node skill.js help
```

### 상태 전이 머신

마켓별 상태는 다음과 같이 전이됩니다:
`FLAT` (미보유) -> `ENTRY_PENDING` (매수 중) -> `OPEN` (보유) -> `EXIT_PENDING` (매도 중) -> `FLAT` (종료)

## ⚙️ 설정 (Environment Variables)

`.env` 파일 또는 OpenClaw 환경 설정을 통해 다음 변수들을 조정할 수 있습니다:

- `WATCHLIST`: 감시할 마켓 리스트 (예: `KRW-BTC,KRW-ETH`)
- `TARGET_PROFIT`: 익절 비율 (기본: `0.05` / 5%)
- `STOP_LOSS`: 손절 비율 (기본: `-0.05` / -5%)
- `K_VALUE`: 변동성 돌파 계수 (기본: `0.5`)
- `BUDGET_KRW`: 마켓별 매수 예산 (단위: KRW)
- `BUY_COOLDOWN_SEC`: 매수 후 재진입 방지 시간 (초)
- `LOCK_TTL_SEC`: 실행 락 유지 시간 (초)

## ⚖️ 라이선스

이 프로젝트는 ISC 라이선스를 따릅니다.
