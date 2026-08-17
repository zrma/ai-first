# Stable v1.3 Release And Adoption

상태: 완료

## Goal

contract audit hardening의 formatter-compatible patch인 stable `v1.3.1` source를 공개하고
승인된 소비 저장소 집합을 repository-owned overlay와 native lifecycle을 보존한 채
이관한다. `v1.3.0`은 게시됐지만 adoption 전에 generated Markdown의 ordered-list
continuation 호환성 gap이 발견되어 source를 이동하지 않고 patch release로 교정한다.

## In scope

- `1.3.1` self-hosting identity와 canonical central gate
- signed annotated `v1.3.1` tag, remote tag/commit equality와 terminal CI
- 기본 working copy 밖의 VCS-isolated consumer migration
- 저장소별 standalone, native와 publication gate
- 저장소별 default-branch remote equality와 same-SHA terminal CI

## Non-goals

- package registry 또는 GitHub Release 생성
- 소비 저장소의 제품 기능, dependency 또는 보안 전수 조사
- 소비 저장소 이름, 개수, local path, WIP와 진행 원문의 public tracking
- 기존 WIP 정리, history rewrite 또는 deployment mutation

## Acceptance criteria

1. central self-hosting 선언과 generated output이 stable `1.3.1` identity로 drift 없이
   합성된다.
2. canonical/publication gate를 통과한 central commit이 public `main`과 signed
   annotated `v1.3.1` tag에서 동일하게 확인되고 terminal CI가 성공한다.
3. 각 대상은 기본 working copy 밖의 격리 checkout에서 `v1.3.1` release source와
   verified commit을 lock에 기록한다.
4. 각 대상의 standalone, repository-native와 publication gate가 통과한다.
5. 각 대상의 remote default branch가 의도한 migration commit과 같고 same-SHA CI가
   terminal success다.
6. 완료 packet은 `docs/milestones/`로 이동하고 active pointer를 제거한다.

## Completion Evidence

- `1.3.1` self-hosting render, standalone check와 canonical central gate가 통과했다.
- signed annotated `v1.3.1` tag의 local/remote tag object, peeled commit과 서명을
  확인하고 tag target의 Python CI가 terminal success임을 확인했다.
- 이미 게시된 `v1.3.0` tag는 이동하지 않고 formatter-compatible `v1.3.1` source를
  adoption 기준으로 사용했다.
- 승인된 소비 저장소 집합을 VCS-isolated checkout에서 갱신하고 각 대상의 standalone,
  native와 publication gate를 통과시켰다.
- 각 대상의 remote default branch equality와 same-SHA terminal CI를 확인했다.
- package registry와 GitHub Release는 생성하지 않았고, 소비 inventory와 local
  coordination 원문을 tracked artifact에 기록하지 않았다.

## Verification

```sh
scripts/check.sh
python3 .ai-first/check.py
```

소비 저장소에서는 같은 release checkout으로 render/check한 뒤 repository-owned
canonical/publication gate를 추가로 실행했다.

## Completion boundary

central release source, 승인된 대상별 독립 migration과 terminal evidence, central
completed-history closeout을 모두 완료했다. tag target과 이후 closeout commit은 별도
SHA로 유지한다.
