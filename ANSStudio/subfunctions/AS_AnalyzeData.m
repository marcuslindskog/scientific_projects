function [ID, w, R2, PC] = AS_AnalyzeData(rawData)

nrBins = max(rawData(:,6));

ID = rawData(1,1);
trialsInBin = zeros(nrBins,1);
correctInBin = zeros(nrBins,1);
ratio = zeros(nrBins,1);


for k = 1:nrBins
   check = 0;
   trial = 1;
   while check == 0
      if rawData(trial, 6) == k
          ratio(k) = rawData(trial, 5);
          check = 1;
      else
          trial = trial +1;
      end     
   end   
end

for j = 1:size(rawData, 1)
    
    for i = 1:nrBins
        if rawData(j, 6) == i
            trialsInBin(i) = trialsInBin(i)+1;
            correctInBin(i) = correctInBin(i) + rawData(j,10);
            break;
        end
        
    end
   
end

dataPC = correctInBin ./ trialsInBin;


W0 = .10 + (.45-.10).*rand(1,1);

options = optimset('LargeScale', 'off','MaxIter', 50, 'Algorithm', 'levenberg-marquardt', 'TolFun', 1e-12, 'TolX', 1e-12);
W = lsqnonlin(@AS_FitWeberFraction,W0, [],[],options, dataPC, ratio);

w = W(1);
modelPC = AS_WeberPrediction(w, ratio);
PC = mean(rawData(:,10));
R2 = corr(modelPC, dataPC)^2;

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%                           Helper functions
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%%%AS_FitWeberFraction
function F = AS_FitWeberFraction(W, T, r)
w = W(1);

A = abs(r-1);
B = r.^2;
C = 1;
D = sqrt(B+C);

PredErr = 0.5*erfc(A./(sqrt(2)*w*D));
PredCorr = 1-PredErr;

F = T-PredCorr;

%%%AS_WeberPrediction
function PredCorr = AS_WeberPrediction(w,r)

A = abs(r-1);
B = r.^2;
C = 1;
D = sqrt(B+C);

L = A./(sqrt(2)*w*D);
q = erfc(L);

PredCorr =1-( 0.5*q);




