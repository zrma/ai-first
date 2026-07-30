# Security Policy

## Supported versions

stable release 전에는 default branch의 최신 revision만 보안 수정을 받는다.

## Reporting a vulnerability

GitHub의 private vulnerability reporting을 사용한다. public issue, discussion 또는
pull request에 exploit detail, credential, private repository identity, local path,
host·cluster 정보와 실제 환경 log를 올리지 않는다.

보고에는 합성된 최소 재현, 영향받는 framework version, 기대 경계와 실제 동작을
포함한다. 실제 private 환경 evidence가 필요하면 공개 artifact와 분리해 최소 범위로
공유한다.

접수만으로 수정 완료를 의미하지 않는다. 재현, 수정, 회귀 검증과 영향받는 공개
artifact 확인까지 완료된 뒤 close한다.
