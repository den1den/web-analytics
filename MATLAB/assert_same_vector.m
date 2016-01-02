function [ ] = assert_same_vector( x1, x2, abstol, reltol )
%ASSERT_SAME_VECTOR Summary of this function goes here
%   Detailed explanation goes here
reltol_check = exist('reltol','var');

for i = 1 : size(x1, 1);
    diff = abs(x1(i)-x2(i));
    assert(diff <= abstol, ...
        'Fail on abstol: x1(%d) ~= x2(%d), %s ~= %s with(abstol=%d)', ...
        i, i, x1(i), x2(i), abstol );
    if reltol_check;
        assert(diff/x1(i) <= reltol, ...
            'Fail on reltol: x1(%d) ~= x2(%d), %s ~= %s with(reltol=%d)', ...
            i, i, x1(i), x2(i), abstol );
    end
end

