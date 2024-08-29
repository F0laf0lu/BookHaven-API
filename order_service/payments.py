import requests


class PayStack:

    BASE_URL = 'https://api.paystack.co/transaction'
    PAYSTACK_SK = 'sk_test_1b60305d6d910d71d16db6442a436034c671f9be'

    def initiate_payment(self, email, amount, **kwargs):
        path = '/initialize'
        headers = {"Authorization": f"Bearer {self.PAYSTACK_SK}", "Content-Type": "application/json"}

        url = self.BASE_URL + path
        body = {
            'email': email,
            'amount': amount,
        }
        response = requests.post(url, headers=headers, json=body)

        if response.status_code == 200:
            response_data = response.json()
            return response_data
        response_data = response.json()
    
        return response_data['status'], response_data['message']

    def verify_payment(self, reference):
        path  = f'/verify/{reference}'
        headers = {"Authorization": f"Bearer {self.PAYSTACK_SK}", "Content-Type": "application/json"}

        url = self.BASE_URL + path
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            response_data = response.json()
            return response_data['status'], response_data['data']

        response_data = response.json()

        return response_data['status'], response_data['message']



# new = PayStack()

# print(new.initiate_payment('admin@app.com', 50000))

# print(new.verify_payment('qhdqs9xv39'))