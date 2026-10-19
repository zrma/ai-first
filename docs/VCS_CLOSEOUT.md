# Local VCS task workflow

`1.10.1`의 선택형 `vcs-closeout`은 agent의 change 작업을 시작 기록, 사본 소유,
선형 통합, 종료 확인으로 연결한다. `vcs-jj`와 Python 3.11+, Git, jj가 필요하다.
선언/lock schema 1과 기존 `--revision`/`--closeout` 명령은 유지한다.
도구는 읽기, working-copy snapshot과 private 상태 기록만 수행하며 자동 삭제·push를 하지 않는다.

## Start and resume

첫 수정과 임시 사본 생성 전에 canonical workspace root에서 실행한다.

```sh
export AI_FIRST_VCS_SESSION="<private-state-directory>/task.json"
python3 .ai-first/vcs.py start
# 중단했던 같은 작업은 덮어쓰지 않고 이어간다.
python3 .ai-first/vcs.py resume
```

상태 파일은 모든 저장소 checkout 밖의 새 파일이어야 하며 permission 0600으로 생성된다.
기존 working copy, workspace/root, 참조 없는 head, Git worktree, bookmark와 tag를
기록한다. 같은 파일로 start를 반복하면 실패한다. 환경 변수 대신 `--state`도 지원한다.
read-only answer/review에는 세션을 만들지 않는다. 기존 native start-work/readiness는
시작 기록 뒤에 실행하며 native helper에도 같은 환경 변수를 전달한다.

## Own a task copy

새 사본을 만들기 전에 canonical root에서 등록한다.

```sh
python3 .ai-first/vcs.py own --path "<new-task-copy>"
# 이후 승인된 native jj workspace 또는 Git-backed 격리 사본을 생성한다.
```

이미 존재하는 경로, 기본/기존 workspace 안팎을 덮는 경로는 거부한다. 등록은 삭제
권한이 아니며 생성 실패·중단 시에도 같은 기록을 보존한다. 관련 작업이 이미 진행
중이거나 기본 WC가 dirty이면 별도 사본에서 작업하고 원래 WIP를 그대로 둔다.
소유하지 않은 기존 작업을 정리 대상으로 바꾸지 않는다.

## Validate linear integration

native gate와 attribution description 뒤, bookmark를 이동하기 직전에 실행한다.

```sh
python3 .ai-first/vcs.py integrate --revision <candidate>
# 승인된 publication에만:
jj git fetch --remote origin
python3 .ai-first/vcs.py integrate --revision <candidate> --remote origin
```

후보가 현재 main과 시작 main을 선형으로 이어야 하며 conflict와 새 merge를 거부한다.
remote 옵션은 실제 remote head를 조회하고 fetched ID 및 후보 조상을 대조한다.
stale이면 bookmark/push 전에 멈추고 미출고 변경만 최신 remote 위에 선형 재적용한 뒤
native 검증을 다시 한다. 기존 published history와 release ref는 재작성하지 않는다.
검사 자체가 publication을 승인하거나 bookmark를 이동하지 않는다. native finalize는
이 검사를 bookmark 이동 전에 연결한다. shared jj workspace에서는 `@`도 지원하고,
별도 clone은 결과를 canonical repository에 가져온 뒤 full commit ID로 검사한다.

기본 bookmark는 `main`이며 `[vcs].bookmark`로 설정한다. 과거 merge를 보존하는
`[vcs].linear_history_base`는 도입 당시 full lowercase commit ID로 고정한다. 검사
통과를 위해 앞으로 옮기지 않는다. `--base`는 기존 일회 검사에서 지원한다.

## Finish and reclaim

완료 결과에 durable bookmark를 남기고 새 empty WC를 만든다. publication이 없으면
기본 bookmark 대신 task bookmark로 결과를 보존한다. 출고 시 remote SHA를 대조한다.
소유 사본의 고유 결과가 durable history에 포함됐는지 확인한 뒤 해당 사본만 등록을
해제하고 회수 가능한 방식으로 경로를 정리한다. jj forget이 Git 등록도 없앨 수 있으므로
각 inventory를 다시 읽는다. canonical root에서 마지막으로 실행한다.

```sh
python3 .ai-first/vcs.py finish
```

완료 후보, empty WC/expected parent, 새 orphan head, 미분류 workspace/Git 등록과
소유 경로의 directory/symlink 잔여물을 검사한다. 공유 Git hook의 직접 경로 참조와 hooksPath도 확인한다. package prepare가 공통 hook을
임시 사본의 실행 파일에 연결했다면 canonical workspace에서 native hook 설치 절차로
복구한다. 사용자 정의 hook을 무조건 덮어쓰지 않으며 검사기는 hook을 실행하지 않는다.
기존 dirty WC는 정확한 시작 ID를,
기존 secondary workspace는 시작 위치와 ID를, 기존 bookmark와 release tag는 원래
대상을 유지해야 한다. 동시 작업으로 바뀌면 삭제/복원하지 않고 보존·분류 후 재개한다.
성공한 기록은 재사용하지 않는다. 실패·중단은 완료가 아니며 기록과 이유·재개점을 남긴다.

## Native and CI boundaries

일반 `.ai-first/check.py`는 input/output/interface 무결성을 검사한다. 로컬 이력과
마감 검사를 일반 CI에 자동 삽입하지 않으므로 CI 전용 후보 변수나 full-history checkout은
요구하지 않는다. 기존 제품 CI와 native gate는 유지한다. native helper는 세션 변수가
있으면 resume/integrate를 호출하고 generated agent 지침은 change 작업에서 그 변수를
설정하도록 요구한다. helper가 없는 저장소는 같은 공통 명령을 직접 실행한다.

이는 agent 지침과 명시적 실행 검사이며 임의 명령을 강제 차단하는 hook/sandbox나
server-side branch rule은 아니다. 생성 시 등록하지 않은 외부 clone의 전수 발견,
고유 결과의 의미상 중복 판정, GitHub release asset 변조 검증은 지원하지 않는다.
기존 `--closeout`의 keep 인자는 일회 감사 호환용이며 시작 기록을 대체하지 않는다.

jj 0.38 이전 root metadata는 현재 root와 유일한 WC ID가 확인되는 경우만 지원한다.
위치를 모르는 secondary나 모호한 identity는 실패하며 임의 경로를 추정하지 않는다.
