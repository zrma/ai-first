# Handoff

## 현재 단계

`ai-first`는 self-hosting core, public foundation, representative pilot, stable
release, portfolio adoption과 active-work lifecycle hardening을 완료했다. stable
`v1.1.1` release와 승인된 소비 저장소 집합의 pinned update도 닫혔다. 현재 `1.2.0`
development line에서 VCS closeout과 permission continuity를 강화하고 있다.

`1.2.0` 선언, core, `vcs-jj`/`public-repository`/`openai-agent-guidance`
profile, repository overlay, deterministic render, content-addressed lock, central drift
check와 standalone checker가 동작한다. synthetic consumer fixture가 central checkout
없이 generated input/output drift를 검증한다.

## 현재 milestone

활성 milestone은 `docs/todo-vcs-closeout-permission-continuity/spec.md`다.

완료된 Stage 0부터 Stage 6까지의 summary와 상세 packet은
`docs/completed-milestones.md`와 `docs/milestones/`에 있다. 현재 Stage 7은 local commit
closeout과 한 번 승인된 publication transaction의 지속 규칙을 release와 소비 저장소
evidence까지 닫는다.

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
- stable release: signed annotated `v1.1.1`, remote tag/commit equality verified
- private vulnerability reporting: enabled

## 보호 경계

- 다른 저장소의 local path, 이름별 migration 상태, WIP와 private inventory를 이
  공개 저장소에 기록하지 않는다.
- 다른 저장소 adoption은 기본 working copy 밖의 VCS-isolated migration checkout에서
  수행하고 repository-native metadata gate를 그대로 보존한다.
- 소비 저장소의 push는 framework publish와 별개의 permission boundary다.
