function [ x ] = insert_empty( x, rm )
%INSERT_EMPTY Insert empty rows in x at indices rm
rm = sort(rm);
for n = 1: size(rm,1);
    i = rm(n);
    if i == 1;
        x = [0; x];
    else
        if i == size(x,1) + 1;
            x = [x; 0];
        else
            a = x(1:i-1);
            b = x(i:size(x, 1));
            x = [a; 0; b];
        end
    end
end