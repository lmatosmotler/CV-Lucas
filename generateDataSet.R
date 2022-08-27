dataSetGenerator <- function(nb.Inliers,nb.Outliers){
  X11=rnorm(n = nb.Inliers, mean = -1, sd = 1.4)
  X12=rnorm(n = nb.Inliers, mean = 1, sd = 1.4)
  X13=rnorm(n = nb.Outliers, mean = 24, sd = 0.1)
  X1 = append(X11,X12)
  X1=append(X1,X13)
  
  X21=rnorm(n = nb.Inliers, mean = -1, sd = 1.4)
  X22=rnorm(n = nb.Inliers, mean = 1, sd = 1.4)
  X23=rnorm(n = nb.Outliers, mean = 8, sd = 0.1)
  X2 = append(X21,X22)
  X2=append(X2,X23)
  
  Y1 = replicate(nb.Inliers, 1)
  Y2 = replicate(nb.Inliers, -1)
  Y3 = replicate(nb.Outliers, 1)
  Y = append(Y1, Y2)
  Y = append(Y, Y3)
  
  DS = data.frame(Y, X1, X2)
  DS
}

dataSetPlotter<-function(DS){
  DS[,"Y.plot"] = DS[,1]
  DS$Y.plot = factor(DS$Y.plot)
  mycolors = c('green','red')
  with(DS,plot(DS[,2],DS[,3],col=mycolors[Y.plot]))
}

dataSetPreTest<-function(DS){
  DS[,"Score"] = replicate(630,0)
  DS[,"IsOutlier"] = replicate(630,TRUE)
  DS
}

dataSetsOGenerator <- function(DS){
  DSsansOutlier = DS[1:600,1:3]
  DSsansOutlier
}

make.grid = function(x, n = 75) {
  grange = apply(x, 2, range)
  x1 = seq(from = grange[1,1], to = grange[2,1], length = n)
  x2 = seq(from = grange[1,2], to = grange[2,2], length = n)
  expand.grid(X1 = x1, X2 = x2)
}