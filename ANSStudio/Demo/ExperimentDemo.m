function ExperimentDemo()
% function ExperimentDemo()
%
%This demo experiment shows an example of how an experiment is created. It
%creates stimulus similar to the ones used in Lindskog,
%Winman, & Juslin (2013) (Frontiers in Human Neuoroscience) and presents
%five trials with these stimuli.
% Depending on your hardware setup you might need to uncomment the line:
% Screen('Preference', 'SkipSyncTests', 1);
% to make the script run
% INPUT   
%
% OUTPUT
%
% Latest update by Marcus Lindskog, 27 June 2016

Screen('Preference', 'SkipSyncTests', 1);

%% Stimuli setup
% Below follows a description of the variables that you can control for the
% stimuli that are displayed during an experiment.

% ratios      : the ratio of the number of dots in the two presented
% arrays. This can be set either as a fraction (i.e. 1/2) or as a decimal
% number (i.e. .5).
% minTotal    : the minimum number of dots in the two arrays combined.
% maxTotal    : the maximum number of dots in the two arrays combined.
% minimum     : the minimum number of dots in any of the two arrays.
% trialsTotal : the total number of trials. 
% precision   : a parameter regulating how closely the ratios in "ratios"
% should be estimated.
% controlType : 1 - Half of the trials are area controlled (i.e. both
% arrays have the same cummulative area) and half of the trials are
% size controlled (i.e both arrays have the same average dot size) (see
% Halberda et al. (2008) for more on this control procedure. 2 - All
% trials are area controlled. 3 - All trials are size controlled.
% tolerance   : a parameter regulating the minimum allowed deviation
% between average dot size for size controlled stimuli.

ratios = [1/2 3/4 5/6 7/8 9/10];
minTotal = 11;
maxTotal = 30;
minimum = 6;
trialsTotal = 5;
prec = .01;
controlType = 1;
tolerance = .001;


%% Display setup
% Below follows a description of the variables that you can control for the
% how the stimuli are displayed during an experiment.

% screenSetup : a vector [pxWidth pxHeight cmWidth cmHeight] specififying  
% the dimensions of the screen the stimuli are to be presented on. If this 
% vector is empty the script will query the screen for its dimensions .
% visualSetup : a vector specifying - i) viewing distance to the screen in
% cm, ii) minimum and maximum diameter in degrees of visual angle of the dots,
% and iii) the degrees of visual angle of the window in which the stimuli
% are displayed.
% dotColor    : the color of the two arrays, given as RGB-codes.
% colorNames  : the name of the colors. This is displayed in the response
% screen.
% windowColor : the color of the background on which dots are displayed,
% given as RGB-code.

screenSetup = [];
visualSetup = [60 .5 .9 13];
dotColor = [0 0 255; 255 255 0];
colorNames = {'Blue', 'Yellow'};
windowColor = [148 148 148];


%% Stimuli are created
%Read documentation for the function AS_CreateStimuli for details.
theStimuli = AS_CreateStimuli(ratios, minTotal, maxTotal, minimum, prec, trialsTotal, tolerance, visualSetup,screenSetup, controlType);


%% Presentation Setup
% Below follows a description of the variables that you can control for the
% presentation of the stimuli during an experiment.

% presentationTime : the presentation time, in seconds, of the stimuli.
% simseq           : if the two arrays should be presented simultaneously
% (0) or sequentially (1).
% sideByside       : if the two arrays should be presented intermixed (0)
% or side by side (1).
% ISI              : if simseq == 1 the ISI determines the interstimulus
% interval between the two presentations.

presentationTime = .200;
simseq = 0;
sideByside = 0;
ISI = 0;


sideBysideDistScale = 1;
print = 1;
video = 0;



%% Running the experiment and collecting data
DemoIDNumber = 99;
%Read documentation for the function AS_RunExperiment for details about how
%the experiment is run and data extracted.
rawData = AS_RunExperiment(theStimuli, presentationTime,ISI, simseq, sideByside, dotColor,colorNames,windowColor,visualSetup, DemoIDNumber);
%AS_DisplayStimuli(theStimuli, presentationTime,ISI, simseq, sideByside,sideBysideDistScale,  dotColor,windowColor,visualSetup, screenSetup, print, video);

%Data can be written as csv-files, native matlab mat-files, or as
% ansres-files. The latter allows for basic data analysis using an
% ANS-studio script.
csvwrite('RawDataFiles/DemoData.csv',rawData);
save('RawDataFiles/DemoData.ansres','rawData');
save('RawDataFiles/DemoData.mat', 'rawData');