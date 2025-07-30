from .Common import Common as Parent
import json


class Group(Parent):

    def getAll(self):
        try:
            jsonResponse = self.requestUrl('/groups')
        except Exception as ex:
            if Parent.VERBOSE:
                print('Exception:', ex)
            return '%s' % ex

        if (jsonResponse['succes']):
            if Parent.VERBOSE:
                print('getAll', jsonResponse)
            return json.loads(jsonResponse['data'])
        else:
            return jsonResponse['messages'][0]

    def getNodes(self, name):
        return True

    def add(self, name):
        data = {
            'name': name,
        }
        try:
            jsonResponse = self.requestUrl('/groups', data, 'POST')
        except Exception as ex:
            return '%s' % ex

        if (jsonResponse['succes']):
            return name
        else:
            return jsonResponse['messages'][0]