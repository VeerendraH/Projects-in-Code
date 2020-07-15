function Resultant_Matrix = Process_Results(s)
    %
    %   After processing the model and finding s, use this function to process the final results

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
    %   Running the Analysis
    for i = 1:length(eta)-1

        fuv_array = [f(1,i),u(1,i),v(1,i)];

        kmat = RK_Coefficients(fuv_array,h);
        
        wmat = (1/6)*[1 2 2 1];

        f(i+1) = f(i) + wmat*kmat(:,1);
        u(i+1) = u(i) + wmat*kmat(:,2);
        v(i+1) = v(i) + wmat*kmat(:,3);




    end

    phi = u(end) - 1; 

    %   Part - 3
    %   Display the results

    subplot(3,2,[1 2])
    plot(eta,f)
    title('Function f(eta)')
    ylabel('f(eta)')
    xlabel('eta')

    subplot(3,2,[3 4])
    plot(eta,u)
    title('Function u(eta)')
    ylabel('u(eta)')
    xlabel('eta')

    subplot(3,2,[5 6])
    plot(eta,v)
    title('Function v(eta)')
    ylabel('v(eta)')
    xlabel('eta')

    %   Save Results
    Resultant_Matrix = [eta',f',u',v'];
    xlswrite('Results Output.xlsx',Resultant_Matrix);

    

end