%read the files
folder = 'PageRank';
number_format = 'u'; formatSpec = ['%' number_format ' %' number_format];
edges_file = fopen([folder '/edges.txt'], 'r');
edges = fscanf(edges_file, formatSpec, [2 Inf]);
edges = edges';
% edges(i,1) = a AND edges(i,2) = b means a has a link towards b
fclose(edges_file);
nodes_file = fopen([folder '/nodes.txt'], 'r');
nodes = fscanf(nodes_file, formatSpec, [2 Inf]);
% nodes(2,i) is the class of node i (i>0)
fclose(nodes_file);

p = 0.85;
[~, n] = size(nodes);
[n_edges, ~] = size(edges);

%create matrix G
G = zeros(n, n);
for i = 1 : n_edges;
    a = edges(i,1)
    b = edges(i,2)
    G(a, b) = G(a, b) + 1;
end

for i = 1 : n;
    for j = 1 : n;
        
    end
end
%y = @(x) x*2;
