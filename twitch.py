import json
import requests

class Twitch:

    def __init__(self, credentials):
        self.client_id = credentials['client_id']
        self.oauth_token = credentials['oauth_token']
        self.channel_login = credentials['channel_login']

    def get_drop_campaigns(self):
        response = requests.post(
            'https://gql.twitch.tv/gql',
            headers={
                'Content-Type': 'text/plain;charset=UTF-8',
                'Client-Id': self.client_id,
                'Authorization': 'OAuth ' + self.oauth_token
            },
            data=json.dumps([
                {
                    'operationName': 'ViewerDropsDashboard',
                    'extensions': {
                        'persistedQuery': {
                            'version': 1,
                            'sha256Hash': 'e8b98b52bbd7ccd37d0b671ad0d47be5238caa5bea637d2a65776175b4a23a64'
                        }
                    }
                }
            ])
        )

        try:
            return response.json()[0]['data']['currentUser']['dropCampaigns']
        except Exception as e:
            print(e)
            return None

    def get_drop_campaign_details(self, dropIds):
        data = []
        
        for dropId in dropIds:
            data.append({
                'operationName': 'DropCampaignDetails',
                'extensions': {
                    'persistedQuery': {
                        'version': 1,
                        'sha256Hash': 'f6396f5ffdde867a8f6f6da18286e4baf02e5b98d14689a69b5af320a4c7b7b8'
                    }
                },
                'variables': {
                    'dropID': dropId,
                    'channelLogin': self.channel_login
                }
            })
        
        response = requests.post(
            'https://gql.twitch.tv/gql',
            headers={
                'Content-Type': 'text/plain;charset=UTF-8',
                'Client-Id': self.client_id,
                'Authorization': 'OAuth ' + self.oauth_token
            },
            data=json.dumps(data)
        )

        try:
            return [x['data']['user']['dropCampaign'] for x in response.json()]
        except Exception as e:
            print(e)
            return None
