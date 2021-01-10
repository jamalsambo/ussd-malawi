from flask import Flask, request
import requests
import json
import requests

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

    elif (len(option) == 1 and option[0] == '1'):
        # number = {'numero': option[0]}
        # r =requests.post('http://localhost:3000/api/account/router-text/', data=number)
        # resposta = json.loads(r.text)
        response = "CON Por favor, insira o numero de telefone da sua conta Solar-Works:\n "

    elif (len(option) == 2 and option[0] == '1'):
        response = "CON Por favor insira um numero de conta Solar-Works"

    elif (len(option) == 3 and option[0] == '1'):
        response = "CON Por favor insira o valor da compra"

    elif (len(option) == 4 and option[0] == '1'):
        phone = option[1]
        conta = option[2]
        valor = option[3]

        response = "CON Tens a certeza que queres pagar a energia no valor de " + \
            valor+" para a conta "+conta+" atravez do numero "+phone+" \n"
        response += "1. Confirmar \n"
        response += "2. Cancelar"

    elif (len(option) == 5 and option[0] == '1'):
        codigo = "5685-5584-5695-5898-5584"
        response = "END Pagamento efectuado com sucesso, o seu codigo de recarga e: " + codigo

    elif (len(option) == 1 and option[0] == '2'):
        response = "CON Select Operation \n"
        response += "1. Reload codes \n"
        response += "2. Balance \n"

    elif (len(option) == 2 and option[0] == '2' and option[1] == '1'):
        response = "END Latest refills \n"
        response += "1234-4569-7895-5698-7895 \n"
        response += "1234-4569-7895-5698-7895 \n"
        response += "1234-4569-7895-5698-7895 \n"

    elif (len(option) == 2 and option[0] == '2' and option[1] == '2'):
        response = "CON Enter the account number\n"

    elif (len(option) == 3 and option[0] == '2' and option[1] == '2'):
        conta = option[2]
        r = requests.get('https://api-prod.solarworksmalawi.lamt.app/lamt/account/?search=paymentReference==' +
                         conta, auth=('', ''))

        accounts = json.loads(r.text)
        for accountStatus in accounts:
           
            response = "END Your account balance and the following\n"
            response += "Last Payment At: " + str(accountStatus['accountStatus']['lastPaymentAt']) + "\n"
            response += "Expected Amount Paid: " + str(accountStatus['accountStatus']['expectedAmountPaid']) + "\n"
            response += "Total Payment Received: " + str(accountStatus['accountStatus']['totalPaymentReceived']) + "\n"
            response += "Total Value Received: " + str(accountStatus['accountStatus']['totalValueReceived']) + "\n"
            response += "Account Balance: " + str(accountStatus['accountStatus']['accountBalance']) + "\n"
            response += "Last Payment At: " + str(accountStatus['accountStatus']['lastPaymentAmount']) + "\n" 
            response += "Account Balance Days: " + str(accountStatus['accountStatus']['accountBalanceDays']) + "\n"
    
    return response

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)
