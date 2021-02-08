import pandas as pd

for YEAR in ["2018", "2019", "2020"]:
    data_path_atp_matches = "../data/atp_matches_" + YEAR + ".csv"

    data_atp_matches = pd.read_csv(data_path_atp_matches)
    data_atp_matches = data_atp_matches.drop_duplicates(keep="first")

    data_atp_matches.to_csv("../data/atp_matches_" + YEAR + "_cleaned.csv", index=False)

data_path_atp_players = "../data/atp_players.csv"

path_atp_rankings_10s = "../data/atp_rankings_10s.csv"
path_atp_rankings_current = "../data/atp_rankings_current.csv"

atp_rankings_10s = pd.read_csv(path_atp_rankings_10s)
atp_rankings_current = pd.read_csv(path_atp_rankings_current)

atp_rankings_10s = atp_rankings_10s.drop_duplicates(keep="first")
atp_rankings_current = atp_rankings_current.drop_duplicates(keep="first")

atp_rankings_10s.to_csv("../data/atp_rankings_10s_cleaned.csv", index=False)
atp_rankings_current.to_csv("../data/atp_rankings_current_cleaned.csv", index=False)

atp_players = pd.read_csv(data_path_atp_players)
print("atp_players - is player_id null? {}".format(atp_players['player_id'].isnull().values.any()))
print("atp_players - is player_id unique? {}".format(atp_players['player_id'].is_unique))
