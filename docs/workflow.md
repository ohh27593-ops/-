# Workflow

## 1. 개요

이 프로젝트는 경북대 밥친구 프로그램의 운영 흐름을 자동화하기 위한 코드들로 구성되어 있습니다.

전체 흐름은 다음과 같습니다.

1. `first_survey_loader.py`에서 1차 설문 응답을 불러옵니다.
2. `user_registry_update.py`에서 기존 가입자 정보를 갱신합니다.
3. `new_user_extractor.py`에서 신규 가입자만 따로 추출합니다.
4. `kakao_verification_sender.py`에서 카카오톡 인증 안내를 보냅니다.
5. `second_survey_loader.py`에서 2차 설문 응답을 불러옵니다.
6. `question_proposal_exporter.py`에서 질문과 제안을 분리 저장합니다.
7. `weekday_match_file_generator.py`에서 요일별 매칭 파일을 생성합니다.

---

## 2. 1차 설문 처리 흐름

관련 파일:
- `src/onboarding/first_survey_loader.py`
- `src/onboarding/user_registry_update.py`
- `src/onboarding/new_user_extractor.py`

주요 처리 흐름:

1. 1차 설문 Google Sheet에 연결합니다.
2. 응답 데이터를 모두 읽어옵니다.
3. `타임스탬프` 문자열을 `datetime`으로 변환합니다.
4. 운영에 필요한 형태로 데이터를 정리합니다.
   - `stamp`
   - `phone`
   - `name`
   - `integ`
5. 기존 가입자 정보와 비교합니다.
6. 중복 가입을 제거합니다.
7. 비건전 사용자 및 탈퇴 사용자 정보를 반영합니다.
8. 최종적으로 다음 파일들을 저장합니다.
   - 갱신된 가입자 정보 파일
   - 신규 가입자 파일

---

## 3. 카카오톡 인증 안내 흐름

관련 파일:
- `src/messaging/kakao_verification_sender.py`

주요 처리 흐름:

1. 카카오톡 안내 대상이 들어 있는 Google Sheet 또는 Excel 데이터를 불러옵니다.
2. 기존 연락처 목록과 전화번호를 비교합니다.
3. 신규 인원만 따로 추가합니다.
4. `pyautogui`를 사용해 카카오톡 메시지를 자동 전송합니다.
5. 전송 여부를 Excel 파일에 기록합니다.
6. 최종 Excel 파일을 저장합니다.

즉, 이 단계는 단순 조회가 아니라  
**신규 사용자에게 인증 안내를 보내는 운영 단계**입니다.

---

## 4. 2차 설문 처리 흐름

관련 파일:
- `src/followup_survey/second_survey_loader.py`
- `src/followup_survey/question_proposal_exporter.py`
- `src/followup_survey/weekday_match_file_generator.py`

주요 처리 흐름:

1. 2차 설문 Google Sheet에 연결합니다.
2. 응답 데이터를 모두 읽어옵니다.
3. 실제 참여 의사가 있는 사용자만 남깁니다.
4. 기존 정상 가입자 목록과 대조합니다.
5. 다음 정보를 추출합니다.
   - 요일별 가능 시간대
   - 선호 활동
   - 질문
   - 추가 제안
6. 결과를 각각의 파일로 저장합니다.
   - 2차 설문 반영 사용자 파일
   - 질문 파일
   - 제안 파일
   - 요일별 매칭 파일

---

## 5. 요일별 매칭 파일 생성

`weekday_match_file_generator.py`는 각 요일별로 별도의 파일을 생성합니다.

생성 대상:
- Monday
- Tuesday
- Wednesday
- Thursday
- Friday
- Saturday
- Sunday

각 파일에는 기본적으로 다음 정보가 들어갑니다.

- 전화번호
- 해당 요일의 원본 가능 시간대
- 파생된 boolean 정보
  - `morning`
  - `lunch`
  - `afternoon`
  - `cafe`
  - `walk`
  - `restaurant`
  - `recreation`
  - `exercise`

이 구조를 만드는 이유는  
나중에 실제 매칭 로직을 짤 때 조건 비교를 훨씬 쉽게 하기 위해서입니다.

예를 들어 사용자가 “수요일 점심 가능”, “카페 선호”라고 응답했다면  
이를 문자열 그대로 두는 것보다

\[
\text{lunch} = True,\quad \text{cafe} = True
\]

처럼 바꾸는 편이 이후 필터링과 매칭에 더 유리합니다.

---

## 6. 공통 유틸리티

관련 파일:
- `src/shared/time_utils.py`
- `src/shared/sheet_utils.py`

역할은 다음과 같습니다.

### `time_utils.py`
한글 오전/오후 형식으로 적힌 시간 문자열을 `datetime`으로 바꾸는 기능을 담당합니다.

### `sheet_utils.py`
Google Sheet 연결과 worksheet 접근을 조금 더 공통적으로 처리하기 위한 보조 함수 파일입니다.

즉, 여러 파일에서 반복되는 부분을 따로 뺀 것입니다.
