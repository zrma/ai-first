# Bootstrap Core

상태: 완료

## Goal

AI-first identity와 layer contract를 실행 가능한 최소 composition framework로
materialize하고 이 저장소 자체에서 self-hosting drift check를 통과한다.

## In scope

- versioned consumer declaration
- core와 capability profile source
- repository overlay source
- deterministic `AGENTS.md`와 `docs/agent-harness.md` composition
- input/output digest lock
- render와 check command
- self-hosting configuration
- standalone synthetic consumer fixture
- invalid configuration과 manual output drift failure test
- repository publication boundary checker

## Non-goals

- 모든 예정 profile 구현
- 원격 package registry 배포
- 소비 저장소 migration
- model별 prompt 최적화
- GUI 또는 hosted control plane
- central repository가 소비 저장소 inventory를 추적하는 기능

## Contract

- core identity와 permission/evidence 기준은 repository overlay가 약화할 수 없다.
- output은 central checkout 없이 AI가 읽고 repository-local check를 실행할 수 있다.
- update는 framework version과 digest를 lock한다.
- 같은 입력은 byte-for-byte 동일한 output과 lock을 생성한다.
- 수동 output 수정은 check에서 실패한다.
- local development source와 released source의 차이를 lock에 표시한다.
- fixture와 공개 문서는 합성된 identifier만 사용한다.

## Acceptance criteria

1. 선언 파일 하나로 profile과 overlay를 선택할 수 있다.
2. render가 `AGENTS.md`, `docs/agent-harness.md`와 lock을 결정적으로 생성한다.
3. check가 clean self-hosting state를 성공으로 판정한다.
4. output 또는 input을 수정하면 check가 non-zero로 실패한다.
5. synthetic consumer fixture가 framework checkout 없이 필요한 tracked surface를
   포함한다.
6. `scripts/check.sh`가 unit, self-hosting, fixture, syntax와 publication self-test를
   한 번에 실행한다.
7. tracked artifact에서 local/private inventory가 검출되지 않는다.

## Verification

현재 bootstrap gate:

```sh
scripts/check.sh
```

tooling 구현 후 canonical gate에 다음 표면을 추가한다.

```sh
python3 -m unittest discover -s tests -p 'test_*.py'
python3 -m ai_first check --repo .
```

완료 evidence:

- `scripts/check.sh`
- deterministic double render unit test
- manual output와 overlay drift failure test
- unsafe relative path와 symlink escape failure test
- standalone generated checker fixture
- repository publication boundary self-test와 tracked scan

## Decision boundaries

- license와 public remote 생성은 local self-hosting green 이후 결정한다.
- incompatible schema 또는 core identity 변경은 owner decision이다.
- implementation language는 standalone성과 dependency cost evidence로 결정한다.
