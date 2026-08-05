# Architecture

## 목적

`ai-first`는 공통 운영 계약을 중앙에서 발전시키면서도 각 소비 저장소가 독립적으로
clone, 이해, 검증될 수 있게 하는 versioned composition framework다.

## 계층

### 1. Identity

`docs/AI_FIRST_CHARTER.md`가 인간과 AI의 관계, 주도권과 공동 책임을 정의한다.
이 계층은 model, vendor, 언어와 배포 환경이 바뀌어도 유지한다.

### 2. Core operating contract

모든 소비 저장소가 지켜야 할 request mode, initiative, persistence, verification,
handoff, permission과 publication boundary를 정의한다.

### 3. Capability profiles

VCS, 언어, runtime 또는 위험 표면에 필요한 공통 specialization을 선택한다.
예상 profile은 `vcs-jj`, `public-repository`, `openai-agent-guidance`, `rust`,
`typescript`, `k8s`, `game`과 model capability다.

profile은 core의 permission 또는 evidence 기준을 약화할 수 없다.

### 4. Repository overlay

소비 저장소가 제품 목적, source of truth, architecture, domain invariant, 검증 명령,
active work와 추가 escalation rule을 소유한다.

공통 interface를 표준화하되 프로젝트 내용을 generic template로 평탄화하지 않는다.

### 5. Machine-private overlay

credential, 실제 host·cluster·endpoint, private repository inventory와 복구용 환경
정보는 공개 framework와 소비 저장소 밖의 권한 있는 machine-local 계층에 둔다.

## 합성 계약

소비 저장소는 선언 파일과 lock을 tracked 상태로 보유한다.

```text
.ai-first.toml
.ai-first.lock
.ai-first/overlays/
AGENTS.md
docs/agent-harness.md
```

- `.ai-first.toml`: framework version, profile, overlay, output과 repository check
  선언의 source of truth.
- `.ai-first.lock`: framework source kind/revision, 입력과 생성 결과 digest.
- `.ai-first/overlays/`: repository-owned 내용.
- `AGENTS.md`, `docs/agent-harness.md`: core, profile과 overlay를 합성한 tracked output.

생성 output은 명확한 generated boundary를 포함하고, 수동 변경은 `check`에서 drift로
실패해야 한다. repository-owned 변경은 overlay에서 수행한다.

## 독립 실행 계약

소비 저장소는 다음 조건을 만족해야 한다.

- 중앙 checkout 또는 sibling-relative path 없이 AI가 시작할 수 있다.
- core contract와 필요한 profile 내용이 tracked output에 포함된다.
- framework 도구가 없어도 현재 생성 결과와 repository-local 검증을 실행할 수 있다.
- update에만 명시적으로 선택한 framework release, immutable commit 또는 local
  development source를 사용한다.

따라서 live symlink, 필수 git submodule과 machine-specific include path를 사용하지
않는다.

## Update transaction

framework update는 다음 transaction으로 처리한다.

1. 대상 저장소의 상태, active workspace와 publication class를 읽는다.
2. 기본 working copy 밖에 VCS-isolated migration checkout을 만든다. `jj workspace`를
   우선하되 repository-native gate가 실제 Git worktree metadata를 요구하면 격리된
   Git-backed checkout을 colocated `jj`로 관리한다.
3. 목표 framework version, immutable source revision과 profile을 선택한다.
4. core, profile과 overlay를 결정적으로 합성한다.
5. lock과 generated output diff를 검토한다.
6. repository-local focused/canonical/publication gate를 실행한다.
7. 각 logical unit을 설명된 `jj` change로 닫고 새 empty working-copy change를 만든다.
8. 통합, push와 release는 task-local authorization에 기록된 exact action/target 범위에서
   수행하고, 범위가 유지되는 동안 단계별 재승인을 요구하지 않는다.

여러 저장소를 하나의 원자적 change나 일괄 push로 취급하지 않는다.
격리를 위해 repository-native gate를 생략하거나 완화하지 않으며, 작업 시작·todo
마감·교훈 이관 같은 저장소 고유 lifecycle도 기존 계약대로 닫는다.

## Framework repository

framework 저장소 자체도 같은 선언, 합성, drift check와 publication gate를 적용하는
self-hosting consumer다. bootstrap 동안 수동 source와 generated output의 경계를 먼저
고정하고, 첫 vertical slice에서 self-hosting check를 통과시킨다.

## Non-goals

- 모든 프로젝트 문서를 동일한 내용으로 만드는 것
- AI에게 external write 또는 파괴적 작업의 무제한 권한을 주는 것
- 특정 model의 prompt collection이 되는 것
- 중앙 저장소에서 소비 저장소의 private/local inventory를 추적하는 것
- 소비 저장소의 native test와 release gate를 대체하는 것
