# Stable v1

상태: 완료

## Goal

대표 도입에서 확인한 isolation, native lifecycle과 publication evidence를 반영해
AI-first framework의 첫 stable compatibility contract와 immutable release를 공개한다.

## In scope

- `1.0.0` framework identity와 schema compatibility policy
- VCS-isolated migration checkout 및 repository-native lifecycle 계약
- source checkout 기반 adoption/update interface와 release pin 형식
- self-hosting/synthetic regression, publication gate와 terminal CI

## Non-goals

- package registry 배포
- language/toolchain별 profile의 근거 없는 확대
- 소비 저장소 inventory 추적
- 전체 portfolio adoption

## Acceptance criteria

1. compatibility policy가 framework/schema/profile/output 변경 규칙을 정의한다.
2. self-hosting 선언과 generated output이 `1.0.0` identity로 drift 없이 합성된다.
3. adoption/update interface가 annotated release pin과 검증된 commit을 lock에 기록한다.
4. Python 3.11/3.14 synthetic/self-hosting gate가 통과한다.
5. Apache-2.0, repository gate와 machine-local publication gate가 통과한다.
6. public `main`, immutable release identity, remote SHA와 terminal CI가 일치한다.

## Verification

```sh
scripts/check.sh
python3 .ai-first/check.py
```

## Current evidence

- 완료: compatibility policy, `1.0.0` self-hosting identity, annotated release tag
  validation, verified `source_commit` lock, Python 3.11-compatible unit/self-hosting gate.
- local: `scripts/check.sh`, 16 synthetic/publication tests green.
- 완료: public release-ready commit의 Python 3.11/3.14 terminal CI, signed annotated
  `v1.0.0` tag publication, remote tag object/peeled commit equality와 실제
  release-source render/standalone 검증.

## Decision boundaries

- v1 distribution은 public source checkout을 canonical path로 하고 package registry는
  실제 소비 근거가 생길 때 별도 결정한다.
- release/tag와 remote push는 local gate 이후 별도 publication boundary다.
