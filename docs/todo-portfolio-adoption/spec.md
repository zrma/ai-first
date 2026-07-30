# Portfolio Adoption

상태: 진행 중

## Goal

승인된 소비 저장소 집합을 stable `v1.0.0` core와 repository-owned overlay 위에
저장소별 독립 change로 순차 정립한다.

## In scope

- 기본 working copy 밖의 VCS-isolated migration checkout
- stable annotated release pin과 verified source commit lock
- 저장소 목적, source of truth, domain invariant와 native lifecycle overlay
- standalone/generated interface와 repository-native canonical gate
- 저장소별 publication boundary, remote identity와 terminal CI

## Non-goals

- 소비 저장소 이름, 개수, local path와 unpublished 상태의 public tracking
- 저장소 제품 기능 변경
- 기존 WIP 정리와 history rewrite
- 여러 저장소를 하나의 atomic push 또는 release로 취급

## Acceptance criteria

1. 각 대상은 기본 working copy와 격리된 checkout에서 독립적으로 도입된다.
2. framework `v1.0.0` release tag와 verified commit이 lock에 기록된다.
3. repository overlay가 기존 identity, native workflow와 validation을 보존한다.
4. standalone check와 repository-native canonical gate가 통과한다.
5. public/internal publication class에 맞는 경계 검사가 통과한다.
6. 승인된 publication 대상은 remote SHA와 terminal CI까지 저장소별로 검증된다.
7. machine-local coordination이 승인된 대상 집합과 진행 상태를 소유한다.

## Verification

framework는 다음 gate로 common contract drift를 확인한다.

```sh
scripts/check.sh
python3 .ai-first/check.py
```

각 소비 저장소에서는 repository-owned canonical/publication gate를 추가로 실행한다.

## Decision boundaries

- 대상 선택, 순서와 machine-local inventory는 공개 framework 밖에서 관리한다.
- repository-specific 규칙의 core 승격은 독립 근거 또는 framework invariant가
  있을 때만 별도 framework change로 수행한다.
- push, release와 deploy는 저장소별 명시적 publication boundary다.
