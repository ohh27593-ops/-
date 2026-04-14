# File Roles

## 1. 개요

이 문서는 `knu-meal-friend-automation` 저장소 안에 있는 주요 파일들이 각각 어떤 역할을 하는지 정리한 문서입니다.

이 프로젝트는 크게 다음 4개의 영역으로 나뉩니다.

- 1차 설문 및 가입 관리
- 카카오톡 인증 안내
- 2차 설문 처리
- 공통 유틸리티

---

## 2. 루트 파일

### `README.md`
저장소의 전체 소개 문서입니다.  
프로젝트 목적, 주요 기능, 폴더 구조, 실행 흐름 등을 설명합니다.

### `requirements.txt`
이 프로젝트를 실행하기 위해 필요한 외부 라이브러리 목록입니다.  
`pip install -r requirements.txt`로 설치할 수 있습니다.

### `.gitignore`
GitHub에 올리면 안 되는 파일들을 제외하기 위한 설정 파일입니다.  
예를 들어 실제 인증키, 실제 엑셀 데이터, 캐시 파일 등이 여기에 포함됩니다.

---

## 3. `config_examples/`

### `config_examples/credentials_example.json`
Google Service Account 인증 파일의 형식을 보여주는 예시 파일입니다.  
실제 인증키가 아니라, 어떤 구조의 JSON 파일이 필요한지 설명하기 위한 용도입니다.

### `config_examples/env_example.txt`
프로젝트 실행 시 필요한 설정값 예시를 적어둔 파일입니다.  
예를 들어 시트 ID, 워크시트 이름, 데이터 파일 경로 등이 들어갑니다.

---

## 4. `src/onboarding/`

이 폴더는 1차 설문 응답을 기반으로 가입자 정보를 다루는 코드들로 구성되어 있습니다.

### `src/onboarding/first_survey_loader.py`
1차 설문 Google Sheet에 연결하여 응답을 불러오고,  
`stamp`, `phone`, `name`, `integ` 형식으로 전처리하는 파일입니다.

즉, 이 파일의 역할은

\[
\text{원본 설문 응답} \rightarrow \text{운영용 데이터 형식}
\]

으로 바꾸는 것입니다.

### `src/onboarding/user_registry_update.py`
기존 가입자 정보 파일과 1차 설문 응답을 비교하여  
가입자 마스터 파일을 갱신하는 역할을 합니다.

주요 기능:
- 기존 가입자 불러오기
- 중복 가입 제거
- 신규 가입자 반영
- 비건전 사용자 반영
- 탈퇴 사용자 반영
- 최종 가입자 파일 저장

즉, 이 파일은 가입자 관리의 중심 파일입니다.

### `src/onboarding/new_user_extractor.py`
1차 설문 응답 중에서 신규 가입자만 따로 추출하는 역할을 합니다.

이 파일은 전체 가입자 마스터를 갱신하기보다,
신규 사용자 목록만 따로 저장하는 데 초점이 있습니다.

즉,

\[
\text{1차 설문 응답} - \text{기존 가입자} = \text{신규 가입자}
\]

의 역할을 담당합니다.

### `src/onboarding/legacy/onboarding_initial_version.py`
가입 관리 로직의 초기 실험 버전입니다.

특징:
- 기존 자료와 최근 응답 비교
- `merge`를 통한 데이터 정합성 확인
- 출력 중심의 검증용 코드

즉, 실제 운영용이라기보다  
초기 로직 검증과 개발 과정을 보여주는 파일입니다.

### `src/onboarding/legacy/onboarding_intermediate_version.py`
초기 실험 버전보다 더 발전한 중간 단계 코드입니다.

특징:
- 실제 가입자 파일 저장
- 신규 가입자 파일 저장
- 비건전/탈퇴 사용자 반영

즉, 초기버전과 최종 갱신 버전 사이에 있는  
실사용 가능 단계의 코드라고 볼 수 있습니다.

---

## 5. `src/messaging/`

### `src/messaging/kakao_verification_sender.py`
신규 사용자에게 카카오톡 인증 안내를 보내는 파일입니다.

주요 기능:
- Google Sheet 또는 Excel에서 연락 대상 읽기
- 기존 연락처와 비교
- 신규 사용자만 추가
- `pyautogui`로 카카오톡 메시지 자동 전송
- 전송 여부를 Excel에 기록

즉, 이 파일은 가입 이후의 실제 운영 커뮤니케이션을 담당합니다.

---

## 6. `src/followup_survey/`

이 폴더는 2차 설문 응답을 다루는 코드들로 구성되어 있습니다.

### `src/followup_survey/second_survey_loader.py`
2차 설문 응답을 불러와 참여 의사자만 남기고,
기존 정상 가입자와 대조하여 사용할 수 있는 사용자 데이터로 정리하는 파일입니다.

주요 기능:
- 2차 설문 불러오기
- 참여 의사 필터링
- 기존 정상 가입자 대조
- 질문/제안/요일별 가능 시간대/선호 활동 추출
- 결과 파일 저장

즉, 2차 설문 처리의 중심 파일입니다.

### `src/followup_survey/question_proposal_exporter.py`
2차 설문에서 사용자가 남긴 질문과 추가 제안을 따로 분리해서 저장하는 파일입니다.

이 파일이 필요한 이유는,
질문과 제안을 운영자가 따로 확인해야 하기 때문입니다.

즉,
- 질문은 문의 대응용
- 제안은 서비스 개선용

으로 볼 수 있습니다.

### `src/followup_survey/weekday_match_file_generator.py`
2차 설문 데이터를 바탕으로 요일별 매칭 파일을 생성하는 역할을 합니다.

예를 들어 월요일, 화요일, 수요일별로 각각 파일을 만들고,
각 파일 안에 아래와 같은 파생 정보를 포함합니다.

- `morning`
- `lunch`
- `afternoon`
- `cafe`
- `walk`
- `restaurant`
- `recreation`
- `exercise`

즉, 이후 실제 매칭 알고리즘이 쓰기 좋은 형태로 데이터를 가공하는 파일입니다.

---

## 7. `src/shared/`

### `src/shared/time_utils.py`
한글 오전/오후 형식의 시간 문자열을 `datetime`으로 변환하는 보조 함수 파일입니다.

여러 파일에서 반복적으로 쓰는 시간 변환 로직을 공통으로 분리한 것입니다.

### `src/shared/sheet_utils.py`
Google Sheet 연결 및 worksheet 접근을 공통 함수로 정리한 파일입니다.

즉, 여러 파일에서 반복되는
- 인증
- 시트 연결
- 워크시트 선택

과정을 조금 더 재사용하기 쉽게 만든 보조 파일입니다.

---

## 8. `sample_data/`

### `sample_data/input/`
입력 예시 데이터를 넣는 폴더입니다.  
실제 운영 데이터가 아니라, 비식별 처리된 예시 데이터만 넣어야 합니다.

### `sample_data/output/`
코드 실행 결과 예시를 넣는 폴더입니다.  
역시 실제 개인정보가 아니라 예시 결과만 넣어야 합니다.

### `sample_data/anonymized_sample.xlsx`
비식별 처리된 샘플 엑셀 파일입니다.  
실제 데이터 구조가 어떻게 생겼는지 보여주기 위한 예시 파일입니다.

---

## 9. `docs/`

### `docs/workflow.md`
프로젝트 전체 실행 흐름을 설명하는 문서입니다.  
각 파일이 어떤 순서로 이어지는지 설명합니다.

### `docs/file_roles.md`
각 파일의 역할을 설명하는 문서입니다.  
즉, 지금 보고 있는 이 문서입니다.

---

## 10. 전체 역할 요약

이 프로젝트의 파일들은 전체적으로 다음 흐름을 이룹니다.

\[
\text{1차 설문} \rightarrow \text{가입자 관리} \rightarrow \text{인증 안내} \rightarrow \text{2차 설문} \rightarrow \text{매칭 준비}
\]

이를 파일 기준으로 다시 쓰면 다음과 같습니다.

1. `first_survey_loader.py`  
   → 1차 설문 응답 불러오기

2. `user_registry_update.py`  
   → 가입자 마스터 갱신

3. `new_user_extractor.py`  
   → 신규 사용자만 추출

4. `kakao_verification_sender.py`  
   → 카카오톡 인증 안내 전송

5. `second_survey_loader.py`  
   → 2차 설문 응답 정리

6. `question_proposal_exporter.py`  
   → 질문/제안 분리 저장

7. `weekday_match_file_generator.py`  
   → 요일별 매칭 파일 생성

즉, 각 파일은 따로 놀지 않고  
운영 흐름 안에서 서로 이어지는 구조를 가지고 있습니다.
