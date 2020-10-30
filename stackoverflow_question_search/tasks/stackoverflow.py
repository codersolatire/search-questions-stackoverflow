#import beautifulsoup, requests and json

import requests as rq
from bs4 import BeautifulSoup
import json

#Stackoverflow url 
datastack = rq.get("https://stackoverflow.com/questions")

soup = BeautifulSoup(datastack.text,"html.parser")

#CSS class question-summary used to take out all questions
questions = soup.select(".question-summary") 


questions_data = {
	"questions":[]
}

for que in questions:
	q = que.select_one('.question-hyperlink').getText()
	vote_count = que.select_one('.vote-count-post').getText()
	views = que.select_one('.views').attrs['title']
	tags = [i.getText() for i in (que.select('.post-tag'))]
	
	#json used to store data in a json format
	questions_data['questions'].append({
		"question" : q,
		"views": views,
		"vote_count": vote_count,
		"tags": tags
	})
		
#result_json = json.dumps(questions_data, sort_keys = True, indent=4)

#store results in scrapped_data.json file
with open('scrapped_data.json','w') as fp:
	json.dump(questions_data,fp)