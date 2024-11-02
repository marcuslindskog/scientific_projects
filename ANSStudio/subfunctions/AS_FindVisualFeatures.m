  
function visualFeatures= AS_FindVisualFeatures(visualSetup, screenSetup)
if nargin == 1 || isempty(screenSetup)
    [pixwidth, pixheight]=Screen('WindowSize', 0);
    set(0,'Units','centimeters');
    myScreen = get(0,'ScreenSize');
else
    pixwidth = screenSetup(1);
    pixheight = screenSetup(2);
    myScreen = [0 0 screenSetup(3) screenSetup(4)];
end


pix=myScreen(3)/pixwidth; 

degperpix=(2*atan(pix/(2*visualSetup(1))))*(180/pi);
pixperdeg=1/degperpix;

minDiameter = pixperdeg*visualSetup(2);
maxDiameter = pixperdeg*visualSetup(3);
window = pixperdeg*visualSetup(4);

set(0,'Units','pixels');
visualFeatures = [minDiameter maxDiameter window pixwidth pixheight pixperdeg];
end
