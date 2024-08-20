from flask import Flask, request, jsonify

app = Flask(__name__)

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

if __name__ == '__main__':
    app.run(debug=True,port=5001)