# text_summarization
Develop and implement text summarisation extraction algorithm from 2 sources

## Algorithms:
- SumTextOne source link: https://blog.floydhub.com/gentle-introduction-to-text-summarization-in-machine-learning/
- SumTextTwo source link: https://medium.com/datapy-ai/nlp-building-text-summarizer-part-1-902fec337b81

## Web app link
The web app is using dash for its base and heroku to host it. 
Link: https://textsumms.herokuapp.com/

### Web app explanation
Currently, the web app could summarise any text from a wikipedia by giving the wikipedia link in the text input, or simply change the end part of the link, i.e, https://en.wikipedia.org/wiki/Chosen_title (change Chosen_title). Each algorithm has their own parameter. For the first algorithm, you can change the threshold parameter, which will only take sentences that exceed a given score (the average score from all sentences * chosen threshold). Increasing the threshold will reduce the number of sentences that will appear in the summarization box. The slider range in the second algorithm indicate the number of sentences you want to get out of the summarization box. For more information, please visit the source link for each algorithms.

