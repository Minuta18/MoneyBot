import requests

class RequestMaker:
    def __init__(self):
        self.session = requests.Session()
        self.session.trust_env = False

    def get(self, *args, **kwargs) -> requests.Response:
        return requests.get(*args, **kwargs)
    
    def post(self, *args, **kwargs) -> requests.Response:
        return requests.post(*args, **kwargs)
    
    def put(self, *args, **kwargs) -> requests.Response:
        return requests.put(*args, **kwargs)
    
    def delete(self, *args, **kwargs) -> requests.Response:
        return requests.delete(*args, **kwargs)