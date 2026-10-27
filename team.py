import tracing
from agent import Agent
from tools import web_search, calculate
from concurrent.futures import ThreadPoolExecutor

planner = Agent(
    "Planner",
    "You break a topic into 3 short research sub-questions. "
    "Return one per line, with no numbering.",
)

researcher = Agent(
    "Researcher",
    "You answer a research question. Use web_search once, and search again "
    "only if the first results clearly lack the answer. Use calculate for any "
    "math. Reply in 3-4 sentences and end with the source URLs you used.",
    tools=[web_search, calculate],
)

writer = Agent(
    "Writer",
    "You write a clear, well-structured report of under 300 words from research "
    "notes. Use short headings, only state what the notes support, and list "
    "the sources at the end.",
)

critic = Agent(
    "Critic",
    "You review a report against the research notes. If it is accurate, clear "
    "and well organized, reply with exactly the word APPROVED. Otherwise reply "
    "with 2-3 specific fixes.",
)

def research(question):
    return f"Q: {question}\nA: {researcher.run(question)}"

def run_team(topic, max_revisions=2):
    tracing.reset()
    print(f"\n=== Topic: {topic} ===")

    plan = planner.run(topic)
    questions = [q.strip() for q in plan.splitlines() if q.strip()]

    with ThreadPoolExecutor(max_workers=3) as pool:
        notes = list(pool.map(research, questions))
    notes_text = "\n\n".join(notes)

    report = writer.run(f"Topic: {topic}\n\nResearch notes:\n{notes_text}")

    for i in range(max_revisions + 1):
        review = critic.run(f"Notes:\n{notes_text}\n\nReport:\n{report}")
        if review.strip().upper().startswith("APPROVED"):
            tracing.log("Critic", "verdict", "approved")
            break
        if i == max_revisions:
            tracing.log("Critic", "verdict", "revision limit reached")
            break
        tracing.log("Critic", "verdict", f"changes requested (round {i + 1})")
        report = writer.run(
            f"Topic: {topic}\n\nResearch notes:\n{notes_text}\n\n"
            f"Previous report:\n{report}\n\nCritic feedback:\n{review}\n\n"
            "Rewrite the report and apply the feedback. Include every source "
            "URL from the notes in the Sources section."
        )

    return report

if __name__ == "__main__":
    topic = input("Topic: ")
    print("\n" + run_team(topic))
    print("\n--- Trace ---")
    for e in tracing.events:
        print(f'{e["at"]:>6}s  {e["agent"]:<11}{e["kind"]:<10}{e["detail"][:70]!r}')