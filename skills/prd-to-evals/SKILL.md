---
name: prd-to-evals
description: Turns any AI product requirements doc (or a one-line feature idea) into a starter eval set a PM can run before launch. Classifies the product into an archetype, ranks failure modes by stakes, writes about 20 balanced test cases (including should-refuse and should-hedge cases), picks a grader for each, and sets a pass bar plus a do-not-ship trigger. Use when the user says "write evals for this PRD", "how will we know this works", "test plan for my AI feature", "what could go wrong with this feature", or pastes an AI feature spec.
---

# PRD to evals

Goal: answer "how will we know it worked?" before anything is built. Output is a file of test cases, not advice.

## Step 1: Intake (ask only what the PRD does not already answer)
1. Who is the user, and what job does the AI do for them?
2. What goes in, and what comes out?
3. Does it take actions in a real system (refunds, bookings, sends)?
4. What is the worst outcome, and who is hurt by it?
5. What does a good answer look like, and who decides? (This sets the grader.)

If the PM cannot answer #4, stop and help them answer it first. It decides the ranking in step 3.

## Step 2: Classify
Pick one or more archetypes from `references/archetypes.md`. If the product fits none, say so and ask more questions. Do not force a fit.

## Step 3: Rank failure modes
Take the universal list in `references/failure-modes.md`. Weight each by archetype and by the stakes from intake #4. Keep the top 3 as focus modes. Say why in one line each.

## Step 4: Write about 20 cases
- At least a third are should-hedge, should-refuse, or should-escalate cases.
- Include 2 or more cases where the right behavior is to answer (guards against over-refusal).
- Every case carries the failure mode it tests.
- Cases must be self-contained: put the facts needed to grade in the policy or context file, and invent nothing the PRD does not support.
- Case schema (one JSON object per line in `evals.jsonl`):
  `id`, `failure_mode`, `should` (answer | hedge | refuse | escalate), `input`, `must_include` (list), `must_not_include` (list), `rubric` (one sentence for a model judge, or empty).

## Step 5: Pick graders
- Fixed facts or labels: code check via `must_include` / `must_not_include`.
- Judgment (tone, hedging, escalation): model judge with the rubric. The judge may answer PASS, FAIL, or UNKNOWN. Never force a verdict.
- High stakes: flag for human review in the report.
- Actions: grade the final state of the system, not the steps taken.

## Step 6: Pass bar
Per focus mode, give a threshold and one explicit do-not-ship trigger (for example: any case where the bot promises a refund it cannot grant).

## Step 7: Hand off
Tell the PM: read the transcripts of failures yourself before trusting any score, and calibrate the model judge against your own labels on 5 cases. A 0% pass rate across a mode usually means a broken case, not a broken product.

## Rules
- Be honest about limits. Cases are a starting set drawn from the PRD, not proof of safety.
- Never use real customer, employer, or confidential data in examples.
- No em dashes in any output.
