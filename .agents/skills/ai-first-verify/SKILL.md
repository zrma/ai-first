---
name: ai-first-verify
description: 변경을 검증하거나 완료를 보고할 때 연결된 native 검증을 실행하고 요청 시나리오와 증거를 대조한다. ai-first verification profile이 설치된 저장소에 사용하며 일반 질의나 계획만 요청한 경우 검증 실행으로 확대하지 않는다.
---

# Change verification

사용자가 원한 결과와 실제 검증 범위를 연결한다. 공통 runtime은 실행 결과를 처리하고,
repository의 native runner와 acceptance 자료는 제품별 판단 근거를 제공한다.

1. `python3 .ai-first/verify.py --plan`으로 연결을 확인한다. unbound이면 후보의 native
   명령·모드와 side effect를 읽고 현재 권한 안의 entrypoint를 `--bind ID`로 연결한다.
   binding 변경 뒤 pinned framework로 render한다. native 명령 목록을 다시 복제하지 않는다.
2. `python3 .ai-first/verify.py --run`을 실행한다. 좁은 작업은 `--select ID`, 결과 보존은
   `--output <private-report>`를 사용한다. output은 repository 밖의 새 파일이어야 한다.
3. check별 status, coverage와 native 출력의 test count/skip을 읽는다. 내부 skip을 exit 0으로
   숨기는 runner의 passed를 full gate로 보고하지 않는다. 미선택 check의 not_run은 정상이다.
4. 기존 결과는 `--report <private-report>`로 source와 binding freshness를 확인한다.
   ignored dependency, 외부 상태와 실행 환경의 동일성은 이 검사로 보증하지 않는다.
5. native spec의 acceptance와 coverage를 대조하고, runner 밖의 사용자 시나리오는 기존
   browser/live/artifact 검사로 보완한다. 미검증과 기능 미충족을 구분해 보고한다.

## Binding

`.ai-first/verification.toml`은 아래와 같은 작은 adapter다. `argv`는 shell 문자열이
아닌 argument 배열이며 저장소 루트에서 실행된다. 기본 timeout은 300초다.
기존 native 모드·선택 옵션은 해당 runner의 계약을 따른다.

```toml
schema_version = 1

[[checks]]
id = "native-check"
argv = ["sh", "scripts/check.sh"]
coverage = ["Repository native local gate"]
timeout_seconds = 300
skip_exit_codes = [77]
```

skip exit code는 runner가 실제 정의한 경우에만 지정한다. 없는 것을 추정하지 않는다.
runtime은 passed, failed, skipped, unavailable, timeout, interrupted와 not_run을
구분한다. 하나라도 passed가 아니면 전체 결과는 incomplete이며, source 변경은 stale이다.
완료 조건의 의미, external write 권한, human acceptance와 lifecycle closeout은 기존
repository 계약이 소유한다.
