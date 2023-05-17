function trainingSig = generate_goldCode(num_code, n)
%   Input
%         n: one of 5, 6, 7, 9, 10, 11 
%         num_code : number of training signals

    code = goldcode(n);

    % Use BPSK
    code_bpsk = code.*exp(1j*pi/4);
    index = 4;
    cum_code = zeros(size(code,2),num_code);
    % Reference signal for cross correlation
    txfilter = comm.RaisedCosineTransmitFilter;

    for i = index:index:num_code*index+1
        cum_code(:,i/index) = code_bpsk(i,:)';                              % cumulated gold code sequences
    end

    trainingSig = txfilter([cum_code; ...
                    zeros(10,num_code)]); % Pad extra zeros

end



