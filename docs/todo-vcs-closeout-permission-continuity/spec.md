# VCS Closeout And Permission Continuity

상태: 진행 중

## Goal

AI-first change 작업이 검증된 결과를 설명 없는 mutable working copy에 남기거나, 이미
명확히 승인된 commit/push/release transaction을 단계마다 다시 묻고 중단하는 현상을
core contract와 VCS profile에서 방지한다.

## Scope

- change/build/fix의 기본 local 종료 상태를 described logical change와 empty working
  copy로 정의한다.
- local closeout과 external publication permission을 분리한다.
- 직접 승인 또는 exact action/target을 열거한 직전 계획의 승인을 bounded-task
  authorization으로 정의한다.
- 재승인이 필요한 target, owner, version, visibility, material scope, destructive
  history, cost와 secret 경계를 명시한다.
- central self-hosting fixture와 소비 저장소 generated artifact로 계약을 검증한다.

## Non-goals

- vague한 과거 관행이나 관계만으로 external write 권한을 추론하는 것
- repository publication, privacy, signing 또는 native gate를 완화하는 것
- 사용자 WIP가 있는 기본 working copy를 자동 정리하는 것
- 모든 소비 환경에 `Stop` hook을 기본 설치하는 것

## Acceptance

- generated `AGENTS.md`가 local logical change closeout을 publication permission 없이
  수행하도록 지시한다.
- generated agent harness가 task-local authorization의 지속과 재승인 trigger를
  구분한다.
- `vcs-jj` profile이 `jj describe` 뒤 `jj new`로 logical unit을 닫고, 미승인 상태에서
  default bookmark를 이동하지 않도록 지시한다.
- publication 권한이 없으면 local clean closeout 뒤 exact pending action만 보고하고,
  권한이 있으면 gate부터 remote identity와 terminal evidence까지 재요청 없이 진행한다.
- user no-commit, repository 금지와 blocked isolated WIP가 명시적 예외로 남는다.
- `scripts/check.sh`, repository publication gate와 machine-local guard가 통과한다.
- signed `v1.2.0` source와 승인된 소비 저장소 update가 remote equality와 terminal CI를
  통과한다.

## Completion Boundary

core/profile 구현과 local green만으로 완료하지 않는다. signed `v1.2.0` source,
승인된 소비 저장소의 pinned update, repository-native gate, remote equality와 terminal
CI가 모두 닫힌 뒤 이 packet을 `docs/milestones/`로 이동하고 active pointer를 제거한다.

## Verification

- synthetic generated-guidance assertions
- central render/drift and harness interface
- full `scripts/check.sh`
- repository and machine-local publication boundary
- signed release tag, remote identity and Python CI
- 소비 저장소 standalone/native gate, remote equality and terminal CI
