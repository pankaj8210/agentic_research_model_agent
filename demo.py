from agent import ResearchAgent

if __name__ == "__main__":
    query = "Environmental impact of cryptocurrency mining"
    agent = ResearchAgent(query)
    report = agent.run()
    print("\nFinal Report:\n", report)