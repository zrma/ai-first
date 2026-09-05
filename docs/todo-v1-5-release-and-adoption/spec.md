# v1.5 release and adoption

상태: 진행 중

## 목적과 범위

spec 설계 정립과 완료 artifact 전환 계약을 `1.5.0`으로 공개하고 관리 대상 소비
저장소에 최종 release source로 적용한다. framework와 소비 저장소 모두 최신 원격
기본 브랜치 위에서 작업하며 기존 WIP와 domain contract를 보존한다.

## 관계와 경계

framework release source identity가 소비 pin의 선행 조건이다. 소비 저장소의
pin, generated artifact와 native interface assertion을 함께 갱신하며 공개 framework의
상태 문서에는 대상별 inventory와 local evidence를 넣지 않는다.

현재 검증된 candidate의 제품 동작 변경은 추가하지 않는다. 다른 작업의 최신 main
변경과 겹치면 해당 diff를 먼저 통합·검증한다. publication은 각 저장소의 native 및
privacy gate, remote equality와 same-SHA terminal CI로 독립적으로 닫는다.

## 완료 조건

- framework `scripts/check.sh`와 repository/machine-local publication gate 통과
- signed annotated `v1.5.0`, local/remote tag object 및 source commit identity 일치
- framework main/source의 same-SHA terminal CI 성공
- 각 소비 저장소의 최신 main 기반, 최종 release pin과 native/publication gate 통과
- 소비 저장소별 remote main equality와 same-SHA terminal CI 성공
- 유지할 결과를 완료 요약과 compatibility/handoff/status에 이관하고 이 packet 정리
- logical change와 empty working copy로 닫고 최종 기본 작업공간 상태 확인

## 검증과 이관

framework canonical gate: `scripts/check.sh`. 소비 저장소는 repository-native gate와
standalone check를 사용한다. CI, 서명과 remote ref는 local green과 별도로 검증한다.
최종 계약은 `docs/COMPATIBILITY.md`, 결과·한계는 `docs/completed-milestones.md`,
현재 상태는 `docs/HANDOFF.md`, `docs/status.md`, `docs/roadmap.md`가 소유한다.
