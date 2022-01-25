Nballoons = 30
maxPress = 32

flag = 0
balloons = matrix(nrow = Nballoons, ncol = maxPress+1)
while(flag==0){ 
for(k in 1:Nballoons){
  balloonSeq = rep(0,maxPress)
  boom[k] <- sample(1:maxPress,1)
  balloonSeq[boom[k]] <- 1
  balloons[k,1:maxPress] <- balloonSeq
  balloons[k,maxPress+1] <- boom[k]
  
}

 boomFirst <- mean(boom[1:(Nballoons/2)])
 boomSecond <- mean(boom[(Nballoons/2+1):Nballoons])
 
 if(boomFirst==16&boomSecond==16){
   flag =1
 }
  
}

printBalloons <- data.frame(rep(0, Nballoons), balloons)

write.csv(printBalloons, "BART_Input.csv", row.names = FALSE,col.names = =FALSE)
