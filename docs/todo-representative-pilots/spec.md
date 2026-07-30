# Representative Pilots

상태: 진행 중

## Goal

서로 다른 개발·운영·위험 특성을 가진 대표 소비 저장소에서 AI-first core와
repository-owned overlay가 실제 작업 흐름을 보존하며 동작하는지 검증한다.

## In scope

- 각 소비 저장소의 기본 working copy와 분리된 `jj workspace`
- framework version, immutable source revision과 input digest를 고정한 tracked lock
- 저장소 목적, source of truth, domain invariant와 native gate를 보존하는 overlay
- central framework checkout 없이 동작하는 generated artifact와 standalone check
- 도입 전후 repository-native gate 및 clean migration change
- pilot evidence로 확인된 common contract와 profile의 최소 고도화

## Non-goals

- 소비 저장소 inventory나 machine-local workspace path의 공개 추적
- pilot 저장소의 제품 기능 변경
- 소비 저장소의 기존 WIP 정리 또는 history rewrite
- stable v1 tag, package registry 배포 또는 전체 portfolio adoption

## Acceptance criteria

1. 모든 pilot은 기본 working copy를 건드리지 않는 dedicated workspace에서 수행한다.
2. 기존 project identity와 repository-native instructions가 overlay로 보존된다.
3. generated artifact는 framework version/digest를 pin하고 standalone check를 통과한다.
4. 각 저장소의 canonical native gate가 도입 후에도 통과한다.
5. framework에 환류한 변경은 synthetic regression과 self-hosting gate로 검증한다.
6. pilot별 publication은 framework publication과 분리된 explicit boundary로 취급한다.

## Verification

```sh
scripts/check.sh
python3 .ai-first/check.py
```

소비 저장소에서는 해당 저장소가 선언한 canonical native gate를 추가로 실행한다.
구체적인 대상 identity, workspace path와 unpublished 상태는 machine-local 계층에서만
관리한다.

## Decision boundaries

- pilot 선택과 순서는 machine-local coordination이 소유한다.
- repository-specific 규칙을 common core로 승격하려면 둘 이상의 독립 근거 또는
  명시적인 framework invariant가 필요하다.
- 소비 저장소 push, release와 deploy는 저장소별 별도 publication boundary다.
