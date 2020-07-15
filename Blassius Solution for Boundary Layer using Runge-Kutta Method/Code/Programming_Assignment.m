%   AM5530 : Advanced Fluid Mechanics Computer Assignment

%   Numerical Solution for Blasius Equation

%   Initial value of s
s = 1;
Delta_s = [];

S_Increment_Threshold = 0.000001;               % Threshold error value
Residual = S_Increment_Threshold + 1;           % For initially passing through the while loop

%   Loop Iterator
while Residual > S_Increment_Threshold          % While condition to run the loop
    phi      =  RK_Evaluator_Phi(s)        ;    % Calculate Phi
    phiprime =  RK_Evaluator_Phiprime(s)   ;    % Calculate Phi prime wrt s
    
    s0       = s                           ;    % Old s value
    s        = NR_Evaluator(s,phi,phiprime);    % New s value

    Residual = abs(s - s0)                 ;    % Error
    Delta_s  = [Delta_s;Residual]          ;

end

%   Process the Results
Results = Process_Results(s);


