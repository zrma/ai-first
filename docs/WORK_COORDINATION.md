# Work coordination

`1.7.0-dev`의 선택형 `work-coordination` profile은 독립 변경을 배정하고 검증된 revision을
통합하는 실행 도구다. 반복되는 clone·수정 범위 확인·인계 상태·전체 검증 처리를 공통화한다.
`verification` profile, Python 3.11 이상, Git과 jj가 필요하다. 실제 검증 버전은 jj 0.45.1이다.

## 설치와 실행

선언의 `profiles`에 `verification`, `work-coordination`을 추가하고 pinned framework로
render한다. `.ai-first/work.py`와 `.agents/skills/ai-first-work/`의 skill/metadata를 배포한다.
중앙 checkout이 없는 clone에서도 실행되며, native 검증 연결은 `docs/VERIFICATION.md`를 따른다.

```sh
python3 .ai-first/verify.py --plan
python3 .ai-first/work.py init --state <private-state> \
  --objective 'Implement the agreed independent changes' --write src/loader.py src/summary.py
python3 .ai-first/work.py assign --state <private-state> \
  --id loader --objective 'Implement the loader contract' --write src/loader.py --check loader
python3 .ai-first/work.py assign --state <private-state> \
  --id summary --objective 'Implement the summary contract' --write src/summary.py --check summary
```

`--check`에는 연결된 native check ID를 사용한다. 생략하면 모든 check를 배정한다.
단일 agent도 한 assignment에 전체 수정 범위를 받아 같은 도구를 사용할 수 있다.
central CLI는 `scripts/ai-first work` 뒤에 동일한 subcommand를 받는다.

`init`은 source revision/content와 binding을 고정하고 local `feature/` bookmark를 만든다.
원본 working copy와 default bookmark는 이동하지 않는다. `assign`은 별도 colocated jj clone을
준비한다. 같은 경로 또는 상위·하위 디렉터리를 두 worker에 배정하면 거부한다. 수정 범위는
literal repository-relative path이며 glob을 받지 않는다. 같은 파일의 순서 의존 편집은
독립 task로 배정하지 않는다.

반환된 packet의 `workspace`, `objective`, `write_scope`, `check_ids`, repository 지침과
원래 승인 범위를 host agent 호출에 전달한다. Codex collaboration으로 실제 worker 두 개를
실행했다. CLI가 agent를 생성하거나 호출 budget을 집행하지는 않으며 spawn, messaging,
cancellation과 사용 권한은 host가 소유한다. 다른 vendor용 adapter의 지원은 미검증이다.

## 검증 인계와 통합

worker는 배정 workspace에서 native 규칙대로 변경하고 logical local change로 닫는다.
coordinator 또는 worker가 다음 명령을 실행한다.

```sh
python3 .ai-first/work.py handoff --state <private-state> --id loader
python3 .ai-first/work.py handoff --state <private-state> --id summary
python3 .ai-first/work.py integrate --state <private-state>
```

handoff는 기준 revision의 ancestry, conflict, 수정 경로와 binding 보존을 검사한 뒤
배정된 native 검증을 실행한다. 실행 전후 source가 같고 선택한 check가 모두 passed여야
`handed_off`가 된다. 미선택 check의 not_run은 이 좁은 인계를 실패시키지 않는다.

integrate는 모든 인계와 현재 source/worker revision을 다시 확인한다. 별도 clone에 실제
worker revision을 합치고 **전체 binding**을 실행한다. 개별 성공은 통합 성공을 대신하지
않으며 conflict나 전체 검증 실패는 실패한 workspace와 결과를 보존한다. 검증 도중 원본
source나 worker가 진전한 경우도 완료로 승격하지 않는다.

`verified`는 연결한 검증의 성공이다. coordinator는 반환된 workspace에서 원래 acceptance,
실제 diff와 미검증 사용자 시나리오를 검토하고 native lifecycle에 따라 채택한다. 도구는
원본 checkout으로 결과를 복사하거나 default bookmark를 옮기거나 publish하지 않는다.

## 상태와 재개

| 명령 | 역할 |
| --- | --- |
| `status --state <private-state>` | 작업·worker·이전 통합 시도와 결과 조회 |
| `packet --state <private-state> --id loader` | 재배정할 workspace와 계약 회수 |
| `resume --state <private-state> --id loader` | 기존 파일/시도를 보존하고 worker 인계를 다시 열기 |
| `resume --state <private-state>` | 중단된 통합 시도를 남기고 새 통합 허용 |
| `unlock --state <private-state>` | lock 소유 process가 종료됐음을 확인한 경우에만 lock 제거 |

resume 전 host에서 이전 worker/coordinator가 멈췄음을 확인한다. 도구가 agent 생존 여부를
추정하지 않는다. 동시 상태 변경은 짧은 lock으로 거부하며, 진행 중인 작업을 확인한 뒤
명령을 재시도한다. 검증 시도의 token은 이전 실행이 재개된 작업의 결과를 덮어쓰지 않게 한다.
source가 진전했으면 기존 work를 보존하고 새 기준에서 work를 연다. 자동 rebase는 하지 않는다.
clone 준비 실패도 보존하고 원인을 확인한 뒤 새 state로 시작한다.

state는 repository 밖의 새 디렉터리여야 하며 생성 권한은 directory 700, JSON 600이다.
revision, local path, argv와 native 출력은 private state에만 남긴다. 소유 범위 검사는 사후
acceptance gate이며 OS sandbox나 악의적인 worker에 대한 보안 경계가 아니다. ignored 파일,
외부 dependency와 live 상태의 동일성도 보증하지 않는다. worker는 다른 workspace/state를
직접 수정하지 않아야 한다.

## 지원 경계와 검증

최초 지원은 independent path 작업과 local Git-backed jj clone이다. native gate가 Git
worktree registration, 설치된 ignored dependency 또는 machine-local configuration을
요구하면 해당 준비를 repository 절차대로 수행해야 한다. 이를 위해 gate를 생략하지 않는다.
범용 scheduler, 자동 cleanup, vendor SDK와 비용/secret 권한은 포함하지 않는다. 생성한
workspace와 local bookmark는 native 보존 정책에 따라 별도로 정리한다.

회귀 테스트는 실제 jj clone에서 정상 통합, 소유 범위·오래된 기준·변경된 인계 거부,
불완전 인계, 실제 native 통합 실패와 중단 재개를 검증한다. 별도 standalone distribution
검사는 framework checkout 없이 실행하고 profile dependency/collision/opt-out을 검사한다.
CI는 [공식 jj 0.45.1 release](https://github.com/jj-vcs/jj/releases/tag/v0.45.1)의 Linux archive를
checksum으로 검증하고 jj 부재를 실패 처리한다. 로컬 canonical gate와 CI 설정 검증은 수행했지만
이 candidate를 공개하지 않았으므로 새 CI run의 성공은 아직 주장하지 않는다.

실제 파일 편집 비교와 도입 비용·시간·표본 한계는 `docs/completed-milestones.md`가 소유한다.
