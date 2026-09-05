# Spec-to-artifact lifecycle

상태: 진행 중

## 목적

todo spec을 milestone 또는 bounded specification의 목적, 범위, 조건과 관계를
명시하고 논리적 누락·모순·미결정을 해소하는 임시 설계 계약으로 정립한다.
완료 시 실제 결과와 유지할 지식을 적절한 artifact에 이관하고 작업 packet을
정리한다. 완료 폴더 이동만으로 지식 이관을 대신하지 않는다.

## 범위와 경계

- model/vendor 중립적 core의 spec 정립, 구현 중 정합성, 완료 이관 계약을 보강한다.
- schema와 harness Structure ID를 유지하는 `1.5.0-dev` minor 개발 변경으로 준비한다.
- self-hosting의 완료 packet에서 결정·근거·한계를 선별해 기존 문서에 이관한다.
- 과거 spec 존재를 강제하는 gate를 제거하고 durable 문서 참조와 lifecycle을 검증한다.
- 소비 저장소는 현재 remote와 관리 의도를 확인하고 VCS-isolated checkout에서
  새 source pin, generated artifact와 충돌하는 lifecycle overlay만 갱신한다.
- 소비 저장소의 제품 변경, 무관한 WIP 정리, 완료 기록 전수 재작성은 포함하지 않는다.
- framework/consumer publication은 local 구현과 별개이며 exact action과 target에 대한
  권한과 publication gate가 필요하다. 대상별 원문은 machine-local 계층에서 관리한다.

## 완료 조건과 검증

- generated bootstrap/harness만으로 spec의 목적과 완료 이관 기준을 복원할 수 있다.
- 중요한 결정 이유·알려진 한계는 architecture, compatibility, lifecycle 문서 또는
  완료 요약에 남고, 과거 질문을 현재 과제로 오인할 참조는 제거된다.
- 원본 보존은 명시적인 추적·운영 필요가 있을 때만 선택하며 이관을 대체하지 않는다.
- `scripts/check.sh`가 deterministic render, standalone lifecycle, navigation,
  harness interface, publication과 synthetic consumer fixture를 통과한다.
- framework local 결과는 described change와 empty working copy로 닫는다.
- 소비 저장소는 각 native gate와 standalone check로 확인하고, 미검증 또는 외부
  단계가 남으면 구현 완료와 구분해 재개 조건을 남긴다.

## 지식 이관 위치

- 공통 계약: `framework/core/AGENTS.md`, `framework/core/agent-harness.md`
- 지속 사용할 lifecycle 설명: `docs/WORK_LIFECYCLE.md`
- 기존 설계 결정: `docs/ARCHITECTURE.md`, `docs/COMPATIBILITY.md`
- 과거 결과와 검증 범위: `docs/completed-milestones.md`
- 현재 준비 상태와 후속 trigger: `docs/HANDOFF.md`, `docs/status.md`, `docs/roadmap.md`

local framework acceptance가 닫히면 이 packet은 제거한다. 소비 저장소 적용 및
publication의 남은 상태는 handoff로 이관하며 완료했다고 표현하지 않는다.
