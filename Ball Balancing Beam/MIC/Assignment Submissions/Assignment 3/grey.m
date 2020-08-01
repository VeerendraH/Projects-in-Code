function y = grey(n)
%UNTITLED3 Summary of this function goes here
%   Detailed explanation goes here

if (n-1)>0,  %Recursive loop employed%
    t=grey(n-1);
    numofrows = size(t,1)
    one = [ones(numofrows,1) t] %Starting with zero%
    zero = [zeros(numofrows,1) flipud(t)] %Starting with one%
    y=[one;zero];
else
    y=[1;0] ;
end

end

