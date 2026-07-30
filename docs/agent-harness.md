# Agent Harness

## Interface

- Structure ID: `ai-first-harness-v1`.
- Framework version: `0.1.0-dev`.
- Convergence stage: `bootstrap`.
- Target stage: `self-hosting`.
- Canonical check: `scripts/check-agent-harness-interface.sh`.
- Publication class: `public`.
- Publication boundary: `docs/PUBLICATION.md`.

`AGENTS.md`가 짧고 항상 필요한 core contract를 소유하고, 이 문서는 framework
architecture, 현재 milestone과 검증 표면으로 가는 canonical operating map이다.

## Project Objective

AI가 인간의 방향과 명시적 경계 안에서 프로젝트를 능동적으로 전진시키고, 인간이
방향지시자·동반자·project manager로 참여할 수 있는 versioned project operating
framework를 제공한다.

## Source Of Truth

- 정체성: `docs/AI_FIRST_CHARTER.md`.
- layer와 composition: `docs/ARCHITECTURE.md`.
- 현재 상태와 순서: `docs/HANDOFF.md`, `docs/status.md`, `docs/roadmap.md`.
- 현재 작업: 활성 `docs/todo-*/spec.md`와 `open-questions.md`.
- 공개 경계: `docs/PUBLICATION.md`.
- 저장소 interface와 checks: `docs/REPO_MANIFEST.yaml`.

## Autonomy And Permissions

- acceptance가 명확한 local, reversible framework 작업은 구현, 검증, 문서화와 local
  `jj` change까지 진행한다.
- 다음 repository-owned gap을 능동적으로 선택하되 identity, product direction,
  trust, 비용, secret, 파괴적 작업과 external write는 에스컬레이션한다.
- 소비 저장소 변경은 전용 migration workspace에서 수행하고 기존 working copy와
  active change를 보존한다.
- 소비 저장소 목록, local 경로, WIP와 private inventory는 tracked public artifact로
  옮기지 않는다.

## Execution Loop

1. `jj status`, handoff/status/roadmap와 활성 todo를 읽는다.
2. identity, core, profile, overlay, tooling 중 하나의 논리적 boundary를 고정한다.
3. acceptance, 검증 명령, generated surface와 publication impact를 먼저 기록한다.
4. 가장 작은 end-to-end fixture 또는 failing check를 만든다.
5. 구현 후 focused test에서 `scripts/check.sh`까지 넓힌다.
6. self-hosting output과 standalone consumer fixture를 함께 확인한다.
7. durable 상태만 handoff/status/roadmap/todo에 반영한다.
8. 하나의 검증 가능한 `jj` change로 닫고 external write 전에는 publication gate를
   실행한다.

## Verification And Evidence

- 전체 local gate: `scripts/check.sh`.
- harness interface: `scripts/check-agent-harness-interface.sh`.
- bootstrap 단계에서는 문서 interface, shell syntax와 tracked privacy를 검사한다.
- tooling 단계에서는 deterministic render, lock drift, standalone consumer와 invalid
  configuration failure를 test fixture로 검증한다.
- migration 단계에서는 target repository의 native gate가 최종 evidence다.
- 최종 보고는 framework local green, target local green, remote publication과 CI를
  서로 다른 상태로 구분한다.

## Escalation

identity 변경, core permission 약화, incompatible schema, license, public visibility,
external write, published-history rewrite 또는 소비 저장소의 제품 방향을 바꾸는
결정에서만 인간에게 최소 판단을 요청한다.

## VCS And Publish

- local VCS는 `jj`를 사용한다.
- change description은 `<type>: <summary>` 형식과 configured attribution을 따른다.
- change는 independently explainable하고 검증 가능한 milestone 단위로 유지한다.
- 다른 저장소 adoption은 전용 `jj workspace`와 독립 change를 사용한다.
- push, remote 생성, visibility, tag/release는 별도 external-write boundary다.
- 최초 공개와 public update 전에는 repository publication gate와 권한 있는
  machine-local private-inventory gate를 모두 통과한다.

## Harness Evaluation And Improvement

대표 저장소 fixture와 실제 pilot에서 context recovery, next-work selection, completion,
evidence quality, escalation precision, update drift와 migration cost를 평가한다.

반복 실패는 가장 가까운 core rule, profile, schema validation, test fixture 또는
repository overlay에 기계화한다. 특정 프로젝트의 예외를 공통 core에 섣불리 올리지
않는다.

## Framework Overlay

- framework는 model/vendor 중립적 identity와 contract를 소유한다.
- 합성 결과는 tracked 상태로 남고 central checkout 없이 이해 가능해야 한다.
- local development source를 사용한 update도 release version과 digest 차이를
  명시해야 한다.
- public framework는 소비 repository inventory나 account-wide 진행 상태를 공개하지
  않는다.

## Related Documents

- Identity: `docs/AI_FIRST_CHARTER.md`.
- Architecture: `docs/ARCHITECTURE.md`.
- Navigation: `docs/HANDOFF.md`.
- Current state: `docs/status.md`.
- Direction: `docs/roadmap.md`.
- Publication policy: `docs/PUBLICATION.md`.
- Active milestone: `docs/todo-bootstrap-core/spec.md`.
- Declared checks: `docs/REPO_MANIFEST.yaml`.
