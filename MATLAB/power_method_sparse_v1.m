function [ x, t ] = power_method_sparse_v1( Gs, n, p )
%POWER_METHOD_SPARSE_V1 First power method approach (with sparse matrices)
assert(issparse(Gs));
assert(p~=0, 'Not implmented, can be done quicker')

tic;
c = sum(Gs, 1);
k = find(c~=0);
D = sparse(k,k,1./c(k),n,n);
e = ones(n, 1);
I = speye(n, n);
x = (I - p*Gs*D)\e;
x = x/sum(x);
t = toc;
end