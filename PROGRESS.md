# FollowThrough: Progress

Submit by **Thu 23 Oct 2026, 8 PM IST** (hard deadline 24 Oct, 12:30 AM IST).
Last updated: Mon 19 Oct 2026

## Day 0: Setup
- [x] Join the hackathon on Devpost
- [x] Create an AWS account
- [x] Create the GitHub repo with an MIT license
- [x] Install the AWS CLI (2.38.1)
- [ ] Ask the organisers for Alexa AI CLI access (gated, see friction log FL-003). **Biggest risk**
- [ ] Create an Amazon Developer account
- [ ] Create an IAM access key and run `aws configure` (region `us-east-1`)
- [ ] Make the repo public; delete the old `amazonhackathon2026` repo

## Day 1, Mon: Server end to end
- [x] MCP server with Streamable HTTP at `/mcp` ([server.py](server.py))
- [x] Tools: `create_task`, `whats_pending`, `mark_done`, `snooze`, `get_task_history`
- [x] End-to-end test, each tool ~5 ms against the 500 ms limit ([test_server.py](test_server.py))
- [x] Friction log started ([friction-log.md](friction-log.md))
- [ ] Deploy to Lambda with a public HTTPS URL; measure latency, including the slow first call after idle
- [ ] Register with Alexa+ (`alexa-ai new mcp` → `alexa-ai deploy`), once CLI access arrives

## Day 2, Tue: Core feature
- [ ] DynamoDB storage, replacing in-memory storage
- [ ] Reminder loop: EventBridge Scheduler → Lambda → phone push
- [ ] Bedrock turns natural-language deadlines into dates

## Day 3, Wed: Product
- [ ] Agent Skill (`skills/followthrough/SKILL.md`)
- [ ] Simulated Alexa+ web app (start early if CLI access is still pending Tue evening)
- [ ] Escalation to an accountability buddy
- [ ] Polish spoken replies; Hinglish example

## Day 4, Thu: Submit by 8 PM
- [ ] Demo video under 3 min (public, English, no copyrighted music)
- [ ] Final README with an architecture diagram
- [ ] Devpost form: description, video, Alexa+ track, AWS Builder and Open Source mini challenges
- [ ] Product feedback on every tool and AWS service used
- [ ] Friction log reviewed with the pre-submission checklist
