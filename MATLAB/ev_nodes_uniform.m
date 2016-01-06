function [ G, rm ] = ev_nodes_uniform( G, seed, remove_nodes, remove_edges )
%EV_NODES_UNIFORM Randomly only remove edges and nodes
rng(seed);
del_indices = randperm(size(G,1), remove_nodes);
rm = del_indices';
G(rm, :) = [];
G(:, rm) = [];
G = ev_edges_uniform(G, seed, remove_edges);
end

