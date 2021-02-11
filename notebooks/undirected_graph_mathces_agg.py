# Imports
import pandas as pd
import networkx as nx
from notebooks.utility import add_player_node, get_ranking_data, year_string_to_enum, calculate_centralities, \
    players_nationalities, get_points_data, get_all_players, calculate_sum_of_differences, calculate_graph_centralities
import collections
import matplotlib.pyplot as plt
import numpy as np

G = nx.Graph()

data_path_atp_players = "../data/atp_players.csv"
data_atp_players = pd.read_csv(data_path_atp_players)

data_atp_players['player_id'].apply(pd.to_numeric)  # inace posmatra kao string
column_labels = ['player_id', 'first_name', 'last_name', 'country_code', 'hand']
selected_players_data = data_atp_players[column_labels]

for YEAR in ["2018", "2019", "2020"]:
    # Path strings
    data_path_atp_matches = "../data/atp_matches_" + YEAR + "_cleaned.csv"

    # Load data
    data_atp_matches = pd.read_csv(data_path_atp_matches)

    # Remove unnecessary columns
    data_atp_matches = data_atp_matches.drop([
                                            # 'tourney_id',
                                            #  'tourney_name',
                                            #  'surface',
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

    # match_num nam nije unique, tako da treba da dodamo neku unique kolonu i obrisemo match_num kolonu
    data_atp_matches = data_atp_matches.drop(['match_num'], axis=1)
    data_atp_matches['id'] = data_atp_matches.index

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
            G.add_edge(winner_id, loser_id, weight=1, y2018=0, y2019=0, y2020=0)
        G.edges[winner_id, loser_id]["y"+YEAR] += 1



# Centralnosti - pitanje 4
df_centralities, DC_dict, CC_dict, BC_dict, EVC_dict = calculate_centralities(G)
df_centralities.to_excel("../models/centralities_undirected_agg.xls")

# Broj igraca po nacionalnosti - pitanje 6
df_nationalities = players_nationalities(G)
df_nationalities_grouped = df_nationalities.groupby(['country_code']).agg(['count'])
df_nationalities_grouped.to_excel("../models/nationalities_undirected_agg.xls")

# Igraci sa brojem osvojenih poena na kraju godine - pitanje 7
# data_all_players = get_all_players()
# df_atp_points_end_of_year = get_points_data(year_string_to_enum(YEAR), data_all_players)
# df_atp_points_end_of_year.to_excel("../models/atp_points_undirected_agg.xls")

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

plt.savefig("../pics/degree_histogram_agg.png")

#%%
plt.clf()
plt.close()

degree_list = []
avg_rank_list = []
for node, node_data in G.nodes.items():
    degree = G.degree[node]
    avg_rank = node_data['avg_rank']
    if avg_rank == -1:
        continue
    degree_list.append(degree)
    avg_rank_list.append(avg_rank)

plt.title("Degree Rank Correlation")
plt.ylabel("Rank")
plt.xlabel("Degree")
plt.scatter(degree_list, avg_rank_list)
# plt.show()
plt.savefig("../pics/degree_rank_correlation_agg.png")
#%%

n = G.number_of_nodes()
m = G.number_of_edges()
p = (2*float(m)) / (n*(n-1))
er_graph = nx.erdos_renyi_graph(n, p)
er_output_path = "../models/random_er_graph_agg.gml"
nx.write_gml(er_graph, er_output_path)

#%%


n = G.number_of_nodes()
m = G.number_of_edges()
ba_graph = nx.barabasi_albert_graph(n, 6)
ba_output_path = "../models/random_ba_graph_agg.gml"
nx.write_gml(ba_graph, ba_output_path)

#%%

giantG = max((G.subgraph(c) for c in nx.connected_components(G)), key=len)
giantER = max((er_graph.subgraph(c) for c in nx.connected_components(er_graph)), key=len)
L = nx.average_shortest_path_length(giantG)
Lr = nx.average_shortest_path_length(giantER)
C = nx.average_clustering(giantG)
Cr = nx.average_clustering(giantER)

sigma = (C / Cr) / (L / Lr)
print("Sigma: {}".format(sigma))

#%%

roger_federer_node = [x for x, y in G.nodes(data=True) if y['name'] == "Roger Federer"][0]
rafael_nadal_node = [x for x, y in G.nodes(data=True) if y['name'] == "Rafael Nadal"][0]
novak_djokovic_node = [x for x, y in G.nodes(data=True) if y['name'] == "Novak Djokovic"][0]

roger_federer_ego_network = nx.ego_graph(G, roger_federer_node)
output_path_roger_federer_ego = "../models/roger_federer_ego_network_agg.gml"
nx.write_gml(roger_federer_ego_network, output_path_roger_federer_ego)

rafael_nadal_ego_network = nx.ego_graph(G, rafael_nadal_node)
output_path_rafael_nadal_ego = "../models/rafael_nadal_ego_network_agg.gml"
nx.write_gml(rafael_nadal_ego_network, output_path_rafael_nadal_ego)

novak_djokovic_ego_network = nx.ego_graph(G, novak_djokovic_node)
output_path_novak_djokovic_ego = "../models/novak_djokovic_ego_network_agg.gml"
nx.write_gml(novak_djokovic_ego_network, output_path_novak_djokovic_ego)

#%%
ego_networks_union = roger_federer_ego_network

for ego_network in [rafael_nadal_ego_network, novak_djokovic_ego_network]:

    for edge in ego_network.edges:
        player_1_id = int(edge[0])
        player_2_id = int(edge[1])
        if player_1_id not in ego_networks_union.nodes:
            add_player_node(ego_networks_union, player_1_id, selected_players_data, ranking_data)
        if player_2_id not in ego_networks_union.nodes:
            add_player_node(ego_networks_union, player_2_id, selected_players_data, ranking_data)

        edge_info = ego_network.edges[edge]
        if edge not in ego_networks_union.edges:
            ego_networks_union.add_edge(player_1_id, player_2_id, weight=edge_info['weight'])

output_path_ego_networks_union = "../models/big_3_ego_networks_union_agg.gml"
nx.write_gml(ego_networks_union, output_path_ego_networks_union)

#%%
# Upis grafa
output_path = "../models/matches_agg_undirected_weights.gml"
nx.write_gml(G, output_path)
