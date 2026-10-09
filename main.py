import os
import argparse
from dotenv import load_dotenv
from openai import OpenAI

from module.system_prompt import system_prompt
from functions.call_functions import available_functions
from functions.call_functions import call_function


#block that defines the main function for the ai agent
def main():
    load_dotenv()

    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        raise ValueError("OPENROUTER_API_KEY is not set in the environment variables.")

    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )

    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User Prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": args.user_prompt},
    ]

    for _ in range(20):
        response = client.chat.completions.create(
            model="openrouter/free",
            messages=messages,
            tools=available_functions,
        )

        prompt_usage = response.usage.prompt_tokens
        completion_usage = response.usage.completion_tokens

        if args.verbose:
            print(f"User prompt: {args.user_prompt}")
            print(f"Response tokens: {completion_usage}")
            print(f"Prompt tokens: {prompt_usage}")

        message = response.choices[0].message

        # Add the assistant's response to the conversation history.
        messages.append(message)

        # If there are no tool calls, the model is finished.
        if not message.tool_calls:
            print("Final response:")
            print(message.content)
            return

        # Execute every tool call requested by the model.
        for tool_call in message.tool_calls:
            result_message = call_function(tool_call, args.verbose)

            if not result_message["content"]:
                raise Exception("Function call returned empty content")

            if args.verbose:
                print(f"-> {result_message['content']}")

            # Add the tool's result to the conversation history.
            messages.append(result_message)

    print("Maximum iterations reached without a final response.")


if __name__ == "__main__":
    main()