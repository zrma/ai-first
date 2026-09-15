# Handoff

## 현재 단계

현재 published stable은 `v1.7.2`다. 고정된 검토 snapshot과 범위, 중요한 요구사항·영향
경로별 근거와 미확인 범위, 누적 finding 상태와 후발 지적의 기원 구분을 core generated
지침으로 전달한다. 상세 계약은 `docs/WORK_LIFECYCLE.md`가 소유한다.

출고 당시 source/tag·Release·CI와 소비 adoption 검증 결과는
`docs/completed-milestones.md`의 v1.7.2 구간에 있다. 이후 local 유지보수 변경의
검증과 published source의 evidence는 구별한다.

## 현재 milestone

문서 탐색과 렌더러 유지보수 정리를 진행한다.
`docs/todo-maintenance-refactor/spec.md`와 `open-questions.md`가 범위·완료 기준을
소유한다. 상태 문서의 중복 이력 정리 후 렌더러 책임 분리와 관련 테스트를 정리한다.
이 작업은 local 유지보수이며 release와 소비 adoption은 포함하지 않는다.

`verification`은 선택형 보조 기능이고 `work-coordination`은 실험적 opt-in이다.
소비 저장소에 새 binding/runtime을 일괄 추가하지 않았다. self-hosting은 verification만
선택한다. `docs/VERIFICATION.md`와 `docs/WORK_COORDINATION.md`가 사용법과 지원 경계를,
`docs/completed-milestones.md`가 평가·출고 결과와 한계를 소유한다.

self-hosting, model/vendor 중립 core, capability profile, repository overlay,
deterministic render, content-addressed lock과 central/standalone checker를 유지한다.
소비 저장소는 중앙 checkout 없이 generated artifact와 공통 interface를 검사한다.
일반 속도·비용·품질 우위는 입증되지 않았다. 다음 확대는 반복 업무의 실측 효용 또는
명시적 요구를 기준으로 판단한다. 타 vendor adapter와 일반 orchestration platform은
미지원이다. 대상별 inventory와 평가·출고 원문은 machine-local 계층에서 관리한다.

## 시작 순서

적용되는 agent 지침과 정체성·권한·공개 경계는 항상 준수한다. 상세 문서는 요청과
관련된 경로부터 읽고, 판단에 필요한 근거가 부족하면 범위를 넓힌다.

1. 설명·조사·리뷰·계획은 질문 대상 문서·코드·설정에서 시작한다. 필요한 재현·검증은
   수행하되 시작 절차만을 이유로 전체 검사를 실행하지 않는다.
2. 작업 재개·변경·다음 과제 선택은 `jj status`, 이 문서의 현재 단계와
   `docs/status.md`, 관련 활성 `docs/todo-*/spec.md`와 `open-questions.md`를 확인한다.
   우선순위·후속 방향을 판단할 때 `docs/roadmap.md`를 읽는다.
3. 정체성·역할은 `docs/AI_FIRST_CHARTER.md`, 구조·합성은 `docs/ARCHITECTURE.md`,
   호환성·도입은 `docs/COMPATIBILITY.md`, spec·변경 리뷰·완료 이관은
   `docs/WORK_LIFECYCLE.md`에서 해당 작업에 필요한 내용을 확인한다.
4. 변경 검증은 `docs/VERIFICATION.md`에 따라 연결된 native gate를 실행한다.
   이 저장소의 필수 local gate는 `scripts/check.sh`다. 공개 기록 작성과 publication은
   `docs/PUBLICATION.md`의 경계를 확인한다.

## 현재 검증

`scripts/check.sh`는 central/standalone drift, harness interface, repository publication
boundary, navigation, CI contract, Python syntax와 61개 회귀 테스트를 검사한다. 실제 jj
clone 통합을 포함하며 CI는 pinned jj 설치와 부재 시 실패를 요구한다. release source의
Python 3.11/3.14 CI가 통과했다. 소비 update의 독립 리뷰에서 generated 전달 경로와
기존 계약 보존을 확인했다. 필수 근거 누락·불필요한 탐색이나 기록 부담이 반복되면 실제
사례를 기준으로 해당 지침을 조정한다.

## Publication 상태

- tracked content class: `public`
- remote: `v1.7.2` release 및 소비 adoption verified
- license: `Apache-2.0`
- CI: release source의 Python 3.11/3.14 success; 소비 저장소 동일 SHA CI verified
- stable release: signed annotated `v1.7.2`, 서명·remote tag/source equality와 GitHub Release verified
- private vulnerability reporting: enabled

## 보호 경계

- 다른 저장소의 local path, 이름별 migration 상태, WIP와 private inventory를 이
  공개 저장소에 기록하지 않는다.
- 다른 저장소 adoption은 기본 working copy 밖의 VCS-isolated migration checkout에서
  수행하고 repository-native metadata gate를 그대로 보존한다.
- 소비 저장소의 push는 framework publish와 별개의 permission boundary다.
