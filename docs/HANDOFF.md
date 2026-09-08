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

현재 active milestone은 없다. `v1.6.0` source와 signed annotated tag, GitHub Release,
승인된 활성 소비 저장소의 release pin·native gate·원격 반영·동일 SHA의 terminal CI를
확인했다. 기존 제품 작업과 고유 이력을 보존했다.

완료 결과와 다음 capability의 시작 조건은 `docs/completed-milestones.md`와
`docs/COMPATIBILITY.md`, spec 정립과 지식 이관은 `docs/WORK_LIFECYCLE.md`가 소유한다.
대상별 inventory와 검증 원문은 machine-local 계층에서 관리한다.

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
