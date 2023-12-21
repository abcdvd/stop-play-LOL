import pandas as pd
import pickle

region_list = ['kr', 'jp1', 'la1', 'la2', 'na1']
tier_list = ['DIAMOND', 'PLATINUM', 'GOLD']

def merge_player(region_list, tier_list):
    for region in region_list:
        df = pd.DataFrame()
        for j in tier_list:
            data = pd.read_pickle(f'./multi national player list/V2/{region}_{j}_one_player_list.pkl')
            df = pd.concat([df, data], axis=0)

        df.to_pickle(f'./player list/V2/{region}.pkl')

    print('Done')

def merge_V1(region_list):
    for region in region_list:
        df = pd.DataFrame()
        for j in range(0, 12000):
            try:
                data = pd.read_pickle(f"./데이터 저장소/V2/{region}/{region}_{j}.pkl")
                df = pd.concat([df, data], axis=0)
            except:
                pass
        df.to_pickle(f"./데이터 저장소/V2_/{region}_timeline.pkl")

        print(f"{region} Done")


merge_V1(['kr'])
# merge_player(region_list, tier_list)