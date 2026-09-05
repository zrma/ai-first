# Handoff

## 현재 단계

`ai-first`는 self-hosting core부터 GPT-6 Astra guidance와 활성 소비 저장소
adoption까지 Stage 0부터 Stage 10을 완료했다. 현재 stable은 `v1.4.0`이다.

self-hosting 선언, model/vendor 중립적 core, capability profile, repository overlay,
deterministic render, content-addressed lock, central drift check와 standalone checker가
동작한다. synthetic consumer fixture는 central checkout 없이 generated input/output
drift와 lock metadata 정합성을 검증한다.

## 현재 milestone

현재 작업은 `docs/todo-spec-artifact-lifecycle/spec.md`와 `open-questions.md`다.
spec 설계 계약과 완료 지식 이관을 보강한 뒤 소비 저장소 적용을 준비한다.

`v1.4.0` signed annotated source tag의 identity와 terminal Python CI를 확인했고,
승인된 활성 소비 저장소의 release pin도 native/publication gate, remote equality와
same-SHA terminal CI까지 닫혔다. 고정 source tag와 이후 상태 문서 commit은 구분한다.

완료된 계약과 evidence는 `docs/completed-milestones.md`, 상세 packet은
`docs/milestones/gpt-6-astra-adoption/`와 `docs/milestones/`에 있다.

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
- remote: public `main` publication과 commit equality 확인
- license: `Apache-2.0`
- CI: Python 3.11/3.14 success
- stable release: signed annotated `v1.4.0`, remote tag/commit equality와 terminal CI verified
- private vulnerability reporting: enabled

## 보호 경계

- 다른 저장소의 local path, 이름별 migration 상태, WIP와 private inventory를 이
  공개 저장소에 기록하지 않는다.
- 다른 저장소 adoption은 기본 working copy 밖의 VCS-isolated migration checkout에서
  수행하고 repository-native metadata gate를 그대로 보존한다.
- 소비 저장소의 push는 framework publish와 별개의 permission boundary다.
