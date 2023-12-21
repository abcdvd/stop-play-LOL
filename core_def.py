import requests
from urllib.request import urlopen
from urllib.parse import quote
import pandas as pd
import urllib.request, json
import urllib
from bs4 import BeautifulSoup
import numpy as np
import time

def read_buffer(response):
    response.text = response.read()
    return response


def summoner_info_by_name(API_KEY, name, region):
    username = quote(name)
    url = f"https://{region}.api.riotgames.com/lol/summoner/v4/summoners/by-name/{username}?api_key={API_KEY}"
    with urlopen(url) as url:
        profile = json.loads(url.read().decode())
    return profile


def summoner_info_by_summonerId(API_KEY, ID, region):
    ID = quote(ID)
    url = f"https://{region}.api.riotgames.com/lol/summoner/v4/summoners/{ID}?api_key={API_KEY}"
    with urlopen(url) as url:
        profile = json.loads(url.read().decode())
    return profile


def summoner_info_by_puuid(API_KEY, puuid):
    url = "https://kr.api.riotgames.com/lol/summoner/v4/summoners/by-puuid/" + puuid + '?api_key=' + API_KEY
    with urlopen(url) as url:
        profile = json.loads(url.read().decode())
    return profile


def get_matchID_by_puuid(API_KEY, puuid, start, count, region, endTime=''):
    # endTime format : 'endTime=1651224583&'
    # input : API_KEY(str), puuid(str), start(int), count(int)
    # output : match_id(list)
    translator = {"kr":"asia", "jp1":"asia", "na1":"americas", "la1":"americas", "la2":"americas"}
    continent = translator[region]
    match_url = f"https://{continent}.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?{endTime}type=ranked&start={str(start)}&count={str(count)}&api_key={API_KEY}"
    with urllib.request.urlopen(match_url) as url:
        match_id = json.loads(url.read().decode())
    return match_id


def get_matchINFO_by_matchID(API_KEY, matchID, region):
    translator = {"kr":"asia", "jp1":"asia", "na1":"americas", "la1":"americas", "la2":"americas"}
    continent = translator[region]
    game_history_url = f"https://{continent}.api.riotgames.com/lol/match/v5/matches/{matchID}?api_key={API_KEY}"
    with urllib.request.urlopen(game_history_url) as url:
        matchINFO = json.loads(url.read().decode())
    return matchINFO

def get_matchTimeLine_by_matchID(API_KEY, matchID, region):
    translator = {"kr":"asia", "jp1":"asia", "na1":"americas", "la1":"americas", "la2":"americas"}
    continent = translator[region]
    game_history_url = f"https://{continent}.api.riotgames.com/lol/match/v5/matches/{matchID}/timeline?api_key={API_KEY}"
    with urllib.request.urlopen(game_history_url) as url:
        matchINFO = json.loads(url.read().decode())
    return matchINFO

def collect_summonerprofile(API_KEY, region, tier, division, page):
    division_to_rome = {1:'I', 2:"II", 3:"III", 4:"IV"}
    division = division_to_rome[division]
    URL = "https://"+region+".api.riotgames.com/lol/league/v4/entries/RANKED_SOLO_5x5/"+tier+"/"+division+"?page=" + page + "&api_key=" + API_KEY
    with urllib.request.urlopen(URL) as URL:
        response = json.loads(URL.read().decode())
    return response


def spectator(API_KEY, Id, region):
    spectator_url = f"https://{region}.api.riotgames.com/lol/spectator/v4/active-games/by-summoner/{Id}?api_key={API_KEY}"
    with urllib.request.urlopen(spectator_url) as url:
        profile = json.loads(url.read().decode())
    return profile


def recent_game_5_win_rate(username):
    username = quote(username)
    url = 'https://fow.kr/find/'+username

    # Give 5 chances to avoid error
    for C in range(5):
        try:
            tables = pd.read_html(url)
            time.sleep(1)
            sta = tables[-2]
            recent_game_5 = sta['승'].head()
            try:
                recent_win_rate = recent_game_5.value_counts()['승'] / 5 * 100
                return recent_win_rate
            except:
                return 0
        except:
            pass
    print('def recent_game_5_win_rate   NOT WORKED')
    return np.nan

def analyse_latest_position_history_RIOTAPI(API_KEY, puuid, match_list, position, region):
    # input : match_list(list), position(str)('TOP', 'JUNGLE', 'MID', 'BOTTOM', 'SUPPORT'), region(str)
    # output : appropriate_data(list)
    translator = {"TOP":1, "JUNGLE":2, "MID":3, "BOTTOM":4, "TOP":5, 
                "kr":"asia", "jp1":"asia", "na1":"americas", "la1":"americas", "la2":"americas"}
    numeric = translator[position]
    continent = translator[region]

    count = 0  # prevent the situation dividing with 0
    for target_matchId in match_list:
        URL = f'https://{continent}.api.riotgames.com/lol/match/v5/matches/{target_matchId}?api_key={API_KEY}'
        
        with urllib.request.urlopen(URL) as URL:
            match = json.loads(URL.read().decode())
        iNdex = match['metadata']['participants'].index(puuid)

        WinRate, kills, deaths, assists, totalDamageDealtToChampions, totalDamageTaken, totalHealsOnTeammates, wardsPlaced, visionScore = 0,0,0,0,0,0,0,0,0
        
        hot_watch = match['info']['participants'][iNdex]
        condition = match['info']['gameMode'] == 'CLASSIC' and match['info']['gameType' ] == 'MATCHED_GAME'
        
        if numeric == iNdex and condition:
            kills += hot_watch['kills']
            deaths += hot_watch['deaths']
            assists += hot_watch['assists']
            totalDamageDealtToChampions += hot_watch['totalDamageDealtToChampions']
            totalDamageTaken += hot_watch['totalDamageTaken']
            totalHealsOnTeammates += hot_watch['totalHealsOnTeammates']
            wardsPlaced += hot_watch['wardsPlaced']
            visionScore += hot_watch['visionScore']
            
            if hot_watch['win']==True:
                WinRate += 1
            count += 1
    
    saVe = [WinRate, kills, deaths, assists, totalDamageDealtToChampions, totalDamageTaken, totalHealsOnTeammates, wardsPlaced, visionScore]
    if count != 0:
        appropriate_data = list(map(lambda i:i/count, saVe))
        appropriate_data.insert(0, count)
        return appropriate_data
    else:
        saVe.insert(0, count)
        return appropriate_data


def get_player_champion_statistic_RIOTAPI_OPGG(API_KEY, username, region, Id, championId, ChampName):
    # input : championId(int)
    # output (dict) : [total_champions_mastery_levels, Champion_mastery_points, Champion, Num Win, Num Lose, WinRate, Avg Kills, Avg Deaths, Avg Assists, KDA, Gold, CS, Avg Damage Dealt, Avg Damage Taken, Num Double Kills, Num Tripple Kills, Num Quadra Kills, Num Penta Kills]
    dic = {}
    URL = f'https://{region}.api.riotgames.com/lol/champion-mastery/v4/champion-masteries/by-summoner/{Id}?api_key={API_KEY}'
    with urllib.request.urlopen(URL) as url:
        ChampionMasteryDto = json.loads(url.read().decode())

    total_champions_mastery_levels = 0
    for element in ChampionMasteryDto:
        total_champions_mastery_levels += element['championLevel']
        if element['championId'] == championId:
            dic['Champion_mastery_points'] = element['championPoints']

    dic['total_champions_mastery_levels'] = total_champions_mastery_levels

    name = quote(username)
    url = 'https://www.op.gg/summoners/' + region + '/' + name + '/champions'
    q = urlopen(url)
    soup = BeautifulSoup(q.read(), 'html.parser')
    objects = soup.find('div', 'content')

    objects = objects.find_all('td')

    bucket = []
    for i, obj in enumerate(objects):
        bucket.append(obj.text)
        if (i+1) % 15 == 0:
            bucket.pop(0)
            bucket.pop(0)
            if bucket[0] ==ChampName:
                break
            bucket =[]

    dic['Champion'] = bucket[0]
    pasta = bucket[1]
    cond_one = 'W' in pasta
    cond_two = 'L' in pasta

    if cond_one and cond_two:
        W = pasta.index('W')
        L = pasta.index('L')
        dic['Num Win'] = float(pasta[:W])
        dic['Num Lose'] = float(pasta[W+1:L])
        dic['WinRate'] = float(pasta[L+1:-1])

    if cond_one and (not cond_two):
        W = pasta.index("W")
        dic['Num Win'] = float(pasta[:W])
        dic['Num Lose'] = 0.0
        dic['WinRate'] = 100.0

    if (not cond_one) and cond_two:
        L = pasta.index("L")
        dic['Num Win'] = 0.0
        dic['Num Lose'] = float(pasta[:L])
        dic['WinRate'] = 0.0

    kda = bucket[2]
    first = kda.find('/')
    end = kda.rfind('/')

    dic['Avg Kills'] = float(kda[:first-1])
    dic['Avg Deaths'] = float(kda[first+2:end-2])

    scap = kda[end+2:]
    first = scap.find('.')
    middle = scap.rfind('.')
    end = scap.rfind(':')
    dic['Avg Assists'] = float(scap[:first+2])
    dic['KDA'] = float(scap[first+2:end])


    dic['Gold'] = float(bucket[3].replace(",", ""))

    pos = bucket[4].find("(")
    dic['CS'] = float(bucket[4][:pos])
    dic['Avg Damage Dealt'] = float(bucket[7].replace(",", ""))
    dic['Avg Damage Taken'] = float(bucket[8].replace(",", ""))

    if bucket[9] == '':
        dic['Num Double Kills'] = 0.0
    else:
        dic['Num Double Kills'] = float(bucket[9])
        
    if bucket[10] == '':
        dic['Num Tripple Kills'] = 0.0
    else:
        dic['Num Tripple Kills'] = float(bucket[10])
        
    if bucket[11] == '':
        dic['Num Quadra Kills'] = 0.0
    else:
        dic['Num Quadra Kills'] = float(bucket[11])
        
    if bucket[12] == '':
        dic['Num Penta Kills'] = 0.0
    else:
        dic['Num Penta Kills'] = float(bucket[12])
    
    return dic

def analyse_current_match_data(data, index_name):

    # Blue team data
    df = data[0]

    train_Blue = pd.DataFrame()

    s1 = df['랭크 승률']
    s2 = df['S2022 챔피언 정보']
    s3 = df['S2022 챔피언 정보.1']

    s = []
    for string in s1:
        try:
            stone = string.find('%')
            s.append( float(string[:stone]) )

            stone = string.find('(')
            s.append( float(string[stone+1:-4]) )
        except:
            s.append(np.nan)
            s.append(np.nan)

    for string in s2:
        try:
            stone = string.find('%')
            s.append( float(string[:stone]) )

            stone = string.find('(')
            s.append( float(string[stone+1:-4]) )
        except:
            s.append(np.nan)
            s.append(np.nan)

    for string in s3:
        try:
            stone = string.find('KDA')
            s.append( float(string[:stone-1]) )

            first = string.find('/')
            second = string.rfind('/')
            s.append( float(string[stone+3:first-1]))
            s.append( float(string[first+2:second-1]))
            s.append( float(string[second+2:]))

        except:
            s.append(np.nan)
            s.append(np.nan)
            s.append(np.nan)
            s.append(np.nan)

    train_Blue[index_name] = pd.Series(s)

    index_a = ['Blue 1 total rank win rate', 'Blue 1 total rank n_game', 'Blue 2 total rank win rate', 'Blue 2 total rank n_game', 'Blue 3 total rank win rate', 'Blue 3 total rank n_game', 'Blue 4 total rank win rate', 'Blue 4 total rank n_game', 'Blue 5 total rank win rate', 'Blue 5 total rank n_game']
    index_b = ['Blue 1 champ rank win rate', 'Blue 1 champ rank n_game', 'Blue 2 champ rank win rate', 'Blue 2 champ rank n_game', 'Blue 3 champ rank win rate', 'Blue 3 champ rank n_game', 'Blue 4 champ rank win rate', 'Blue 4 champ rank n_game', 'Blue 5 champ rank win rate', 'Blue 5 champ rank n_game']
    index_c = ['Blue 1 KDA', 'Blue 1 K', 'Blue 1 D', 'Blue 1 A', 'Blue 2 KDA', 'Blue 2 K', 'Blue 2 D', 'Blue 2 A', 'Blue 3 KDA', 'Blue 3 K', 'Blue 3 D', 'Blue 3 A', 'Blue 4 KDA', 'Blue 4 K', 'Blue 4 D', 'Blue 4 A', 'Blue 5 KDA', 'Blue 5 K', 'Blue 5 D', 'Blue 5 A']
    index_Blue = index_a + index_b + index_c

    train_Blue.index = index_Blue



    # Red team data

    df = data[1]

    train_Red = pd.DataFrame()

    s1 = df['랭크 승률']
    s2 = df['S2022 챔피언 정보']
    s3 = df['S2022 챔피언 정보.1']

    s = []
    for string in s1:
        try:
            stone = string.find('%')
            s.append( float(string[:stone]) )

            stone = string.find('(')
            s.append( float(string[stone+1:-4]) )
        except:
            s.append(np.nan)
            s.append(np.nan)

    for string in s2:
        try:
            stone = string.find('%')
            s.append( float(string[:stone]) )

            stone = string.find('(')
            s.append( float(string[stone+1:-4]) )
        except:
            s.append(np.nan)
            s.append(np.nan)

    for string in s3:
        try:
            stone = string.find('KDA')
            s.append( float(string[:stone-1]) )

            first = string.find('/')
            second = string.rfind('/')
            s.append( float(string[stone+3:first-1]))
            s.append( float(string[first+2:second-1]))
            s.append( float(string[second+2:]))

        except:
            s.append(np.nan)
            s.append(np.nan)
            s.append(np.nan)
            s.append(np.nan)

    train_Red[index_name] = pd.Series(s)

    index_Red = []
    for string in index_Blue:
        index_Red.append(string.replace('Blue', 'Red'))

    train_Red.index = index_Red

    train = pd.concat([train_Blue, train_Red])
    return train



def fow_watcher(API_KEY):

    html = urlopen("https://fow.kr/specs")
    bsObject = BeautifulSoup(html, "html.parser")

    semi = []
    for name in bsObject.find_all("a"):
        semi.append(name.text)

    start = semi.index("모든 챔피언")
    end = semi.index("이용약관")

    count = 1
    n_game = 1
    data = {"Blue 1":[], "Blue 2":[], "Blue 3":[], "Blue 4":[], "Blue 5":[], "Red 1":[], "Red 2":[], "Red 3":[], "Red 4":[], "Red 5":[]}

    for name in semi[start+1:end]:

        if name != "관전하기":
            if count < 6:
                data[f"Blue {count}"].append(name)
            else:
                data[f"Red {count-5}"].append(name)

            if count == 10:
                count = 0
                

            count += 1

    df = pd.DataFrame(data)

    # match ID를 기록한다.
    id_list = []
    for i in range(len(df)):
        username = df.iloc[i][0]
        Id = summoner_info_by_name(API_KEY, username)['id']
        print('Collect match Id Success !')

        try:
            profile = spectator(API_KEY, Id)
            id_list.append("KR_" + str(profile["gameId"]))
            print('    RIOT API positive !')
        except:
            print('    Respose from RIOT API negative !!')
            id_list.append(np.nan)

    df["gameId"] = id_list

    return df

