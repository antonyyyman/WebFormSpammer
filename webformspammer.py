import requests
import random
import time
from bs4 import BeautifulSoup

def get_csrf_token(session, url):
    response = session.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        token = soup.find('input', {'name': '_csrfToken'})
        if token:
            return token.get('value')
        else:
            print("CSRF token not found.")
    else:
        print(f"Failed to load page: {response.status_code}")
    return None

def generate_random_string(length):
    letters = 'abcdefghijklmnopqrstuvwxyz'
    return ''.join(random.choice(letters) for i in range(length))

def send_form_submission(session, url, form_data):
    response = session.post(url, data=form_data)
    return response.status_code, response.text

def main():
    url = "https://review.u24s1004.iedev.org/contact-us" #URL of page containing any form
    action_url = url #in our case action is just same as URL but needs to adjust based on what the submit action actually is
    session = requests.Session()
    query_nature_options = ['General Enquiry', 'Room Hire', 'Enrolment Info'] #Whitebox test, otherwise will normally have to guess this if such options exist

    while True:
        csrf_token = get_csrf_token(session, url)
        if not csrf_token:
            print("Skipping form submission due to missing CSRF token.")
            time.sleep(1)
            continue
        
        form_data = {
            'email': generate_random_string(10) + '@example.com',
            'name': generate_random_string(10),
            'lname': generate_random_string(10),
            'enquiry_type': random.choice(query_nature_options),  
            'message': generate_random_string(50),
            'appointment_req_time': '2024-12-12',
            '_csrfToken': csrf_token
        }
        
        print(f"Submitting form with data: {form_data}")  # Debug, track data, not sending properly.
        
        try:
            status_code, response_text = send_form_submission(session, action_url, form_data)
            print(f"Form submitted with status code: {status_code}")
            if status_code != 200:
                print(f"Response text: {response_text}")
            else:
                if "There are errors in your form" in response_text:
                    print("Form submission failed due to validation errors.")
                else:
                    print("Form submission successful.")
        except Exception as e:
            print(f"An error occurred: {e}")
        
        time.sleep(1)

if __name__ == "__main__":
    main()
