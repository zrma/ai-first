# Handoff

## 현재 단계

`ai-first`는 self-hosting core, public foundation, representative pilot, stable
release, portfolio adoption, active-work lifecycle, VCS closeout/permission continuity와
contract audit hardening까지 Stage 0부터 Stage 8을 완료했다. stable `v1.2.0`과 승인된 소비 저장소
집합의 pinned update는 repository-native gate, remote equality와 terminal CI까지 닫혔다.

release-ready `1.3.1` self-hosting 선언, core,
`vcs-jj`/`public-repository`/`openai-agent-guidance` profile, repository overlay,
deterministic render, content-addressed lock, central drift check와 standalone checker가
동작한다. synthetic consumer fixture가 central checkout 없이 generated input/output
drift와 lock metadata 정합성을 검증한다.

## 현재 milestone

현재 active milestone은 stable `v1.3.1` patch release와 승인된 소비 저장소 집합의
migration이다. `v1.3.0`은 게시됐지만 generated Markdown formatter 호환성 수정이
필요해 adoption source를 `v1.3.1`로 전환했다. 범위, acceptance와 publication 순서는
`docs/todo-v1-3-release-and-adoption/`이 소유한다.

완료된 Stage 0부터 Stage 8까지의 summary와 상세 packet은
`docs/completed-milestones.md`와 `docs/milestones/`에 있다.

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
- stable release: signed annotated `v1.3.0`, remote tag/commit equality verified;
  `v1.3.1` patch publication 진행 중
- private vulnerability reporting: enabled

## 보호 경계

- 다른 저장소의 local path, 이름별 migration 상태, WIP와 private inventory를 이
  공개 저장소에 기록하지 않는다.
- 다른 저장소 adoption은 기본 working copy 밖의 VCS-isolated migration checkout에서
  수행하고 repository-native metadata gate를 그대로 보존한다.
- 소비 저장소의 push는 framework publish와 별개의 permission boundary다.
