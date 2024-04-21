import os
import random

from dotenv import load_dotenv
from openai import OpenAI


def get_hint(client, guess, number):
    # Determine the hint based on how close the guess is to the number
    if guess < number:
        hint = "too low"
    elif guess > number:
        hint = "too high"
    else:
        return "Congratulations! You've guessed the number!"

    prompt = f"The guess {guess} is {hint}. Provide an encouraging hint to help guess closer to the number."
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system",
             "content": "You are an funny assistant providing hints for a number guessing game. "
                        "make a passive aggresive joke when the guess is wrong, and then give the hint"},
            {"role": "user", "content": prompt}
        ]
    )
    return completion.choices[0].message.content


def main():
    load_dotenv()
    client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

    number = random.randint(1, 100)  # Random number between 1 and 100
    attempts = 0

    print("Welcome to the Guess the Number Game!")
    print("I'm thinking of a number between 1 and 100.")

    while True:
        try:
            guess = int(input("Make a guess: "))
            attempts += 1
            hint = get_hint(client, guess, number)
            print(hint)
            if guess == number:
                print(f"You guessed the number in {attempts} attempts!")
                break
        except ValueError:
            print("Please enter a valid integer.")


if __name__ == "__main__":
    main()
