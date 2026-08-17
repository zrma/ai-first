# Stable v1.3 Release And Adoption Open Questions

## Blocking

없음.

## Resolved

- canonical distribution은 기존 v1 계약대로 public source checkout을 유지한다.
- release artifact는 signed annotated Git tag이며 package registry와 GitHub Release는
  이번 범위에 포함하지 않는다.
- migration은 승인된 대상별 독립 change, gate, push와 same-SHA CI로 닫는다.

## Non-blocking

- 새 profile catalog는 실제로 반복되는 소비 요구가 확인될 때 별도 milestone로 연다.
