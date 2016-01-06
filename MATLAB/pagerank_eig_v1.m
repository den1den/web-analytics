function [ x, t ] = pagerank_eig_v1( Gs, p, n, teleport, A_func )
%PAGERANK_EIG_V1 Using eig()
[A, t_a] = A_func(Gs, p, n, teleport);

tic;

[V, D] = eigs(A);
x = zeros(n,1);

for i = 1: size(V, 2);
    v = V(:,i);
    if sign(min(v)) == sign(max(v)) && sign(min(v)) ~= 0;
        assert(abs(D(i,i))>.99); % assume |eigenvalue| = 1
        x = v;
        break;
    end
end

x_sum = sum(x);
x = x / x_sum;

t = toc + t_a;
disp(t)
whos()
end
