# VCS integration and closeout

Status: active

## Goal

선형 통합과 task-owned 임시 사본 회수의 재발 방지 규칙·검사를 공통 하네스로 제공하고
활성 소비 저장소에 검증·출고한다.

## Context

logical change 종료와 임시 사본의 회수는 다른 postcondition이다. 기존 published
history, release와 active/WIP는 보존하면서 앞으로의 잘못된 통합과 잔여물을 검출한다.

## Scope And Impact

- vcs-jj profile의 선형 통합·fail-fast·사본 회수 계약 보강
- 선택형 vcs-closeout profile과 standalone runtime, native/CI 연결
- 기존 history checkpoint, inherited work와 명시적 보존 대상 지원
- 새 minor release와 활성 소비 저장소의 immutable source adoption

## Constraints

- 선언/lock schema 1, 구조 ID와 기존 profile·overlay·native gate·제품 동작을 유지한다.
- 기존 tag/release와 과거 merge, unique history와 WIP를 재작성하거나 삭제하지 않는다.
- 소비 inventory·경로·진행 원문은 machine-local evidence에 둔다.
- 검사기는 임시 사본이나 head를 자동 삭제하지 않는다.

## Acceptance

| ID | Verify | Required result |
| --- | --- | --- |
| C1 | render/standalone tests | opt-in 의존성·checksum·충돌·opt-out 보존, 미선택 소비자 유지 |
| C2 | real Git/JJ tests | 새 merge·shallow·잘못된 checkpoint 차단, 과거 history 보존 |
| C3 | real JJ/filesystem tests | WC·workspace·head·Git metadata·task 경로별 검사, inherited work 보존 |
| C4 | native gates | 중앙 전체 gate와 소비자 source/standalone/interface/native/publication 통과 |
| C5 | remote/API/CI | signed 새 source/tag와 소비 pin, remote equality와 same-SHA CI |
| C6 | local closeout | task-owned 사본 회수, 기존 WIP·refs·release 보존 재확인 |

## Out Of Scope

- 기존 공개 history의 선형 재작성과 product runtime/model migration
- 보관된 저장소 adoption, 모든 저장소의 GitHub administration 일괄 변경
- 임의 파일시스템 전수 삭제와 실제 agent 효용·재작업 감소의 미측정 주장

## Artifact Closeout

소유 계약은 docs/VCS_CLOSEOUT.md, profile/runtime과 compatibility 문서다. 결과와 한계를
완료 요약에 이관하고 packet과 active pointer를 제거한다.

## 구현 중 확인한 호환성

실제 local closeout에서 jj 0.38 이전 current workspace의 root metadata 부재를 확인했다.
현재 root와 유일한 WC ID로 확인되는 경우를 지원하고 unknown secondary는 계속 거부한다.
공개된 v1.9.0은 보존하며 v1.9.1로 보완한다. 원래 WIP·release 보존 기준은 유지한다.
