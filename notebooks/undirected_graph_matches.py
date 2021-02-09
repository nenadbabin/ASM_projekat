# Imports
import pandas as pd
import networkx as nx
from notebooks.utility import add_player_node, get_ranking_data, year_string_to_enum, calculate_centralities, \
    players_nationalities, get_points_data, get_all_players, calculate_sum_of_differences, calculate_graph_centralities
import collections
import matplotlib.pyplot as plt

YEAR = "2018"

# Path strings
data_path_atp_matches = "../data/atp_matches_" + YEAR + "_cleaned.csv"
data_path_atp_players = "../data/atp_players.csv"

# Load data
data_atp_matches = pd.read_csv(data_path_atp_matches)
data_atp_players = pd.read_csv(data_path_atp_players)

# Remove unnecessary columns
data_atp_matches = data_atp_matches.drop(['tourney_id',
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

print("Rows: {}".format(data_atp_matches.shape[0]))
print("Columns: {}".format(data_atp_matches.shape[1]))

# Check if match_num is unique
print("data_atp_matches - is match_num null? {}".format(data_atp_matches['match_num'].isnull().values.any()))
print("data_atp_matches - is match_num unique? {}".format(data_atp_matches['match_num'].is_unique))

print(data_atp_players.dtypes)

# match_num nam nije unique, tako da treba da dodamo neku unique kolonu i obrisemo match_num kolonu
data_atp_matches = data_atp_matches.drop(['match_num'], axis=1)
data_atp_matches['id'] = data_atp_matches.index

G = nx.Graph()

data_atp_players['player_id'].apply(pd.to_numeric)   # inace posmatra kao string
column_labels = ['player_id', 'first_name', 'last_name', 'country_code', 'hand']
selected_players_data = data_atp_players[column_labels]

ranking_data = get_ranking_data(year_string_to_enum(YEAR))

# Create graph with weights
for _, winner_id, loser_id in data_atp_matches[['winner_id', 'loser_id']].itertuples():
    if winner_id not in G.nodes:
        add_player_node(G, winner_id, selected_players_data, ranking_data)
    if loser_id not in G.nodes:
        add_player_node(G, loser_id, selected_players_data, ranking_data)

    if (winner_id, loser_id) in G.edges:
        G.edges[winner_id, loser_id]['weight'] += 1
    else:
        G.add_edge(winner_id, loser_id, weight=1)

# Centralnosti - pitanje 4
df_centralities, DC_dict, CC_dict, BC_dict, EVC_dict = calculate_centralities(G)
df_centralities.to_excel("../models/centralities_undirected_" + YEAR + ".xls")

# Broj igraca po nacionalnosti - pitanje 6
df_nationalities = players_nationalities(G)
df_nationalities_grouped = df_nationalities.groupby(['country_code']).agg(['count'])
df_nationalities_grouped.to_excel("../models/nationalities_undirected_" + YEAR + ".xls")

# Igraci sa brojem osvojenih poena na kraju godine - pitanje 7
data_all_players = get_all_players()
df_atp_points_end_of_year = get_points_data(year_string_to_enum(YEAR), data_all_players)
df_atp_points_end_of_year.to_excel("../models/atp_points_undirected_" + YEAR + ".xls")

# Asortativnost - pitanje 10
assortativity_country = nx.attribute_assortativity_coefficient(G, "country_code")
assortativity_avg_rank = nx.numeric_assortativity_coefficient(G, "rank_class")
assortativity_degree_weighted = nx.degree_assortativity_coefficient(G, weight="weight")
assortativity_degree = nx.degree_assortativity_coefficient(G)

print("assortativity_country: {}".format(assortativity_country))
print("assortativity_avg_rank: {}".format(assortativity_avg_rank))
print("assortativity_degree_weighted: {}".format(assortativity_degree_weighted))
print("assortativity_degree: {}".format(assortativity_degree))

# pitanje 11
average_edge_weight = G.size(weight='weight') / G.size()
print("average_edge_weight: {}".format(average_edge_weight))

# pitanje 14
graph_density = nx.density(G)
print("graph_density: {}".format(graph_density))

# pitanje 15
network_DC, network_CC, network_BC = calculate_graph_centralities(G, DC_dict, CC_dict, BC_dict)

print("network_DC: {}". format(network_DC))
print("network_CC: {}". format(network_CC))
print("network_BC: {}". format(network_BC))

# pitanje 16
# diameter = nx.diameter(G)
# avg_path_length = nx.average_shortest_path_length(G)
#
# print("Diameter: {}".format(diameter))
# print("Average path length: {}".format(avg_path_length))

# pitanje 17
degree_sequence = sorted([d for n, d in G.degree()], reverse=True)  # degree sequence
degreeCount = collections.Counter(degree_sequence)
deg, cnt = zip(*degreeCount.items())

fig, ax = plt.subplots()
plt.bar(deg, cnt, width=0.80, color="b")

plt.title("Degree Histogram")
plt.ylabel("Count")
plt.xlabel("Degree")
ax.set_xticks([d + 0.4 for d in deg])
ax.set_xticklabels(deg)

# draw graph in inset
plt.axes([0.4, 0.4, 0.5, 0.5])
Gcc = G.subgraph(sorted(nx.connected_components(G), key=len, reverse=True)[0])
pos = nx.spring_layout(G)
plt.axis("off")
nx.draw_networkx_nodes(G, pos, node_size=20)
nx.draw_networkx_edges(G, pos, alpha=0.4)
# plt.show()

plt.savefig("../pics/degree_histogram_" + YEAR + ".png")

G.degree

# Upis grafa
output_path = "../models/matches_" + YEAR + "_undirected_weights.gml"

nx.write_gml(G, output_path)
