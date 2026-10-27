from agent import Agent
from tools import web_search, calculate

researcher = Agent(
    "Researcher",
    "You answer a research question. Use web_search for facts and calculate "
    "for any math. Reply in 3-4 sentences and end with the source URLs you used.",
    tools=[web_search, calculate],
)

print(researcher.run(
    "How are machine learning algorithms used to predict football player market value?"
))