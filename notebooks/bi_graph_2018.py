# %%

# Imports
import pandas as pd
import networkx as nx
from notebooks.utility import add_player_node

# %%

# Path strings
data_path_atp_matches_2018 = "../data/atp_matches_2018.csv"
data_path_atp_players = "../data/atp_players.csv"

# Load data
data_atp_matches_2018 = pd.read_csv(data_path_atp_matches_2018)
data_atp_players = pd.read_csv(data_path_atp_players)

# %%

# Remove unnecessary columns
data_atp_matches_2018 = data_atp_matches_2018.drop([
                                                    # 'tourney_id',
                                                    # 'tourney_name',
                                                    # 'surface',
                                                    # 'draw_size',
                                                    # 'tourney_level',
                                                    # 'tourney_date',
                                                    # 'match_num',
                                                    # 'winner_id',
                                                    'winner_seed',
                                                    'winner_entry',
                                                    'winner_name',
                                                    'winner_hand',
                                                    'winner_ht',
                                                    'winner_ioc',
                                                    'winner_age',
                                                    # 'loser_id',
                                                    'loser_seed',
                                                    'loser_entry',
                                                    'loser_name',
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

print("Rows: {}".format(data_atp_matches_2018.shape[0]))
print("Columns: {}".format(data_atp_matches_2018.shape[1]))

# Check if match_num is unique
print("data_atp_matches_2018 - is match_num null? {}".format(data_atp_matches_2018['match_num'].isnull().values.any()))
print("data_atp_matches_2018 - is match_num unique? {}".format(data_atp_matches_2018['match_num'].is_unique))

print(data_atp_players.dtypes)

# %%

# match_num nam nije unique, tako da treba da dodamo neku unique kolonu i obrisemo match_num kolonu

data_atp_matches_2018 = data_atp_matches_2018.drop(['match_num'], axis=1)
data_atp_matches_2018['id'] = data_atp_matches_2018.index

# %%
G = nx.DiGraph()

grouped_by_tournaments = data_atp_matches_2018[['tourney_id', 'tourney_name', 'tourney_level', 'tourney_date',
                                                'surface', 'draw_size']].groupby(by=['tourney_id', 'tourney_name'])

tournaments = grouped_by_tournaments.groups.keys()

for tourney_id, tourney_name in tournaments:
    if "Davis Cup" in tourney_name:
        tourney_id = "2018 Davis Cup"
        tourney_name = "Davis Cup"
    G.add_node(tourney_id, tourney_name=tourney_name)

column_labels = ['player_id', 'first_name', 'last_name', 'country_code', 'hand']
selected_players_data = data_atp_players[column_labels]

# Create graph with weights
for _, winner_id, loser_id, tourney_id, tourney_name in data_atp_matches_2018[['winner_id', 'loser_id', 'tourney_id',
                                                                               'tourney_name']].itertuples():
    if "Davis Cup" in tourney_name:
        tourney_id = "2018 Davis Cup"
        tourney_name = "Davis Cup"

    if winner_id not in G.nodes:
        add_player_node(G, winner_id, selected_players_data)
    if loser_id not in G.nodes:
        add_player_node(G, loser_id, selected_players_data)

    if (winner_id, tourney_id) in G.edges:
        G.edges[winner_id, tourney_id]['weight'] += 1
    else:
        G.add_edge(winner_id, tourney_id, weight=1)

    if (loser_id, tourney_id) in G.edges:
        G.edges[loser_id, tourney_id]['weight'] += 1
    else:
        G.add_edge(loser_id, tourney_id, weight=1)

# %%

output_path = "../models/matches_2018_digraph_davis_cup.gml"

nx.write_gml(G, output_path)
