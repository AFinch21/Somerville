import requests

def get_questions():
    
    url = "http://localhost:80/get_question_list"
    
    # Make the POST request
    response = requests.get(url)

    # Check the response
    
    
    if response.status_code == 200:
        return response.json()
    else:
        print("Request failed with status code:", response.status_code)
        


def get_response(question):
    
    url = "http://localhost:80/answer_question"
    
    data = {
        "message": question,
        "max_retries": 3,
        "status": "string"
    }

    # Make the POST request
    response = requests.post(url, json=data)

    # Check the response
    if response.status_code == 200:
        return response.json()
    else:
        print("Request failed with status code:", response.status_code)