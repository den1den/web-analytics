function [ x, t ] = pagerank_eig_v1( Gs, p, n, telport, A_func )
%PAGERANK_EIG_V1 Using eig()
[A, t_a] = A_func(Gs, p, n, telport);

tic;
x = eig(A);
t = toc + t_a;

end

