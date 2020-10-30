import requests as rq
from bs4 import BeautifulSoup
import json
from ast import literal_eval

class StackExchange:
    def fetchresults(self, params):

        datastack = rq.get("https://stackoverflow.com/questions/tagged/"+params+"/")

        soup = BeautifulSoup(datastack.text,"html.parser")

        questions = soup.select(".question-summary") 

        questions_data = {
            "questions": []
        }

        for que in questions:
            q = que.select_one('.question-hyperlink').getText()
            vote_count = que.select_one('.vote-count-post').getText()
            views = que.select_one('.views').attrs['title']
            tags = [i.getText() for i in (que.select('.post-tag'))]
            
            questions_data['questions'].append({
                "question" : q,
                "views": views,
                "vote_count": vote_count,
                "tags": tags
            })

        result_json = json.dumps(questions_data, sort_keys = True, indent=4)

        return result_json

    def fetchResultStackExchange(self, parameters):

        BASEURL = "https://api.stackexchange.com/2.2/search/advanced"

        datastack = rq.get(BASEURL,params=parameters)

        # datastack = rq.get("https://api.stackexchange.com/2.2/search/advanced?order=desc&sort=activity&q=raml%20rest&site=stackoverflow")

        stack_data = datastack.json()

        json_stack = json.dumps(stack_data, indent = 4)

        # print(type(json_stack))
        print(json_stack)

        return json_stack