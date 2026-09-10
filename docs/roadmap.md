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

상태: 완료

## Stage 10 — GPT-6 Astra guidance and adoption

공식 Astra 지침으로 `openai-agent-guidance` profile을 갱신하고 schema/core 경계를
유지한다. 아카이브 여부와 원격 기본 브랜치의 관리 선언·lifecycle을 확인한 활성 소비
저장소를 격리 checkout에서 검증하고, 승인된 publication과 same-SHA CI로 닫는다.

상태: 완료. 결과와 검증 범위는 `docs/completed-milestones.md`에 있다.

## Stage 11 — Spec-to-artifact lifecycle

마일스톤의 설계 정합성을 spec으로 확보하고 완료 결과를 지속할 artifact로 이관한다.
framework self-hosting 정리와 소비 저장소 적용을 각각 검증한다.

상태: 완료. signed `v1.5.0`과 승인된 소비 저장소의 release pin, native/publication
gate, remote equality와 same-SHA terminal CI를 확인했다. 결과와 검증 한계는
`docs/completed-milestones.md`, 현재 상태는 `docs/HANDOFF.md`가 소유한다.

## Stage 12 — Intent-aware change review

기존 spec에 문제·원하는 결과·영향·제약·non-goal을 구별하고, 변경 전 기준과 spec
변경 자체를 diff·검증과 대조한다. PR/local 리뷰 기록에서 완료 후에도 필요한 당시
기준과 최종 소유 artifact를 추적한다. 문서량·리뷰 깊이는 위험에 비례시키며
native 형식과 기존 permission/schema를 보존한다.

상태: 완료. signed `v1.6.0` release와 승인된 활성 소비 저장소의 release pin,
native/publication gate, remote equality 및 same-SHA terminal CI를 확인했다.
계약은 `docs/WORK_LIFECYCLE.md`, 검증 범위와 한계는 `docs/completed-milestones.md`,
현재 상태는 `docs/HANDOFF.md`가 소유한다.


## Stage 13 — Reusable verification workflow

공통 검증 runtime·skill을 versioned optional profile로 배포하고 native runner를 한 번
연결한다. 실제 실행·결과·standalone 및 도입 비용을 검증한다.

상태: local candidate 구현·평가 완료. 사용법은 `docs/VERIFICATION.md`, 결과와 한계는
`docs/completed-milestones.md`를 따른다. 행동 판단 개선과 기존 직접 실행 대비 수작업
감소는 입증하지 못했으므로 portfolio 확대를 자동으로 진행하지 않는다. 반복 업무의
절감 evidence 또는 명시적 요구가 다음 시작 조건이다.
