# Active-work Lifecycle Hardening

상태: 진행 중

## Goal

terminal 상태로 닫힌 milestone packet이 active-work namespace와 pointer에 남아 다음
세션에서 현재 작업으로 오인되는 현상을 framework contract와 deterministic gate로
방지한다.

## Scope

- active-work packet의 시작, 진행, 완료와 archive lifecycle을 core에 명시한다.
- `docs/todo-*/spec.md`의 terminal status를 standalone checker가 거부한다.
- active packet과 completed history를 구분하는 fixture를 추가한다.
- framework self-hosting 문서에서 완료 packet을 completed milestone 영역으로 이동한다.
- 호환 가능한 stable `1.1.0` release를 준비한다.

## Non-goals

- 소비 저장소 inventory나 이름별 migration 상태의 중앙 추적
- 소비 저장소의 work packet을 중앙에서 자동 수정하는 기능
- 이번 local change에서 stable tag, release 또는 portfolio update 수행
- repository-specific todo 형식과 native finalize command의 대체

## Acceptance

- terminal status가 active-work path에 있으면 standalone check가 path와 함께 실패한다.
- 진행 중인 active packet과 active namespace 밖의 completed packet은 통과한다.
- 완료된 framework milestone은 `docs/todo-*` 밖에 있고 navigation link가 유효하다.
- handoff, status, roadmap와 manifest가 같은 active milestone을 가리킨다.
- generated output과 lock이 `1.1.0` source와 lifecycle contract를 반영한다.
- `scripts/check.sh`와 repository publication boundary가 통과한다.

## Completion Boundary

local framework change가 검증된 뒤에도 stable release와 소비 저장소 update는 별도
publication permission이 필요하다. 해당 rollout과 terminal CI까지 닫기 전에는 이
packet을 terminal 상태로 바꾸지 않는다. 완료 시 `docs/milestones/`로 이동하고
manifest의 stale active pointer를 제거한다.

## Verification

- focused standalone lifecycle fixture
- generated render/check와 lock drift
- repository navigation과 harness interface
- full `scripts/check.sh`
- repository와 machine-local publication boundary
