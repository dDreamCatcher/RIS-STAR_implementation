function [channelEstimate, payload] = estimate_channel(rxSig, goldSeqRef, numAnt)

    nTxAntennas = numAnt;
    rxSigLen = length(rxSig);

    figure(1); cla reset; hold on;

    % Detect training signal in TX1 by cross correlation
    crossCorr = cell(nTxAntennas,1);
    for txID = 1:nTxAntennas
        crossCorr{txID} = xcorr(rxSig,goldSeqRef(:,txID));
        crossCorr{txID} = crossCorr{txID}((rxSigLen+1):end);
        plot(abs(crossCorr{txID}));
    end


    L = size(goldSeqRef,1);
    payloadLen = 64*256; % 64 symbols with IFFT length of 256
    payload = zeros(payloadLen,1);
    numPayload = 0;
    myStartIdx1 = [];

    %% FOR TX1
    if nTxAntennas > 0
        % Find intervals containing peaks of cross correlation FOR CHANNEL 1 - TX1
        % At least 80% of global maximum
        peakIntervals1 = find(abs(crossCorr{1})>(0.8*max(abs(crossCorr{1}))));
        % We know that the training signal has more than 1000 samples
        peakCandidates1 = find((peakIntervals1(2:end)-peakIntervals1(1:end-1))>1000);
    %     if ~isempty(peakCandidates1)
    %         peakCandidates1 = peakCandidates1(1:end-1);  % Don't use the last one
    %     end
        channelEstimate = zeros(nTxAntennas, length(peakCandidates1));
        for i = 1:length(peakCandidates1)
            startIndex = peakIntervals1(peakCandidates1(i)+1);
            myStartIdx1(i) = startIndex;  %#ok<AGROW>
            % Focus on a small window that contains a peak. +/- 100 samples
            if startIndex > 100; windowRange = startIndex+(-100:100);
            else;                windowRange = 1:(startIndex+100);
            end
    
            dataWindow = [];
            for txID = 1:nTxAntennas
                dataWindow = [dataWindow crossCorr{txID}(windowRange)];  %#ok<AGROW>
            end
            dataWindow = abs(dataWindow);
    
            % Find exact locations of the peaks (one in each of 4 cross correlations)
            [~,maxLoc] = max(dataWindow); % maxLoc is a 1x4 vector
            finalPeakLoc = startIndex-101;
                
            indexAll = finalPeakLoc + maxLoc + rxSigLen;
            indexMin = min(indexAll);
            indexMax = max(indexAll);
    
            if (indexMax-rxSigLen+L+400+payloadLen) <= rxSigLen % 400 samples between training signal and payload
                % Got a complete payload
                % Extract received training signal and payload
                receivedTrainingSig = rxSig((indexMin-rxSigLen+1):(indexMax-rxSigLen+L));
                payload = payload + ...
                  rxSig((indexMax-rxSigLen+L+400+1):(indexMax-rxSigLen+L+400+payloadLen));
                numPayload = numPayload + 1;
    
                % Training signals from the 4 TX antennas may arrive at the RX at slightly different times.
                % Potentially off by 1 or 2 samples. Need to align Gold sequences before least squares fit.
                refSigShifted = zeros(L+indexMax-indexMin,nTxAntennas);
                for txID = 1:nTxAntennas
                    refSigShifted((indexAll(txID)-indexMin)+(1:L),txID) = goldSeqRef(:,txID);
                end
    
                % Use least squares fit to estimate channel response
                channelEstimate(:,i) = refSigShifted\receivedTrainingSig;
            else
                % Got an incomplete payload at the end of rxSig
                channelEstimate(:,i) = [];
                break;
            end
        end
%         channelEstimate = mean(channelEstimate.');
    else
        channelEstimate = [];
    end
end



