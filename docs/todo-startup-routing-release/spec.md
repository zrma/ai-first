# Startup routing patch release

## Status

Active

## 문제와 원하는 결과

요청별 초기 탐색 안내를 정리한 local 변경을 stable release와 소비 저장소의 pinned
generated artifact에 반영한다. 설명·조사에 불필요한 전체 읽기·검사를 요구하는 해석을
줄이면서 변경 작업의 필수 검증과 권한·공개 경계를 유지한다.

## 범위와 제약

- `v1.7.1` 패치 release의 version, fixture, source identity와 문서를 정합화한다.
- 기존 schema, profile 선택, runtime, native gate와 제품 동작을 유지한다.
- 활성 소비 저장소를 현재 원격 기본 브랜치에서 격리 갱신하고 기존 overlay·active work와
  원본 working copy를 보존한다. 요청별 탐색 안내와 직접 충돌하는 overlay만 최소 조정한다.
- 공개 source, signed annotated tag와 GitHub Release를 검증하고 소비 저장소의
  source pin, standalone/native gate, remote equality와 동일 SHA CI를 확인한다.

## Non-goal

새 evaluation·session 관리·hook·위임 정책, profile 자동 선택과 제품 release/deployment를
추가하지 않는다. 문서 정합성이나 gate 통과를 실제 token·시간 절감의 증거로 해석하지 않는다.

## Acceptance

1. `v1.7.1` source가 central/standalone, interface, publication, navigation과 기존
   회귀 검증을 통과한다. schema와 runtime 계약은 유지된다.
2. 공개 기본 브랜치, signed tag의 object/target, GitHub Release와 source CI가 일치한다.
3. 소비 저장소의 현재 원격 상태를 기준으로 source pin과 생성 결과를 갱신하며, 관련 없는
   변경·profile·active work·원본 working copy를 보존한다.
4. 각 소비 저장소의 native/publication gate, 원격 revision과 동일 SHA terminal CI가
   통과한다. 미실행 제품·live 시나리오와 성능 미측정은 별도로 명시한다.
5. 출고 후 결과·판단 근거·한계를 `docs/completed-milestones.md`에 이관하고 stable 상태와
   후속 trigger를 handoff/status에 반영한 뒤 이 packet과 active pointer를 정리한다.

## 관계와 검증

초기 탐색 계약은 `framework/core/AGENTS.md`, `framework/core/agent-harness.md`와
repository overlay가, 실행 범위는 `docs/HANDOFF.md`가 소유한다. 출고·소비 계약은
`docs/COMPATIBILITY.md`, 공개 경계는 `docs/PUBLICATION.md`, native 검증은
`docs/VERIFICATION.md`를 따른다. 대상별 inventory와 raw evidence는 machine-local에 둔다.
