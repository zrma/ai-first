# Handoff

## 현재 단계

`ai-first`는 self-hosting core부터 GPT-6 Astra guidance와 활성 소비 저장소
adoption 및 spec-to-artifact lifecycle까지 Stage 0부터 Stage 11을 완료했다.
Stage 12의 의도 기반 변경 리뷰는 `1.6.0-dev` local candidate로 구현·검증했다.
현재 published stable은 `v1.5.0`이다.

self-hosting 선언, model/vendor 중립적 core, capability profile, repository overlay,
deterministic render, content-addressed lock, central drift check와 standalone checker가
동작한다. synthetic consumer fixture는 central checkout 없이 generated input/output
drift와 lock metadata 정합성을 검증한다.

## 현재 milestone

현재 active milestone은 `docs/todo-release-1.6/spec.md`의 stable release와 adoption이다.
`1.6.0` source와 생성 결과를 검증하고 framework publication, signed tag와 release,
활성 소비 저장소의 release pin·native gate·원격 반영·동일 SHA의 CI를 순서대로 확인한다.
기존 제품 작업과 고유 이력은 보존한다. 대상별 증거는 machine-local 계층에서 관리한다.

완료 결과는 `docs/completed-milestones.md`, spec 정립과 지식 이관은
`docs/WORK_LIFECYCLE.md`를 따른다. 대상별 evidence는 machine-local 계층에서 관리한다.

## 시작 순서

1. `jj status`
2. `docs/AI_FIRST_CHARTER.md`
3. `docs/ARCHITECTURE.md`
4. `docs/COMPATIBILITY.md`
5. `docs/status.md`
6. task-relevant active `docs/todo-*/spec.md`와 `open-questions.md`가 있으면 해당 문서
7. `scripts/check.sh`

## 현재 검증

`scripts/check.sh`가 central/standalone drift, harness interface, repository publication
boundary, navigation, Python syntax와 unit fixture를 검사한다.

## Publication 상태

- tracked content class: `public`
- remote: 기존 `v1.5.0` lifecycle closeout까지 public `main`에 반영
- license: `Apache-2.0`
- CI: published `v1.5.0`의 Python 3.11/3.14 success; development candidate는 local 검증
- stable release: signed annotated `v1.5.0`, remote tag/commit equality와 terminal CI verified
- private vulnerability reporting: enabled

## 보호 경계

- 다른 저장소의 local path, 이름별 migration 상태, WIP와 private inventory를 이
  공개 저장소에 기록하지 않는다.
- 다른 저장소 adoption은 기본 working copy 밖의 VCS-isolated migration checkout에서
  수행하고 repository-native metadata gate를 그대로 보존한다.
- 소비 저장소의 push는 framework publish와 별개의 permission boundary다.
