# Handoff

## 현재 단계

`ai-first`는 Stage 0부터 Stage 15까지의 구현·평가와 비례적 release/adoption을 완료했다.
현재 published stable은 `v1.7.0`이다. signed release source와 원격 tag identity, GitHub
Release 및 Python 3.11/3.14 CI를 확인했다.

self-hosting 선언, model/vendor 중립적 core, capability profile, repository overlay,
deterministic render, content-addressed lock, central drift check와 standalone checker가
동작한다. 소비 저장소는 중앙 checkout 없이 generated artifact와 공통 interface를 검사한다.

## 현재 milestone

현재 작업은 `docs/todo-startup-routing-release/spec.md`의 `v1.7.1` 패치 출고다.
공통 interface assertion을 standalone checker에 위임하고 활성
소비 저장소의 release pin과 native 검사를 갱신했다. 기존 profile·overlay·진행 중 작업과
원본 working copy를 보존했으며 저장소별 native/publication gate, remote equality와
동일 SHA terminal CI를 확인했다.

`verification`은 선택형 보조 기능이고 `work-coordination`은 실험적 opt-in이다. 소비
저장소에 새 binding/runtime을 일괄 추가하지 않았다. self-hosting은 verification만 선택한다.
`docs/VERIFICATION.md`와 `docs/WORK_COORDINATION.md`가 사용법·지원 경계를,
`docs/completed-milestones.md`가 평가·출고 결과와 한계를 소유한다.

두 격리 소비 clone에서 최초 위임 후 다음 version/profile 갱신의 native 검사 파일 수정
0회를 확인했다. 같은 실제 편집 과제의 세 arm은 모두 고정 acceptance 8개를 통과했지만
일반적인 속도·비용·품질 우위는 입증하지 못했다. 다음 확대는 반복 업무의 실측 효용 또는
명시적 요구를 기준으로 정한다. 타 vendor adapter와 일반 orchestration platform은 미지원이다.
대상별 inventory와 평가·출고 원문은 machine-local 계층에서 관리한다.

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

이 안내는 요청 범위에 비례하는 기존 계약과 시작 절차를 맞춘다. 실제 작업의 문서 읽기,
token·시간 절감 효과는 미측정이며, 필수 근거·검증 누락과 불필요한 탐색이 반복되면
해당 탐색 경로를 조정한다.

## 현재 검증

`scripts/check.sh`는 central/standalone drift, harness interface, repository publication
boundary, navigation, CI contract, Python syntax와 61개 회귀 테스트를 검사한다. 실제 jj clone
통합을 포함하며 CI는 pinned jj 설치와 부재 시 실패를 요구한다. release source의
Python 3.11/3.14 CI가 통과했다.

## Publication 상태

- tracked content class: `public`
- remote: `v1.7.0` release와 adoption 완료를 public `main`에 반영
- license: `Apache-2.0`
- CI: release source의 Python 3.11/3.14 success; 소비 저장소의 동일 SHA CI verified
- stable release: signed annotated `v1.7.0`, 서명·remote tag/source equality와 GitHub Release verified
- private vulnerability reporting: enabled

## 보호 경계

- 다른 저장소의 local path, 이름별 migration 상태, WIP와 private inventory를 이
  공개 저장소에 기록하지 않는다.
- 다른 저장소 adoption은 기본 working copy 밖의 VCS-isolated migration checkout에서
  수행하고 repository-native metadata gate를 그대로 보존한다.
- 소비 저장소의 push는 framework publish와 별개의 permission boundary다.
