import time

_start = time.time()
events = []

def reset():
    global _start
    _start = time.time()
    events.clear()

def log(agent, kind, detail):
    events.append({
        "at": round(time.time() - _start, 1),
        "agent": agent,
        "kind": kind,
        "detail": str(detail)[:300],
    })