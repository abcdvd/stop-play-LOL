import core_def
import time
import pandas as pd
from multiprocessing import Pool
import sys, os

def fool(API, region):
    player_list = pd.read_pickle(f'./player list/V2/{region}.pkl')
    XY = pd.DataFrame()

    start_index = 0
    end_index = player_list.shape[0]

    for i in range(start_index, end_index):
        while True:
            try:
                summonerId = player_list.iloc[i, 2]
                tier = player_list.iloc[i, 0]

                profile = core_def.summoner_info_by_summonerId(API, summonerId, region)
                puuid = profile['puuid']
                
                matchId = core_def.get_matchID_by_puuid(API, puuid, 0, 1, region)[0]
                matchTimeLine = core_def.get_matchTimeLine_by_matchID(API, matchId, region)["info"]["frames"]
                gameDuration = round(matchTimeLine[-1]['timestamp']/1000/60)

                match_info = core_def.get_matchINFO_by_matchID(API, matchId, region)
                win = match_info["info"]["participants"][0]["win"]  # blue team win (boolean)
                gameMode = match_info["info"]["gameMode"]
                if gameMode != "CLASSIC":
                    break

                dic = {}
                for c in range(1, 11):
                    dic[f"{c}_level"] = []
                    dic[f"{c}_minionsKilled"] = []
                    dic[f"{c}_totalGold"] = []
                    dic[f"{c}_totalDamageTaken"] = []
                    dic[f"{c}_totalDamageDone"] = []
                    dic[f"{c}_WARD_PLACED"] = []
                    dic[f"{c}_WARD_KILL"] = []
                dic['time'] = []

                ward_control = {}
                for q in range(1, 11):
                    ward_control[f"{q}_PLACED"] = []
                    ward_control[f"{q}_KILL"] = []


                for element in matchTimeLine[:-1]:
                    events = element["events"]
                    participantFrames = element["participantFrames"]
                    timestamp = round(element["timestamp"]/1000/60, 1)

                    for event in events:
                        if event["type"] == "WARD_PLACED":
                            try:
                                num = event["creatorId"]
                                ward_control[f"{num}_PLACED"].append(1)
                            except:
                                pass
                        
                        if event["type"] == "WARD_KILL":
                            try:
                                num = event["killerId"]
                                ward_control[f"{num}_KILL"].append(1)
                            except:
                                pass
                    
                    if (timestamp>0):
                        for j in range(1, 11):
                            dic[f"{j}_level"].append(participantFrames[f"{j}"]["level"])
                            dic[f"{j}_minionsKilled"].append(participantFrames[f"{j}"]["minionsKilled"])
                            dic[f"{j}_totalGold"].append(participantFrames[f"{j}"]["totalGold"])
                            dic[f"{j}_totalDamageTaken"].append(participantFrames[f"{j}"]["damageStats"]["totalDamageTaken"])
                            dic[f"{j}_totalDamageDone"].append(participantFrames[f"{j}"]["damageStats"]["totalDamageDone"])
                            dic[f"{j}_WARD_PLACED"].append(sum(ward_control[f"{j}_PLACED"]))
                            dic[f"{j}_WARD_KILL"].append(sum(ward_control[f"{j}_KILL"]))
                        dic['time'].append(timestamp)

                df = pd.DataFrame(dic)
                df['gameDuration'] = gameDuration
                df['region'] = region
                df['tier'] = tier
                df['gameId'] = matchId
                df['win'] = win

                df.to_pickle(f"./데이터 저장소/V2/{region}/{region}_{i}.pkl")

                XY = pd.concat([XY, df], axis=0)
                break

            except Exception as ex:
                exc_type, exc_obj, exc_tb = sys.exc_info()
                print(f'{region} {i} Reason : {ex}  Line : {exc_tb.tb_lineno}')
                print("sleeping 10 sec")
                time.sleep(10)
    XY.to_pickle(f"./데이터 저장소/V2_/{region}_timeline.pkl")

    # return matchTimeLine
    




if __name__=='__main__':
    API = 'RGAPI-af1e40e6-9a52-4102-8114-4fdd6fbd8973'
    regions = ['kr', 'jp1', 'na1', 'la1', 'la2']


    for region in regions:
        start = time.time()
        fool(API, region)
        end = time.time()
        print(f"{region} complete {end-start}s seconds ---")
    print("Done")