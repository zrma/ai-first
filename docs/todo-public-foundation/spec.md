# Public Foundation

상태: 완료

## Goal

self-hosting framework의 license, CI와 publication boundary를 닫고 최초 public remote의
default branch, immutable commit identity와 terminal CI를 검증한다.

## In scope

- owner가 선택한 open-source license
- public README, contribution와 security boundary
- canonical `scripts/check.sh` CI
- repository publication gate와 machine-local inventory gate
- public remote 생성과 `main` publication
- remote commit equality, default branch, visibility와 terminal CI 확인
- publish 후 clean local working copy

## Non-goals

- stable v1 tag 또는 release
- package registry 배포
- 소비 저장소 migration
- project-specific profile 확장

## Acceptance criteria

1. license 선택이 tracked license와 manifest에 일치한다.
2. fresh checkout과 CI에서 `scripts/check.sh`가 통과한다.
3. repository checker와 machine-local `all` gate가 최초 공개 후보를 통과한다.
4. public remote의 default branch가 `main`이고 intended local commit과 동일하다.
5. terminal CI가 success이고 open publication blocker가 없다.
6. local working copy가 clean하며 remote 상태와 구분해 보고된다.

## Verification

```sh
scripts/check.sh
scripts/check-publication-boundary.py
```

최초 remote가 만들어진 뒤 권한 있는 machine-local checker의 `all` mode, remote ref와
CI를 별도 확인한다.

## Decision boundaries

- owner가 `Apache-2.0`을 선택했으며 tracked license와 manifest에 반영한다.
- public remote 생성과 최초 push는 이 milestone의 명시적 publication action이다.
- stable release/tag는 별도 milestone이다.

## 완료 evidence

- canonical local gate와 repository publication checker 통과
- 권한 있는 machine-local checker의 `all` mode 통과
- public visibility, `main` default branch와 local/remote commit equality 확인
- Python 3.11/3.14 terminal CI success
- GitHub private vulnerability reporting 활성화
- clean local working copy 확인
