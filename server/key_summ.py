from summarizer import Summarizer
import re

#function for passing in 1 keyword and generating a summary
def key_summar(transcript, keyword):
    combined = ""
    for line in transcript:
        line = line.rstrip()
        combined += line
    text = re.split('[?.]', combined)

    paragraph = ""
    for i in text:
        if keyword in i:
            paragraph += i + '.'
    print (paragraph)
    sentences = re.split('[.]', paragraph)
    model = Summarizer()
    if len(sentences)<10 or len(sentences)==10:
        result = model(paragraph, ratio= 0.8)
        result = result[:-1]
    elif len(sentences)>10:
        result = model(paragraph, ratio= 0.2)
        result = result[:-1]
    full = re.split('[.]', result) 
    final = ""
    final = keyword + ":" 
    for i in full:
        final += '-' + i + '\n'   
    return final
"""
keywords = "habituation"
keywords = keywords.split(', ')
summary = ""
for key in keywords:
    with open ('text-files/SOSC 1960 memory_otter.ai.txt', 'r') as transcript:
        summary += key_summar (transcript, key)
        
print(summary)

"""