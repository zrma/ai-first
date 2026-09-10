# Operational workflows

상태: 진행 중

## 문제와 원하는 결과

공통 계약만 읽게 하는 skill은 이미 충분한 지침을 가진 agent에게 추가 이익이 없을 수
있다. 이전 trial에서는 framework version/source/profile이 native 검사 코드에도 복제되어
매번 수동 갱신이 필요했다. 갱신의 중복 수정 지점을 없애고, 여러 agent가 독립 변경을
실제로 나누어 수행하고 검증된 결과를 통합하는 공통 실행 기능을 제공한다.

## 범위와 소유권

1. 기존 standalone checker에 공통 interface 검증을 완결한다. 소비 저장소는 공통
   version·source·profile·heading assertion을 복제하지 않고 해당 checker를 호출한다.
   제품 고유 invariant, native gate, publication과 외부 source 검증은 유지한다.
2. 선택형 work coordination CLI가 작업 기준·수정 소유 범위·격리 workspace를 준비하고,
   revision과 검증을 포함한 인계를 검증한 뒤 통합 workspace에서 최종 검증을 실행한다.
   실제 작업·결과는 repository 밖의 private state로 보존한다. native spec을 대체하지 않는다.
3. 최초 지원 범위는 jj 기반 독립 작업이다. 같은 경로의 동시 소유는 거부하고 통합은
   별도 workspace에서 수행한다. 원본 working copy와 publication bookmark는 이동하지 않는다.
   중단된 agent의 workspace를 보존하고 상태 조회 및 재개 인계가 가능해야 한다.
4. agent 실행환경은 공통 작업 packet과 CLI를 소비한다. 이번에는 사용 가능한 Codex
   collaboration으로 실제 실행을 검증하며, 다른 vendor의 실행 지원이나 일반 DAG
   scheduler, 자동 publish·history rewrite·workspace 삭제를 구현했다고 주장하지 않는다.
5. 기존 verify skill은 일반 판단 지침의 반복을 줄이고 실제 command/결과 처리에 집중한다.

## 완료 기준

- 두 기존 consumer에서 한 번 공통 검사를 연결한 뒤 다음 version/profile 갱신 때 native
  검사 파일 수정이 0회다. 기존 제품 검사와 실패 탐지력은 보존한다.
- 정상 interface와 잘못된 header/profile/output role/source metadata의 회귀 검증을 통과한다.
- 실제 workspace 생성·소유 범위 위반·오래된 기준·불완전 인계·통합 실패·재개 상태를
  검증한다. individual PASS를 통합 PASS로 승격하지 않는다.
- 중앙 checkout 없이 generated coordination 도구가 동작한다.
- 같은 실제 파일 수정 과제를 기존 단일 agent, workflow 단일 agent, workflow 다중 agent로
  수행한다. 모델·자료·총 도구 예산을 맞추고 결과 품질·개입·통합 실패·벽시계 시간과
  관측 가능한 비용을 비교한다. 작은 표본과 미측정 비용을 밝힌다.
- 결과와 원래 acceptance를 대조해 owning artifact로 이관하고 canonical local gate,
  public artifact gate와 logical jj closeout까지 완료한다. release와 portfolio 적용은 제외한다.
