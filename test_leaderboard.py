import requests
import json

MY_URL = "https://flappy-scores-ec9d5-default-rtdb.firebaseio.com/scores.json"

def test_the_cloud():
    print("Trying to talk to the cloud...")
    
    my_data = {"name": "Rohit_Noob", "score": 999}
    
    response = requests.post(MY_URL, json=my_data)
    
    if response.status_code == 200:
        print("✅ SUCCESS! Go check your browser, you should see your name!")
    else:
        print("❌ ERROR! Something went wrong. Check your link.")

test_the_cloud()