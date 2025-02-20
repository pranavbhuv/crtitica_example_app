import requests
import json
from socketio import Client
import urllib3
from urllib.parse import urlencode
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Configuration from environment variables
SERVER_URL = os.getenv('SERVER_URL')
ACCOUNT_ID = os.getenv('ACCOUNT_ID')
PROJECT_ID = os.getenv('PROJECT_ID')

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

try:
    # Test #1: Project Registration
    print("Starting Test #1: Project Registration...")
    url = f"{SERVER_URL}/accounts/{ACCOUNT_ID}/projects"
    response = requests.get(url, verify=False)
    print("Projects Response:", response.json())

    # Add a new project if it doesn't exist
    project_data = {"project_name": "Project X"}
    response = requests.post(url, json=project_data, verify=False)
    print("Project Registration Response:", response.json())
    print("Test #1 completed.\n")

    # Critica cr = new Critica(API_KEY, "Project A")

    # # Test #2: Chat Approval
    print("Starting Test #2: Chat Approval...")
    url = f"{SERVER_URL}/chat_is_approved/{ACCOUNT_ID}/{PROJECT_ID}"
    response = requests.get(url, verify=False)
    print("Chat Approval Response:", response.json())
    print("Test #2 completed.\n")

    # cr.is_approved(); -> true or false

    # # Test #3: Socket.IO Testing
    print("Starting Test #3: Socket.IO test...")
    sio = Client()

    @sio.on('connect')
    def on_connect():
        print('Socket.IO Connected!')

    @sio.on('disconnect')
    def on_disconnect():
        print('Socket.IO Disconnected!')

    @sio.on('response')
    def on_response(data):
        print('Received response:', data)

    @sio.on('connect_error')
    def on_connect_error(data):
        print('Connection Error:', data)

    try:
        # Connect to the Socket.IO server with query parameters in the URL
        base_url = SERVER_URL
        account_id = ACCOUNT_ID
        project_id = PROJECT_ID

        # URL encode the parameters properly
        query_params = urlencode({'account_id': account_id, 'project_id': project_id})
        url = f'{base_url}?{query_params}'

        sio.connect(url,
                   wait_timeout=10,
                   transports=['websocket'])

        try:
            while True:
                message = input("Enter message (or 'quit' to exit): ")
                if message.lower() == 'quit':
                    break

                test_message = {
                    'account_id': ACCOUNT_ID,
                    'project_id': PROJECT_ID,
                    'message': message
                }
                sio.emit('message', test_message)

        except KeyboardInterrupt:
            print("\nExiting...")
        finally:
            sio.disconnect()
            print("Socket.IO test completed.\n")

    except Exception as e:
        print("Socket.IO Connection Error:", str(e))

    # output is not a string, it's a dict
    # def test(input):
    #     output = cr.pipe(input)
    #     test(gpt_response(output))


    # text_field(keyboard_controller) ->
    # text_field(cr.pipe(gpt_response_maker()))


except Exception as e:
    print("Error occurred:", str(e))
