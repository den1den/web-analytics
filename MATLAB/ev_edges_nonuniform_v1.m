function [ G ] = ev_edges_nonuniform_v1( G, seed, nds, remove )
%EV_EDGES_NONUNIFORM_V1 Summary of this function goes here
s = RandStream('mt19937ar', 'Seed', seed);
in_count = full(nds(:,1));
for i = 1: remove;
    node = randsample(s, size(G,1), 1, true, in_count);
    in_edges = G(:,node);
    remove_edge = randsample(s, find(in_edges), 1);
    G(remove_edge, node) = 0;
    in_count(node) = in_count(node) - 1;
end
end