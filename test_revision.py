import team
import tracing

team.critic.role = (
    "You are a very strict editor. On your first review of any report, reply "
    "with 2 specific fixes. Reply with exactly APPROVED only after the report "
    "has been revised at least once."
)

team.run_team("The impact of AI on football analytics")
for e in tracing.events:
    print(f'{e["at"]:>6}s  {e["agent"]:<11}{e["kind"]:<10}{e["detail"][:70]!r}')