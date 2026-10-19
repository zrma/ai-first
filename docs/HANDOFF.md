# Handoff

## 현재 단계

현재 published stable은 `v1.9.1`이다. 선택형 `vcs-closeout`이 선형 후보 이력과
명시적 local closeout을 검사한다. `vcs-jj` 지침은 선형 통합, fail-fast publication과
작업 사본 회수 계약을 소유한다. 기존 WIP·고유 history·tag/release를 보존하고 자동
삭제하지 않는다. source와 검증 한계는 `docs/completed-milestones.md`에 있다.

## 현재 milestone

`docs/todo-local-vcs-flow/spec.md`와 `open-questions.md`에 따라 `1.10.0`의
로컬 시작·선형 통합·마감 연결을 구현·검증 중이다. 기존 stable과 release는 보존한다.

`verification`은 선택형 보조 기능이고 `work-coordination`은 실험적 opt-in이다.
self-hosting은 verification과 vcs-closeout을 선택한다. 기존 소비자의 verification과
coordination 선택은 보존하며 native 명령과 제품 acceptance를 유지한다.
`docs/VERIFICATION.md`와 `docs/WORK_COORDINATION.md`가 사용법과 지원 경계를 소유한다.

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

central/standalone drift, harness interface, repository publication boundary, navigation,
CI contract와 87개 테스트를 통과했다. 실제 Git/Jujutsu fixture와 legacy metadata 회귀를
포함하며 signed release를 fresh clone한 검사와 Python 3.11/3.14 동일 source SHA CI가
성공했다. 실제 legacy current workspace closeout도 검증했다.

활성 소비 저장소의 pin/source, standalone/interface, native gate, publication, remote와
동일 SHA terminal CI를 각각 확인했다. 소비 task-owned 사본 회수와 기본 workspace 마감도
검증했다. 기존 WIP·고유 분기·태그·릴리스 파일과 native 선택적 skip 계약을 보존했다. 제품 runtime migration과 실제 agent의 재작업·시간·비용
효과는 검증하지 않았다. 테스트 수를 행동 coverage나 효용 실측으로 해석하지 않는다.

## Publication 상태

- tracked content class: `public`
- remote: `v1.9.1` source release 및 소비 adoption verified
- license: `Apache-2.0`
- CI: release source의 Python 3.11/3.14 success; 소비 저장소 동일 SHA terminal CI success
- stable release: signed annotated `v1.9.1`, 서명·remote tag/source equality와 GitHub Release verified
- private vulnerability reporting: enabled

## 보호 경계

- 다른 저장소의 local path, 이름별 migration 상태, WIP와 private inventory를 이
  공개 저장소에 기록하지 않는다.
- 다른 저장소 adoption은 기본 working copy 밖의 VCS-isolated migration checkout에서
  수행하고 repository-native metadata gate를 그대로 보존한다.
- 소비 저장소의 push는 framework publish와 별개의 permission boundary다.
