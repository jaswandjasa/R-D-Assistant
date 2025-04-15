from crew.main_crew import AssistantCrew

def chat_loop():
    print("Welcome to the R&D Assistant! Type 'exit' to quit.")
    crew = AssistantCrew()
    
    while True:
        prompt = input("\nWhat do you want me to help you with? ")
        if prompt.lower() == "exit":
            print("Goodbye!")
            break
        
        try:
            result = crew.run(prompt)
            print("\nResult:\n", result)
        except Exception as e:
            print(f"\nError: {str(e)}")

if __name__ == "__main__":
    chat_loop()