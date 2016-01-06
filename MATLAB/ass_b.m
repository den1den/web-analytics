% First read in the matrixes G and Gs as the connectivity matrix and
% sparse connectivity matrix.
folder = 'PageRank';
edges = dlmread([folder '/edges.txt']);
% if you take edge_i = edges(1,:); (i>0)
% then node `edge_i(1)` has a link towardse node `edge_i(2)`
edges_a = edges(:,1);
edges_b = edges(:,2);
nodes = dlmread([folder '/nodes.txt']);
% nodes(2,i) is the class of node i (i>0), and nodes(1,i) == i
% nodes is a n by 2 vector, thus the size is the first dimension
n = size(nodes, 1);
% matrix Gs is a sparse matrix with g(edges_a(i), edges_b(i)) == 1 for all i
G = sparse(edges_a, edges_b, 1, n, n);
nds = [sum(G, 1)' sum(G,2)];
%nds(1,1) = out degree of site 1, nds(1,2) = in degree of site 1

% CONSTANTS
% p is the chance on clicking a link instead of a random page
p = 0.85;
seed = 12345678;
abstol = 10^-4;
max_it = 10^4;
teleport = true;
alg = @(G) pagerank_power_sparse_v1(G, p, size(G,1), teleport, abstol, max_it);

remove_edges = 200;
remove_nodes = 20;

G_1 = ev_edges_uniform(G, seed, remove_edges);
[G_2, rm_2] = ev_nodes_uniform(G, seed, remove_nodes, 0);
G_3 = ev_edges_nonuniform_v1(G, seed, nds, remove_edges);
[G_4, rm_4] = ev_nodes_nonuniform_v1(G, seed, remove_nodes);

x = alg(G); %x(1) == pagerank van site 1
[pr_0, site_ids] = sort(x, 'descend'); rk_0 = (1:size(x))';
x_1 = alg(G_1);
x_2 = alg(G_2); x_2 = insert_empty(x_2, rm_2);
x_3 = alg(G_3);
x_4 = alg(G_4); x_4 = insert_empty(x_4, rm_4);



pr_1 = x_1(site_ids);
[~, rk_1] = sort(x_1); rk_1(site_ids);
pr_2 = x_2(site_ids);
[~, rk_2] = sort(x_2); rk_2(site_ids);
pr_3 = x_3(site_ids);
[~, rk_3] = sort(x_3); rk_3(site_ids);
pr_4 = x_4(site_ids);
[~, rk_4] = sort(x_4); rk_4(site_ids);

header = ['id' 'pr' 'rk' 'pr_edges_uniform' 'rk' 'pr_nodes_uniform' 'rk' ...
    'pr_edges_nuniform' 'rk' 'pr_nodes_nonuniform' 'rk'];
table = [site_ids pr_0 rk_0 pr_1 rk_1 pr_2 rk_2 pr_3 rk_3 pr_4 rk_4];
csvwrite('ass_b_table.csv', table);
csvwrite('ass_b_remove_edges.csv', remove_edges);

break