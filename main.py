from openai import OpenAI

client = OpenAI()

def chef(chef_type):
    chef_types = {
        "1": "You are a Chinese innovative and skilled chef specializing in vegan cuisine. You help people by suggesting dishes based on available ingredients, providing detailed recipes, and offering constructive criticism on user-submitted recipes. You are an art lover, a wine enthusiast, and have a deep connection to nature. You possess a real sense for creating innovative food.",
        "2": "You are an Italian sushi master specializing in sweet cuisine. You help people by suggesting dishes based on available ingredients, providing detailed recipes, and offering constructive criticism on user-submitted recipes. You have a playful personality, love making jokes, and enjoy creating tricky, fun foods.",
    }
    return {"role": "system", "content": chef_types.get(chef_type, "")}

def check_input(choice, content):
    options = {
        "1": f"Suggest some dishes based on these ingredients: {content}. Do not include the recipe at this stage. You don't suggest any drinks",
        "2": f"Suggest a detailed recipe and preparation steps for making {content}.You don't suggest any drinks",
        "3": f"Critique this recipe and suggest changes: {content}.",
        "suggesting dishes based on ingredients": f"Suggest some dishes based on these ingredients: {content}. Do not include the recipe at this stage. You don't suggest any drinks",
        "giving recipes to dishes": f"Suggest a detailed recipe and preparation steps for making {content}.",
        "Critiquing the recipes": f"Critique this recipe and suggest changes: {content}.",
        "change chef": "Change chef"
    }
    return {"role": "user", "content": options.get(choice, "Invalid choice. Please select an option by entering '1' for suggesting dishes based on ingredients, '2' for giving recipes to dishes, '3' for Critiquing the recipes given by the user, or '4' to change the chef. You can also use the phrases 'suggesting dishes based on ingredients', 'giving recipes to dishes', or 'Critiquing the recipes' to select the respective options.")}

def ai_response(model, messages):
    stream = client.chat.completions.create(
        model=model,
        messages=messages,
        stream=True,
    )
    
    collected_messages = []
    for chunk in stream:
        chunk_message = chunk.choices[0].delta.content or ""
        print(chunk_message, end="")
        collected_messages.append(chunk_message)
    
    return "".join(collected_messages)

def select_chef():
    while True:
        chef_type = input("Select a chef type (1: Chinese innovative chef, 2: Italian sushi master, 0: Exit):\n").strip()
        
        if chef_type in ["0"]:
            print("Exiting...")
            exit()
        elif chef_type in ["1", "2"]:
            return chef_type
        else:
            print("Invalid choice. Please start with '1' for Chinese innovative chef, or '2' for Italian sushi master.")

def user_interaction():
    while True:
        user_input = input("Select an option (1: Suggesting dishes based on ingredients, 2: Giving recipes to dishes, 3: Critiquing the recipes given by the user, 4: Change chef, 0: Exit):\n").strip().lower()
        
        if user_input in ["0", "exit"]:
            print("Exiting...")
            exit()
        
        if user_input in ["4", "change chef"]:
            return "change chef", ""
        
        if user_input in ["1", "suggesting dishes based on ingredients"]:
            content = input("What are the ingredients?\n")
        elif user_input in ["2", "giving recipes to dishes"]:
            content = input("What is the name of the recipe?\n")
        elif user_input in ["3", "Critiquing the recipes"]:
            print("What is the recipe that you want critiqued? Press Enter twice to submit.")
            content_lines = []
            while True:
                line = input()
                if line:
                    content_lines.append(line)
                else:
                    break
            content = "\n".join(content_lines)
        else:
            print("Invalid choice. Please select an option by entering '1' for suggesting dishes based on ingredients, '2' for giving recipes to dishes, '3' for Critiquing the recipes given by the user, or '4' to change the chef. You can also use the phrases 'suggesting dishes based on ingredients', 'giving recipes to dishes', or 'Critiquing the recipes' to select the respective options.")
            continue
        
        return user_input, content

def main():
    messages = []
    print("Welcome to Chef GPT\n")
    while True:
        chef_type = select_chef()
        messages.append(chef(chef_type))
        
        while True:
            user_input, content = user_interaction()
            
            if user_input == "change chef":
                break
            
            user_message = check_input(user_input, content)
            
            if user_message["content"] == "Change chef":
                break
            
            messages.append(user_message)
            
            collected_message = ai_response("gpt-3.5-turbo", messages)
            print("\n")
            messages.append({"role": "assistant", "content": collected_message})

if __name__ == "__main__":
    main()
