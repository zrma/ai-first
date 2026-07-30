# Publication Policy

## Content class

이 저장소의 tracked artifact는 remote visibility와 무관하게 `public-ready` 기준을
사용한다.

## 허용

- AI-first identity와 일반화된 operating contract
- repository type을 식별하지 않는 capability profile
- 합성 schema, deterministic tool과 synthetic fixture
- repository-owned decision과 redacted 검증 판정
- `<repo-root>`, `<private-host>`, `<internal-ip>`, `<cluster-context>` 같은 placeholder

## 금지

- prompt, 대화 transcript, memory 원문과 raw tool output
- local absolute path, username, machine·host·cluster identifier
- credential, secret, internal endpoint/address
- private repository 이름, URL, revision과 checkout inventory
- 소비 저장소별 local WIP, workspace path와 unpublished migration 상태
- account-wide private portfolio inventory

## 최초 공개 gate

1. `scripts/check.sh`
2. repository publication boundary check
3. 권한 있는 machine-local private-inventory gate의 `all` mode
4. local `jj` change description과 attribution 확인
5. public remote 생성과 intended bookmark push
6. remote bookmark SHA와 default branch 확인
7. terminal CI 확인
8. clean working copy 확인

remote 생성, visibility 변경, push, tag와 release는 각각 외부 write다.

## 현재 상태

- remote: 빈 public repository 생성 및 visibility 확인
- license: `Apache-2.0`
- publication: 최초 push 전 gate 진행 중
