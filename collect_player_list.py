import core_def
import json
import pandas as pd
import requests
import numpy as np
import time

API_KEY = 'RGAPI-37f2da3f-1ddb-4e58-b5ac-819b9cd37601'

# 'kr', 'na1', 'jp1', 'la1', 'la2', 'eun1' 'euw1' 다이아 1, 플레트넘 1, 골드 1 구간 사람들 목록 수집
for region in ['kr', 'na1', 'jp1', 'la1', 'la2']:
    for tier in ['DIAMOND', 'PLATINUM', 'GOLD']:

        df = pd.DataFrame()
        for page in range(1, 51):
            page = str(page)
            try:
                profile =core_def.collect_summonerprofile(API_KEY, region, tier, 1, page)
                addData = pd.DataFrame(profile)
                df = pd.concat([df, addData])
                if (int(page)%10==0) or int(page)==1:
                    print(f'{region} {tier} {page} th')
            except:
                print('sleeping....')
                time.sleep(30)

        df = df[["tier", "rank", "summonerId", "summonerName", "wins", "losses"]]
        df['win_rate'] = round(df['wins'] / (df['wins'] + df['losses']), 2)
        df['region'] = region
        df.to_pickle(f'./multi national player list/V2/{region}_{tier}_one_player_list.pkl')
        print(f'Completely stored {region} {tier}')

# for _ in range(2):
#     for i in range(500):
#         try:
#             profile =core_def.collect_summonerprofile(API_KEY, 'la1', 'DIAMOND', 1, '1')
#             if (i+1)%15==0:
#                 print(f'{i+1} th')
#                 time.sleep(5)
#         except:
#             start = time.time()
#             print(f'break {i+1}')
#             break

#     L = True
#     while L:
#         try:
#             profile =core_def.collect_summonerprofile(API_KEY, 'la1', 'DIAMOND', 1, '1')
#             L = False
#             end = time.time()
#             print("success")
#             print(end-start)
#         except:
#             pass



