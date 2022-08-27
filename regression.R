regression<-function(DS){
  dataSetPlotter(DS)
  DS[,1]<-factor(DS[,1])
  model <- glm(DS[,1]~DS[,2]+DS[,3], data = DS,family = "binomial")
  #summary(model)
  w<-model$coefficients
  #print(w)
  abline(a=w[1],b=w[2:3])
  
  w<-c(w[2],w[3],w[1])
  print(paste0("w",w))
  w
}

plotPostMom<-function(DS,w){
  dataSetPlotter(DS[,1:3])
  abline(a=w[3],b=w[1:2])
}