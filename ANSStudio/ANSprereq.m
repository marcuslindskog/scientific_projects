function ANSprereq()
checkANS = exist('AS_RunExperiment.m', 'file');
rng('shuffle');
if checkANS == 0
  addpath('Demo/');
  addpath('PrintedImages/');
  addpath('RawDataFiles/'); 
  addpath('Studies/');
  addpath('subfunctions/');
  addpath('jheapcl/');
  javaaddpath(which('MatlabGarbageCollector.jar'));
end