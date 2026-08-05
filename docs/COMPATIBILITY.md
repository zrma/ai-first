# Compatibility

## Version axes

AI-first v1은 서로 다른 compatibility 축을 명시적으로 분리한다.

- `framework_version`: semantic versioning을 따르는 core/profile/tool release.
- `.ai-first.toml`의 `schema_version`: 선언 형식의 parser contract.
- `.ai-first.lock`의 `schema_version`: standalone verification contract.
- harness Structure ID: generated 문서의 공통 interface contract.

`framework_version` major가 바뀌거나 schema/Structure ID가 바뀌면 소비 저장소는
명시적인 migration과 전체 repository-native gate를 실행해야 한다. minor는
backward-compatible capability, patch는 contract를 바꾸지 않는 수정만 허용한다.

현재 self-hosting framework development version은 `1.2.0`이다. logical local VCS
closeout과 bounded-task permission continuity가 추가됐지만 schema version 1과
`ai-first-harness-v1` Structure ID는 유지한다. stable 소비 저장소는 versioned release를
pin하고 repository별 update transaction으로 올린다.

## Source identity

`.ai-first.toml`은 framework source를 다음 중 하나로 고정한다.

- `development`: revision 없음. framework 자체 개발과 local experiment 전용.
- `commit`: full lowercase 40-character commit SHA. checkout `HEAD`, clean state와
  일치해야 한다.
- `release`: stable `vMAJOR.MINOR.PATCH` annotated Git tag. tag가 가리키는 commit,
  checkout `HEAD`와 clean state가 모두 일치해야 한다.

lock은 선언된 source revision과 검증된 `source_commit`을 함께 기록한다. release tag
이동이나 다른 checkout에서의 합성은 fail-closed 한다.

## Canonical v1 distribution

v1의 canonical distribution은 public source checkout이다. package registry와
standalone binary는 필수 경로가 아니다.

소비 저장소 update는 기본 working copy 밖의 VCS-isolated checkout에서 수행한다.
framework checkout은 public annotated release tag에 고정하고 소비 선언을 다음처럼
갱신한다.

```toml
schema_version = 1
framework_version = "1.2.0"
source_kind = "release"
source_revision = "v1.2.0"
```

그 checkout의 CLI로 render/check한 뒤 standalone check와 repository-native gate를
실행한다.

```sh
<framework-checkout>/scripts/ai-first render --repo <consumer-repo>
<framework-checkout>/scripts/ai-first check --repo <consumer-repo>
python3 <consumer-repo>/.ai-first/check.py
```

generated artifact는 계속 tracked 상태로 남으므로 framework checkout은 consumer의
일상 실행 dependency가 아니다.

## Compatibility promise

- v1.x는 schema version 1 선언과 lock을 읽는다.
- core permission, evidence와 privacy contract는 minor/patch에서 약화하지 않는다.
- profile 제거, output 의미 변경과 required field 추가는 major migration이다.
- additive profile과 optional metadata는 minor에서 추가할 수 있다.
- repository overlay와 native gate는 framework update가 덮어쓰거나 우회하지 않는다.
