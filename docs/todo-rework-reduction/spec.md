# Rework reduction

## 의도와 범위

- 문제: 의도·제약과 누적 리뷰 계약이 있어도 수정된 구현에 맞춰 테스트 기대값을
  정하거나, 교정한 오류가 같은 산출물의 다른 위치에 남을 수 있다.
- 원하는 결과: 변경할 결과와 유지할 동작을 원래 요구에서 함께 확인하고, 사용자
  교정을 같은 원인의 관련 위치에 적용한다. 새 선호·범위 변경은 기존 요구 누락과 구분한다.
- 영향: core AGENTS/harness의 소비자 전달 경로와 work lifecycle의 리뷰 기준.
- 제약: 기존 native 검증·권한·문서량 비례 원칙을 유지한다. 고정 리뷰 횟수, 새 장부,
  새 skill/runtime/schema와 소비자별 필수 필드를 추가하지 않는다.
- Non-goal: 소비 저장소·전역/머신 로컬 skill 수정, 출고·일괄 adoption과 효과 실측.

## 기존 계약과 결정

기존 Change review와 Verification, `docs/WORK_LIFECYCLE.md`를 소유 위치로 사용한다.
회귀 기대값과 교정 적용 범위를 기존 문장에 구체화하고 별도 절차를 만들지 않는다.
기존 검증 skill은 실행 결과·coverage를 소유하므로 의미 판단 지침을 중복하지 않는다.
경로 탐색과 검증 cadence는 기존 실행 지침이 이미 다루며 새 공통 의무를 만들지 않는다.
단일 명령 오류를 framework-wide 운영 절차로 일반화하지 않는다.

## Acceptance와 검증

1. 두 generated entrypoint에 원래 요구에서 도출한 테스트 기대값과 유지할 동작의
   확인 기준이 전달된다. 구현·테스트가 서로 일치한다는 사실만으로 충족을 주장하지 않는다.
2. 교정은 해당 산출물·기능 안의 같은 원인에 적용하며 무관한 전수 조사로 넓히지 않는다.
   사용자가 확정한 사실·의미·범위를 보존하고 새 선호·요구와 기존 누락을 구분한다.
3. 기존 조항과 scenario를 갱신하고 새 파일·장부·검사 횟수를 소비자에게 요구하지 않는다.
4. 기존 native gate, generated/standalone 정합성과 실제 render의 전달 검증을 통과한다.
   이는 지침 전달 검증이며 실제 agent의 재작업 감소를 입증하는 행동 평가가 아니다.
5. 완료 지식은 lifecycle과 completed summary에 이관하고 packet과 active pointer를 정리한다.

## 결정 경계

공개 가능한 일반 계약만 기록한다. 개인 작업 원문·대상 식별자·inventory는 보존하지 않는다.
local logical change로 닫으며 release, push와 소비 adoption은 별도 권한 범위다.
