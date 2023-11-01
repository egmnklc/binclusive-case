from flask import Flask, request, render_template
import openai

openai.api_key = 'API-KEY'

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/check_code', methods=['POST'])
def check_code():
    code = request.form['code']

    print("Sending query to OpenAI...")
    # Query OpenAI API for review
    response = openai.Completion.create(
      engine="text-davinci-002",
      prompt=f"Review the following code for accessibility issues. Provide problem header, problem description, and solution approaches according to the code. Format your answer like problem:..., description:..., solution:....\n\n{code}\n",
      max_tokens=500
    )
    
    print("Response received:\n Plain response is:", response)
    feedback_text = response.choices[0].text
    
    # Split feedback into separate lines and filter out empty lines
    lines = [line for line in feedback_text.split("\r\n") if line]
    print("lines:", lines)

    # Process the feedback
    feedbacks = [{'problem': lines[i], 'description': lines[i+1], 'solution': lines[i+2]} for i in range(0, len(lines), 3)]

    print("Feedback is: ", feedbacks)
    return render_template('results.html', feedbacks=feedbacks)

if __name__ == '__main__':
    app.run()
