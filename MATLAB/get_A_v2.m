function [ A, t ] = get_A_v2( Gs, p, n, teleport )
%Sparse symbolic calculation of A = p*G*D + e*z'
tic;
c = sum(Gs, 1);
k = find(c~=0);
c_sym = sym('c_sym');
c_sym = 1./c(k);
Ds = sparse(k,k,c_sym,n,n);
e = ones(n, 1);
if teleport
    z = ((1-p)*(c~=0) + (c==0))/n;
    A = p*Gs*Ds+e*z;
else
    z = (c==0)/n;
    A1 = Gs*Ds;
    A2 = e*z;
    A = A1 + A2;
end
t = toc;
end