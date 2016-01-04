function [ x, t, result ] = pagerank_power_sparse_v1( Gs, p, n, teleport, abstol, max_it )
%PAGERANK_POWER_SPARSE_V1 Sparse power method
assert(issparse(Gs));

tic;

c = sum(Gs,1);
k = find(c~=0);
D = sparse(k,k,1./c(k),n,n);
e = ones(n,1);
if teleport
    z = ((1-p)*(c~=0) + (c==0))/n;
    G = p*Gs*D;
else
    z = (c==0)/n;
    G = Gs*D;
end

xold = zeros(n,1);  % Zero vector
x = ones(n,1)/n; % Homogeneous vector with sum of 1
it = 0;
while norm(x-xold) > abstol && it < max_it
    xold = x;
    x = G*x + e*(z*x);
    it = it + 1;
end
if it >= max_it && norm(x-xold) > abstol
    fprintf(1, ...
        'Pagerank power sparse v1 did not converge with max_it=%d',...
        max_it);
    result = false;
else
    result = true;
    x = x / sum(x);
end
t = toc;
end