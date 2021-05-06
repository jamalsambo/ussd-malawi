from flask import Flask, request
import json, datetime, requests

app = Flask(__name__)

response = ""


@app.route('/', methods=['POST', 'GET'])
def ussd_callback():
    global response
    session_id = request.values.get("sessionId", None)
    service_code = request.values.get("serviceCode", None)
    phone_number = request.values.get("phoneNumber", None)
    text = request.values.get("text", "default")

    option = text.split("*")

    if(len(option) == 1 and option[0] == ''):
        response = "CON WELCOME TO THE SOLAR WORKS MENU - MALAWI \n Choose an option \n"
        # response += "1. Make payment \n"
        response += "2. SW service menu"

    elif (len(option) == 5 and option[0] == '1'):
        codigo = "5685-5584-5695-5898-5584"
        response = "END Pagamento efectuado com sucesso, o seu codigo de recarga e: " + codigo

    elif (len(option) == 1 and option[0] == '2'):
        response = "CON Select Operation \n"
        response += "1. Reload codes \n"
        response += "2. Balance \n"

    elif (len(option) == 2 and option[0] == '2' and option[1] == '1'):
        response = "CON Enter the account number\n"
    
    elif (len(option) == 3 and option[0] == '2' and option[1] == '1'):
        recharge = ""
        days = ""
        accountId = option[2]
        r1 = requests.get('https://api-prod.solarworksmalawi.lamt.app/lamt/account/'+ accountId +'/asset', auth=('solarworksmalawi', 'A3BCb6WvtdwJpNNW'))
        assetRespose = json.loads(r1.content)

        for asset in assetRespose:
            assetId = asset['uuid']

            r2 = requests.get('https://api-prod.solarworksmalawi.lamt.app/shs-hub/asset/'+ assetId +'/token/?lastToken=true', auth=('solarworksmalawi', 'A3BCb6WvtdwJpNNW'))
        
            fullToken = json.loads(r2.content)

            for lastToken in fullToken:
                recharge = lastToken['token']
                days = lastToken['duration']

        response = "END Latest refills \n"
        response += "recharge: " + str(recharge) + "\n"
        response += "Days: " + str(days)

    elif (len(option) == 2 and option[0] == '2' and option[1] == '2'):
        response = "CON Enter the account number\n"

    elif (len(option) == 3 and option[0] == '2' and option[1] == '2'):
        conta = option[2]
        r = requests.get('https://api-prod.solarworksmalawi.lamt.app/lamt/account/?search=paymentReference==' +
                         conta, auth=('solarworksmalawi', 'A3BCb6WvtdwJpNNW'))

        accounts = json.loads(r.text)
        for accountStatus in accounts:

            dataPayment = accountStatus['accountStatus']['lastPaymentAt']
            date_time_obj = datetime.datetime.strptime(dataPayment, '%Y-%m-%dT%H:%M:%S.000+0000')

            num_format = "{:,}".format
           
            response = "END Your account balance and the following\n"
            response += "Last Payment At: " + str(date_time_obj) + "\n"
            response += "Expected Amount Paid: " + str(num_format(accountStatus['accountStatus']['expectedAmountPaid'])) + "\n"
            response += "Total Payment Received: " + str(num_format(accountStatus['accountStatus']['totalPaymentReceived'])) + "\n"
            response += "Total Value Received: " + str(num_format(accountStatus['accountStatus']['totalValueReceived'])) + "\n"
            response += "Account Balance: " + str(num_format(accountStatus['accountStatus']['accountBalance'])) + "\n"
            response += "Last Payment At: " + str(num_format(accountStatus['accountStatus']['lastPaymentAmount'])) + "\n" 
            response += "Account Balance Days: " + str(accountStatus['accountStatus']['accountBalanceDays']) + "\n"
    
    return response

if __name__ == "__main__":
    app.run()
