from openai import OpenAI
from dotenv import load_dotenv
import os


# Function to generate a personalized greeting using OpenAI's API
def generate_greeting(client, name, interests):
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system",
             "content": "You are a friendly assistant, skilled in creating personalized greetings."},
            {"role": "user", "content": f"Create a greeting for someone named {name} who likes {interests}."}
        ]
    )
    message = completion.choices[0].message
    return message.content


# Main function to interact with the user
def main():
    load_dotenv()
    client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

    print("Hello! I'm here to create a personalized greeting for you.")
    name = input("What's your name? ")
    interests = input("What are some of your interests? (e.g., reading, gaming, hiking) ")

    # Generate the greeting
    greeting = generate_greeting(client, name, interests)
    print(f"\n{greeting}")


if __name__ == "__main__":
    main()
