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
abstol = 10^-4;
max_it = 10^4;
teleport = true;
alg = @(G) pagerank_power_sparse_v1(G, p, size(G,1), teleport, abstol, max_it);
REPEAT = 200;
N = 20;

%calculate the baseline (and determine the ordering)
x = alg(G); %x(1) == pagerank van site 1
[pr_0, order] = sort(x, 'descend'); rk_0 = (1:size(x))';

result1 = [];
result2 = [];
result3 = [];
result4 = [];

for n = 1: N;
    %define what to do with the edges
    remove_edges = N*2;
    remove_nodes = N;
    
    pr_1 = []; rk_1 = []; pr_2 = []; rk_2 = []; pr_3 = []; rk_3 = [];
    pr_4 = []; rk_4 = [];
    er1 = []; er2 = []; er3 = []; er4 = [];
    ep1 = []; ep2 = []; ep3 = []; ep4 = [];

    %repeat it a couple of times with different seeds
    for repeat = 1: REPEAT;
        seed = repeat+123456789;
        
        %remove edges uniformly
        G_1 = ev_edges_uniform(G, seed, remove_edges);
        x_1 = alg(G_1);
        
        %remove nodes uniformly
        [G_2, rm_2] = ev_nodes_uniform(G, seed, remove_nodes, 0);
        x_2 = alg(G_2); x_2 = insert_empty(x_2, rm_2);
        
        %remove edges non uniformly
        G_3 = ev_edges_nonuniform_v1(G, seed, nds, remove_edges);
        x_3 = alg(G_3);
        
        %remove nodes non uniformly
        [G_4, rm_4] = ev_nodes_nonuniform_v1(G, seed, remove_nodes);
        x_4 = alg(G_4); x_4 = insert_empty(x_4, rm_4);
        
        %order output and fill deleted nodes with zero's
        pr_1 = [pr_1 x_1(site_ids)];
        [~, rk] = sort(x_1); rk(site_ids);
        rk_1 = [rk_1 rk];
        pr_2 = [pr_2 x_2(site_ids)];
        [~, rk] = sort(x_2); rk(site_ids);
        rk_2 = [rk_2 rk];
        pr_3 = [pr_3 x_3(site_ids)];
        [~, rk] = sort(x_3); rk(site_ids);
        rk_3 = [rk_3 rk];
        pr_4 = [pr_4 x_4(site_ids)];
        [~, rk] = sort(x_4); rk(site_ids);
        rk_4 = [rk_4 rk];
    end
    
    Ns = ones(size(order, 1))*n;
    result1 = [result1; order pr_0 rk_0 Ns pr_0 rk_0 pr_1 rk_1 pr_2 rk_2 pr_3 rk_3 pr_4 rk_4];
    %result2 = [result2; order Ns er1 ep1 er2 ep2 er3 ep3 er4 ep4];
end

csvwrite('ass_b_result1.csv', result1);
%csvwrite('ass_b_result2.csv', result2);

break