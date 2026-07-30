### Capability Profile: public-repository

- tracked artifact는 remote visibility와 무관하게 public-ready content를 유지한다.
- prompt, transcript, raw tool output, local path, private inventory, host·cluster
  identifier, internal endpoint/address와 credential을 tracked file에 넣지 않는다.
- public push, visibility 변경, tag/release와 history rewrite 전에는 repository
  checker와 권한 있는 machine-local inventory checker를 모두 실행한다.
