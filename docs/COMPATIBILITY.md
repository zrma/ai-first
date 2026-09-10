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

framework `1.5.0`은 spec 정립과 artifact 전환의 완료 계약을 보강한다.
선언/lock schema version 1과 `ai-first-harness-v1`, GPT-6 Astra profile을 유지한다.
기존 archive를 기계적으로 금지하지 않고 지식 이관 이후 명시적인 보존 필요를
판단하게 한다. application runtime model, endpoint와 tool contract는 변경하지 않는다.

stable 소비 저장소는 versioned release를 pin하고 repository별 update transaction으로
올린다. signed annotated source와 저장소별 terminal evidence를 검증한다.
현재 publication 상태는 `docs/HANDOFF.md`가 소유한다.

`1.6.0`은 기존 spec·검증·이관 계약을 의도 기반 변경 리뷰로 구체화하는
release다. 의도 정보, 기준 변경 검토와 리뷰 참조의 예시는
`docs/WORK_LIFECYCLE.md`에 있다. 선언/lock schema version 1, harness Structure ID와
기존 native packet 형식을 유지하며 새 parser 필드, 중앙 readiness 명령 또는 PR
사용을 요구하지 않는다. 공통 guidance는 합성 결과에 포함되므로 중앙 문서가 없어도
소비 저장소에서 동작한다. 기존 heading과 출력 역할을 유지하는 범위이며 새 필수
형식을 도입한다면 별도의 compatibility/migration 판단이 필요하다.

출시와 소비 저장소 적용 상태는 `docs/HANDOFF.md`가 소유한다. 지침의 합성·구조
검증을 agent 행동 개선의 실측 evidence로 해석하지 않는다.

소비 저장소의 concise routing gate는 공통 생성 본문과 repository-owned overlay의
소유 경계를 구별할 수 있다. 고정 framework 본문의 무결성은 source/render/standalone
검증으로 확인하고, native routing의 기존 예산은 그대로 보존한다. 전체 문서 크기를
자동으로 제한하던 정책과는 구별하며 source 갱신의 diff review를 생략하지 않는다.

## Optional verification capability

`1.7.0`는 `verification` profile을 선택할 때만 runtime/skill output 세 개를 추가한다.
선언·lock schema 1과 기존 output role은 유지한다. 미선택 소비자는 새 binding을 만들
필요가 없다. 선택한 소비자는 작은 repository-owned argv/coverage binding을 사용하며,
존재하는 binding은 lock의 input이 된다. native manifest/readiness schema는 변경하지 않는다.

공통 interface assertion은 standalone checker가 소유한다. 기존 native script의 중복 pin은
최초 migration에서 한 번 위임하고 제품 검사와 publication 호출을 유지한다. 이후 버전과
profile 변경은 선언/lock/generated output으로 검증한다. collision과 opt-out 보존 규칙,
report contract는 `docs/VERIFICATION.md`가
소유한다. verification은 선택형 보조 기능이다. 기존 native 명령 하나로 충분한 작업에 새 실행 단계를
강제하지 않는다. work-coordination은 실험적 opt-in이며 소비 저장소 갱신 시 자동 선택하지 않는다.

## Optional work coordination

`work-coordination`은 `verification`을 요구하며 `.ai-first/work.py`와 `ai-first-work`
skill/metadata 세 output을 추가한다. runtime은 Python stdlib, Git과 jj를 사용한다.
실제 검증한 jj 버전은 `0.45.1`이다. native Git worktree registration이 필요한 저장소에는
이 clone 방식의 지원을 주장하지 않으며 gate를 생략하지 않는다.

최초 contract는 독립적인 literal path ownership, private state schema 1과 Codex host를
통한 packet 실행이다. 다른 host의 spawn/cancel API 지원, 순서 의존 작업의 scheduler와
자동 cleanup은 포함하지 않는다. 상세 상태와 재개 계약은 `docs/WORK_COORDINATION.md`에 있다.
기존 profile 미선택 소비자는 변경되지 않는다.

## Source identity

`.ai-first.toml`은 framework source를 다음 중 하나로 고정한다.

- `development`: revision 없음. framework 자체 개발과 local experiment 전용.
- `commit`: full lowercase 40-character commit SHA. checkout `HEAD`, clean state와
  일치해야 한다.
- `release`: stable `vMAJOR.MINOR.PATCH` annotated Git tag. tag가 가리키는 commit,
  checkout `HEAD`와 clean state가 모두 일치해야 한다.

lock은 선언된 source revision과 검증된 `source_commit`을 함께 기록한다. release tag
이동이나 다른 checkout에서의 합성은 fail-closed 한다.

standalone checker는 tracked config/input/output과 lock metadata의 내부 정합성을
검증한다. 외부 Git tag·commit의 실제 identity와 서명은 release source checkout과
publication 검증이 소유하며 standalone 결과만으로 재검증됐다고 주장하지 않는다.

## Canonical v1 distribution

v1의 canonical distribution은 public source checkout이다. package registry와
standalone binary는 필수 경로가 아니다.

소비 저장소 update는 기본 working copy 밖의 VCS-isolated checkout에서 수행한다.
framework checkout은 public annotated release tag에 고정하고 소비 선언을 다음처럼
갱신한다.

```toml
schema_version = 1
framework_version = "1.7.0"
source_kind = "release"
source_revision = "v1.7.0"
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

## 추가 capability의 시작 조건

package registry, standalone binary는 반복되는 installation friction이 확인될 때
검토한다. language/toolchain profile은 둘 이상의 독립 소비 근거가 있을 때,
adoption scaffold 확대는 반복되는 수동 overlay 오류가 확인될 때 검토한다.
현재 이 가능성 자체를 active milestone로 취급하지 않는다.

별도 VCS profile, opt-in 종료 hook, optional lifecycle namespace·terminal vocabulary와
native gate 선언 확장도 실제 소비 요구나 반복 실패가 확인되면 범위와 compatibility를
별도 평가한다. 기존 구조를 미리 일반화하거나 종료 hook을 기본 설치하지 않는다.
