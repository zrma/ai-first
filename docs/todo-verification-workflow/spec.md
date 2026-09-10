# Reusable verification workflow

상태: 진행 중

## 문제와 원하는 결과

계약 문서만 배포하면 소비 저장소마다 검증 절차·실행 wrapper·스킬을 다시 작성해야
한다. 공통 실행과 결과 처리를 framework가 제공하고 native runner는 한 번 연결한다.
새 저장소도 이미 지원하는 toolchain의 실제 명령을 제안받아 사용할 수 있어야 한다.
검증 성공을 사용자의 요청 충족으로 확대 해석하지 않도록 evidence의 범위를 드러낸다.

## 범위와 관계

- 선택형 `verification` profile로 standalone runtime과 repository skill을 versioned
  generated artifact로 배포한다. 기존 선언은 선택하지 않아도 계속 동작한다.
- `verify --plan`, `--run`, `--report`와 discovery/binding으로 실행·상태·freshness를
  공통화한다. native runner 내부의 명령 목록이나 native lifecycle schema는 복제하지 않는다.
- binding은 repository-owned 명령·범위 선언이다. discovery는 후보이며 실행 권한이 아니다.
  새 저장소에는 Python unittest, Cargo, Go 등 실제 실행 가능한 기본 후보를 제공한다.
- runtime은 실패·skip·도구 부재·timeout·검증 도중 source 변경을 구분하고 보고한다.
  report에는 revision, content identity, platform과 declared coverage를 남기되 raw log와
  private environment를 tracked 산출물에 저장하지 않는다.
- 스킬은 사용자의 원래 시나리오와 증거의 대상·방향·실행 경로를 대조하고 미검증을
  밝힌다. 제품 의미와 인간의 acceptance는 소비 저장소가 소유한다.

## 제약과 non-goal

publication, release, 배포, 자동 workspace 정리, 비용 있는 통합 테스트의 자동 실행은
범위 밖이다. universal semantic judge나 또 다른 native manifest 표준을 만들지 않는다.
consumer trial은 기본 working copy 밖에서 수행하고 고유 변경을 보존한다.

## 완료 기준

1. 하나의 runtime source가 중앙 CLI와 독립 clone에서 동작하고 generated drift가 검출된다.
2. 실패·skip·unavailable·timeout·stale evidence 및 malformed binding의 회귀 검증을 통과한다.
3. 이질적인 기존 consumer의 runner를 복제 없이 연결하고 held-out 작은 저장소를 framework
   수정 없이 실행한다. 추가 선언·manual glue·재작업과 관측 가능한 실행 비용을 비교한다.
4. 동일 model/tool/input/budget의 bounded before/after 행동 사례와 정상 반례를 독립 평가한다.
   작은 표본의 한계와 개선이 없었던 결과도 기록하며 효과가 없으면 적용 범위를 확장하지 않는다.
5. canonical local gate와 public artifact gate를 통과하고 결과·판단·한계를 owning docs로
   이관한다. logical jj change와 empty working copy로 닫는다. 외부 publication은 하지 않는다.
