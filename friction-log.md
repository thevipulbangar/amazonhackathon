# Friction Log: FollowThrough

**Project:** FollowThrough: Adaptive Reminders That Don't Stop Until It's Done
**Track:** Alexa+ (Build, Ship, Shape: Amazon Developer Hackathon)
**Purpose:** A record of every bug, blocker, setup problem, unexpected behavior and documentation gap we hit while building an Alexa+ MCP server for students with deadlines.

> **Evidence rule:** Only entries in [Verified Incidents](#3-verified-incidents) are real. Entries in [Illustrative Examples](#4-illustrative-examples--verify-before-using) are made-up placeholders that show what a good entry looks like. Never submit an illustrative example as feedback unless someone on the team has reproduced it and replaced its Actual Result with what they observed.

---

## Table of Contents

1. [Summary Dashboard](#1-summary-dashboard)
2. [Logging Procedure](#2-logging-procedure)
3. [Verified Incidents](#3-verified-incidents)
4. [Illustrative Examples: Verify Before Using](#4-illustrative-examples--verify-before-using)
5. [Unresolved Hypotheses](#5-unresolved-hypotheses)
6. [Real-Incident Template](#6-real-incident-template)
7. [Product Feedback for Hackathon Submission](#7-product-feedback-for-hackathon-submission)
8. [End-of-Day Review Checklist](#8-end-of-day-review-checklist)
9. [Pre-Submission Checklist](#9-pre-submission-checklist)

---

## 1. Summary Dashboard

Update this section by hand at every end-of-day review. Count **verified incidents only**. Illustrative examples and hypotheses never count.

| Metric | Value |
|---|---|
| Total verified incidents | 7 |
| Critical + High severity | 1 (FL-003) |
| Open (Open / Investigating) | 3 |
| Workaround Available | 1 |
| Resolved | 3 |
| Estimated development time lost | ~1.5 h |
| Most frequently affected tool or service | Alexa AI CLI / Alexa+ docs (3), MCP Python SDK (2) |
| Last updated | 2026-10-19 |

**Planned components and whether any friction has been logged for them yet:**

- [x] MCP Python SDK
- [ ] Streamable HTTP transport
- [x] Alexa AI CLI (`alexa-ai configure / new mcp / deploy`)
- [ ] Deployment / public HTTPS endpoint
- [ ] DynamoDB
- [ ] AWS Lambda + EventBridge Scheduler
- [ ] Amazon Bedrock
- [ ] Notification provider (SNS / Telegram / email)
- [ ] Alexa+ simulator web app
- [x] Documentation
- [x] Development workflow / tooling

---

## 2. Logging Procedure

### 2.1 When to create an entry
Log it **when it happens**, not from memory at the end of the day. Create an entry whenever:
- something fails, errors, hangs, or behaves differently from what the docs or our expectations say;
- documentation is missing, outdated, contradictory, or sent you to the wrong place;
- a setup, auth, account, or region step blocks progress;
- you spend more than about 10 minutes working out something that should have been obvious;
- you have to work around a product limitation.

If you're unsure, log it as **Investigating**. Deleting an entry later costs nothing; reconstructing one from memory rarely works.

### 2.2 Reproduce it so someone else can verify it
- Write numbered steps that start from a known state (a clean venv, a fresh terminal, a specific commit).
- Give exact commands, URLs, file names, and the **versions** involved (OS, Python, SDK, CLI, region).
- Paste the exact error text. A paraphrase isn't evidence.
- Ask a teammate to follow your steps. If they get the same result, note "reproduced by <name>".

### 2.3 Expected result vs actual result
- **Expected:** what the docs, the spec, or a reasonable developer would predict. If you can, cite the source ("Quickstart step 3 says…").
- **Actual:** only what you observed: the output, error, status code, or behavior. No guesses about the cause. Put theories in the Workaround or Suggestion field, or in [Unresolved Hypotheses](#5-unresolved-hypotheses).

### 2.4 Assign severity consistently

| Severity | Definition | Test question |
|---|---|---|
| **Critical** | Blocks the core demo or makes the system unusable | Could we still record the demo video? If not, it's Critical. |
| **High** | Blocks a major feature or delays development significantly (more than about 1 hour) | Did we lose a feature or half a day? |
| **Medium** | Breaks something, but there's a reasonable workaround | Did a workaround get us moving in under an hour? |
| **Low** | Minor inconvenience, confusing docs, cosmetic issue | Was it just annoying? |

Grade by impact **on us**, not by how angry we felt. If you're between two levels, pick the lower one and explain why.

### 2.5 Workarounds and improvements
- **Workaround:** the exact steps that got us unblocked, so a teammate can repeat them. Write "None yet" if you don't have one.
- **Suggestion:** one concrete change Amazon or the tool owner could make, such as a doc fix, a clearer error message, a CLI flag, or a default. "Make it better" is not a suggestion.

### 2.6 Update an entry after it's resolved
- Change the Status to **Resolved** (or **Workaround Available** if the root problem is still there).
- Record what fixed it and how you checked (for example, "re-ran `test_server.py`, all assertions pass").
- Never delete a resolved entry. The history is what the judges are scoring.
- Update the [Summary Dashboard](#1-summary-dashboard).

### 2.7 Why honesty beats volume
Judges and product teams act on feedback they can reproduce. One entry with exact versions, steps, and error text is worth more than ten vague complaints. Made-up or exaggerated entries can't be reproduced, waste the product team's time, and damage the credibility of everything else in the submission. If it didn't happen, it doesn't go in.

### 2.8 Redact secrets
Before you paste logs, terminal output, or screenshots, remove **passwords, API keys, AWS access keys, session or OAuth tokens, account IDs, personal email addresses, phone numbers, and other personal information**. Replace them with `<REDACTED>`.

---

## 3. Verified Incidents

These entries were observed directly during development and include real error text.
Environment for FL-001 and FL-002: Windows 11 Home 10.0.26200, Python 3.14.3, `mcp` 2.3.0 from PyPI, fresh venv.

| ID | Date & Time | Task | Steps to Reproduce | Expected Result | Actual Result | Severity | Workaround | Suggestion / Product Feedback | Status |
|---|---|---|---|---|---|---|---|---|---|
| FL-001 | 2026-10-18 (evening IST; exact time not recorded) | Create the MCP server skeleton in Python | 1. `python -m venv .venv` 2. `pip install mcp` (installs 2.3.0) 3. `from mcp.server.fastmcp import FastMCP`, the import used in most MCP tutorials and examples | The import succeeds and the FastMCP server can be used | `ModuleNotFoundError: No module named 'mcp.server.fastmcp'. This is mcp 2.x, where FastMCP was renamed to MCPServer (from mcp.server.mcpserver import MCPServer) and other APIs changed` | Low | Used `from mcp.server.mcpserver import MCPServer`; `@mcp.tool()` and `streamable_http_app()` still work | The error message is excellent because it names the fix. Alexa+ MCP quickstarts and samples should pin an SDK version or show the `mcp` 2.x API so new developers don't hit this on step one | Resolved |
| FL-002 | 2026-10-18 (evening IST; exact time not recorded) | Write an in-process Streamable HTTP test client | 1. Same environment as FL-001 2. In a test, `import httpx` and pass an `httpx.AsyncClient` to `mcp.client.streamable_http.streamable_http_client` | `httpx` is available, because MCP's HTTP client was historically built on it | `ModuleNotFoundError: No module named 'httpx'`. `mcp` 2.3.0 depends on `httpx2`, and `streamable_http_client` takes `http_client: httpx2.AsyncClient` | Low | `import httpx2 as httpx`. The test then passes and all 5 tools answer in ~4–6 ms | Mention the `httpx` to `httpx2` switch prominently in the SDK migration guide and in client examples | Resolved |
| FL-003 | 2026-10-18 (evening IST; exact time not recorded) | Install the Alexa AI CLI | 1. Open the MCP Toolkit quickstart (`/docs/alexaplus/add-ons/mcp-toolkit-quickstart`) 2. Step 1 says "Download and install CLI" 3. Search npm for the CLI | A public install command, e.g. `npm install -g <package>` | The quickstart gives no command. The install steps are on a separate page (`set-up-your-development-environment`): `@alexa-ai/cli` is served from a private CodeArtifact registry and needs an IAM user that assumes `AddOn3PDeveloperToolsRead` in Amazon's account, which the page says is granted via "the AWS account you gave the Alexa Solutions Architect". `npm search alexa-ai` instead returns an unrelated third-party package named `alexa-ai` (a WhatsApp bot) | High | Asked in the hackathon Discord (2026-10-19): no Alexa+ support channel or answer. Building our own simulated Alexa+ web app, which the rules allow, calling our MCP server | Put the install command, or a clear "access is gated, request it here" link, directly in quickstart step 1. Give hackathon participants a self-serve allowlist. Publish a public placeholder at `@alexa-ai/cli` on npm, and warn about the look-alike `alexa-ai` package | Investigating |
| FL-004 | 2026-10-18 (evening IST; exact time not recorded) | Check the CLI's OS support | 1. Read the requirements in `set-up-your-development-environment` | Windows listed, or explicitly marked unsupported | Requirements say "macOS Sierra or higher or Ubuntu", Node.js 24+. Windows isn't mentioned; our team develops on Windows 11 | Medium | Not yet tested; fallback options are WSL (Ubuntu) or a Linux cloud shell | State Windows support explicitly, or document WSL as the supported route | Open |
| FL-005 | 2026-10-18 (evening IST; exact time not recorded) | Decide whether our MCP server needs OAuth | 1. Read "MCP requirements" in the quickstart 2. Read `mcp-toolkit-authentication` | A clear statement of whether a public server with no user accounts can skip auth, and how the server learns which Alexa user is speaking | The quickstart's authentication checklist reads as mandatory (return 401 with no `WWW-Authenticate`, OAuth 2.1 + PKCE S256). The auth page only describes Tier 1 as "if you have a private MCP Server" and Tier 2 for "user-specific tools". Neither page says whether no-auth is allowed or how to identify a user without account linking | Medium | Planning a single-demo-user server first; per-user storage will need Tier 2 account linking | Add a "no-auth / anonymous" row to the auth tier table, and document which user identifier (if any) reaches the server without account linking | Open |
| FL-006 | 2026-10-19 ~16:15 IST | Configure the AWS CLI on Windows | 1. `winget install Amazon.AWSCLI` while VS Code is open 2. In a new VS Code terminal, run `aws configure` 3. Type values at the prompts | `aws` is found; `aws configure` rejects invalid input (e.g. region "India") | `aws` was not recognised in VS Code terminals until VS Code restarted (PATH is inherited at launch). `aws configure` accepted and saved an invalid region (`India`, `dsasd`), an output format of `asdasd`, and the text "aws login" as an Access Key ID, with no warning. A secret key was also exposed in a screenshot during setup and had to be deleted | Medium | Cleared `~/.aws/credentials` and `config`; signed in with `aws login` (browser-based, short-lived credentials); deleted the exposed key with `aws iam delete-access-key` | Validate the region and output format in `aws configure`; check the access key format; recommend `aws login` before `aws configure` for new users | Resolved |
| FL-007 | 2026-10-19 ~16:40 IST | Deploy the MCP server on the team's AWS account | 1. Sign in with `aws login` (role `AccountFullAccessRole`) 2. `aws lambda list-functions` 3. Try Lightsail `create-bucket` 4. `aws iam simulate-principal-policy` on the role for 28 actions | An account that says "full access" can create Lambda, DynamoDB, Lightsail and S3 resources | `AccessDeniedException ... with an explicit deny in a service control policy` from an AWS Organization. The simulator showed only `bedrock:InvokeModel`, IAM, CloudFront and CloudWatch Logs allowed. Lambda, DynamoDB, EventBridge Scheduler, SNS, SES, S3, Lightsail create, App Runner, ECS, EC2, API Gateway and even `bedrock:Converse` were denied. Read-only Lightsail calls succeeded, which made it look usable | Medium | Moving to a new personal AWS account; `iam simulate-principal-policy` showed the full picture in one call | Show active SCP restrictions in the console (e.g. a banner on blocked service pages), and avoid role names like "FullAccess" on SCP-limited sandboxes | Workaround Available |

> Add new rows here using the next ID (FL-003, FL-004…). Copy the [template](#6-real-incident-template) for detailed notes.

---

## 4. Illustrative Examples: Verify Before Using

> ⚠️ **ILLUSTRATIVE EXAMPLE: VERIFY BEFORE USING.** None of the rows below have happened to this team. They are plausible scenarios that show the level of detail we expect. To promote one: reproduce it, replace **Actual Result** with what you observed, fill in the real date and time, give it the next `FL-` ID, and move it to [Verified Incidents](#3-verified-incidents). If it never happens, leave it here or delete it. **Never submit these as-is.**

| ID | Date & Time | Task | Steps to Reproduce | Expected Result | Actual Result | Severity | Workaround | Suggestion / Product Feedback | Status |
|---|---|---|---|---|---|---|---|---|---|
| EX-01 | *(unverified)* | Authenticate the Alexa AI CLI | 1. Install the Alexa AI CLI 2. `alexa-ai configure` 3. Log in with an Amazon Developer account registered in India | Login succeeds and Alexa+ MCP commands become available | **[UNVERIFIED: replace with observed output]** e.g. the login succeeds but `alexa-ai new mcp` reports Alexa+ isn't available for the account's region or marketplace | High | Use the simulator web app for the demo and record the exact CLI output as evidence | List supported marketplaces and regions up front in the quickstart; have `configure` warn about region eligibility immediately | Open |
| EX-02 | *(unverified)* | Connect a client to the MCP server and discover tools | 1. `python server.py` 2. `npx @modelcontextprotocol/inspector` 3. Connect to `http://localhost:8000/mcp` with the Streamable HTTP transport | Inspector lists all 5 FollowThrough tools | **[UNVERIFIED: replace with observed output]** e.g. a connection error or empty tool list because of a wrong transport choice, a missing `/mcp` path, or a host header rejection | Medium | Confirm the transport type and full path; check the server's transport security settings | Inspector should show the HTTP status and response body when the handshake fails | Open |
| EX-03 | *(unverified)* | Deploy to a public HTTPS endpoint | 1. Deploy the server container to App Runner or a Lambda Function URL 2. Register the URL with `alexa-ai new mcp --mcp-server-url https://…/mcp` | Alexa+ reaches the endpoint and lists the tools | **[UNVERIFIED: replace with observed output]** e.g. registration fails because of a trailing-slash mismatch, a TLS problem, or a 403 from host validation | High | Test the public URL with Inspector before registering; check `/mcp` with and without the trailing slash | `alexa-ai new mcp` should run a live preflight check of the URL and print the actual HTTP response | Open |
| EX-04 | *(unverified)* | Meet the 500 ms round-trip latency requirement | 1. Deploy to Lambda 2. Call `whats_pending` after the function has been idle 3. Time the round trip | Response in under 500 ms | **[UNVERIFIED: replace with measured numbers]** e.g. the first call after idle takes well over 500 ms because of a cold start | High | Provisioned concurrency, App Runner (always warm), or a scheduled warm-up ping | Docs should say whether 500 ms covers cold starts and recommend hosting patterns that meet it | Open |
| EX-05 | *(unverified)* | Store tasks in DynamoDB | 1. Create table `followthrough-tasks` 2. Deploy the server with an execution role 3. Call `create_task` | The task is written to DynamoDB | **[UNVERIFIED: replace with observed output]** e.g. `AccessDeniedException` because the role is missing `dynamodb:PutItem` | Medium | Add a least-privilege policy for the table ARN | Show the exact missing action and resource in the console or error message, with a one-click policy fix | Open |
| EX-06 | *(unverified)* | Parse natural language with Bedrock | 1. Call Bedrock with "kal subah 9 baje tak DBMS assignment submit karna hai" 2. Ask for JSON `{title, deadline}` | Valid JSON with an ISO 8601 deadline in IST | **[UNVERIFIED: replace with observed output]** e.g. `AccessDeniedException` because model access isn't enabled in the region, or a deadline that ignores the user's timezone | Medium | Request model access; pass the current date and timezone in the prompt; validate the output with a schema | Make model access state obvious in the error message; document timezone handling for structured output | Open |
| EX-07 | *(unverified)* | Send repeat reminders with EventBridge Scheduler | 1. Create a schedule that invokes the nag Lambda every N minutes 2. Leave the task undone | The Lambda fires on schedule and a push notification arrives | **[UNVERIFIED: replace with observed output]** e.g. the schedule never fires because the scheduler role can't invoke the Lambda, or SNS SMS is unavailable for the destination country | High | Fix the scheduler role trust policy; use email, Telegram, or another available provider | Show a "last invocation failed: reason" field on the schedule in the console | Open |
| EX-08 | *(unverified)* | Follow the Alexa+ MCP Toolkit docs | 1. Follow the MCP Toolkit quickstart step by step | Every step matches the current CLI and SDK | **[UNVERIFIED: replace with exact doc URL, step, and mismatch]** e.g. a command flag or SDK import in the docs no longer matches the released tool | Low | Use `--help` output or the SDK migration guide | Version-stamp the docs and link a changelog for the CLI | Open |

---

## 5. Unresolved Hypotheses

Suspected issues we haven't confirmed yet. These are **not incidents**. Move one to [Verified Incidents](#3-verified-incidents) once it's reproduced, or strike it out once it's ruled out.

| # | Hypothesis | How to confirm or rule out | Owner | Status |
|---|---|---|---|---|
| H-1 | Alexa+ access for the MCP toolkit may be limited from India, which would force us to demo with the simulator | Run `alexa-ai configure` and `alexa-ai new mcp` with our account and record the output | | Open |
| H-2 | ~~How Alexa+ identifies the end user~~: partly answered by FL-005. Per-user identity seems to come only via Tier 2 account linking (OAuth). Still to confirm: whether any user id reaches a no-auth server | Inspect incoming request headers once connected | | Investigating |

---

## 6. Real-Incident Template

Copy this block for every new incident and fill in every field. Then add a one-line summary row to the [Verified Incidents](#3-verified-incidents) table. **Redact secrets and personal data first.**

```markdown
### FL-XXX: <short title>

- **Incident ID:** FL-XXX
- **Date and time:** YYYY-MM-DD HH:MM IST
- **Team member:**
- **Task being attempted:**
- **Tool, service, or component:**
- **Environment and versions:** OS, Python/Node, SDK/CLI versions, AWS region
- **Steps to reproduce:**
  1.
  2.
  3.
- **Expected result:** (cite the doc or spec if possible)
- **Actual result:** (only what you observed)
- **Error message or evidence:** (exact text, log excerpt, screenshot path, all <REDACTED> where needed)
- **Severity:** Critical / High / Medium / Low
- **Workaround:**
- **Time lost:**
- **Suggested improvement:**
- **Status:** Open / Investigating / Workaround Available / Resolved
- **Resolution and verification:** (what fixed it, and how you confirmed it)
```

---

## 7. Product Feedback for Hackathon Submission

Write one block per **verified** incident that a product team could act on. Keep each block short, specific, and constructive. Put real Alexa+ developer-experience friction first.

### Feedback: FL-001 and FL-002, MCP Python SDK 2.x API changes

- **Product or tool:** MCP Python SDK (`mcp` 2.3.0), as used by the Alexa+ MCP integration path
- **Problem encountered:** The common tutorial imports `from mcp.server.fastmcp import FastMCP` and plain `httpx` don't work in 2.x. FastMCP is now `MCPServer`, and the client uses `httpx2`.
- **Developer impact:** About 10 minutes lost at the very first step of building the server. The cost would be higher for developers new to Python packaging.
- **Evidence:** Exact `ModuleNotFoundError` text recorded in FL-001 and FL-002. The fix was verified by an end-to-end test with all 5 tools.
- **Proposed improvement:** Pin the SDK version in the Alexa+ MCP quickstart, or update samples to the 2.x API, and call out the `httpx2` change in the migration guide.
- **Why the improvement matters:** A hackathon developer's first ten minutes decide whether they keep going. A sample that fails on its first import erodes trust in the rest of the docs.

### Feedback template (copy for each new verified incident)

```markdown
### Feedback: FL-XXX, <short title>

- **Product or tool:**
- **Problem encountered:**
- **Developer impact:** (time lost, features blocked)
- **Evidence:** (link to FL-XXX; exact error text)
- **Proposed improvement:**
- **Why the improvement matters:**
```

---

## 8. End-of-Day Review Checklist

- [ ] Every problem hit today has an entry, or a reason it doesn't need one
- [ ] Each new entry has numbered steps, versions, and exact error text
- [ ] Statuses are updated; resolved entries record how the fix was verified
- [ ] Time lost is filled in for each new entry
- [ ] Open items have an owner and a next step
- [ ] Hypotheses are confirmed, ruled out, or carried over to tomorrow
- [ ] Summary Dashboard is updated (verified incidents only)
- [ ] Secrets and personal data are redacted

---

## 9. Pre-Submission Checklist

- [ ] **Evidence:** every submitted entry has observed results and exact error text; no `[UNVERIFIED]` markers remain in submitted content
- [ ] **No illustrative examples submitted as real:** EX-rows are excluded or were promoted only after reproduction
- [ ] **Severity:** each level checked against the table in [2.4](#24-assign-severity-consistently)
- [ ] **Status:** every entry is Resolved, Workaround Available, or Open with a clear explanation
- [ ] **Timestamps:** real, or marked "exact time not recorded"; none invented
- [ ] **Feedback quality:** each feedback block names a product, an impact, evidence, and one concrete fix
- [ ] **Coverage:** feedback covers every tool or SDK used, including AWS services (a Devpost requirement)
- [ ] **Redaction:** no keys, tokens, account IDs, or personal data
- [ ] **Dashboard:** numbers match the verified table
- [ ] **Copy test:** the tables paste cleanly into Google Sheets or Docs
