import openai
import os
import re

# Define the OpenAI API Key
openai.api_key = os.getenv("OPENAI_API_KEY")

def parse_choices(response):
    """Parse the choices from the model's response"""
    choices = re.findall(r"\d[\.\)]\s*.+", response)
    return choices

def ask_question(messages):
    print("Thinking...")
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        max_tokens=2000
    )
    return response.choices[0].message['content'].strip()

def main():
    print("Welcome to the OpenAI interactive Python app!")

    user_input = ''
    last_choices = []

    while True:
        if not user_input:
            user_input = input("\nPlease type in your question or 'Q' to quit: ")

        # Exit the loop if the user types 'Q'
        if user_input.upper() == 'Q':
            break

        user_message = {"role": "system", "content": "Please answer and then give me three choices for my next prompt."}
        user_prompt = {"role": "user", "content": user_input}

        messages = [user_message, user_prompt]
        response = ask_question(messages)
        last_choices = parse_choices(response)

        print("\nOpenAI Response:\n", response)
        print("\nDEBUG: Last Choices:\n", last_choices)  # Debug print for the choices

        user_input = ''  # Clear user_input so it's ready for the next choice or question
        choice = input("\nType in '1', '2', or '3' for the respective choice, 'Q' to quit, or type in a new question: ")

        if choice.upper() == 'Q':
            break
        elif choice in ["1", "2", "3"]:
            # If the user's input is a number, we should get that choice from the previous response
            # Note: This assumes that the AI's response has three choices formatted in a certain way
            # In real world application, you'd want to handle this more robustly
            user_input = last_choices[int(choice) - 1]
        else:
            user_input = choice

    print("Thank you for using the OpenAI interactive Python app!")

if __name__ == "__main__":
    main()
