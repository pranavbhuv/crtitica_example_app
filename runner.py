from dotenv import load_dotenv
import os
from critica_py_lib import Critica

def run_tests():
    """Run example tests using the Critica library"""
    load_dotenv()

    def handle_response(data):
        """Handle responses from the server"""
        print("\nReceived response from server:")
        print("Message:", data.get('message'))
        print("Status:", data.get('status'))
        # Process the response data as needed
        # You might want to send it to your GPT model here

    # Initialize client
    critica = Critica(
        server_url=os.getenv('SERVER_URL'),
        account_id=os.getenv('ACCOUNT_ID'),
        project_id=os.getenv('PROJECT_ID')
    )

    # Set up the response handler
    critica.set_response_handler(handle_response)

    try:
        # Test #1: Project Registration
        print("\nTest #1: Project Registration")
        response = critica.register_project("Project X")
        print("Project Registration Response:", response)

        # Test #2: Chat Approval
        print("\nTest #2: Chat Approval")
        is_approved = critica.is_approved()
        print("Chat Approved:", is_approved)

        # Test #3: Socket.IO Testing
        print("\nTest #3: Socket.IO Testing")
        critica.connect_socket()

        # Interactive message testing
        try:
            while True:
                message = input("\nEnter message (or 'quit' to exit): ")
                if message.lower() == 'quit':
                    break
                critica.send_message(message)

        except KeyboardInterrupt:
            print("\nExiting...")
        finally:
            critica.disconnect_socket()

    except Exception as e:
        print("Error:", str(e))

if __name__ == "__main__":
    run_tests()
