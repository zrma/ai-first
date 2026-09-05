# GPT-6 Astra guidance and adoption

상태: 진행 중

## 목적과 범위

`openai-agent-guidance` baseline을 GPT-6 Astra (`gpt-6-astra`)로 갱신하고
backward-compatible framework `1.4.0`과 활성 소비 저장소의 pinned adoption을 준비한다.
core는 model/vendor 중립성을 유지하며 schema와 harness Structure ID는 변경하지 않는다.

## 근거와 결정

- 공식 [Using GPT-6 Astra](https://developers.openai.com/api/docs/guides/latest-model)의
  prompting/migration 지침을 2026-09-05에 확인했다.
- 기존 persistence, permission continuity와 scope proportionality는 core가 소유한다.
  profile에는 승인 질문, skill 해석, 설명·검증 범위의 Astra calibration만 보강한다.
- 명시된 model과 workload 역할을 보존한다. application runtime/API migration,
  새 tool capability와 multi-agent 운영 도입은 이번 adoption에 포함하지 않는다.
- 관리 대상은 GitHub에서 아카이브되지 않고 원격 기본 브랜치에서 AI-first 선언과
  활성 관리 의도가 확인된 저장소다. active milestone 부재만으로 제외하지 않는다.
- 소비 저장소의 이름별 inventory, workspace, revision과 검증 원문은 machine-local
  계층에서만 관리한다. 기본 working copy와 기존 작업은 보존한다.

## Acceptance

- [x] profile source, self-hosting output, version fixture와 interface gate가 일치한다.
- [x] `scripts/check.sh`와 repository publication gate가 통과한다.
- [x] 활성 소비 저장소의 standalone/native gate 및 overlay 보존을 확인한다.
- [ ] 승인된 framework publication에서 remote commit, signed annotated `v1.4.0`과
  same-SHA terminal CI를 확인한다.
- [ ] 소비 저장소 release pin과 독립 publication, remote equality, same-SHA CI를 확인한다.
- [ ] terminal packet을 completed history로 이동하고 current pointer를 정리한다.

## 실행 순서와 중단 조건

1. profile과 self-hosting 변경을 canonical gate로 검증하고 logical local change로 닫는다.
2. immutable source commit으로 소비 저장소 변경을 격리 준비하고 native gate를 확인한다.
3. local 검증이 끝나면 exact publication action과 대상에 대한 권한을 확인한다.
4. framework release 후 소비 저장소 release pin을 확정하고 변경된 pin/lock을 재검증한다.
5. 저장소별 publication과 terminal evidence를 독립적으로 닫는다.

미확인 관리 대상, unrelated WIP 충돌, native gate 실패 또는 미승인 external action이
있으면 해당 저장소의 다음 의존 단계만 보류하고 원인과 재개 조건을 남긴다.

## 현재 evidence

- central/standalone drift, harness interface, publication/navigation/CI contract와
  unit fixture 21개가 local에서 통과했다. 이는 model 행동의 실측 평가나
  remote publication 완료를 의미하지 않는다.
- 소비 저장소의 short routing-map gate에서 profile 길이 초과를 확인해 상세
  calibration은 harness에 유지하고 bootstrap profile을 기존 크기로 축약했다.
- 대상별 native gate와 최종 source pin의 standalone/interface 검증이 통과했다.
  bootstrap 축약 후에는 변경된 generated 표면의 길이·formatter 호환성을 재확인했다.
- 공개 대상의 repository gate와 machine-local private-inventory gate가 통과했다.
- publication 직전 원격 기본 브랜치가 전진하면 기존 prepared change를 덮어쓰거나
  history를 rewrite하지 않고 새 base에서 변경을 재합성·검증한다.
