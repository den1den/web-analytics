function [ G, rm ] = ev_nodes_nonuniform_v1( G, seed, remove )
%EV_NODES_NONUNIFORM_V1 Summary of this function goes here
rm = zeros(remove,1);
s = RandStream('mt19937ar', 'Seed', seed);
nds = full(sum(G,2));
for i = 1: remove;
    node = randsample(s, size(G,1), 1, true, nds);
    rm(i) = node;
    nds(node) = 0; % remove from the population
end
G(rm, :) = [];
G(:, rm) = [];
end