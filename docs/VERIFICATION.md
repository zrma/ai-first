# Verification workflow

`1.7.0-dev`의 선택형 `verification` profile은 공통 실행 도구와 검증 스킬을 배포한다.
native runner를 하나의 명령으로 연결하고 실행 결과와 source freshness를 공통 형식으로
처리한다. 제품별 acceptance와 native lifecycle은 repository가 계속 소유한다.

## 설치와 연결

기존 `.ai-first.toml`의 `profiles` 배열에 `verification`을 추가하고, 선택한 framework
source의 `scripts/ai-first render --repo <consumer-root>`를 실행한다. 다음 세 파일이
lock의 generated output으로 관리된다.

- `.ai-first/verify.py`: 중앙 CLI와 같은 stdlib runtime
- `.agents/skills/ai-first-verify/SKILL.md`: 요청 시나리오와 검증 증거의 대조 절차
- `.agents/skills/ai-first-verify/agents/openai.yaml`: skill discovery metadata

소비 저장소 루트에서 다음 순서로 연결한다.

```sh
python3 .ai-first/verify.py --plan
python3 .ai-first/verify.py --bind native-check
```

`--plan`은 binding이 없으면 후보를 출력한다. 후보의 native 명령·모드·side effect와 현재
작업 권한을 확인한 다음 선택한다. `--bind`는 `.ai-first/verification.toml`만 새로 만들며
명령을 실행하거나 기존 binding을 덮어쓰지 않는다. 바뀐 binding은 render로 lock에 반영한다.
central CLI에서도 `scripts/ai-first verify --repo <consumer-root>` 뒤에 같은 옵션을 쓴다.

discovery는 `scripts/check.sh`와 package script `check`/`test`를 먼저 제안한다. native
entrypoint가 없으면 Cargo workspace test, Go package test, Python unittest discovery를
해당 project 파일에서 찾아 제안한다. Python test 파일이 있다고 unittest와 호환됨을
보장하지는 않으므로 출력의 실제 test count와 native toolchain을 확인한다.
후보가 없는 custom project는 기존 runner 하나를 다음 형식으로 연결한다.

```toml
schema_version = 1

[[checks]]
id = "native-check"
argv = ["bash", "scripts/check.sh", "--fast"]
coverage = ["Native fast gate; browser and release checks excluded"]
timeout_seconds = 300
```

`argv`는 shell 문자열이 아닌 argument 배열이며 저장소 루트에서 실행한다. native manifest의
명령들을 복사하지 말고 manifest runner와 그 모드를 연결한다. `skip_exit_codes`는 runner가
정의한 nonzero skip code가 있을 때만 지정한다. coverage는 실제 연결 모드와 일치해야 한다.
native interface checker가 version/source/profile을 고정했다면 update transaction에서 그
pin도 갱신해야 한다. 이 profile은 해당 repository gate를 우회하거나 자동 수정하지 않는다.

## 실행과 결과 재사용

```sh
python3 .ai-first/verify.py --run
python3 .ai-first/verify.py --run --select native-check
python3 .ai-first/verify.py --run --output <private-report>
python3 .ai-first/verify.py --report <private-report>
```

기본 JSON은 stdout, native 출력은 stderr로 분리한다. `--output`은 repository 밖의
존재하지 않는 파일에만 저장한다. stdout을 tracked 파일로 redirect하지 않는다.
검증 로그와 command metadata에는 private 정보가 있을 수 있으므로 공개 기록에는 필요한
판정만 정제한다. 저장할 파일의 부모 디렉터리는 미리 준비한다.

| Check 상태 | 의미 |
| --- | --- |
| passed | 명령이 0을 반환 |
| failed | skip code가 아닌 실패 exit |
| skipped | binding에 명시한 skip exit |
| unavailable | 실행 파일 부재 또는 실행 불가 |
| timeout | 제한 시간을 넘겨 프로세스 종료 |
| interrupted | 실행 중 interrupt를 받아 종료 |
| not_run | 선택하지 않았거나 interrupt 이후 실행하지 않음 |

모든 check가 passed일 때 aggregate도 passed다. 나머지는 incomplete다. 검증 전후의
source identity가 다르면 stale이 우선한다. `--run`과 `--report`는 passed에만 exit 0,
incomplete/stale에는 exit 1, binding·입력 오류에는 exit 2를 반환한다. `--plan`의 unbound는
실행 성공이 아니라 후보 탐색 성공이다.

report에는 check별 coverage·exit·소요 시간, 검증 전후 revision/content digest와 OS/Python
version을 남긴다. `--report`는 현재 binding, source와 대조한다. 이는 서명된 증명이나
환경 재현 보증이 아니다. jj/Git에서는 현재 source 목록을 사용하고, VCS가 없는 저장소는
build/dependency 디렉터리를 제외한 filesystem fingerprint를 사용한다.
ignored 파일, submodule 내부, 실제 toolchain/dependency version, remote/live 상태는
이 fingerprint의 범위 밖이다. symlink target의 외부 내용도 읽지 않는다.
revision도 비교하므로 jj describe/new처럼 내용이 같아도 revision이 바뀌면 stale이다.
원래 report의 content digest와 diff를 검토해 증거의 재사용 가능성을 판단할 수 있지만
이를 새 revision에서 실제 실행한 결과나 same-SHA CI라고 표시하지 않는다.

native runner가 내부 check를 생략하고도 exit 0을 반환하면 공통 runtime은 이를 알 수 없다.
예를 들어 quick mode의 passed를 full gate 통과로 보고하지 않는다. 스킬은 native 출력의
count/skip와 원래 요청의 대상·방향·실행 경로를 함께 확인한다. source revision이 같아도
새 탭 성공이 기존 탭 복구를 입증하지 않으며, 의미·시각적 acceptance는 제품 소유자가 판단한다.

## 갱신과 제거

runtime과 스킬은 framework version 및 lock digest로 함께 갱신된다. 기존 repository의
같은 경로에 framework가 소유하지 않는 다른 스킬이 있으면 render가 중단되어 보존한다.
profile을 제거하고 render하면 이전 lock이 소유한 변경되지 않은 generated 파일만 제거한다.
수동 수정이 있으면 먼저 보존 또는 복원할 때까지 중단한다. binding은 repository 소유이므로
남겨 둔다. 기존 profile 미선택 소비 저장소의 schema와 output은 그대로 유지된다.

## 검증 기준

runtime 회귀 검증은 실패/skip/도구 부재/timeout, subset, stale source, report 재사용,
binding 오류, private output 경계와 profile 도입·제거를 다룬다. standalone fixture는
central checkout 없이 runtime 실행과 generated skill drift 검출을 확인한다.
실제 consumer와 held-out 평가의 결과 및 한계는 `docs/completed-milestones.md`가 소유한다.

repository skill의 위치와 discovery 규칙은 [공식 Codex skills 문서](https://developers.openai.com/codex/skills)를
확인했다. 일반 prompt 규칙을 더 쌓기보다 outcome과 기존 권한을 보존하는 설계는
[공식 최신 model guide](https://developers.openai.com/api/docs/guides/latest-model)를 따른다.
