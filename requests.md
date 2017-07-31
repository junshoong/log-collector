### 과제명

비정상 셧다운 자동 로그수집 도구 개발
(irregular shutdown auto-log-collector)

### 과제 목표

- OS 상 기록되는 성능 데이터와 메시지 데이터의 종류에 대해 알아본다
- OS 상 정상/비정상 셧다운 판별할 수 있는 방법을 생각해본다
- http를 통해 데이터를 전송하는 방법에 대해 알아본다
- web을 통해 데이터를 읽는 방법에 대해 알아본다

### 예상 결과물

- irregular shutdown auto-log-collector
- web-based log viewer

1. OS 부팅 직후, 본 도구를 자동 실행할 수 있어야한다.
2. 본 도구를 통해 해당 OS 부팅 직전 셧다운에 대한 정상/비정상을 판별할 수 있어야 한다
3. 비정상으로 판별된 경우, 성능 데이터 및 메시지 데이터를 로컬 상 수집할 수 있어야 한다
4. http를 통해, 수집된 데이터를 원격에 위치한 viewer server로 전송할 수 있어야 한다
5. viewer server로 전송된 데이터는 일련의 규칙에 맞춰 체계적으로 저장할 수 있어야 한다
6. viewer server 상 web-gui 환경에서 해당 데이터를 출력할 수 있어야 한다

### 관련 키워드

- sar
- /var/log/messages
- netconsole

