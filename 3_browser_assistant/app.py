import os

import openai
from dotenv import load_dotenv
from flask import Flask, render_template, request

app = Flask(__name__)
load_dotenv()  # Load environment variables from .env file

# Initialize OpenAI client
client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))


@app.route('/', methods=['GET', 'POST'])
def index():
    response = None
    if request.method == 'POST':
        user_input = request.form['prompt']
        # Using OpenAI's chat completion with roles
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system",
                 "content": "You are a funny assistant responding to your boss "
                            "Make a passive-aggressive joke when your boss talks to you"},
                {"role": "user", "content": user_input}
            ]
        )
        response = completion.choices[0].message.content
    return render_template('index.html', response=response)


if __name__ == '__main__':
    app.run(debug=True)
