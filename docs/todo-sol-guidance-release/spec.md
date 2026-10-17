# Sol guidance patch release

상태: 진행 중

## 의도와 범위

공식 문서 재검토에서 보완한 GPT-6.1 Sol API migration 지침을 소비 저장소가
immutable release source로 사용할 수 있게 `v1.8.1` patch로 출고한다. cache TTL/과금,
effort update 호환성, Ultrafast/data residency와 logprobs 제거 안내를 전달한다.

영향은 provider guidance와 framework version/source pin 및 generated artifact다.
core·runtime·schema·profile 선택·overlay·native lifecycle·기존 작업과 이력을 유지한다.
제품 runtime release, live mutation, 새 optional capability 활성화와 Sol 행동 효과
eval은 범위 밖이다. 대상 inventory와 raw evidence는 machine-local 계층에만 둔다.

## 실행과 조건

- source의 self-hosting/fixture version과 generated output을 함께 갱신한다.
- canonical native gate와 repository/private-inventory publication gate를 통과한 source에
  signed annotated `v1.8.1` tag와 GitHub Release를 발행한다.
- 승인된 활성 소비 대상을 current remote default branch 기준으로 격리해 갱신한다.
  원격이 전진하면 기존 이력을 보존하는 새 base에서 다시 합성·검증한다.
- 각 native gate와 source/render/standalone, 보존 입력 및 공개 경계를 확인한 뒤 main을
  반영하고 same-SHA terminal CI와 remote equality를 확인한다.

## Acceptance

- [ ] source/version/generated 정합성과 canonical gate를 확인한다.
- [ ] signed tag·source·Release identity와 source SHA CI를 확인한다.
- [ ] 소비 저장소의 기존 입력·작업을 보존하고 native gate와 remote/same-SHA CI를 확인한다.
- [ ] 결과·결정·한계를 owning artifact로 이관하고 packet과 stale pointer를 제거한다.
