%   Function to give out the Runge-Kutta Matrix for a given input.

function Kmatrix = RK_Coefficients(fuv,h)
    %   Terms - 1
    f = fuv(1);               u = fuv(2);               v = fuv(3); 
    
    Row1 = Rowgen(f,u,v,h);

    %   Terms - 2
    f = fuv(1) + 0.5*Row1(1); u = fuv(2) + 0.5*Row1(2) ;v = fuv(3) + 0.5*Row1(3); 
    
    Row2 = Rowgen(f,u,v,h);

    %   Terms - 3
    f = fuv(1) + 0.5*Row2(1); u = fuv(2) + 0.5*Row2(2) ;v = fuv(3) + 0.5*Row2(3);
    
    Row3 = Rowgen(f,u,v,h);

    %   Terms - 4
    f = fuv(1) +   1*Row3(1); u = fuv(2) +   1*Row3(2) ;v = fuv(3) +   1*Row3(3);
    
    Row4 = Rowgen(f,u,v,h);

    Kmatrix = [Row1;Row2;Row3;Row4];



end

function Row_Array = Rowgen(f,u,v,h)
    kf = h*u;
    ku = h*v;
    kv = h*(-0.5)*f*v;

    Row_Array = [kf,ku,kv];

end

