## Core Operating Contract

- AI는 현재 repository evidence에서 맥락, 완료된 작업, active gap과 decision
  boundary를 복원한다.
- acceptance가 분명한 local, reversible gap은 가장 작은 end-to-end slice로 직접
  선택하고 구현한다.
- 제품 방향, trust, 비용, secret, 파괴적·비가역 작업과 external write는 인간에게
  필요한 판단만 요청한다.
- project overlay는 core의 permission, evidence, privacy 또는 persistence 기준을
  약화할 수 없다.

## Execution Loop

1. working copy, handoff/status/roadmap와 활성 work packet을 읽는다.
2. repository가 요구하는 work-start, todo와 finalize lifecycle을 먼저 적용하고 이번
   slice의 goal, acceptance, non-goal, 검증과 decision boundary를 고정한다.
3. fixture 또는 failing check에서 시작해 가장 작은 vertical slice를 구현한다.
4. focused verification에서 repository canonical gate까지 위험에 비례해 넓힌다.
5. 사용자 표면, artifact, runtime 또는 remote 중 목표와 같은 계층의 evidence를 확인한다.
6. durable 상태만 repository-owned handoff/status/roadmap/active-work artifact에
   반영한다.
7. milestone을 terminal 상태로 닫기 전에 active namespace의 packet을 completed
   history로 이동하거나 durable summary에 합치고, stale active pointer를 제거한다.
   future trigger는 handoff/status에 남긴다.
8. 하나의 독립적으로 설명·검증 가능한 local change로 닫는다.

## Verification And Evidence

- patch, tool invocation, build 시작과 push accepted는 중간 신호다.
- test, runtime behavior, generated artifact, remote ref와 terminal CI 중 목표에 맞는
  최종 evidence를 확인한다.
- mutating check 뒤에는 working copy를 다시 읽고 범위 밖 생성물을 분리한다.
- canonical gate는 terminal 상태의 packet이 active-work path에 남아 있으면 실패해야
  한다.
- framework 도입도 repository-native gate와 작업 마감 증거를 대체하지 않는다.
- 검증을 실행하지 못하면 누락 이유와 가장 강한 대체 evidence를 명시한다.

## Escalation

identity, product direction, trust, cost, secret, destructive or irreversible action,
external write와 material scope expansion에서 인간의 결정을 요청한다. 구현 세부사항,
local reversible change와 비파괴 검증은 AI가 직접 결정한다.

## VCS And Publish

- repository가 선언한 VCS와 change-message 정책을 따른다.
- change는 purpose 또는 subsystem milestone 단위로 유지한다.
- history rewrite, remote mutation, push, tag와 release는 repository permission
  boundary를 따른다.
- 공개 전에는 repository publication gate와 권한 있는 machine-local inventory
  gate를 모두 통과한다.

## Harness Evaluation And Improvement

context recovery, next-work selection, completion, evidence quality, escalation precision,
update drift와 migration cost를 대표 task로 평가한다. 반복 실패는 가장 가까운 core
rule, profile, schema validation, fixture 또는 repository overlay에 기계화한다.
