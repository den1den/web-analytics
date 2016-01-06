function [ G ] = ev_edges_uniform( G, seed, remove )
%EV_EDGES_UNIFORM Randomly only remove only edges
rng(seed);
[row,col] = find(G);
for i = randperm(size(row,1), remove);
    G(row(i), col(i)) = 0;
end
end
