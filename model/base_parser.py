import json

class BaseParser(object):

    def __init__(self,file):
        self.file = file
        self.data = {}
        self.content = None

    def parse(self):
        raise Exception("method not implemented")

    def set_content(self):
        raise Exception("method not implemented")


    def dic_to_json_parse(self):
        return json.dumps(self.data)
