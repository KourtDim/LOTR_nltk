import bs4
import urllib.request
import nltk
import pandas as pd
import random
import string

"""
PART OF SPEECH TAGS

CC coordinating conjunction
CD cardinal digit
DT determiner
EX existential there (like: “there is” … think of it like “there exists”)
FW foreign word
IN preposition/subordinating conjunction
JJ adjective ‘big’
JJR adjective, comparative ‘bigger’
JJS adjective, superlative ‘biggest’
LS list marker 1)
MD modal could, will
NN noun, singular ‘desk’
NNS noun plural ‘desks’
NNP proper noun, singular ‘Harrison’
NNPS proper noun, plural ‘Americans’
PDT predeterminer ‘all the kids’
POS possessive ending parent‘s
PRP personal pronoun I, he, she
PRP$ possessive pronoun my, his, hers
RB adverb very, silently,
RBR adverb, comparative better
RBS adverb, superlative best
RP particle give up
TO to go ‘to‘ the store.
UH interjection errrrrrrrm
VB verb, base form take
VBD verb, past tense took
VBG verb, gerund/present participle taking
VBN verb, past participle taken
VBP verb, sing. present, non-3d take
VBZ verb, 3rd person sing. present takes
WDT wh-determiner which
WP wh-pronoun who, what
WP$ possessive wh-pronoun whose
WRB wh-abverb where, when
"""
book_titles= ["The_Fellowship_of_the_Ring", "The_Two_Towers", "The_Return_of_the_King"]

## Fetching the urls
url_fellowship = urllib.request.urlopen("https://archive.org/stream/TheLordOfTheRing1TheFellowshipOfTheRing/The%20Lord%20Of%20The%20Ring%201-The%20Fellowship%20Of%20The%20Ring_djvu.txt").read()
url_two_towers = urllib.request.urlopen("https://archive.org/stream/TheLordOfTheRing1TheFellowshipOfTheRing/The%20Lord%20Of%20The%20Ring%202-The%20Two%20Towers_djvu.txt")
url_return_of_the_king = urllib.request.urlopen("https://archive.org/stream/TheLordOfTheRing1TheFellowshipOfTheRing/The%20Return%20Of%20The%20King_djvu.txt")

url = [url_fellowship,url_two_towers,url_return_of_the_king]
selection = int(input("Select which book from the LotR series to analyze: \n press 1 for The Fellowship of the Ring \n press 2 for The Two Towers \n press 3 for The Return of the King \n"))


template = "The book selected for analysis is: {book}"
if int(selection) == 1: 
     s_url = url[0]
     title = book_titles[0]
     print(template.format(book= title))
elif int(selection) == 2:
     s_url = url[1]
     title = book_titles[1]
     print(template.format(book= title))
elif int(selection) == 3: 
     s_url = url[2]
     title = book_titles[2]
     print(template.format(book= title))

#    Soup
soup = bs4.BeautifulSoup(s_url,"lxml")

#find the text:
text=  str(soup.pre)
text= text.replace("\n","")


#Tokenize the text in sentences

sentences=nltk.tokenize.sent_tokenize(text)


### Dataframe

#    Create a dataframe from the whole text for analysis

#    Create empty list

#    Populate the list

slen = len(sentences)
sample_df = pd.DataFrame()
sample=[]
index =[]
length = []
words = []
wordcount = []
stopword_filter=[]
stopword_wcount=[]
part_of_speech=[]

for i in range(slen):
     index.append(i)
     s = sentences[i]
     s.replace("â€™","'")
     l = len(s)
     w = nltk.tokenize.word_tokenize(s)
     words.append(w)
     wordcount.append(len(w))
     tag = nltk.pos_tag(w)
     part_of_speech.append(tag)
     sample.append(s)
     length.append(l)
     


#    Populate the  dataframe with the data

     
sample_df["Sent_Index"]=index
sample_df["Sentence"]=sample
sample_df["Len"]=length
sample_df["Words"]=words
sample_df["Wordcount"]=wordcount
sample_df["Part_of_speech"]=part_of_speech


#Creating Stopwords
stop_words= nltk.corpus.stopwords.words('english')
#Adding extra stopwords
more_stopwords = [",",".","'","I","!","The","?",";",":","He","'s","It","She","´","’","<",">","`","“","\n"]
#Extending the stopwords list
stop_words.extend(more_stopwords)

for s in range(slen):
     a = []
     for i in sample_df["Words"][s]:
          if i not in stop_words:
               a.append(i)
     stopword_filter.append(a)
     stopword_wcount.append(len(a))
                     
          
sample_df["Stopword_filter"]=stopword_filter
sample_df["Stopword_wcount"]=stopword_wcount


#    Store the dataframe in a csv file    
sample_df.to_csv(title+"_data.csv")

w =[]
t =[]

signs = ["'",",",".",";",":","-","_","?","!","''","¨","^","´","`","'",'"','/',"\"","â€™","``",'"','´','""',"' "," '"]

for i in part_of_speech:
     for l,k in i:
          if l in signs or k in signs:
               del(l,k)
          else:
               w.append(l)
               t.append(k)

pos_df = pd.DataFrame()
pos_df["Word"]= w
pos_df["PoS_Tag"]=t

pos_df.to_csv(title+"_PoS.csv")

#### Filter the text from stopwords

##   First create empty lists

filtered_sample =[]
"""
for i in sample_df["sentence"]:
     for word in nltk.word_tokenize(i):
          if word not in stop_words:
               filtered_sample.append(word)
"""

#Tokenize the text in words

print(title, " consists of: ", len(sample_df["Sentence"]), " sentences and ", len(pos_df["Word"]), " words")

"""

#Count words per sentence

words_per_sentence_fellowship=[]
#words_per_sentence_two_towers=[]
#words_per_sentence_return_of_the_king=[]

for i in sentences_fellowship:
     nltk.tokenize.word_tokenize(i)
     words_per_sentence_fellowship.append(i)

#for i in sentences_two_towers:
#     nltk.tokenize.word_tokenize(i)
#     words_per_sentence_two_towers.append(i)

#for i in sentences_return_of_the_king:
#     nltk.tokenize.word_tokenize(i)
#     words_per_sentence_return_of_the_king.append(i)

#Create a list with the word counts for each sentence
     
list_words_per_sentence_fellowship=[]
#list_words_per_sentence_two_towers=[]
#list_words_per_sentence_return_of_the_king=[]

for i in sentences_fellowship:
     list_words_per_sentence_fellowship.append(len(i))

#for i in sentences_two_towers:
#     list_words_per_sentence_two_towers.append(len(i))

#for i in sentences_return_of_the_king:
#     list_words_per_sentence_return_of_the_king.append(len(i))

print("In the book ", book_titles[0], "the average amount of words per sentence is: ", int(sum(list_words_per_sentence_fellowship)/len(list_words_per_sentence_fellowship)), " words")
#print("In the book ", book_titles[1], "the average amount of words per sentence is: ", int(sum(list_words_per_sentence_two_towers)/len(list_words_per_sentence_two_towers)), " words")
#print("In the book ", book_titles[2], "the average amount of words per sentence is: ", int(sum(list_words_per_sentence_return_of_the_king)/len(list_words_per_sentence_return_of_the_king)), " words")

#Creating Stopwords

stop_words= nltk.corpus.stopwords.words('english')
#Adding extra stopwords
more_stopwords = [",",".","'","I","!","The","?",";",":","He","'s","It","She","´","n't","’","<",">","`","1","2","3","4","5","6","7","8","9","0","“"]
#Extending the stopwords list
stop_words.extend(more_stopwords)

#### Filter the text from stopwords
"""
##   First create empty lists

tokenized_text=[]
#filtered_text_two_towers =[]
#filtered_text_return_of_the_king =[]

##   Build the for loop that will popoulate the lists with the filtered text

for w in nltk.tokenize.word_tokenize(text):
     if w not in stop_words:
          tokenized_text.append(w)
          
#for w in words_two_towers:
#     if w not in stop_words:
#          filtered_text_two_towers.append(w)
          
#for w in words_return_of_the_king:
#     if w not in stop_words:
#          filtered_text_return_of_the_king.append(w)

## Create a Pandas DataFrame with the filtered words for analysis
          
df_words = pd.DataFrame(tokenized_text,columns=["words"])
#df_words_two_towers = pd.DataFrame(filtered_text_two_towers,columns=["words"])
#df_words_return_of_the_king = pd.DataFrame(filtered_text_return_of_the_king,columns=["words"])

n = 50
used_words = df_words["words"].value_counts()[:n].index.tolist()
print("\n"," The ", n , " most used words in ", title ," where: \n", used_words,"\n")


"""
part_of_speech_fellowship=[]

for i in filtered_text_fellowship:
     tag=nltk.pos_tag(i)
     part_of_speech_fellowship.append(tag)


def extract_entities(text_fellowship):
     entities=[]
     for sent in nltk.sent_tokenize(text_fellowship):
          for chunk in nltk.ne_chunk(nltk.pos_tag(nltk.word_tokenize(sent))):
               if hasattr(chunk, 'label'):
                    entities.append((chunk.label(), ' '.join(c[0] for c in chunk.leaves())))
     return entities
                    
a= extract_entities(text_fellowship)

"""
