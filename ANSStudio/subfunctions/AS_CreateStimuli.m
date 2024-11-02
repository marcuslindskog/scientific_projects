function stimuli = AS_CreateStimuli(ratios, minTotal, maxTotal, minimum, prec, trialsTotal, tolerance, visualSetup,screenSetup, controlType, constants)
%function stimuli = AS_CreateStimuli(ratios, minTotal, maxTotal, minimum, prec, trialsTotal, tolerance, visualSetup,controlType, constants)
%
%This function creats the stimulus set that can be displayed in an
%experiment while collecting data (using AS_RunExperiment) or
%just displayed on the screen and saved as images or a video (using
%AS_DisplayStimuli).
% INPUT
%       ratios      :  the ratio of the number of dots in the two
%                       presented arrays.
%       minTotal	:  the minimum number of dots in the two arrays combined.
%       maxTotal    :  the maximum number of dots in the two arrays combined.
%       minimum     :  the minimum number of dots in any of the two arrays.
%       precision   :  a parameter regulating how closely the ratios in "ratios"
%                      should be estimated.
%       trialsTotal	:  the total number of trials to be generated.
%       tolerance   :  a parameter regulating the minimum allowed deviation
%                      between average dot size for size controlled stimuli.
%       visualSetup :  a vector specifying - i) viewing distance to the
%                      screen in cm, ii) minimum and maximum diameter in
%                      degrees visual angl of the dots, and iii) the
%                      degrees of visual angle of the window in which
%                      the stimuli are displayed.
%       screenSetup :  a vector specifying - i) height of screen in pixels.
%                      , ii) width of screen in pixels, iii) height of
%                      screen in centimeters and iv) width of screen in
%                      centimeters. If an empty vector is entered,
%                      will query the screen for its dimensions.
%       controlType :  1 - Half of the trials are area controlled (i.e. both
%                      arrays have the same cummulative area) and half
%                      of the trials are size controlled (i.e both arrays
%                      have the same average dot size) (see Halberda et al.
%                      (2008) for more on this control procedure. 2 - All
%                      trials are area controlled. 3 - All trials are size
%                      controlled.
%       constants   : if a number is provided as a constant one of the
%                     arrays will always contain that many dots.
%
% OUTPUT
%       stimuli     : a matrix of information about the number of dots in
%       each set....
%
% Latest update by Marcus Lindskog, 27 Jun 2016

%% Find numerosity combinations
% See documentation below for AS_DivideTotalTrials on how the script finds
% all combination of numerosities that match the criteria passed to the
% function.
if nargin > 10
    stimuliSetup = AS_DivideTotalTrials(ratios, minTotal, maxTotal, minimum, trialsTotal, prec, constants);
else
    stimuliSetup = AS_DivideTotalTrials(ratios, minTotal, maxTotal, minimum, trialsTotal, prec);
    
end

%% Find visual features
% See documentation in separate fle for AS_FindVisualFeatures on how
% ANS Studio finds the visual features of the stimuli.
if isempty(screenSetup) == 0
    visualFeatures = AS_FindVisualFeatures(visualSetup, screenSetup);
else
    visualFeatures = AS_FindVisualFeatures(visualSetup);
end

%% Generate the stimuli
stimuli = AS_GetStimuli(stimuliSetup, tolerance, visualFeatures, controlType);


%% Helper Functions
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%                           Helper functions
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

function stimulusSetup = AS_DivideTotalTrials(ratios, minTotal, maxTotal, minimum, trialsTotal, prec, constants)
% function stimulusSetup = AS_DivideTotalTrials(ratios, minTotal, maxTotal, minimum, trialsTotal, prec, constants)
%
%This helper function first creates all unique possible numerosity combinations given
%the vector of ratios, minTotal, maxTotal, minimum and prec.
%This function will devide the total number of requested trials over the n
%ratios in the ratios vector. If it is possible to evenly devide the
%requested number of trials over the n ratios this will be done.
%Else the remaining trials will be randomly devided over the the ratios. The
%function then devides the trials in each bin i) to the two stimulustypes and ii) over the
%different numerosity combinations.

% INPUT
%       ratios      :  the ratio of the number of dots in the two
%                       presented arrays.
%       minTotal	:  the minimum number of dots in the two arrays combined.
%       maxTotal    :  the maximum number of dots in the two arrays combined.
%       minimum     :  the minimum number of dots in any of the two arrays.
%       trialsTotal :  the total number of trials to be generated.
%       precision   :  a parameter regulating how closely the ratios in "ratios"
%                      should be estimated.
%       constants   : if a number is provided as a constant one of the
%                     arrays will always contain that many dots.
%
% OUTPUT
%       stimulusSetup  :   a matrix that has information about the number of
%                        dots in each set, which ratio and ratio-type the
%                        trial has and wether it should be area or size
%                        controlled.
%
% Latest update by Marcus Lindskog, 27 June 2016

%% Find all numerosity combinations

%Empty vector to hold the numerosity combinations.
numerosityCombinations = [];
vec = 1:round(maxTotal);
vec = vec';

A = repmat(vec, [round(maxTotal) 1]);
B = [];

for i = 1:length(vec)
    B = [B; repmat(vec(i), [length(vec) 1])];
end

% All possible combinations of values up to the total number of maximum dots
% are created and put into myCombs.
myCombs = [A B];

% Loop that goes over all the combinations in myCombs and retains those that
% meet the maxTotal, minTotal, minimum, and ratio criteria passed to the
% function.
for j = 1:length(ratios)
    for k = 1:size(myCombs, 1)
        total = myCombs(k,1)+myCombs(k,2);
        ratio = min(myCombs(k,:))/max(myCombs(k,:));
        if total <= maxTotal && total >=minTotal && min(myCombs(k,:))>=minimum && abs(ratio - ratios(j)) < prec
            
            tester = 0;
            for l = 1:size(numerosityCombinations,1)
                if min(myCombs(k,:)) == min(numerosityCombinations(l,1:2)) && max(myCombs(k,:)) == max(numerosityCombinations(l,1:2))
                    tester = tester +  1;
                end
            end
            if tester == 0
                numerosityCombinations = [numerosityCombinations; myCombs(k,:) ratios(j) j];
            end
        end
        
    end
    
    
    
end

% If a vector of constant is passed to the function these are also added
% to the stimulus set.
if nargin > 6
    for j = 1:length(constants)
        numerosityCombinations = [numerosityCombinations; constants(j) constants(j) 1.000 size(numerosityCombinations,1)+j];
    end
end

%% Devide the trials
% The trials in each unique ratio is devided into i) to the two
% types of control (area and size), If another control is used this
% this information is ignored, and ii) over the different numerosity
% combinations.

nrInBins = zeros(length(unique(numerosityCombinations(:,3))),1);
stimulusSetup = [];

%This part looks to see if it is possible to divide the total number of
%trials evenly to each ratio. If not it randomly allocates the remainding
%trials to ratios.
if rem(trialsTotal, length(nrInBins)) == 0
    nrInBins(:,1) = trialsTotal/length(nrInBins);
else
    nrInBins(:,1) = (trialsTotal - rem(trialsTotal, length(nrInBins)))/length(nrInBins);
    
    for p  = 1: rem(trialsTotal, length(nrInBins))
        bin = randi(length(nrInBins));
        nrInBins(bin,1) = nrInBins(bin,1)+1;
    end
end

% This part looks how many different ratios-types (e.g. 6 and 7 and
% and 12 and 14 for the ratio 6/7, there is for each ratio.
ratioTypeInBins = zeros(length(nrInBins),1);
for q = 1:size(numerosityCombinations,1)
    for t = 1:length(nrInBins)
        if numerosityCombinations(q,4) ==t
            ratioTypeInBins(t)= ratioTypeInBins(t)+1;
        end
    end
    
end

%This part looks at how many trials of each ratio-type there should be
% for each ratio. If the number of ratios-types are divisible with the
% number of trials the allocation is equal otherwise there is a
% random allocation.

nrTrialsForRatioType = [];

for i = 1:length(nrInBins)
    if rem(nrInBins(i), ratioTypeInBins(i)) == 0
        trials = nrInBins(i)/ratioTypeInBins(i);
        trialVector = repmat(trials, ratioTypeInBins(i),1);
    else
        trials = (nrInBins(i)-rem(nrInBins(i), ratioTypeInBins(i)))/ratioTypeInBins(i);
        trialVector = repmat(trials, ratioTypeInBins(i),1);
        for p  = 1: rem(nrInBins(i), ratioTypeInBins(i))
            bin = randi(length(trialVector));
            trialVector(bin) = trialVector(bin)+1;
        end
        
    end
    nrTrialsForRatioType = [nrTrialsForRatioType; trialVector];
end

for k = 1:size(numerosityCombinations)
    areaControlled=[];
    sizeControlled=[];
    O = nrTrialsForRatioType(k);
    if rem(O,2) == 0
        areaControlled = repmat([numerosityCombinations(k,:) 0], O/2,1);
        sizeControlled = repmat([numerosityCombinations(k,:) 1], O/2,1);
    else
        areaControlled = repmat([numerosityCombinations(k,:) 0], (O-rem(O,2))/2,1);
        sizeControlled = repmat([numerosityCombinations(k,:) 1], (O-rem(O,2))/2,1);
        
        if rand() > .5
            areaControlled = [areaControlled; [numerosityCombinations(k,:) 0]];
        else
            sizeControlled = [sizeControlled; [numerosityCombinations(k,:) 1]];
        end
        
    end
    
    %Finally we create a stimulusSet which has information of the number of
    %dots in each set, which ratio and ratio-type the trial has and if it
    %should be area or size controlled (if applicable).
    
    stimulusSetup = [stimulusSetup; areaControlled; sizeControlled];
    
end

%%%AS_GetStimuli
function stimuli = AS_GetStimuli(stimuliSetup, tolerance, visualFeatures, controlType)
% function stimuli = AS_GetStimuli(stimuliSetup, tolerance, visualFeatures, controlType)

% This helper function calls functions AS_AreaControlledStimulusCreation
% and AS_SizeControlledStimulusCreation to create the actuall stimuli.

% INPUT
%       stimuliSetup   :  output array from AS_DivideTotalTrials
%       tolerance   :  a parameter regulating the minimum allowed deviation
%                      between average dot size for size controlled stimuli.
%       visualSetup :  a vector specifying - i) viewing distance to the
%                      screen in cm, ii) minimum and maximum diameter in
%                      degrees visual angl of the dots, and iii) the
%                      degrees of visual angle of the window in which
%                      the stimuli are displayed.
%       controlType :  1 - Half of the trials are area controlled (i.e. both
%                      arrays have the same cummulative area) and half
%                      of the trials are size controlled (i.e both arrays
%                      have the same average dot size) (see Halberda et al.
%                      (2008) for more on this control procedure. 2 - All
%                      trials are area controlled. 3 - All trials are size
%                      controlled.
%
% OUTPUT
%       stimuli   :   a matrix that has information about the number of
%                        dots in each set, which ratio and ratio-type the
%                        trial has and wether it should be area or size
%                        controlled.
%
% Latest update by Marcus Lindskog, 27 June 2016


minRadius = visualFeatures(1)/2;
maxRadius = visualFeatures(2)/2;
totalAreaAvaliable = visualFeatures(3)^2;


stimuli = [];
for k = 1:size(stimuliSetup,1)
    
    switch controlType
        case  1 %Gives half area controlled and half size controlled
            if stimuliSetup(k,5) == 0
                %Create area controlled stimuli
                holdStim = AS_AreaControlledStimulusCreation(stimuliSetup(k,1),stimuliSetup(k,2),minRadius,maxRadius,totalAreaAvaliable);
                
            else
                %create size controlled stimuli
                holdStim = AS_SizeControlledStimulusCreation(stimuliSetup(k,1),stimuliSetup(k,2),minRadius,maxRadius, tolerance, totalAreaAvaliable);
            end
            
        case 2 %Gives only area controlled stimuli
            holdStim = AS_AreaControlledStimulusCreation(stimuliSetup(k,1),stimuliSetup(k,2),minRadius,maxRadius,totalAreaAvaliable);
            
        case 3 %Gives only size controlled stimuli
            holdStim = AS_SizeControlledStimulusCreation(stimuliSetup(k,1),stimuliSetup(k,2),minRadius,maxRadius, tolerance, totalAreaAvaliable);
    end
    
    
    
    
    
    trial = repmat(k,stimuliSetup(k,1)+stimuliSetup(k,2),1);
    info = repmat(stimuliSetup(k,:),length(trial), 1);
    theSets = [repmat(1,stimuliSetup(k,1),1); repmat(2,stimuliSetup(k,2),1)];
    stimuli = [stimuli; trial info holdStim theSets];
end

%%%AS_AreaControlledStimulusCreation
function stim = AS_AreaControlledStimulusCreation(nrSet1, nrSet2, minRadius, maxRadius, totalAreaAvaliable)
%UNTITLED4 Summary of this function goes here
%   Detailed explanation goes here
minArea = pi*minRadius^2;
maxArea = pi*maxRadius^2;
setChooser = rand();

if setChooser >.5
    firstSet = nrSet1;
    secondSet = nrSet2;
else
    firstSet = nrSet2;
    secondSet = nrSet1;
end

minCumArea = [minArea*firstSet minArea*secondSet];
maxCumArea = [maxArea*firstSet maxArea*secondSet];

totalAreaPossible = 0;
while totalAreaPossible ==0
    firstSetCummulativeArea = max(minCumArea) + (min(maxCumArea) - max(minCumArea)).*rand(1,1);
    firstSetAreas = AS_randfixedsum(firstSet,1,firstSetCummulativeArea,minArea,maxArea);
    secondSetAreas = AS_randfixedsum(secondSet,1,firstSetCummulativeArea,minArea,maxArea);
    if (sum(firstSetAreas)+sum(secondSetAreas))< totalAreaAvaliable
        totalAreaPossible = 1;
    end
end
firstSetRadius = sqrt(firstSetAreas./pi);
secondSetRadius = sqrt(secondSetAreas./pi);


if setChooser >.5
    stim = [firstSetRadius; secondSetRadius];
    
else
    stim = [secondSetRadius; firstSetRadius];
end


%%%AS_SizeControlledStimulusCreation
function stim = AS_SizeControlledStimulusCreation(nrSet1, nrSet2, minRadius, maxRadius, tolerance, totalAreaAvaliable)
%UNTITLED5 Summary of this function goes here
%   Detailed explanation goes here
minArea = pi*minRadius^2;
maxArea = pi*maxRadius^2;
setChooser = rand();

if setChooser >.5
    firstSet = nrSet1;
    secondSet = nrSet2;
else
    firstSet = nrSet2;
    secondSet = nrSet1;
end

totalAreaPossible = 0;
while totalAreaPossible == 0
    %Randomly generate the radiuses for the first set
    firstSetRadius =  minRadius + (maxRadius-minRadius).*rand(firstSet,1);
    
    %Calculate the average area of the first set
    firstSetAverageArea = sum(pi.*firstSetRadius.^2)/length(firstSetRadius);
    
    if (firstSetAverageArea*firstSet + firstSetAverageArea*secondSet) < totalAreaAvaliable
        totalAreaPossible = 1;
    end
    
    control = 1;
    
    while control > tolerance
        secondSetAreas = AS_randfixedsum(secondSet,1,firstSetAverageArea*secondSet,minArea,maxArea);
        
        secondSetRadius = sqrt(secondSetAreas./pi);
        
        %Calculate the average area of the second set
        secondSetAverageArea  = sum(pi.*secondSetRadius.^2)/length(secondSetRadius);
        
        control = abs(firstSetAverageArea - secondSetAverageArea)/firstSetAverageArea;
        
    end
    
    if setChooser >.5
        stim = [firstSetRadius; secondSetRadius];
        
    else
        stim = [secondSetRadius; firstSetRadius];
    end
    
end

%%%AS_randfixedsum
function [x,v] = AS_randfixedsum(n,m,s,a,b)

% [x,v] = randfixedsum(n,m,s,a,b)
%
%   This generates an n by m array x, each of whose m columns
% contains n random values lying in the interval [a,b], but
% subject to the condition that their sum be equal to s.  The
% scalar value s must accordingly satisfy n*a <= s <= n*b.  The
% distribution of values is uniform in the sense that it has the
% conditional probability distribution of a uniform distribution
% over the whole n-cube, given that the sum of the x's is s.
%
%   The scalar v, if requested, returns with the total
% n-1 dimensional volume (content) of the subset satisfying
% this condition.  Consequently if v, considered as a function
% of s and divided by sqrt(n), is integrated with respect to s
% from s = a to s = b, the result would necessarily be the
% n-dimensional volume of the whole cube, namely (b-a)^n.
%
%   This algorithm does no "rejecting" on the sets of x's it
% obtains.  It is designed to generate only those that satisfy all
% the above conditions and to do so with a uniform distribution.
% It accomplishes this by decomposing the space of all possible x
% sets (columns) into n-1 dimensional simplexes.  (Line segments,
% triangles, and tetrahedra, are one-, two-, and three-dimensional
% examples of simplexes, respectively.)  It makes use of three
% different sets of 'rand' variables, one to locate values
% uniformly within each type of simplex, another to randomly
% select representatives of each different type of simplex in
% proportion to their volume, and a third to perform random
% permutations to provide an even distribution of simplex choices
% among like types.  For example, with n equal to 3 and s set at,
% say, 40% of the way from a towards b, there will be 2 different
% types of simplex, in this case triangles, each with its own
% area, and 6 different versions of each from permutations, for
% a total of 12 triangles, and these all fit together to form a
% particular planar non-regular hexagon in 3 dimensions, with v
% returned set equal to the hexagon's area.
%
% Roger Stafford - Jan. 19, 2006

% Check the arguments.
if (m~=round(m))|(n~=round(n))|(m<0)|(n<1)
    error('n must be a whole number and m a non-negative integer.')
elseif (s<n*a)|(s>n*b)|(a>=b)
    error('Inequalities n*a <= s <= n*b and a < b must hold.')
end

% Rescale to a unit cube: 0 <= x(i) <= 1
s = (s-n*a)/(b-a);

% Construct the transition probability table, t.
% t(i,j) will be utilized only in the region where j <= i + 1.
k = max(min(floor(s),n-1),0); % Must have 0 <= k <= n-1
s = max(min(s,k+1),k); % Must have k <= s <= k+1
s1 = s - [k:-1:k-n+1]; % s1 & s2 will never be negative
s2 = [k+n:-1:k+1] - s;
w = zeros(n,n+1); w(1,2) = realmax; % Scale for full 'double' range
t = zeros(n-1,n);
tiny = 2^(-1074); % The smallest positive matlab 'double' no.
for i = 2:n
    tmp1 = w(i-1,2:i+1).*s1(1:i)/i;
    tmp2 = w(i-1,1:i).*s2(n-i+1:n)/i;
    w(i,2:i+1) = tmp1 + tmp2;
    tmp3 = w(i,2:i+1) + tiny; % In case tmp1 & tmp2 are both 0,
    tmp4 = (s2(n-i+1:n) > s1(1:i)); % then t is 0 on left & 1 on right
    t(i-1,1:i) = (tmp2./tmp3).*tmp4 + (1-tmp1./tmp3).*(~tmp4);
end

% Derive the polytope volume v from the appropriate
% element in the bottom row of w.
v = n^(3/2)*(w(n,k+2)/realmax)*(b-a)^(n-1);

% Now compute the matrix x.
x = zeros(n,m);
if m == 0, return, end % If m is zero, quit with x = []
rt = rand(n-1,m); % For random selection of simplex type
rs = rand(n-1,m); % For random location within a simplex
s = repmat(s,1,m);
j = repmat(k+1,1,m); % For indexing in the t table
sm = zeros(1,m); pr = ones(1,m); % Start with sum zero & product 1
for i = n-1:-1:1  % Work backwards in the t table
    e = (rt(n-i,:)<=t(i,j)); % Use rt to choose a transition
    sx = rs(n-i,:).^(1/i); % Use rs to compute next simplex coord.
    sm = sm + (1-sx).*pr.*s/(i+1); % Update sum
    pr = sx.*pr; % Update product
    x(n-i,:) = sm + pr.*e; % Calculate x using simplex coords.
    s = s - e; j = j - e; % Transition adjustment
end
x(n,:) = sm + pr.*s; % Compute the last x

% Randomly permute the order in the columns of x and rescale.
rp = rand(n,m); % Use rp to carry out a matrix 'randperm'
[ig,p] = sort(rp); % The values placed in ig are ignored
x = (b-a)*x(p+repmat([0:n:n*(m-1)],n,1))+a; % Permute & rescale x


