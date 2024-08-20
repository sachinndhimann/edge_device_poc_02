from transformers import GPT2LMHeadModel, GPT2Tokenizer

# Load pre-trained model and tokenizer
model_name = "gpt2"  # Replace with the model that is fine-tuned on wildlife data
model = GPT2LMHeadModel.from_pretrained(model_name)
tokenizer = GPT2Tokenizer.from_pretrained(model_name)

#from flask import Flask, request, jsonify
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('input', '')
    inputs = tokenizer.encode(user_input, return_tensors='pt')

    outputs = model.generate(inputs, max_length=200, do_sample=True, temperature=0.7)
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    
    return jsonify({"response": response})

@app.route('/reset', methods=['POST'])
def reset():
    # Logic to reset any session or context, if needed
    return jsonify({"status": "reset done"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
