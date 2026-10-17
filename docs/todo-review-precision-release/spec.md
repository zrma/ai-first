# Review precision release

## 목적과 범위

published `v1.8.1`의 Sol 지침 보완과 local 리뷰 정밀화 변경을 `v1.8.2`로 통합한다.
원래 요구·계약에 따른 테스트 기대값과 유지할 동작 검증, 같은 원인에 대한 교정 적용
범위를 기존 조항에서 전달한다. 명시된 사실·의미·범위를 보존하고 새 요구와 기존 누락을
구분한다. 기존 변경의 의도와 검증 한계를 최종 diff에서 다시 대조한다.

## 제약과 Non-goal

model/vendor 중립 core와 Sol baseline을 유지한다. schema/Structure ID·runtime·CLI,
기존 profile·overlay·native lifecycle과 active work·local 이력을 보존한다. 새 skill,
고정 장부·필드·리뷰 횟수나 검증 단계를 추가하지 않는다. application runtime model/API
변경과 별도 제품 release·live mutation, 행동·속도·비용 효과 평가는 포함하지 않는다.

## Acceptance와 검증

1. current remote main의 Sol 보완과 local 리뷰 변경이 통합 diff에서 누락되지 않는다.
   두 generated entrypoint의 전달과 native gate의 기존 64개 회귀·실제 jj 통합을 확인한다.
2. source/fixture version과 generated lock을 정합하게 갱신하고 최종 snapshot을 검토한다.
   같은 원인·새 범위·검증 한계를 구분하며 중대한 미해결 finding이 있으면 출고하지 않는다.
3. repository 및 machine-local publication gate 후 signed annotated tag·GitHub Release,
   source/tag identity와 동일 SHA terminal CI를 확인한다. source와 완료 문서 main을 구분한다.
4. current remote 선언과 live archive 상태에서 활성 소비 대상을 확정한다. 격리 checkout에서
   release pin과 generated artifact를 갱신하고 source/standalone/interface·native·publication
   검사, remote equality와 동일 SHA terminal CI로 닫는다. native 내부 skip은 그대로 밝힌다.
5. 기존 WIP·고유 이력과 active work를 보존한다. 원본 작업 사본은 당시 상태가 그대로이고
   clean/empty이며 published target의 조상인 경우에만 새 empty change로 정렬한다.
6. 완료 지식은 owning artifact에 이관하고 이 packet과 stale pointer를 정리한다.
   대상별 inventory와 raw evidence는 repository 밖에서 보존한다.

## 결정 경계

승인 범위는 framework 출고와 활성 소비 pin/adoption이다. 제품 배포·추가 capability와
비가역 history rewrite는 별도다. 지침 전달 성공을 실제 재작업 감소로 주장하지 않는다.
