# Release and adoption 1.6.0

상태: 진행 중

## 목적과 범위

의도 기반 변경 리뷰 계약을 stable `v1.6.0`으로 공개하고 활성 소비 저장소가 같은
immutable source를 사용하게 한다. 영향은 framework release와 소비 저장소의
agent guidance, native lifecycle 연결이다.

- 제약: 기존 제품 동작·schema·권한·WIP와 고유 이력을 보존한다. 소비 변경은 격리된
  checkout에서 native 규칙을 확인해 수행한다. 공개 tracked artifact는 public-ready로 유지한다.
- Non-goal: archived 저장소 갱신, 제품 기능 변경, 새 중앙 readiness schema, agent
  행동 성능의 실측, 제품 release나 운영 환경 배포.
- 대상별 inventory와 검증 원문은 machine-local 계층에서 관리한다.

## Acceptance

1. `1.6.0` source와 generated output이 `scripts/check.sh` 및 publication gate를 통과한다.
2. framework main push, 동일 SHA의 terminal CI, signed annotated `v1.6.0` tag와
   GitHub Release를 검증한다. tag·source commit의 identity를 각각 확인한다.
3. remote 기본 브랜치의 관리 선언과 archive 상태로 활성 소비 대상을 확인한다.
4. 각 소비 저장소에서 release pin, generated output, native template/readiness/overlay의
   정합성과 필요한 보완을 검토하고 repository-native gate를 통과한다.
5. 각 소비 push와 동일 SHA의 terminal CI를 확인하며 기존 WIP와 고유 이력을 보존한다.
6. 결과·판단 이유·한계를 완료 요약과 compatibility/handoff에 이관하고 packet을 정리한다.

## 실행 상태

- 완료: framework source의 local 검증과 독립 리뷰, 현재 remote 대조.
- 다음: stable version 확정, publication gate와 출시, 소비 저장소별 적용·검증.
- 판단: 이번 요청의 publication 권한은 유지하며 새 target·파괴적 이력 변경은 범위 밖이다.
