from typing import List
import requests, json

class YouTubeTagGenerator:
    def __init__(self):
        self.params = (
                        ('client', 'youtube'),
                        ('hl', 'en'),
                        ('gl', 'us'),
                        ('gs_rn', '64'),
                        ('gs_ri', 'youtube'),
                        ('ds', 'yt'),
                        ('cp', '2'),
                        ('gs_id', 'g'),
                        ('xhr', 't'),
                        ('xssi', 't'),
                    )
        self.url = 'https://suggestqueries-clients6.youtube.com/complete/search'

    def show_tags(self, query: str) -> List[str]:
        query = query or ''

        if not bool(len(query.replace(' ',''))): # empty query is not allowed ("", "   ")
            return []
            
        params = self.params + (('q', query),)

        response = requests.get(self.url, params=params).text

        if response[:5] != ")]}'\n": return []
            
        tags = json.loads(response[5:])[1]

        all_tags = [tag[0] for tag in tags]
        
        return all_tags