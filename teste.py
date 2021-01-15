import json, datetime, requests

accountId = '3550'
r1 = requests.get('https://api-prod.solarworksmalawi.lamt.app/lamt/account/'+ accountId +'/asset', auth=('solarworksmalawi', 'A3BCb6WvtdwJpNNW'))
assetRespose = json.loads(r1.content)

for asset in assetRespose:
    assetId = asset['uuid']

    r2 = requests.get('https://api-prod.solarworksmalawi.lamt.app/shs-hub/asset/'+ assetId +'/token/?lastToken=true', auth=('solarworksmalawi', 'A3BCb6WvtdwJpNNW'))
   
    fullToken = json.loads(r2.content)

    for lastToken in fullToken:
        recharge = lastToken['token']
        print(recharge)