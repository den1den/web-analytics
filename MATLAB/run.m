%init
number_format = 'u16';
formatSpec = ['%' number_format ' %' number_format];
edges_file = fopen('PageRank/edges.txt');
edges = textscan(edges_file, formatSpec);
fclose(edges_file);
edges2 = dlmread('PageRank/edges.txt');

nodes_file = fopen('PageRank/nodes.txt');
nodes = textscan(nodes_file, formatSpec);
fclose(nodes_file);

p = 0.85;

%y = @(x) x*2;
