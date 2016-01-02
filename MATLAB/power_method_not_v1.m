function [ x, t ] = power_method_not_v1( G, n, p )
%POWER_METHOD_NOT_V1 First power method approach (not sparse)
assert(~issparse(G));
assert(p~=0, 'Not implmented, can be done quicker');

tic;
c = sum(G, 1);
k = find(c~=0);
D = full(sparse(k,k,1./c(k),n,n)); %TODO should not contain sparse
e = ones(n, 1);
I = eye(n, n);
x = (I - p*G*D)\e;
x = x/sum(x);
t = toc;
end