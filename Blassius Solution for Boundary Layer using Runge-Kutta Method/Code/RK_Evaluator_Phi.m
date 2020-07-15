function [phi] = RK_Evaluator_Phi(s)
    %
    %   Use the following Area to use Runge-Kutta method to evaluate the
    %   value of phi = f'(eta = 10) - 1.

    %   The intention is to take in the parameter dictating the boundary value condition and to run a Runge-Kutta Ananlysis.

    %   Part - 1 
    %   Setup eta and the functions scale
    
    h = 0.1;
    eta = 0:h:10;
    

    f = zeros(size(eta));
    u = zeros(size(eta));
    v = zeros(size(eta));

    %   Boundary Conditions
    f(1) = 0;
    u(1) = 0;
    v(1) = s;

    %   Part - 2
    for i = 1:length(eta)-1

        fuv_array = [f(1,i),u(1,i),v(1,i)];

        kmat = RK_Coefficients(fuv_array,h);
        
        wmat = (1/6)*[1 2 2 1];

        f(i+1) = f(i) + wmat*kmat(:,1);
        u(i+1) = u(i) + wmat*kmat(:,2);
        v(i+1) = v(i) + wmat*kmat(:,3);




    end

    phi = u(end) - 1; 

    %
    subplot(3,2,[1 2])
    plot(eta,f)
    subplot(3,2,[3 4])
    plot(eta,u)
    subplot(3,2,[5 6])
    plot(eta,v)
    %}


end