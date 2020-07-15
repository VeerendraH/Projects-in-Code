function phiprime = RK_Evaluator_Phiprime(s)
    delta_s = 0.0001;

    s1 = s;
    s2 = s + delta_s;
    
    phiprime = (1/delta_s)*(RK_Evaluator_Phi(s2) - RK_Evaluator_Phi(s1));

end