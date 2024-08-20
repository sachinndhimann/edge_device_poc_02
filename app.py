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
url = "http://127.0.0.1:5001/v1/chat/completions"

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

if __name__ == "__main__":
    app.run(port=5000)