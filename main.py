import os
import dotenv
import openai
import json
from datetime import datetime

dotenv.load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")


class Colors:
    BLUE = "\033[94m"
    CYAN = "\033[96m"
    RED = "\033[91m"
    RESET = "\033[0m"


def read_file(path):
    try:
        with open(path) as file:
            return file.read()
    except:
        return ""


def get_system_message(topic):
    topic_files = ["prompt.txt", "data.json"]
    system_message = ""
    for file_name in topic_files:
        file_path = os.path.join("topics", topic, file_name)
        system_message += read_file(file_path)
    return system_message


def get_topic():
    print(f"\n{Colors.RED}[System]{Colors.RESET} Select topic for the conversation:")

    directories = os.listdir("topics")
    for i, dir in enumerate(directories):
        print(f"\t{i+1}. {dir}")
    user_input = input(f"\n{Colors.BLUE}[You]{Colors.RESET} ")

    try:
        number_input = int(user_input)
        if number_input not in range(1, len(directories) + 1):
            print(
                f"\n{Colors.RED}[System]{Colors.RESET} Error: {user_input} is outside the range."
            )
            return get_topic()
    except ValueError:
        print(
            f"\n{Colors.RED}[System]{Colors.RESET} Error: {user_input} is not a valid number."
        )
        return get_topic()

    return directories[number_input - 1]


def chat(prompt, messages=[], role="user", model="gpt-4o"):
    try:
        response = openai.chat.completions.create(
            model=model,
            messages=messages + [{"role": role, "content": prompt}],
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"\n{Colors.RED}[System]{Colors.RESET} An error occurred: {e}")
        return "Sorry, something went wrong with the chat service."


def write_log(messages, topic):
    current_time = datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
    file_name = f"{topic}_{current_time}.json"

    with open(os.path.join("logs", file_name), "a+") as file:
        file.write(json.dumps(messages))


def main():
    topic = get_topic()
    messages = [{"role": "system", "content": get_system_message(topic)}]
    exit_commands = ["quit", "exit", "bye", "leave"]

    print(f"\n{Colors.RED}[System]{Colors.RESET} Chat ready.")

    running = True
    while running:
        user_input = input(f"\n{Colors.BLUE}[You]{Colors.RESET} ")

        if user_input.lower().strip() in exit_commands:
            print(f"\n{Colors.CYAN}[ChatGPT]{Colors.RESET} Bye!")
            running = False

        else:
            response = chat(user_input, messages)
            messages.append({"role": "user", "content": user_input})
            messages.append({"role": "assistant", "content": response})
            print(f"\n{Colors.CYAN}[ChatGPT]{Colors.RESET} " + response)

    write_log(messages, topic)


if __name__ == "__main__":
    main()
