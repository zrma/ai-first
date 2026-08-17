# Contract Audit Hardening

상태: 완료

## Goal

일반적인 contract/status 검토가 명시적 권한 없이 exhaustive capability로
확대되거나, standalone consumer가 `.ai-first.toml`과 내부 정합성이 깨진
framework source metadata를 정상 lock으로 수용하는 문제를 공통 contract과
deterministic gate에서 방지한다.

## Scope

- request mode와 investigation depth를 보존하고, 일반 review를 exhaustive scan,
  long-running multi-agent operation 또는 material cost로 임의 확대하지 않는
  proportionality contract를 core에 추가한다.
- standalone checker가 `.ai-first.toml`과 lock의 framework version, source identity,
  profile 순서를 비교한다.
- `framework_inputs`의 path/digest 형식과 aggregate digest를 다시 계산한다.
- synthetic consumer fixture로 source/profile/digest metadata 변조를 거부하는지
  검증한다.
- 변경은 backward-compatible minor development line `1.3.0-dev`로 표시한다.

## Non-goals

- 소비 저장소의 제품 코드, security 또는 dependency 전수 조사
- 중앙 저장소에서 소비 저장소 inventory를 tracked 상태로 관리하는 기능
- framework checkout 없이 annotated tag와 commit의 외부 Git identity까지
  재검증하는 기능
- `v1.3.0` release, consumer migration, push, tag 또는 release publication

## Acceptance

- generated core가 investigation depth, capability escalation과 material time/cost 경계를
  명시한다.
- 정상 synthetic consumer의 central/standalone check가 모두 통과한다.
- config는 그대로 둔 채 lock의 source kind/revision/commit, profiles, framework
  input digest를 변조하면 standalone check가 구체적인 failure로 거부한다.
- 현재 `v1.2.0` consumer는 변경하지 않고 기존 standalone/harness gate가
  계속 통과한다.
- `scripts/check.sh`와 repository publication boundary가 통과한다.

## Completion Boundary

framework core, standalone checker, regression fixture, generated self-hosting output과
navigation 문서를 같은 local logical change로 닫는다. stable release와 consumer
migration은 별도 publication transaction으로 남긴다.

## Completion Evidence

- generated core와 harness가 investigation depth, capability escalation과 material
  time/token/cost 경계를 명시한다.
- synthetic fixture에서 config와 불일치하는 source/profile metadata, framework input
  aggregate 불일치와 invalid development source commit을 standalone checker가 거부한다.
- self-hosting render/check, 21 tests과 canonical `scripts/check.sh`가 통과했다.
- 기존 stable consumer contract은 변경하지 않았고 standalone/harness interface
  compatibility check가 통과했다.
- stable `v1.3.0` release와 consumer migration은 외부 publication 경계로 남겼다.

## Verification

- focused standalone metadata-tampering fixture
- self-hosting render/check과 generated lock drift
- consumer standalone/harness interface compatibility check
- `scripts/check.sh`
- repository publication boundary과 machine-local diff guard
