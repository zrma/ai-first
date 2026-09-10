# v1.7.0 release and proportional adoption

상태: 진행 중

## 문제와 결과

공통 framework assertion의 복제로 소비 저장소의 버전 갱신마다 native 코드를 반복 수정한다.
검증된 공통 checker를 기본 배포하되 추가 runtime을 일괄 활성화하지 않아 운영 비용을 제한한다.
framework 사용자는 signed release를 pin하고 독립 clone에서 기존 native 검사를 실행할 수 있어야 한다.

## 범위와 제약

- v1.7.0 source를 canonical/publication gate 이후 public main, signed annotated tag와
  GitHub Release로 배포하고 source/remote/tag identity 및 동일 SHA CI를 확인한다.
- 현재 원격에서 framework 선언을 가진 활성 소비 저장소를 VCS-isolated checkout에서
  갱신한다. archived 대상은 제외하고 inventory와 raw evidence는 machine-local로 관리한다.
- version/source pin과 generated output을 갱신하고 중복 공통 assertion을 standalone 호출로
  한 번 위임한다. native 제품 invariant, publication 호출, schema, overlay, active work와
  원본 working copy 및 고유 history를 보존한다.
- verification은 선택형 보조 기능, work-coordination은 실험적 opt-in으로 배포한다.
  소비 저장소의 기존 profile 선택을 보존하며 새 binding/runtime을 일괄 추가하지 않는다.
- 소비 저장소별 native gate와 publication gate 이후 default branch에 반영하고 동일 SHA CI를
  확인한다. 제품 기능, 모델 변경, 앱 버전/tag/release와 live runtime 배포는 범위 밖이다.

## 완료 기준

- framework v1.7.0 signed tag/source/remote/release identity와 canonical 및 terminal CI 성공.
- 각 적용 대상의 immutable source pin, standalone/interface/native 검증, remote equality와
  terminal 동일 SHA CI 성공. CI가 없는 대상은 그 사실과 대체 evidence를 구분한다.
- optional profile이 자동 활성화되지 않고 native 제품 검사·overlay·기존 작업이 보존됨을 확인.
- 처음 정리한 native checker의 반복 pin과 stale pointer가 남지 않으며 완료 지식을 owning
  artifact로 이관한다. 결과와 한계, 다음 trigger를 정리하고 clean logical jj closeout으로 닫는다.
