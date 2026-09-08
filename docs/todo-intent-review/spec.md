# Intent-aware change review

상태: 진행 중

## 목적과 의도

현재 todo spec은 설계와 완료 판정의 기준이지만, 유지해야 할 동작과 영향 범위,
spec 자체의 변경, 완료 후 리뷰 근거를 일관되게 확인하는 절차가 구체적이지 않다.
다음 리뷰어가 대화 없이 원래 문제와 변경 결과를 대조할 수 있게 한다.

- 영향: 공통 core와 generated agent guidance, lifecycle 문서, synthetic consumer 검증.
- 제약: model/vendor 중립성, 기존 permission과 native lifecycle, schema version 1과
  harness Structure ID를 유지한다. 작은 변경에 새 packet이나 PR을 강제하지 않는다.
- Non-goal: 별도 intent 파일, 중앙 work-start 명령, 필수 todo schema, 소비 저장소
  수정, 자동 PR/merge, runtime model 변경, release와 publication.

## 범위와 결정

- spec 안에 문제·원하는 결과·영향·제약·non-goal을 구별하는 정보 계약을 설명한다.
- 변경 전 기준과 spec 변경 이유를 diff 및 검증과 함께 리뷰한다.
- PR/local change의 요약과 immutable spec 참조, 최종 지식 소유 문서를 연결한다.
- 문서량과 리뷰 깊이는 위험·복잡성에 비례시키고 native 생성기/gate가 형식을 소유한다.
- 새 필수 parser 항목 없이 기존 계약을 구체화하는 development version으로 준비한다.

## Acceptance와 검증

1. Core와 lifecycle이 다섯 의도 항목, 기준 변경 검토, 미검증 한계를 설명한다.
2. 작은 변경, 복잡한 변경, 제약 완화, spec 제거 후 리뷰를 구체적 예시로 판단할 수 있다.
3. central checkout 없는 synthetic consumer에도 리뷰 계약이 합성되며, 기존 native
   packet 형식과 standalone 검증은 그대로 동작한다.
4. `scripts/check.sh`가 generated drift, standalone, interface, publication, navigation과
   unit fixture를 통과한다. 자연어 리뷰의 실제 성능을 자동 검사 성공으로 주장하지 않는다.
5. 결과·판단 이유·한계는 `docs/WORK_LIFECYCLE.md`, `docs/COMPATIBILITY.md`,
   `docs/completed-milestones.md`에 이관하고 active packet과 포인터를 정리한다.

## 실행 상태

- 완료: 현행 계약·검사와 적용 범위 대조.
- 다음: core/lifecycle 예시 구현, 합성·검증, 기준 대비 리뷰와 지식 이관.
- 검증 증거: 구현 이후 수행한 범위와 판정을 완료 요약에 기록한다.
