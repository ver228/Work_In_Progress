#install.packages(c("devtools","gplots"))
#source("http://www.bioconductor.org/biocLite.R")
#biocLite(c("Biobase","org.Hs.eg.db","AnnotationDbi"))
#biocLite("alyssafrazee/RSkittleBrewer")

tropical = c('darkorange', 'dodgerblue', 'hotpink', 'limegreen','yellow')
palette(tropical)
par(pch=19)


library(gplots)
library(devtools)
library(Biobase)
library(RSkittleBrewer)
library(org.Hs.eg.db)
library(AnnotationDbi)

con = url("http://bowtie-bio.sourceforge.net/recount/ExpressionSets/bodymap_eset.RData")
load(file=con)
close(con)
bm = bodymap.eset

pdata = pData(bm)
edata = exprs(bm)
fdata = fData(bm)

table(pdata$gender)
table(pdata$gender, pdata$race)

#check quartiles
summary(edata)

#show missing values in the table
table(pdata$age, useNA="ifany")

#check if there are missing values
sum(pdata$age==" ", na.rm=TRUE )

gene_na = rowSums(is.na(edata))
table(gene_na)


dim(fdata)
dim(pdata)
dim(edata)


boxplot(edata[,1])
boxplot(log2(edata+1), col=2, range=0)


par(mfrow=c(1,2))
hist(log2(edata[,1]+1), col=2)
hist(log2(edata[,2]+1), col=2)

par(mfrow=c(1,1))
plot(density(log2(edata[,1]+1)), col=2)
lines(density(log2(edata[,2]+1)), col=3)

#compare two genes
qqplot(log2(edata[,1]+1),log2(edata[,2]+1), col=1)
abline(c(0,1))

#compare two genes (MA plots)
mm = log2(edata[,1]+1) - log2(edata[,2]+1)
aa = log2(edata[,1]+1) + log2(edata[,2]+1)
plot(aa,mm,col=2)

##
edata = as.data.frame(edata)
filt_edata = subset(edata, rowMeans(edata)>1)
dim(filt_edata)

boxplot(as.matrix(log2(filt_edata+1)), col=2)

## consistency
aeid = as.character(fdata[,1])
chr = AnnotationDbi::select(org.Hs.eg.db,keys=aeid,keytype="ENSEMBL",columns="CHR")
#remove duplicated values
chr = chr[!duplicated(chr[,1]),]

head(chr)
dim(chr)
dim(edata)

all(chr[,1] == rownames(edata))

edatay = subset(edata, chr$CHR=="Y")
dim(edatay)

boxplot(colSums(edatay) ~ pdata$gender)
points(colSums(edatay) ~ jitter(as.numeric(pdata$gender)),
       col=as.numeric(pdata$gender), pch=19)

ematrix = as.matrix(edata)[rowMeans(edata)>10000,]
heatmap(ematrix)
colramp = colorRampPalette(c(3,"white",2))(9)
heatmap(ematrix, col=colramp, Rowv=NA, Colv=NA)

heatmap.2(ematrix, col=colramp, Rowv=NA, Colv=NA, dentrogram="none", scale="row", trace="none")

#%%
hist(rnorm(1000), col=2, breaks=100)
hist(log2(edata[,1]+1), col=2, breaks=100)
hist(log2(edata[,1]+1), col=2, breaks=100, xlim=c(1,15), ylim=c(0,400))

hist(rowSums(edata==0), col=2)

low_genes = rowMeans(as.matrix(edata))<5
low_genes2 = rowMedians(as.matrix(edata))<5
table(low_genes,low_genes2)

filt_edata2 = subset(as.data.frame(edata), !low_genes2)
dim(filt_edata2)
hist(log2(filt_edata2[,1]+1), col=2, breaks=100)

#install.packages("dendextend")
library("dendextend")

edata = exprs(bm)
edata = edata[rowMeans(edata) > 5000, ]
edata = log2(edata + 1)

dist1 = dist(t(edata))

heatmap(as.matrix(dist1), col=colramp, Colv=NA, Rowv=NA)

hclust1 = hclust(dist1)
plot(hclust1, hang=-1)

dend = as.dendrogram(hclust1)
#dend = color_labels(hclust1, 4, 1:4)
#color_labels(dend) = c(rep(1,10), rep(1,9))
plot(dend)

kmeans1 = kmeans(edata, centers=3)
names(kmeans1)

matplot(t(kmeans1$centers), type="l", "lwd"=3)
table(kmeans1$cluster)

newdata = as.matrix(edata)[order(kmeans1$cluster),]
heatmap(newdata, col=colramp, Colv=NA, Rowv=NA)

