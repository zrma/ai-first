# VCS integration and closeout

`1.9.1`의 선택형 `vcs-closeout`은 `vcs-jj`와 함께 선형 history와 로컬 작업 마감을
검사한다. 검사는 runtime/model, 제품 native gate나 GitHub administration을 대체하지
않는다. 미선택 소비자에게 runtime이나 검사를 추가하지 않는다.

## Installation

profiles에 `vcs-closeout`을 추가하고 pin한 framework source로 render한다. 기존 schema 1과
Structure ID는 유지하며 `.ai-first/vcs.py` 하나를 lock의 generated output으로 관리한다.
별도 Python package나 중앙 checkout은 실행 의존성이 아니다. Python 3.11+, Git 또는
jj metadata가 필요하다. closeout은 jj workspace를 요구한다.

```sh
python3 .ai-first/check.py
python3 .ai-first/vcs.py --revision <candidate-revision>
python3 .ai-first/vcs.py --closeout
```

standalone check는 lock·output 검증 뒤 history 검사만 수행한다. 로컬 closeout은 정상
개발 중 WIP를 거부하는 전체 gate로 넣지 않고 작업 종료 때 별도로 실행한다.

## Linear history and existing releases

기본 bookmark는 `main`이며 `[vcs].bookmark`로 바꿀 수 있다. 선언이 없으면 모든 조상에서
merge commit을 거부한다. 과거 병합을 보존해야 하면 `[vcs].linear_history_base`에
해당 저장소의 도입 전 commit ID를 고정한다. full lowercase 40-character ID여야 하며
후보의 조상이어야 한다. 기준점을 포함한 과거 이력은 보존하고 그 이후 새 merge만 거부한다.
검사 통과를 위해 매번 기준점을 앞으로 옮기지 않는다. 다른 저장소 revision을 사용하지 않는다.

`--base <ancestor>`는 명시적인 일회 검사에 사용한다. shallow history나 없는 ref는
검증 실패다. 기존 tag/release, unique history와 작업 사본을 선형화하려고 재작성하지
않는다. stale push는 최신 remote 확인과 미출고 변경의 선형 재적용으로 처리하고,
실패 원인이 해결되기 전 후속 tag/release mutation을 진행하지 않는다.

GitHub CI는 full history를 checkout하고 standalone checker에 실제 후보를 전달한다.

```yaml
env:
  AI_FIRST_VCS_REVISION: ${{ github.event.pull_request.head.sha || github.sha }}
# actions/checkout step의 with:
#   fetch-depth: 0
```

이 변수는 standalone checker의 CI binding이다. 직접 runtime을 호출할 때는
`--revision`을 사용한다. synthetic PR merge 자체를 후보로 판단하지 않는다.
다른 CI도 실제 candidate ID를 전달할 수 있다. server-side merge 차단은 repository
별도의 branch rule과 권한 경계이며 이 local/CI 검사만으로 server enforcement를 주장하지 않는다.

## Local closeout

정상 작업 마감은 기본 workspace에서 empty working copy와 expected parent를 확인한다.
출고 후에는 기본 bookmark를 사용하고 local-only 완료는 `--revision <completed-revision>`을
지정한다. native finalize는 기본 bookmark를 암묵적으로 이동하지 않고 검증된 change를
설명한 뒤 새 empty working copy를 만들어야 한다.

새 workspace/worktree/별도 clone을 만들 때 task-local 목록에 기록하고 task 종료 때
각각 unique work 보존·등록 해제·실제 경로 회수를 확인한다. 기록과 복구 정보는 tracked
문서에 넣지 않는다. jj 버전에 따라 forget이 Git worktree 등록도 회수하므로 각 inventory를
재조회한다. 확인된 task-owned 사본만 회수 가능한 방법으로 정리한다.

```sh
python3 .ai-first/vcs.py --closeout --retired-path "<retired-task-copy>"
python3 .ai-first/vcs.py --closeout --keep-workspace active-work
python3 .ai-first/vcs.py --closeout --inherited-working-copy <pre-task-full-commit-id>
```

기존 WIP/고유 분기는 시작 전에 기록한 정확한 commit ID로 보존한다. inherited working
copy가 바뀌면 실패하며 삭제나 복원으로 덮지 않는다. 현재 task가 만든 작업을 inherited로
표시하지 않는다. 기존의 참조 없는 head와 Git worktree도 소유·유지 이유를 확인하고
`--keep-head`와 `--keep-worktree`로 명시한다. 보존할 workspace는 `--keep-workspace`로
지정한다. 정상 empty working copy는 잔여물이 아니다.

검사는 설명되지 않은 보조 workspace, 참조 없는 empty/non-empty head, 별도 Git 등록과
`--retired-path`로 지정한 directory/symlink 잔여물을 각각 거부한다. 어떤 항목도 자동
삭제하지 않는다. 기존 작업 보존을 포함한 closeout과 모든 작업이 종료된 clean 상태를
구분한다. 생성 시 기록하지 않은 외부 clone의 파일시스템 전수 발견은 지원하지 않는다.

## Legacy workspace metadata

jj 0.38 이전에 만든 workspace는 root 경로를 기록하지 않았다. 현재 workspace는
유일한 working-copy commit과 CLI의 현재 root가 확인될 때 검사할 수 있다. 다른
workspace의 경로가 없거나 같은 commit을 공유해 위치가 모호하면 계속 실패하며
임의의 경로를 추정하거나 등록을 제거하지 않는다.
