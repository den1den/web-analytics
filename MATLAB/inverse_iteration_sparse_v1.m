function [ x, t ] = inverse_iteration_sparse_v1( Gs, n, p, abstol, max_it )
%INVERSE_ITERATION_SPARSE_V1 inverse iteration algorithm from Chapter 6
assert(issparse(Gs));

tic;
c = sum(Gs, 1);
k = find(c~=0);
D = sparse(k,k,1./c(k),n,n);
e = ones(n, 1);

G = p*Gs*D;
z = ((1-p)*(c~=0) + (c==0))/n;

x0 = e/n;
x1 = G*x0 + e*(z*x0);
it = 1;
while any(abs(x1-x0) > abstol) && it < max_it
    x0 = x1;
    x1 = G*x0 + e*(z*x0);
    it = it + 1;
end
t = toc;
if it >= max_it
    fprintf(1, ...
        'Inverse iteration sparse did not converge with max_it = %d', max_it);
    x = false;
else
    x = x1;
end
end