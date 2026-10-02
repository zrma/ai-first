# GPT-6.1 Sol guidance and adoption

상태: 진행 중

## 문제와 원하는 결과

현재 provider profile은 GPT-6 Astra를 baseline으로 사용한다. GPT-6.1 Sol을 명시한
작업에서 생성된 지침이 요청된 model과 현재 공식 migration 계약을 가리키도록
backward-compatible framework `1.8.0`과 활성 소비 저장소의 pinned update를 준비한다.

영향은 OpenAI agent guidance를 선택한 저장소의 bootstrap/harness와 source pin이다.
application runtime model/API/tool handler 변경, 새 optional profile·binding·multi-agent
도입과 행동 개선 eval은 이번 범위 밖이다.

## 조건과 관계

- 공식 [GPT-6 guide](https://developers.openai.com/api/docs/guides/latest-model)와
  [GPT-6.1 Sol model page](https://developers.openai.com/api/docs/models/gpt-6.1-sol)를
  2026-10-02에 확인했다. 명시된 target은 일반 latest metadata보다 우선한다.
- family prompting 지침은 Astra 관측에서 나온 시작점이다. Sol의 행동 실측으로
  표현하지 않고 기존 permission·evidence·scope 계약을 보존한다.
- core, schema/Structure ID, renderer/runtime, optional profile 선택과 repository
  overlay·native lifecycle·기존 작업은 유지한다.
- 관리 대상은 current remote default branch의 선언과 활성 관리 의도 및 archived
  상태로 판단한다. 대상 inventory와 검증 원문은 machine-local에서만 관리한다.
- 소비 변경은 기본 working copy 밖에 격리한다. release 전에는 immutable commit pin으로
  준비하고 승인된 publication 후 release pin을 확정한다.

## Acceptance와 검증

- [ ] baseline·공식 API 제약·family guidance의 근거와 한계가 합성 결과에 포함된다.
- [ ] self-hosting/fixture version, generated drift와 연결된 native gate가 통과한다.
- [ ] 활성 소비 저장소의 source/standalone/interface/native gate 및 기존 overlay·profile·
  active work 보존을 확인한다.
- [ ] 승인된 framework main/signed `v1.8.0` tag와 소비 저장소 publication에서 remote
  identity 및 same-SHA terminal CI를 확인한다.
- [ ] 최종 결과·결정·검증 한계를 owning artifact로 이관하고 packet과 stale pointer를 제거한다.

## 중단과 재개

미확인 target, unrelated WIP 충돌, native gate 실패 또는 미승인 external action이
있으면 해당 의존 단계만 보류한다. 원격 base가 전진하면 기존 prepared change를
덮어쓰거나 history를 rewrite하지 않고 새 base에서 다시 합성·검증한다.
