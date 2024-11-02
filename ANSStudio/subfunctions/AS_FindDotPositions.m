function positions  = AS_FindDotPositions(stimuli,visualFeatures, quest)
%This function finds and assigns positions for dots.
            nrTrials = max(stimuli(:,1));
            positions = [];
             
            if nargin < 3 
                quest = 0;
            end
           
            minX = visualFeatures(4)/2 - visualFeatures(3)/2; 
            minY = visualFeatures(5)/2  -  visualFeatures(3)/2;
            maxX = visualFeatures(4)/2  + visualFeatures(3)/2;
            maxY = visualFeatures(5)/2  + visualFeatures(3)/2;

            thisTrialSetcounter = 1;
 switch quest
     case 0
    for trial = 1:nrTrials 
        thisTrialSet = [];
            while stimuli(thisTrialSetcounter,1) == trial
                thisTrialSet = [thisTrialSet; stimuli(thisTrialSetcounter,:)];
                 if thisTrialSetcounter < size(stimuli, 1)
                thisTrialSetcounter = thisTrialSetcounter + 1;
                 else
                     break;
                 end  
            end
    
          nrDots = size(thisTrialSet,1);
          currentPositions = [];
          for dot = 1:nrDots
              if dot == 1
                  outofbounds = 1;
                  while outofbounds==1
                       newX = minX + (maxX-minX).*rand(1,1);
                       newY = minY + (maxY-minY).*rand(1,1);   
                       thisDotPosition = [newX newY newX+2*thisTrialSet(dot,7) newY+2*thisTrialSet(dot,7)];
                       
                       if thisDotPosition(1) > minX && thisDotPosition(3) < maxX && thisDotPosition(2) > minY && thisDotPosition(4) < maxY
                          outofbounds = 0;        
                       end
                  end
                 
                  
                  currentPositions = [currentPositions; thisDotPosition];
              
              else
                   upptagen = 1;
                   while upptagen == 1
                          outofbounds = 1;
                          while outofbounds==1
                               newX = minX + (maxX-minX).*rand(1,1);
                               newY = minY + (maxY-minY).*rand(1,1);   
                               thisDotPosition = [newX newY newX+2*thisTrialSet(dot,7) newY+2*thisTrialSet(dot,7)];

                               if thisDotPosition(1) > minX && thisDotPosition(3) < maxX && thisDotPosition(2) > minY && thisDotPosition(4) < maxY
                                   outofbounds = 0;        
                               end
                          end

                   isupptagen = 0;
                           for j = 1:size(currentPositions,1)
                               comparePosition = currentPositions(j,:);                        
                               if abs(thisDotPosition(1) - comparePosition(1))-8< max([(thisDotPosition(3)-thisDotPosition(1)) (comparePosition(3)-comparePosition(1))]) && abs(thisDotPosition(2) - comparePosition(2))-8< max([(thisDotPosition(4)-thisDotPosition(2)) (comparePosition(4)-comparePosition(2))])
                                   isupptagen = 1;
                               end
                           end

                           if isupptagen == 0
                               upptagen = 0;
                           end
                   end
                   
                   currentPositions = [currentPositions; thisDotPosition];
              end
              positions = [positions thisDotPosition'];
          end
    end
    
     case 1 
             
          nrDots = size(stimuli,1);
          currentPositions = [];
          for dot = 1:nrDots
              if dot == 1
                  outofbounds = 1;
                  while outofbounds==1
                       newX = minX + (maxX-minX).*rand(1,1);
                       newY = minY + (maxY-minY).*rand(1,1);   
                       thisDotPosition = [newX newY newX+2*stimuli(dot) newY+2*stimuli(dot)];
                       
                       if thisDotPosition(1) > minX && thisDotPosition(3) < maxX && thisDotPosition(2) > minY && thisDotPosition(4) < maxY
                          outofbounds = 0;        
                       end
                  end
                 
                  
                  currentPositions = [currentPositions; thisDotPosition];
              
              else
                   upptagen = 1;
                   while upptagen == 1
                          outofbounds = 1;
                          while outofbounds==1
                               newX = minX + (maxX-minX).*rand(1,1);
                               newY = minY + (maxY-minY).*rand(1,1);   
                               thisDotPosition = [newX newY newX+2*stimuli(dot) newY+2*stimuli(dot)];

                               if thisDotPosition(1) > minX && thisDotPosition(3) < maxX && thisDotPosition(2) > minY && thisDotPosition(4) < maxY
                                   outofbounds = 0;        
                               end
                          end

                   isupptagen = 0;
                           for j = 1:size(currentPositions,1)
                               comparePosition = currentPositions(j,:);                        
                               if abs(thisDotPosition(1) - comparePosition(1))-8< max([(thisDotPosition(3)-thisDotPosition(1)) (comparePosition(3)-comparePosition(1))]) && abs(thisDotPosition(2) - comparePosition(2))-8< max([(thisDotPosition(4)-thisDotPosition(2)) (comparePosition(4)-comparePosition(2))])
                                   isupptagen = 1;
                               end
                           end

                           if isupptagen == 0
                               upptagen = 0;
                           end
                   end
                   
                   currentPositions = [currentPositions; thisDotPosition];
              end
              positions = [positions thisDotPosition'];
          end
   
    
end






