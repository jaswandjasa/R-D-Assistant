from crew.main_crew import AssistantCrew

if __name__ == "__main__":
    prompt = input("What do you want me to help you build today? ")
    crew = AssistantCrew()
    result = crew.run(prompt)
    print("\nResult:\n", result)
