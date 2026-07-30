# Handoff

## 현재 단계

`ai-first`는 self-hosting core를 완료하고 public foundation 단계에 있다.

`0.1.0-dev` 선언, core, `vcs-jj`/`public-repository` profile, repository overlay,
deterministic render, content-addressed lock, central drift check와 standalone checker가
동작한다. synthetic consumer fixture가 central checkout 없이 generated input/output
drift를 검증한다.

## 현재 milestone

`docs/todo-public-foundation/spec.md`

목표는 license, CI, publication gate와 public remote evidence를 닫아 framework를
안전하게 공개하는 것이다.

## 시작 순서

1. `jj status`
2. `docs/AI_FIRST_CHARTER.md`
3. `docs/ARCHITECTURE.md`
4. `docs/todo-public-foundation/spec.md`
5. `docs/todo-public-foundation/open-questions.md`
6. `scripts/check.sh`

## 현재 검증

`scripts/check.sh`가 central/standalone drift, harness interface, repository publication
boundary, navigation, Python syntax와 unit fixture를 검사한다.

## Publication 상태

- tracked content class: `public`
- remote: 미생성
- license: 결정 필요
- 최초 public publish: repository gate와 machine-local inventory gate 통과 필요

## 보호 경계

- 다른 저장소의 local path, 이름별 migration 상태, WIP와 private inventory를 이
  공개 저장소에 기록하지 않는다.
- 다른 저장소 adoption은 기본 working copy가 아닌 전용 migration workspace에서
  수행한다.
- 소비 저장소의 push는 framework publish와 별개의 permission boundary다.
