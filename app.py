from flask import Flask, request, jsonify, render_template
import openai
import requests
app = Flask(__name__)

class Chatbot:
    def __init__(self, model="gpt-3.5-turbo", temperature=0.7, max_tokens=150):
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.conversation_history = []
        openai.api_key = ""  # Set the API key

    def ask_question(self, prompt):
        prompt = f"world-wild-life-info: {prompt}"
        self.conversation_history.append({"role": "user", "content": prompt})
        
        try:
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=self.conversation_history,
                temperature=self.temperature,
                max_tokens=self.max_tokens
            )
            print("response: ", response)
            
            # Extracting the content from the response
            answer = response.choices[0].message['content'].strip()
            print("answer:", answer)
            
            self.conversation_history.append({"role": "assistant", "content": answer})
            return answer
        
        except Exception as e:
            print(f"Exception occurred: {e}")
            return "Sorry, something went wrong while processing your request."
        

    def reset_conversation(self):
        self.conversation_history = []

#chatbot = Chatbot(model="gpt-3.5-turbo", temperature=0.7, max_tokens=150)
url = "http://127.0.0.1:5000/v1/chat/completions"

@app.route('/')
def index():
    print("reading index.html")
    return render_template('index.html')

# @app.route('/chat', methods=['POST'])
# def chat():
#     data = request.json
#     print(data)
#     prompt = data.get("prompt", "")
#     print(prompt)
#     if not prompt:
#         return jsonify({"error": "No prompt provided"}), 400

#     response = chatbot.ask_question(prompt)
#     return jsonify({"response": response})

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    print(data)
    prompt = data.get("prompt", "")
    print(prompt)
    if not prompt:
        return jsonify({"error": "No prompt provided"}), 400
    payload = {
    "model": "gpt-4",
    "messages": [{"role": "user", "content": prompt}],
    "max_tokens": 100}
    print("payload")
    print(payload)
    
    # Send the POST request
    response = requests.post(url, json=payload)
    
    # Print the response
    if response.status_code == 200:
        json_response = response.json()
        message = json_response["choices"][0]["message"]["content"]
        #print(f"Prompt: {prompt}\nResponse: {message}\n")
        return jsonify({"response": message})
    else:
        message =f"Failed to get response for prompt: {prompt}, Status Code: {response.status_code}"
        return jsonify({"response": message})

@app.route('/reset', methods=['POST'])
def reset():
    #chatbot.reset_conversation()
    return jsonify({"message": "Conversation history reset"})


@app.route('/user', methods=['GET'])
def user():
    #chatbot.reset_conversation()
    return render_template('user.html')

# Mock responses based on user prompts
response_map = {
    "help": "How can I help you? We provide various resources and ways to get involved with wildlife conservation. What would you like to know?",
    "about us": "We are a global non-profit organization dedicated to wildlife conservation. Our mission is to protect endangered species and their habitats.",
    "donations": "You can make donations through our website, by mail, or by participating in one of our fundraising events. Every contribution helps us protect wildlife.",
    "vision": "Our vision is to ensure that the world’s most vulnerable wildlife species are thriving and protected for future generations.",
    "volunteer": "Join our volunteer program to get involved in hands-on conservation efforts. Visit our volunteer page to learn more and sign up.",
    "contact": "You can reach us via email at info@wildlife-ngo.org, or call our hotline at +1-800-WILDLIFE."
}

@app.route('/v1/chat/completions', methods=['POST'])
def mock_chatgpt():
    data = request.json
    user_message = data['messages'][0]['content'].lower()
    print(user_message)
    # Determine the appropriate response
    response_content = "I'm sorry, I didn't understand that. Could you please clarify?"
    for keyword, response in response_map.items():
        if keyword in user_message:
            response_content = response
            break
    print("response_content", response_content)
    # Update the mock response content
    mock_response = {
        "id": "mock-chatgpt-response",
        "object": "chat.completion",
        "created": 1629000000,
        "model": "gpt-4",
        "choices": [
            {
                "message": {
                    "role": "assistant",
                    "content": response_content
                },
                "finish_reason": "stop",
                "index": 0
            }
        ],
        "usage": {
            "prompt_tokens": len(user_message.split()),
            "completion_tokens": len(response_content.split()),
            "total_tokens": len(user_message.split()) + len(response_content.split())
        }
    }
    
    return jsonify(mock_response)




if __name__ == "__main__":
    app.run(host="0.0.0.0",port=5000)