%
%CONSTANTS and INITIALIZATION
%
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

% the chance on clicking a link instead of a random page
p = 0.85;

% the chance on landing on a specific page
delta = (1 - p) / n;

% matrix G is a sparse matrix with g(edges_a(i), edges_b(i)) == 1 for all i
Gs = sparse(edges_a, edges_b, 1, n, n);
G = full(Gs);

[x_pms, pms_sec] = power_method_sparse_v1(Gs, n, p);
[x_pmn, pmn_sec] = power_method_not_v1(G, n, p);

assert_same_vector(x_pms, x_pmn, 1^-10);

pms_sec
pmn_sec

%y = @(x) x*2;
