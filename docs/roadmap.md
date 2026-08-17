# Roadmap

## Stage 0 — Charter and boundaries

AI-first identity, 인간과 AI의 역할, layer, permission, publication과 migration
boundary를 고정한다.

상태: 완료

## Stage 1 — Self-hosting core

선언 schema, core/profile/overlay composition, lock, deterministic drift check와
standalone fixture를 구현하고 이 저장소 자체에 적용한다.

상태: 완료

## Stage 2 — Public foundation

repository gate, machine-local publication gate, CI와 license를 닫고 공개 remote에서
branch, SHA와 terminal CI를 검증한다.

상태: 완료

## Stage 3 — Representative pilots

서로 다른 개발·운영·위험 특성을 가진 대표 소비 저장소에 VCS-isolated migration
checkout으로 도입한다. repository-native gate와 project identity 보존을 확인한다.

상태: 완료

## Stage 4 — Stable v1

pilot evidence를 반영해 schema, profile, migration contract와 compatibility policy를
안정화하고 versioned v1을 공개한다.

상태: 완료

## Stage 5 — Portfolio adoption

나머지 대상 저장소를 저장소별 독립 change와 gate로 순차 도입한다. framework는
소비 저장소의 inventory나 account-wide 진행 상태를 공개 tracked artifact로
소유하지 않는다.

상태: 완료

## Stage 6 — Active-work lifecycle

완료된 work packet이 active namespace와 pointer에 남지 않도록 terminal 상태를
deterministic gate로 거부하고 completed history와 current work의 경계를 고정한다.

상태: 완료

## Stage 7 — VCS closeout and permission continuity

검증된 local 작업을 logical change와 empty working copy로 기본 마감하고, 명확히 승인된
publication transaction은 같은 bounded task 안에서 중복 승인 없이 terminal evidence까지
계속하는 계약을 고정한다.

상태: 완료

## Stage 8 — Contract audit hardening

일반 contract/status review를 명시 없이 exhaustive capability로 확대하지 않는
proportionality를 core에 고정하고, standalone checker가 lock의 source/profile/input
metadata 정합성을 독립적으로 검증하게 한다.

상태: 완료

## Stage 9 — Stable v1.3 release and adoption

contract audit hardening을 signed annotated `v1.3.0`으로 공개한 뒤, generated Markdown
formatter 호환성 patch인 `v1.3.1`을 adoption source로 사용해 승인된 소비 저장소 집합을
VCS-isolated checkout에서 이관한다. 각 저장소의 standalone/native/publication gate,
remote equality와 same-SHA terminal CI를 독립적으로 확인한다.

상태: 진행 중
