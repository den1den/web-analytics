function [ A, t ] = get_A_v1( Gs, n, p, telport )
%GET_A_NAIVE_V1 Sparse calculation of A = p*G*D + e*z'
tic;
c = sum(Gs, 1);
k = find(c~=0);
Ds = sparse(k,k,1./c(k),n,n);
e = ones(n, 1);
if telport
    z = ((1-p)*(c~=0) + (c==0))/n;
    A = p*Gs*Ds+e*z;
else
    z = (c==0)/n;
    A = Gs*Ds+e*z;
end
t = toc;
end