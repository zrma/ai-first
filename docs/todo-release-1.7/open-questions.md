# Open questions

blocking question은 없다.

- version은 additive profile과 공통 검증 개선을 포함한 minor v1.7.0이다.
- 효과가 확인된 공통 checker 위임만 소비 저장소에 기본 적용한다. optional profile은 기존
  선택을 보존하며 타 vendor adapter나 새로운 조정 기능을 추가하지 않는다.
- framework source checkout의 verification profile은 자체 canonical 결과 처리에 사용한다.
  work-coordination은 self-hosting 기본 선택에서도 제외하고 distribution fixture로 검증한다.
