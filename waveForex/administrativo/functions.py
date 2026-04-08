import base64
import requests


PAYPAL_CLIENT_ID = 'AbX-9XpQlJB5TNcCysD7vrWBMufbzgLPxqQNE2TKQGlgYjHKmuLilBWu56-HjYmTzUSqro3tuYFi0lhv'
PAYPAL_CLIENT_SECRET = 'EFtu1EFML5_Ta6B7CbiIINWK_xLFjEAuvLDRL1HmpajLJD8cs5LtN6IFJYmvniCDOR0FjhV55etyDuh5'
BASE_URL = "https://api-m.sandbox.paypal.com"

def generateAccessToken():
    try:
        auth = f"{PAYPAL_CLIENT_ID}:{PAYPAL_CLIENT_SECRET}"
        auth = base64.b64encode(auth.encode()).decode('utf-8')

        response = requests.post(
            "https://api-m.sandbox.paypal.com/v1/oauth2/token",
            data={"grant_type": "client_credentials"},
            headers={"Authorization": f"Basic {auth}"}
        )

        response.raise_for_status()
        data = response.json()
        return data['access_token']
    except requests.exceptions.RequestException as e:
        print(f"Error generating access token: {e}")
        return None



def create_order(producto):
    print(producto)
    
    try:
        access_token = generateAccessToken()
        if not access_token:
            raise Exception("Access token could not be generated.")
        
        url = "https://api-m.sandbox.paypal.com/v2/checkout/orders"
        payload = {
            "intent": "CAPTURE",
            "purchase_units": [
                {
                    "amount": {
                        "currency_code": "USD",
                        "value": str(producto.precio)  # Asegúrate de usar el precio del producto
                    }
                }
            ]
        }
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {access_token}"
        }
        
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()  # Will raise an HTTPError if the HTTP request returned an unsuccessful status code
        return response.json()
    except requests.exceptions.RequestException as e:
        print('RequestException:', e)
        return {'error': str(e)}
    except Exception as e:
        print('Exception:', e)
        return {'error': str(e)}







def capture_order(orderID):
    access_token = generateAccessToken()
    url = f"https://api-m.sandbox.paypal.com/v2/checkout/orders/{orderID}/capture"
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}"
    }
    
    response = requests.post(url, headers=headers)
    
    return response.json()