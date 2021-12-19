import configparser
import datetime
import json
import requests

from twitch import Twitch


def main():
    config = configparser.ConfigParser()
    config.read('config.ini')

    twitch = Twitch(config['credentials'])
    
    # Get all drop campaigns
    dropCampaigns = twitch.get_drop_campaigns()

    # Filter Sea of Thieves drops
    dropIds = []
    for dropCampaign in dropCampaigns:
        if dropCampaign['game']['id'] == '490377':
            if datetime.datetime.now(datetime.timezone.utc) >= datetime.datetime.strptime(dropCampaign['endAt'], '%Y-%m-%dT%H:%M:%S%z'):
                continue

            dropIds.append(dropCampaign['id'])

    # Request details of Sea of Thieves drops
    SeaOfThievesDrops = twitch.get_drop_campaign_details(dropIds)

    # Filter currently active drops
    for SeaOfThievesDrop in SeaOfThievesDrops:
        print(SeaOfThievesDrop)

if __name__ == '__main__':
    main()