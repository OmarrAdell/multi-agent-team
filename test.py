from agent import Agent

planner = Agent(
    "Planner",
    "You break a topic into 3 short research sub-questions. "
    "Return one per line, with no numbering.",
)

print(planner.run("The impact of AI on football analytics"))