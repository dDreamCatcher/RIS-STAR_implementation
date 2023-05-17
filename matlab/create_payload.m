function txSig = create_payload(trainingSig)
  %% Create data
  % 
  M = 4;  k = log2(M);  % QPSK
  bits{1} = randi([0 1],64*k,1);
  M = 2;  k = log2(M);  % BPSK
  bits{2} = randi([0 1],64*k,1);
   
  % Create symbols
  symbols(1,:) = qammod(bits{1},4,'InputType','bit','UnitAveragePower',true).';  % QPSK
  symbols(2,:) = qammod(bits{2},2,'InputType','bit','UnitAveragePower',true).';  % BPSK
   
  % Construct payload 1:
  % 64 symbols with IFFT length of 256
  % Each symbol uses 2 subcarriers
  modOut1 = [zeros(4,64);        % Zero padding
           symbols(1,:);         % QPSK - 1 subcarrier
           symbols(2,:);         % BPSK - 1 subcarrier
           zeros(256-4-2,64)];   % Zero padding
  payload = reshape(ifft(modOut1),[],1);
  % Scale time-domain signal appropriately
  payload = payload/max(real(payload))*0.5;
    
  % Generate Frame
  txSig = [trainingSig; zeros(400,1); payload; zeros(100,1)] * 0.2;

  % Save
  save(fullfile('data','information.mat'),'bits','symbols','payload','trainingSig', 'txSig');

end