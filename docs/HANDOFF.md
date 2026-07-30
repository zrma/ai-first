# Handoff

## 현재 단계

`ai-first`는 bootstrap 단계다. AI-first 정체성, 인간과 AI의 역할, framework layer,
독립 consumer와 migration workspace 계약이 repository-owned 문서로 정의되어 있다.

합성 CLI, schema, lock, profile과 standalone fixture는 아직 구현되지 않았다.

## 현재 milestone

`docs/todo-bootstrap-core/spec.md`

목표는 framework 선언에서 core, profile과 repository overlay를 결정적으로 합성하고,
이 저장소 자체에서 drift check를 통과하는 최소 self-hosting vertical slice다.

## 시작 순서

1. `jj status`
2. `docs/AI_FIRST_CHARTER.md`
3. `docs/ARCHITECTURE.md`
4. `docs/todo-bootstrap-core/spec.md`
5. `docs/todo-bootstrap-core/open-questions.md`
6. `scripts/check.sh`

## 현재 검증

bootstrap 문서 interface와 shell syntax만 검사한다. tooling 구현 후 deterministic
render와 standalone fixture를 canonical gate에 추가한다.

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
