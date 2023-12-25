# stop-play-LOL


# league-of-legends-winner-predicting
## Use Riot API to predict LOL winner
리그 오브 레전드는 15분부터 항복 투표를 할 수 있다. 항복한 후 AI 분석 결과를 플레이어들에게 공개하면 재미있을 거 같아 이 프로젝트를 진행했다.
먼저 게임 시작 후 15분 시점에 누가 이길지 예측해야 한다.
내 생각에 이 게임의 승리를 예측하는 방법에는 3가지가 있다.

### 계획
1. 게임 시작 후 **T+10** 시점의 데이터로 승리를 예측한다.
2. **[1<= T <= 13]** 1분 간격의 데이터로 예측한다. 
3. **[T+5, T+10, T+15]** 5분 간격의 데이터를 RNN 계열 모델을 통해 승리를 예측한다.
4. **[1<= T <=15]** 더 촘촘한 1분 간격의 sequential 데이터를 활용한다.

### 과정

첫번째 방법은 Kaggle에서 이미 공개된 데이터가 있지만 두번째와 세번째 데이터는 공개된적이 없다. 그래서 **Riot 공식 API**를 이용했다.
**Riot API**를 통해 현재 각 서버의 해당 티어에 속한 **Summoner list**들을 수집할 수 있었고 각 **Summoner**의 과거 **Match List**를 얻을 수 있었고 **MatchId**를 통해 해당 **Match**의 분단위 상세한 데이터도 얻을 수 있게 되었다.

분석에 사용할 변수는 각 라인별로 레벨 차이, 골드 차이, 와드 차이를 고려할 것이다. 그 이유는 첫번째 방법을 통해 이 데이터들이 유효했음을 알기 때문이다.

**Riot API**에는 **request rate limit**가 걸려 있어서 데이터를 얻을 수 있는 속도가 한정적이다. 속도를 초과하면 18초의 **Ban**을 당한다. 따라서 시간 규칙을 지켜가며 데이터를 수집했다.



### 결과

1. 첫번째 방법은 이미 Kaggle에서 분석된적이 있었다. (https://www.kaggle.com/bobbyscience/league-of-legends-diamond-ranked-games-10-min). 이 데이터로는 **71%** 의 정확도를 보였다.

2. 수집한 11,274개의 match 데이터를 직접 수집 후 Kaggle에 공개했다. **75%** 의 정확도를 보였다.
   데이터 : https://www.kaggle.com/datasets/imajne/leage-of-legends-in-game-data-every-1-miniute/data   
   LSTM 코드 : https://www.kaggle.com/code/imajne/lol-lstm-1-13min

3. 수집한 11,348개의 match 데이터를 직접 수집 후 Kaggle에 공개했다. **75%** 정도의 정확도를 보였다.  
   데이터 : https://www.kaggle.com/datasets/imajne/league-of-legends-in-game-data-every-5-min/data  
   LSTM 코드 : https://www.kaggle.com/code/imajne/lol-v1-lstm-roughly-normalized

4. 수집한 11,274개의 match 데이터를 직접 수집 후 Kaggle에 공개했다. **76%** 의 정확도를 보였다.   
   데이터 : https://www.kaggle.com/datasets/imajne/leage-of-legends-in-game-data-every-1-miniute/data   
   LSTM 코드 : https://www.kaggle.com/code/imajne/lol-lstm-1-15min


### 기록


    2022 05 06 입대 전
    kr, jp1, na1, la1, la2의 0~500 범위의 데이터 수집 (다이아) 7,376 초가 걸렸다.
    kr, na1, la1, la2의 501~700 범위의 데이터 수집
    
    kr na1, la1, la2의 7000 ~ 8000 범의의 데이터 수집 (플레티넘) 19,201 초가 걸렸다.
    jp1 의 400~1400 범위의 데이터를 수집

