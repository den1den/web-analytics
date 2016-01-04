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
Gs = sparse(edges_a, edges_b, 1, n, n);
% and matrix G is the full matrix of Gs
G = full(Gs);

% CONSTANTS
% p is the chance on clicking a link instead of a random page
p = 0.85;
% set the tolerances for the calculations
abstol = 10^(-4);
max_it = 10^4;

% VERIFICATION create a correct result for PageRank with teleport
[A_t, a_sec] = get_A_v1(Gs, p, n, true);
X_t = (speye(n, n) - A_t)\ones(n, 1); X_t = X_t /sum(X_t); % pagerank

% CALCULATIONS and VERIFICATIONS
disp('eig() with teleport');
[x_eig_t, eig_t_sec] = pagerank_eig_v1(Gs, p, n, true, @get_A_v1);
assert_same_vector(X_t, x_eig_t, abstol);

disp('eig() without teleport');
[x_eig_nt, eig_nt_sec] = pagerank_eig_v1(Gs, p, n, false, @get_A_v1);

disp('power method with teleport');
[x_p_t, p_t_sec]= pagerank_power_v1(G, p, n, true, @get_A_v1, abstol/2);
assert_same_vector(X_t, x_p_t, abstol);

disp('sparse power method with teleport');
[x_ps_t, ps_t_sec] = pagerank_power_sparse_v1(Gs, p, n, true, abstol/2, max_it);
assert_same_vector(X_t, x_ps_t, abstol);

disp('sparse power method without teleport');
[x_ps_nt, ps_nt_sec, result] = pagerank_power_sparse_v1(Gs, p, n, false, abstol/10, max_it);

% PLOTS
figure(1); clf;
spy(Gs), title('G');
%subplot(1,2,1), spy(Gs), title('G');
%sco = symrcm(Gs);
%subplot(1,2,2), spy(Gs(sco, sco)), title('Sparse reverse Cuthill-McKee ordering');

figure(2); clf;
subplot(3,2,1), bar(x_eig_t), title('eig() with teleport');
subplot(3,2,2), bar(x_eig_nt), title('eig() without teleport');
subplot(3,2,3), bar(x_ps_t), title('Sparse power method with teleport');
subplot(3,2,4), bar(x_ps_nt), title('Sparse power method without teleport');
subplot(3,2,5), bar(x_p_t), title('Power method with teleport');
diff = minus(x_eig_nt, x_ps_nt);
subplot(3,2,6), bar(diff), title('Differences eig() and Power method (without teleport)');

%y = @(x) x*2;