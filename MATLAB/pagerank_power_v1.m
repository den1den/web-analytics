function [ x, t ] = pagerank_power_v1( G, p, n, teleport, A_func, abstol )
%PAGERANK_POWER_V1 Conventional power method
assert(~issparse(G));

[A, t_a] = A_func(G, p, n, teleport);

tic;
xold = zeros(n,1);  % Zero vector
x = ones(n,1)/n; % Homogeneous vector with sum of 1
while norm(x-xold) > abstol
    xold = x;
    x = A * x;
end
t = toc + t_a;

end