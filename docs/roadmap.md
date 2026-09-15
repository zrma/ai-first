# Roadmap

현재 작업은 `docs/status.md`, 재개 지점과 publication 상태는 `docs/HANDOFF.md`가
소유한다. 완료된 Stage 0–15와 후속 release/adoption의 결과·검증 한계는
`docs/completed-milestones.md`에서 확인한다.

## 다음 작업을 시작할 조건

| 후보 | 시작 조건 | 범위를 정할 때 유지할 경계 |
| --- | --- | --- |
| 추가 versioned language/toolchain profile catalog | 둘 이상의 독립 소비 근거 | core는 model/vendor 중립적으로 유지하고 repository 고유 계약은 overlay에 둔다. |
| verification 도입 확대 | 반복 업무의 수작업·재작업 감소 또는 명시적 요구 | 선택형 보조 기능을 유지하고 native 검사와 제품 acceptance를 대체하지 않는다. |
| work-coordination 확대 | 추가 호출 비용을 상쇄하는 반복 운영 효용 또는 명시적 요구 | 실험적 opt-in을 유지하고 타 vendor adapter·일반 orchestration은 별도 범위로 판단한다. |
| startup/review 지침 조정 | 실제 작업에서 필수 근거 누락·불필요한 탐색·기록 부담의 반복 | 지침 배포 성공과 실제 행동 개선을 구별한다. |
| 배포·adoption 도구 확장 | 반복 installation friction 또는 수동 overlay 오류 | 독립 실행, version pin과 repository-native gate를 보존한다. |

추가 capability의 상세 조건과 compatibility 경계는 `docs/COMPATIBILITY.md`가 소유한다.
후보의 존재만으로 active milestone을 열거나 소비 저장소에 기능을 일괄 도입하지 않는다.

## 판단에 남아 있는 한계

verification의 행동 보고 평가에서는 baseline 대비 개선을 관측하지 못했다.
work-coordination은 반복 native 수정 제거와 실제 배정·인계·통합을 확인했지만,
일반 속도·비용·품질 우위는 입증하지 못했다. startup routing의 token·시간 절감과
누적 리뷰 지침의 실제 누락 감소도 미측정이다. 평가 방법과 수치는
`docs/completed-milestones.md`에 유지한다.
