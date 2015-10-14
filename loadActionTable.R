library(tidyr)
library(dplyr)

# Load an action table by name, cleans crud characters,
# and adds a roll column for grouping
loadActionTable <- function(name) {
    filename <- paste0(name, "_actiontable.dat")
    df <- read.csv(filename, stringsAsFactors = FALSE)
    df[,1] <- extract_numeric(df[,1])
    df[,5] <- extract_numeric(df[,5])
    df[,7] <- extract_numeric(df[,7])
    df[,9] <- extract_numeric(df[,9])
    df$roll <- paste0(df[,1],df[,2],df[,3],df[,4],df[,5])
    names(df) <- c("d1","d2","d3","d4","d5","a","sum","ct","avg","roll")
    df
}

# Finds difference between max and next to max values in a list
maxdev <- function(col) { scol <- sort(col, decreasing = TRUE); scol[1]-scol[2] }
# Finds the action (column index-1) which maximizes a list of numbers
maxact <- function(col) { which(col==max(col))[1] - 1 }

# Creates a new data frame keyed by roll containing the best action from each 
# game and finds the deviation between bext action value and the next best value.
compareActionTables <- function(name1, name2) {
    at1 <- loadActionTable(name1)
    at2 <- loadActionTable(name2)
    
    at1 <- at1 %>% group_by(roll) %>% summarize(maxact(avg), maxdev(avg))
    names(at1) <- c("roll","a1", "dev1")
    at2 <- at2 %>% group_by(roll) %>% summarize(maxact(avg), maxdev(avg))
    names(at2) <- c("roll","a2", "dev2")
    merge(at1,at2)
}