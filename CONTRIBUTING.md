# Contributing

`ai-first`는 인간과 AI가 프로젝트를 능동적으로 함께 운영할 수 있는 작고 검증 가능한
framework contract를 지향한다.

## 변경 원칙

- 먼저 `docs/AI_FIRST_CHARTER.md`와 `docs/ARCHITECTURE.md`를 읽는다.
- common core 변경과 repository-specific example을 구분한다.
- 관측된 실패, 명시된 contract 또는 testable acceptance와 연결되지 않는 generic
  instruction을 추가하지 않는다.
- generated `AGENTS.md`, `docs/agent-harness.md`와 `.ai-first/check.py`를 직접 편집하지
  않는다. `.ai-first.toml`, overlay 또는 framework source를 수정한 뒤 render한다.
- prompt, transcript, raw tool output, local path, private inventory와 credential을
  issue, commit, fixture 또는 문서에 넣지 않는다.
- AI-assisted contribution도 사람의 변경과 같은 acceptance, test, review와 provenance
  기준을 통과해야 한다.

## 개발 흐름

```sh
scripts/ai-first render --repo .
scripts/check.sh
```

하나의 change는 하나의 독립적으로 설명·검증 가능한 목적만 가진다. public push나
release 전에는 `docs/PUBLICATION.md`의 gate를 따른다.

## 기여 license

별도로 명시하지 않는 한, 제출한 기여는 프로젝트와 동일한 `Apache-2.0` 조건으로
제공된다.

## 보안 문제

보안 취약점은 public issue로 공개하지 말고 `SECURITY.md`의 private reporting 경로를
사용한다.
