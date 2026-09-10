# Handoff

## 현재 단계

`ai-first`는 self-hosting core부터 GPT-6 Astra guidance와 활성 소비 저장소
adoption, spec-to-artifact lifecycle과 의도 기반 변경 리뷰까지 Stage 0부터 Stage 12를
완료했다. 현재 published stable은 `v1.6.0`이다.

self-hosting 선언, model/vendor 중립적 core, capability profile, repository overlay,
deterministic render, content-addressed lock, central drift check와 standalone checker가
동작한다. synthetic consumer fixture는 central checkout 없이 generated input/output
drift와 lock metadata 정합성을 검증한다.

## 현재 milestone

현재 active milestone은 `docs/todo-operational-workflows/spec.md`의 공통 갱신 검사와
작업 배정·인계·통합 기능이다. `1.7.0-dev`의 선택형 verification runtime·skill을
local candidate로 구현·검증했다. `docs/VERIFICATION.md`가 사용법을,
`docs/completed-milestones.md`가 소비자 연결 비용·행동 평가·한계를 소유한다.
기존 stable release는 `v1.6.0`이며 새 candidate는 공개하거나 기본 소비 저장소에
도입하지 않았다.

공통 실행 코드의 재사용은 확인했으나 기존 직접 실행보다 수작업이 감소했거나 행동
판단이 개선됐다는 근거는 아직 없다. 반복 업무에서 절감 효과가 확인되거나 명시적
추가 요구가 생길 때 다음 범위를 정한다. 대상별 inventory와 평가 원문은 machine-local
계층에서 관리한다.

## 시작 순서

1. `jj status`
2. `docs/AI_FIRST_CHARTER.md`
3. `docs/ARCHITECTURE.md`
4. `docs/COMPATIBILITY.md`
5. `docs/status.md`
6. task-relevant active `docs/todo-*/spec.md`와 `open-questions.md`가 있으면 해당 문서
7. `scripts/check.sh`

## 현재 검증

`scripts/check.sh`가 central/standalone drift, harness interface, repository publication
boundary, navigation, Python syntax와 unit fixture를 검사한다.

## Publication 상태

아래는 기존 `v1.6.0` publication 상태다. `1.7.0-dev`는 local-only다.

- tracked content class: `public`
- remote: `v1.6.0` release와 adoption 완료를 public `main`에 반영
- license: `Apache-2.0`
- CI: `v1.6.0` source의 Python 3.11/3.14 success; 소비 저장소의 동일 SHA CI verified
- stable release: signed annotated `v1.6.0`, 서명·remote tag/source equality와 GitHub Release verified
- private vulnerability reporting: enabled

## 보호 경계

- 다른 저장소의 local path, 이름별 migration 상태, WIP와 private inventory를 이
  공개 저장소에 기록하지 않는다.
- 다른 저장소 adoption은 기본 working copy 밖의 VCS-isolated migration checkout에서
  수행하고 repository-native metadata gate를 그대로 보존한다.
- 소비 저장소의 push는 framework publish와 별개의 permission boundary다.
