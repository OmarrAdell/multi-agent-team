from llm import ask, ask_with_tools
from tracing import log

class Agent:
    def __init__(self, name, role, tools=None):
        self.name = name
        self.role = role
        self.tools = tools

    def run(self, task):
        print(f"[{self.name}] working...")
        log(self.name, "task", task)
        if self.tools:
            result = ask_with_tools(task, self.role, self.tools, name=self.name)
        else:
            result = ask(task, system=self.role)
        log(self.name, "output", result)
        return result