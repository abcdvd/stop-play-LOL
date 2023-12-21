import core_def
import time
import pandas as pd
from multiprocessing import Pool
import sys, os

def fool(API, region, start_index, end_index):

    start_index = int(start_index)
    end_index = int(end_index)

    player_list = pd.read_pickle(f'./player list/V1/{region}.pkl')
    try:
        for i in range(start_index, end_index+1):
            player_name = player_list.iloc[i, 3]
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
            gameType = match_info["info"]["gameType"]

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
                timestamp = round(element["timestamp"]/1000/60)

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
                
                if (timestamp>0) and (timestamp%5==0):
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

            df.to_pickle(f"./데이터 저장소/V1/{region}/{region}_{i}.pkl")
        print(f"{region} {start_index} ~ {end_index}")  

    except Exception as ex:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        print(f'{region} {i} Reason : {ex}  Line : {exc_tb.tb_lineno}')
        time.sleep(10)
    # return matchTimeLine
    




if __name__=='__main__':
    start = time.time()
    API = 'RGAPI-915beed7-f81a-44d2-ba50-659567ed5f8d'
    regions = ['kr', 'na1', 'la1', 'la2']

    # a = 1
    # b = 3
    # for i in range(a, b):
    #     APIs = [API for _ in range(5)]
    #     var1 = [str(a*10 +1) for _ in range(5)]
    #     var2 = [str(b*10) for _ in range(5)]

    #     tasks = zip(APIs, regions, var1, var2)
        
    #     pool = Pool(5)
    #     pool.starmap(fool, tasks)
    #     pool.close()
    #     pool.join()
    #     time.sleep(5)


    a = 1548
    b = 1600
    for i in range(a, b):
        for region in regions:
            fool(API, region, i*10 +1, (i+1)*10)

        i -= 1300
        fool(API, 'jp1', i*10 +1, (i+1)*10)

    end = time.time()
    print(f"--- index range {a*10 +1} ~ {b*10} {end-start}s seconds ---")
    print("Done")