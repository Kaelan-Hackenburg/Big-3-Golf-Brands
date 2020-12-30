############################## Install Packages ##############################
#install.packages('tidytext')
#install.packages('SnowballC')
#install.packages('tm')
#install.packages('wordcloud')
library(tidyverse)
library(tidytext)
library(SnowballC)
library(tm)
library(scales)
##############################################################################

############################## Working Directory #############################
working_directory <- ("/Users/kaelanhackenburg/Python-Kaelan/Pfizer Vaccine")
setwd(working_directory)
##############################################################################

temporary_table <- paste(working_directory, "/pfizer_vaccine_covid.csv", sep = "")
pfizer <- read.csv(temporary_table, header = TRUE)
summary(pfizer)

pfizer_tweets <- select(pfizer, Tweet_Text)

pfizer_td1 <- unnest_tokens(pfizer_tweets, word, Tweet_Text)
counts <- count(pfizer_td1, word)
results1 <- arrange(counts, desc(n))


##################### Remove stop words from the data ###################
data("stop_words")
pfizer_td2 <- anti_join(pfizer_td1, stop_words)
counts2 <- count(pfizer_td2, word)
results2 <- arrange(counts2, desc(n))
#########################################################################

############################ Remove Numeric Values ##########################
pattern <- '\\b[0-9]+\\b'

# Apply the above regex
pfizer_td2$word <- str_replace_all(pfizer_td2$word, pattern, '')
counts3 <- count(pfizer_td2, word)
results3 <- arrange(counts3, desc(n))
#############################################################################

######### Replace all new lines, tabs, and blank spaces with a value of nothing and then filter out those values #########
pfizer_td2$word = str_replace_all(pfizer_td2$word, '[:space:]', '')
pfizer_td3 <- filter(pfizer_td2, !(word == ''))
counts4 <- count(pfizer_td3, word)
results4 <- arrange(counts4, desc(n))
##########################################################################################################################

################################## Remove Unknown Words / Hashtags ###########################
list_remove <- c("xf0","xe2","x9f","x80", "x99s",
                 "t.co","covide","vaccine","pfizer")
pfizer_td3 = filter(pfizer_td3, !(word %in% list_remove))
##############################################################################################

############################ Plot words greater than 0.5 Proportion ##########################
frequency = pfizer_td3 %>%
  count(word) %>%
  arrange(desc(n)) %>%
  mutate(proportion = (n / sum(n)*100)) %>%
  filter(proportion >= 0.5)



ggplot(frequency, aes(x = proportion, y = word)) +
  geom_abline(color = "gray40", lty = 2) +
  geom_jitter(alpha = 0.1, size = 2.5, width = 0.3, height = 0.3) +
  geom_text(aes(label = word), check_overlap = TRUE, vjust = 1.5) +
  scale_color_gradient(limits = c(0, 0.001), low = "darkslategray4", high = "gray75") +
  theme(legend.position="none") +
  labs(y = 'Word', x = 'Proportion')
##############################################################################################


################################# Apply Stemming Using SnowballC #############################
pfizer_td4 <- mutate_at(pfizer_td3, "word", funs(wordStem((.), language = "en")))
counts5 <- count(pfizer_td4, word)
results5 <- arrange(counts5, desc(n))
##############################################################################################

################################# New Frequencies #############################
frequency2 = pfizer_td4 %>%
  count(word) %>%
  arrange(desc(n)) %>%
  mutate(proportion = (n / sum(n)*100)) %>%
  filter(proportion >= 0.5)

ggplot(frequency2, aes(x = proportion, y = word)) +
  geom_abline(color = "gray40", lty = 2) +
  geom_jitter(alpha = 0.1, size = 2.5, width = 0.3, height = 0.3) +
  geom_text(aes(label = word), check_overlap = TRUE, vjust = 1.5) +
  scale_color_gradient(limits = c(0, 0.001), low = "darkslategray4", high = "gray75") +
  theme(legend.position="none") +
  labs(y = 'Word', x = 'Proportion')
###############################################################################


