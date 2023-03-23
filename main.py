import openai
import prompt_toolkit

# Set up the OpenAI API client
openai.api_key = "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"

# Define the conversation function
def converse(prompt):
    # Set up the OpenAI API parameters
    params = {
        "model": "davinci",
        "temperature": 0.5,
        "max_tokens": 1024,
        "top_p": 1,
        "frequency_penalty": 0,
        "presence_penalty": 0,
    }

    # Call the OpenAI API to generate a response
    response = openai.Completion.create(
        prompt=prompt, **params
    )

    # Return the generated response
    return response.choices[0].text.strip()

# Set up the chat loop
while True:
    try:
        # Get user input
        user_input = prompt_toolkit.prompt("> ")

        # Generate a response using the OpenAI API
        response = converse(user_input)

        # Print the response
        print(response)
    except KeyboardInterrupt:
        # Handle Ctrl-C gracefully
        print("Exiting...")
        break
