library(gtools)
findKmed <-function(K, m, Plist){
  
  index<-sort(Plist)
  m <- index[round(length(Plist)/2)]
  return(which(m==Plist))
  
  
}

updateScore <-function(K.med, sizeBlocks, outlierThreshold){
  fin <- length(K.med[1,])
  K.med[,(fin-1)] <- K.med[,(fin-1)]+1
  K.med[,(fin)]<- ifelse((K.med[,(fin-1)] > outlierThreshold & K.med[,(fin)]==TRUE),FALSE,K.med[,(fin)])
  
  return(K.med)
  
}

logistic<-function(y, f){
  
  return(log(1+exp(-1*(2*y-1)*f)))
  #if (y==1) return(log(1+exp(-1*y*f)))
  #else return(log(1+exp(y*f)))
  }

gradient <- function(ut,K.med,sizeBlocks,pos.last.par){
  vec <- c()
  u <- c()
  u <- ut
  for (i in c(1:length(ut))) {
    vec[i] <- 0
    for (j in c(1:sizeBlocks)) {
      vec[i] <- vec[i] - K.med[j,1]*u[i]/(exp(sum(u*K.med[j,2:pos.last.par])*K.med[j,1])+1)
    }
  }
  return(vec)
}

gradientRapideSupport <- function(K.med,u){
  A<-exp(K.med[1,1]*(sum(u[[2]]*K.med[1,2:4])))
  u<-u*(K.med[1,1]*(1/(A+1)))
}

gradientRapide <- function(ut,K.med,sizeBlocks){
  vec <- replicate(length(ut),0)
  u <- c()
  u <- ut
 # for (j in c(1:sizeBlocks)) {
#    vec[j] <- vec[] + gradientRapideSupport(K.med[j,],u)
#  }
  m<-dim(K.med)[2]
  n<-dim(K.med)[1]
  y<-K.med[,1]
  uMat<-t(replicate(n,u))
  x<-K.med[,2:m]
  f<-x*uMat
  esp<-rowSums(f)*y
  A<-1/(1+exp(esp))
  
  for (i in 1:n) {
    vec<-vec+(-1*y[i]*A[i])*u  
  }
  
  # vec <- u+sum(B)
  
  #ate aqui ta bom
  
  
  
  # for (i in 1:n) {
  #   y<-K.med[i,1]
  #   A<-exp(-y*sum(ut*t(K.med[i,2:m])))
  #   A<-A/(1+A)
  #   
  #   for ( j in 1:length(ut))
  #   {
  #     mTemp<--1*y*u[j]*A
  #     vec[j] <- vec[j]+ mTemp
  #   }
  # } 
  return(vec)
}


logistic2 <-function(y,f){
  #return(log(1+exp(-1*x)))
  #return(-1*y*log(1/(1+exp(-1*f)))-(1-y)*log(1-(1/(1+exp(-1*f)))))
  if (y==1) {
    return(-log(f))
  } else {
    return(-log(1-f))
  }
}

gradientScalar <- function(y,f){
  g = 1/(1+exp(-f))
  return(g*y)
}

outliersFinder <- function(DS, N){
  
  fin <- length(DS[1,])
  nbOut <- sum(DS[,fin])
  index.Out <- which(DS[,fin])
  
  cat("Number of otliers in the dataset : ", nbOut)
  
  #print(DS[,(fin-1)])
  #print(sum(DS[,(fin-1)]))
  return(index.Out)
  
}

momGradientDescent <- function(K, bigT, DS, outlierThreshold){
  begin.time <- Sys.time()
  N<-c(1:length(DS[,1]))
  longN = length(N)
  etaT<-1/bigT
  
  if (K < 3 | K > longN/2){
    return("Number of blocks not appropriate")
  }
  
  u = list()
  u[[1]] <- regression(DS)
  print(paste0("u1: ",u))
  
  DS[,"X0"] <- replicate(length(DS[,1]),1)
  
  nb.par = length(DS[1,])-1
  pos.last.par = nb.par + 1
  

  
  for (i in 1:longN) {
    DS[i,"Loss"] <- logistic(DS[i,1],(rowSums(t(u[[1]]*t(DS[i,2:pos.last.par])))))
  }
  
  # DS[,"Loss"] <- logistic(DS[,1],(rowSums(t(u[[1]]*t(DS[,2:pos.last.par])))))
  DS[,"Score"] <- replicate(length(DS[,1]),0)
  DS[,"IsOutlier"] <- replicate(length(DS[,1]),TRUE)
  
  sizeBlocks = longN%/%K
  blocks = matrix(nrow = K, ncol = sizeBlocks)
  Plist = c()
  for (t in c(1:(bigT-1))) {
    # print(t)
    # if ((t%%100)==0) print(t)
    # 
    theta_t = sample(N)
    
    for (i in 1:longN) {
      # if(i==62){
      #   print(rowSums(t(u[[t]]*t(DS[i,2:pos.last.par]))))
      #   print(logistic(DS[i,1],(rowSums(t(u[[t]]*t(DS[i,2:pos.last.par]))))))
      # }
      DS[i,(pos.last.par+1)] <- logistic(DS[i,1],(rowSums(t(u[[t]]*t(DS[i,2:pos.last.par])))))
    }
    # for (i in 1:longN) {
    #   DS[i,(pos.last.par+1)] <-  DS[i,(pos.last.par+1)]+logistic(DS[i,1],(rowSums(t(u[[t]]*t(DS[i,2:pos.last.par])))))
    # }
    
    # DS[,(pos.last.par+1)] <- logistic(DS[,1],(rowSums(t(u[[1]]*t(DS[,2:pos.last.par])))))
    # 
    for (j in c(1:K)) {
      blocks[j,] = theta_t[c(((j-1)*sizeBlocks+1):(j*sizeBlocks))]
    }
    
    
    temp <- 0
    for (i in c(1:K)) {
      # temp = 0
      # for (j in c(1:sizeBlocks)) {
      #   temp = temp + DS[blocks[i,j],pos.last.par+1]
      # }
      Plist[i]<- sum(DS[blocks[i,],pos.last.par+1])
    }
    K.med.Index <- findKmed(K,median(Plist), Plist)
    DS[blocks[K.med.Index,],] <- updateScore(DS[blocks[K.med.Index,],], sizeBlocks, outlierThreshold)
    
    # cat("index Kmed\n")
    # print(blocks[K.med.Index,])
    # OPTION 1 -> ALGORITHME ALIKE
    K.med <- DS[blocks[K.med.Index,],]
    sum.Grads <- gradientRapide(u[[t]],K.med[,1:pos.last.par],sizeBlocks)
    u[[(t+1)]] = u[[t]] - etaT*sum.Grads
    print(u[[(t+1)]])
    
    # OPTION 2 -> MY IDEA
    # K.med <- DS[blocks[K.med.Index,],1:3]
    # K.med[,1]<-factor(K.med[,1])
    # model <- glm(K.med[,1]~K.med[,2]+K.med[,3], data = K.med,family = "binomial")
    # w<-model$coefficients
    # dataSetPlotter(DS[,1:3])
    # abline(a=w[3],b=w[1:2])
    # u[[(t+1)]]<-c(w[2],w[3],w[1])
    
    # print(u[[(t+1)]])
    # u[[(t+1)]] = rnorm(nb.par,mean = 1,sd = 2)
    # # if (norm(rbind(u[[t+1]],u[[]]),"2") < 0.0001){
    #   break()
    # }
    
  }
  index.Outliers <- outliersFinder(DS, N)
  print(index.Outliers)
  teste<-which(resp[[1]][,6]>mean(resp[[1]][,6]))
  DS[,1]<-factor(DS[,1])
  model <- glm(DS[teste,1]~DS[teste,2]+DS[teste,3], data = DS[teste,],family = "binomial")
  w<-model$coefficients
  dataSetPlotter(DS[,1:3])
  abline(a=w[3],b=w[1:2])
  
  end.time <- Sys.time()
  print(end.time-begin.time)
  
  bigT<-bigT-1
  # return(u[[bigT]])
  
  resp<-list()
  resp[[1]]<-DS
  resp[[2]]<-u[[bigT]]
  resp[[3]]<-w
  return(resp)
}

