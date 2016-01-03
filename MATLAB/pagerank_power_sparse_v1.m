function [ x, t ] = pagerank_power_sparse_v1( Gs, n, p, A_func, abstol )
%PAGERANK_POWER_SPARSE_V1 Sparse power method
%   TODO: implement this
assert(issparse(Gs));

[A, t_a] = A_func(Gs, p, n, telport);

tic;
xold = zeros(n,1);  % Zero vector
x = ones(n,1)/n; % Homogeneous vector with sum of 1
while norm(x-xold) > abstol
    xold = x;
    x = A * x;
end
t = toc + t_a;

end