# Renderer maintenance patch release and adoption

상태: 진행 중

## 목적과 범위

local로 검증한 문서·렌더러·테스트 정리를 immutable `v1.7.3` patch로 배포하고
현재 활성 소비 저장소가 같은 signed source를 사용하도록 갱신한다.
framework main push, signed annotated tag, GitHub Release, 활성 소비 저장소의
기본 브랜치 pin/generated 갱신과 각 동일 SHA CI까지 완료한다.

## 제약과 영향

CLI·schema·Structure ID·core/profile 운영 계약·optional 선택·native 제품 검사를
보존한다. version 표기와 source digest 외의 generated 내용을 바꾸지 않는다.
archived 소비 저장소는 제외하고 현재 원격 기본 브랜치를 기준으로 격리 checkout을
사용한다. 원본 working copy의 WIP와 고유 이력을 보존한다. remote가 앞서면 덮어쓰지
않고 현재 base에서 다시 적용·검증한다. 소비 inventory와 원문 evidence는 machine-local
계층에서 관리한다. 제품 runtime rollout, 기능 확대와 기존 history rewrite는 범위 밖이다.

## 완료 조건

- 현재 release 목록에서 중복 tag가 없는 patch version을 사용한다.
- framework native gate, repository/machine-local publication gate와 attribution을 확인한다.
- signed source tag의 서명·원격 tag object/target·GitHub Release와 source의 Python
  3.11/3.14 terminal CI를 확인한다. 공개 source를 새 checkout에서 검증한다.
- 활성 소비 저장소의 pin/source_commit·standalone/interface·native/publication gate,
  원격 기본 브랜치 equality와 동일 SHA terminal CI를 확인한다.
- native lifecycle이 요구하는 시작·종료를 이행하고 기존 profile·overlay·active work를
  보존한다. 실패·skip·미검증은 성공에 합산하지 않는다.
- 출고·adoption 결과와 한계를 완료 요약에 이관하고 handoff/status의 publication 상태,
  active packet과 pointer를 정리한다. source tag와 이후 문서 closeout commit을 구별한다.
