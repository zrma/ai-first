# Handoff

## 현재 단계

현재 published stable은 `v1.8.0`이다. OpenAI agent guidance baseline을
GPT-6.1 Sol (`gpt-6.1-sol`)로 갱신하고 공식 API 제약 및 family prompting 근거의
한계를 반영했다. model/vendor 중립 core, CLI·schema·runtime·optional profile 선택과
소비 저장소 overlay·native lifecycle을 유지한다.
signed source/tag·Release·CI와 활성 소비 adoption 결과는
`docs/completed-milestones.md`의 v1.8.0 구간에 있다.

## 현재 milestone

활성 milestone은 없다. Sol guidance와 pinned adoption의 acceptance를 확인하고
완료 지식을 이관한 뒤 todo packet과 active pointer를 정리했다. release source tag와
이후 완료 문서 commit은 구별한다. 구조와 책임 경계는 `docs/ARCHITECTURE.md`,
결과와 검증 한계는 `docs/completed-milestones.md`, 다음 시작 조건은
`docs/roadmap.md`가 소유한다.

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

연결된 native gate로 central/standalone drift, harness interface, repository publication
boundary, navigation, CI contract, Python syntax와 기존 64개 회귀 테스트를 통과했다.
실제 jj clone 통합도 실행했고 skip은 없었다. 테스트 수를 새 행동 coverage나 Sol의
효과 실측으로 해석하지 않는다.

공개된 signed release source를 새로 clone해 source identity와 native gate를 확인했고,
Python 3.11/3.14 동일 source SHA CI가 성공했다. 활성 소비 저장소는 pin/source identity,
standalone/interface·해당 native gate·publication boundary·remote equality와 동일
SHA terminal CI를 확인했다. 기존 profile·overlay·native 검사·active work와 로컬 이력을
보존했다. native의 선택적·CI 전용 skip은 실제 실행 범위와 구별했다.
application runtime migration과 Sol의 행동·속도·비용 효과는 검증하지 않았다.
필수 근거 누락·불필요한 탐색이나 기록 부담이 반복되면 실제 사례를 기준으로 조정한다.

## Publication 상태

- tracked content class: `public`
- remote: `v1.8.0` release 및 소비 adoption verified
- license: `Apache-2.0`
- CI: release source의 Python 3.11/3.14 success; 소비 저장소 동일 SHA CI verified
- stable release: signed annotated `v1.8.0`, 서명·remote tag/source equality와 GitHub Release verified
- private vulnerability reporting: enabled

## 보호 경계

- 다른 저장소의 local path, 이름별 migration 상태, WIP와 private inventory를 이
  공개 저장소에 기록하지 않는다.
- 다른 저장소 adoption은 기본 working copy 밖의 VCS-isolated migration checkout에서
  수행하고 repository-native metadata gate를 그대로 보존한다.
- 소비 저장소의 push는 framework publish와 별개의 permission boundary다.
