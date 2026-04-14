import pandas as pd
import numpy as np
import sys


# 1. 비교용 지난 자료 가져오기
way_excel = r"data/user_info_second_survey.xlsx"
try:
    to_go_excell = pd.read_excel(way_excel)
except Exception as ereo:
    print('이전 사용자 정보 가져오기에 실패하여 코드를 자동으로 중지합니다. 에러 정보:', ereo)
    sys.exit()

days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']

for col in days:
    be_match = to_go_excell[['phone', f'{col}', 'prefer']]

    be_match = be_match.assign(
        morning=np.where(be_match[f'{col}'].astype('string').str.contains('오전', regex=False, na=False), True, False),
        lunch=np.where(be_match[f'{col}'].astype('string').str.contains('점심', regex=False, na=False), True, False),
        afternoon=np.where(be_match[f'{col}'].astype('string').str.contains('오후', regex=False, na=False), True, False),
        cafe=np.where(be_match['prefer'].astype('string').str.contains('카페', regex=False, na=False), True, False),
        walk=np.where(be_match['prefer'].astype('string').str.contains('산책', regex=False, na=False), True, False),
        restaurant=np.where(be_match['prefer'].astype('string').str.contains('맛집', regex=False, na=False), True, False),
        recreation=np.where(be_match['prefer'].astype('string').str.contains('놀이(보드게임 등)', regex=False, na=False), True, False),
        exercise=np.where(be_match['prefer'].astype('string').str.contains('운동', regex=False, na=False), True, False)
    )
    be_match = be_match.drop(columns=['prefer'])

    # 3) 필터링 후 요일별 파일로 저장
    be_match.to_excel(
        fr"data/user_info_2_{col}.xlsx",
        index=False
    )
