import json
import requests
from flask import Flask, request

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

    if len(option) == 1 and option[0] == '':
        response = "CON Takulandirani ku Solar Works Malawi \n Sankhani: \n"
        # response += "1. Make payment \n"
        response += "2. SW Menu"

    elif len(option) == 1 and option[0] == '2':
        response = "CON Sankhani: \n"
        response += "1. Tokeni \n"
        response += "2. Ndalama Zotsala \n"

    elif len(option) == 2 and option[0] == '2' and option[1] == '1':
        response = "CON Lowetsani reference number\n"

    elif len(option) == 3 and option[0] == '2' and option[1] == '1':
        conta = option[2]
        token = ""
        r = requests.get('https://payg.angazadesign.com/data/accounts_by_number/' +
                         conta, auth=())
        accounts_data = json.loads(r.text)
        account_cliente_qiq = accounts_data['qid']

        url_qid = 'https://payg.angazadesign.com/data/activations'
        PARAMS = {'account_qid': account_cliente_qiq}
        r = requests.get(url=url_qid, params=PARAMS, auth=())
        data = json.loads(r.text)

        arr_keycode = data['_embedded']['item']

        for keycode in arr_keycode:
            lasts_tokens = keycode['keycode']
            if lasts_tokens:
                token = lasts_tokens
            else:
                token = "No Tokin"

        response = "END Tokeni:\n"
        response += token

    elif len(option) == 2 and option[0] == '2' and option[1] == '2':
        response = "CON Lowetsani reference number\n"

    # account query condition
    elif len(option) == 3 and option[0] == '2' and option[1] == '2':
        conta = option[2]

        r = requests.get('https://payg.angazadesign.com/data/accounts_by_number/' +
                         conta, auth=())
        accounts_data = json.loads(r.text)
        # print(accounts_data)
        account_cliente_id = accounts_data['client_qids'][0]

        accounts_request_cliente = requests.get('https://payg.angazadesign.com/data/clients/' +
                                                account_cliente_id, auth=())
        cliente_data = json.loads(accounts_request_cliente.text)

        cliente_name = cliente_data['name']
        day_last_downpay = accounts_data['down_payment_days_included']
        accounts_status = accounts_data['status']
        days_disable = accounts_data['cumulative_days_disabled']
        total_pay_amount = accounts_data['total_paid']

        response = "END Zotsatila za akaunti yanu:\n"
        response += "1.	Name: " + str(cliente_name) + "\n"
        response += "2.	Instalations Day Remaining: " + str(day_last_downpay) + "\n"
        response += "3.	Account Status: " + str(accounts_status) + "\n"
        response += "4.	Disable Days: " + str(days_disable) + "\n"
        response += "5.	Total Payment: " + str(total_pay_amount) + "\n"

    return response


if __name__ == "__main__":
    app.run()
