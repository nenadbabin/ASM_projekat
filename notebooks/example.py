# %%

# Imports
import pandas as pd
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt

# %%

# Path strings
data_path_atp_matches_2018 = "data/atp_matches_2018.csv"
data_path_atp_matches_2019 = "data/atp_matches_2019.csv"
data_path_atp_matches_2020 = "data/atp_matches_2020.csv"
data_path_atp_players = "data/atp_players.csv"
data_path_atp_rankings_10s = "data/atp_rankings_10s.csv"
data_path_atp_rankings_current = "data/atp_rankings_current.csv"

# Load data
data_atp_matches_2018 = pd.read_csv(data_path_atp_matches_2018)
data_atp_matches_2019 = pd.read_csv(data_path_atp_matches_2019)
data_atp_matches_2020 = pd.read_csv(data_path_atp_matches_2020)
data_atp_players = pd.read_csv(data_path_atp_players)
data_atp_rankings_10s = pd.read_csv(data_path_atp_rankings_10s)
data_atp_rankings_current = pd.read_csv(data_path_atp_rankings_current)

# %%

# Remove unnecessary columns
data_atp_matches_2020 = data_atp_matches_2020.drop(['tourney_id',
                                                    'tourney_name',
                                                    'surface',
                                                    'draw_size',
                                                    'tourney_level',
                                                    'tourney_date',
                                                    # 'match_num',
                                                    # 'winner_id',
                                                    'winner_seed',
                                                    'winner_entry',
                                                    'winner_name',  # ne moramo da pamtimo jer to imamo u posbnoj tabeli
                                                    'winner_hand',
                                                    'winner_ht',
                                                    'winner_ioc',
                                                    'winner_age',
                                                    # 'loser_id',
                                                    'loser_seed',
                                                    'loser_entry',
                                                    'loser_name',  # ne moramo da pamtimo jer to imamo u posbnoj tabeli
                                                    'loser_hand',
                                                    'loser_ht',
                                                    'loser_ioc',
                                                    'loser_age',
                                                    'score',
                                                    'best_of',
                                                    'round',
                                                    'minutes',
                                                    'w_ace',
                                                    'w_df',
                                                    'w_svpt',
                                                    'w_1stIn',
                                                    'w_1stWon',
                                                    'w_2ndWon',
                                                    'w_SvGms',
                                                    'w_bpSaved',
                                                    'w_bpFaced',
                                                    'l_ace',
                                                    'l_df',
                                                    'l_svpt',
                                                    'l_1stIn',
                                                    'l_1stWon',
                                                    'l_2ndWon',
                                                    'l_SvGms',
                                                    'l_bpSaved',
                                                    'l_bpFaced',
                                                    'winner_rank',
                                                    'winner_rank_points',
                                                    'loser_rank',
                                                    'loser_rank_points'], axis=1)

# %%

print("Rows: {}".format(data_atp_matches_2020.shape[0]))
print("Columns: {}".format(data_atp_matches_2020.shape[1]))

# Check if match_num is unique
print("data_atp_matches_2020 - is match_num null? {}".format(data_atp_matches_2020['match_num'].isnull().values.any()))
print("data_atp_matches_2020 - is match_num unique? {}".format(data_atp_matches_2020['match_num'].is_unique))

print(data_atp_players.dtypes)

# %%

# match_num nam nije unique, tako da treba da dodamo neku unique kolonu i obrisemo match_num kolonu

data_atp_matches_2020 = data_atp_matches_2020.drop(['match_num'], axis=1)
data_atp_matches_2020['id'] = data_atp_matches_2020.index

# %%

winners = set(data_atp_matches_2020['winner_id'])
losers = set(data_atp_matches_2020['loser_id'])

players = winners.union(losers)

print("Number of players: {}".format(len(players)))

# %%

G = nx.Graph()

column_labels = ['player_id', 'first_name', 'last_name']
selected_players_data = data_atp_players[column_labels]

# Create nodes with players' names
for player_id in players:
    mask = selected_players_data['player_id'] == str(player_id)
    db_player = selected_players_data[mask]
    name = db_player['first_name'].values[0] + " " + db_player['last_name'].values[0]
    G.add_node(player_id, name=name)

# Create graph with weights
for _, winner_id, loser_id in data_atp_matches_2020[['winner_id', 'loser_id']].itertuples():
    if (winner_id, loser_id) in G.edges:
        G.edges[winner_id, loser_id]['weight'] += 1
    else:
        G.add_edge(winner_id, loser_id, weight=1)

# %%

output_path = "models/matches_2020_undirected_weights.gml"

nx.write_gml(G, output_path)
