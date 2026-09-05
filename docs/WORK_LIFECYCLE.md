# Work lifecycle

## Todo spec의 역할

todo spec은 milestone 또는 bounded specification의 목적, 범위, 조건과 관계를
명시해 논리적 누락·모순·미결정을 해소하는 임시 설계 계약이다. 작성 과정은 설계
검토이며, 정립된 spec은 구현과 완료 판정의 기준이다.

이 저장소의 active 작업은 `docs/todo-*/spec.md`와 `open-questions.md`에 둔다.
목적, 범위와 non-goal, 조건·의존 관계, acceptance와 검증, 중요한 결정 경계를
명시한다. 결과를 바꾸는 질문은 의존 구현 전에 해소한다. 질문 파일은 미결정과
해결 근거를 작업 중 관리하고, 구현에서 발견한 사실은 spec과 함께 갱신한다.
완료 기준의 변경은 이유와 영향을 드러내며 미충족 결과를 숨기는 수단으로 쓰지 않는다.

## Artifact 전환

완료 시 spec의 acceptance와 실제 결과·검증을 대조하고 앞으로 유지할 지식을
그 지식의 소유 문서나 코드에 반영한다.

| 유지할 내용 | 적절한 위치 |
| --- | --- |
| 동작과 회귀 방지 | 구현과 의미 있는 테스트 |
| 사용법과 외부 계약 | README, 사용자/API 문서 |
| 구조, 제약, 결정 이유와 포기한 대안 | architecture 또는 필요한 decision record |
| 운영 조건, 복구 방법과 알려진 한계 | 운영 문서와 runbook |
| 완료 결과와 검증 범위 | 기존 완료 요약이나 변경 이력, 필요한 검증 artifact |
| 미완료 작업과 이후 시작 조건 | 현재 active spec 또는 handoff/status/roadmap |

artifact의 목적은 다음 참여자가 결과를 이해하고 사용하고 변경하는 데 필요한
지식을 보존하는 것이다. 별도 milestone 문서나 완료 보고서를 매번 만들지 않는다.
검증 명령만으로 과거 성공을 주장하지 않으며 수행한 범위·판정·한계를 함께 남긴다.
raw output, transcript와 machine-private evidence는 공개 tracked artifact에 넣지 않는다.

이관과 참조 정합성을 확인한 뒤 역할이 끝난 todo spec과 질문 파일을 제거하고
현재 상태 포인터를 갱신한다. 원래 설계와 작업 과정은 VCS 이력에서 추적할 수 있다.
단순히 completed 폴더로 이동하는 것은 artifact 전환을 대신하지 않는다.
원본 보존은 감사·운영 등 명시적인 필요가 있을 때만 선택하며 보존 이유와 역사적
상태를 표시한다. 원본을 보존해도 현재 계약 문서로의 지식 이관은 수행한다.

## 검증 경계

`scripts/check.sh`는 generated drift, standalone lifecycle, 문서 참조와 harness
interface를 검사한다. standalone checker는 terminal `docs/todo-*/spec.md`를
거부한다. 파일 존재 검사로 지식 이관의 의미적 충분성을 증명할 수는 없으므로,
spec과 결과를 대조하는 완료 검토가 필요하다.

framework는 소비 저장소의 native work-start/finalize 명령과 domain artifact를
보존한다. 기존 completed 기록은 원본 보존 필요와 내용의 소유 위치를 검토한 범위에서
정리하며, 버전 업데이트를 이유로 소비 저장소의 과거 기록을 일괄 삭제하지 않는다.
