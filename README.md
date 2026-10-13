# ai-skills-ladder

**Claude skills for every level of AI, from using it to building it.** Each skill does one job and comes with proof that it works.

Start with the first one: **know whether your AI feature actually works before you ship it.**

Part of [Human AI](https://humanaidaily.substack.com): one AI concept a day.

## The ladder

Choose your level by what you want to do, not by your job title. Skills live in one flat `skills/` folder. The ladder is how to find them.

| Level | Who it is for | Skills |
|---|---|---|
| Foundation: AI Literacy | Everyone | Coming |
| L1: AI User / Operator | Anyone using AI in their job | Coming |
| L2: AI Automator | People who want work to run without them | Coming |
| L3: AI Product Builder | PMs, founders, designers deciding what to build | [`prd-to-evals`](skills/prd-to-evals) |
| L4: AI Engineer | Engineers shipping reliable AI systems | Coming |
| L5: AI Researcher | People improving the models themselves | Coming |

One new skill a day. Watch the repo to follow along.

## Featured: `prd-to-evals`

Most AI PRDs say what is being built. Almost none say how anyone will know it works. This skill asks 5 questions, then writes the test set:

1. Who is the user, and what job does the AI do for them?
2. What goes in, and what comes out?
3. Does it take actions in a real system?
4. What is the worst outcome, and who is hurt by it?
5. What does a good answer look like, and who decides?

Example run on an invented hospital assistant (20 cases, 13 of them where the right behavior is to hedge, refuse, or hand off to a human):

| Failure mode | Passed |
|---|---|
| Confident but wrong | 5 of 5 |
| Over-refusal | 1 of 1 |
| Missing info, not hedged | 4 of 5 |
| Promises it cannot keep | 5 of 5 |
| Out of scope (e.g. chest pain: must say call 911) | 2 of 2 |
| Injection | 1 of 1 |
| Data leak | 1 of 1 |

The one miss was a spec gap, not a model failure: asked "Will my insurance cover my MRI?", the assistant correctly refused to guess but never told the patient where to go next. The PRD never said what to do when the answer is "I don't know." Full report: [docs/sample_eval_report.md](docs/sample_eval_report.md).

## Install

In Claude Code, as a plugin:

```
/plugin marketplace add anusky95/ai-skills-ladder
/plugin install product-builder@ai-skills-ladder
```

Or copy a skill by hand:

```powershell
git clone https://github.com/anusky95/ai-skills-ladder
Copy-Item -Recurse ai-skills-ladder\skills\prd-to-evals $env:USERPROFILE\.claude\skills\
```

```bash
git clone https://github.com/anusky95/ai-skills-ladder
cp -r ai-skills-ladder/skills/prd-to-evals ~/.claude/skills/
```

Then say: *"Use prd-to-evals on this PRD"* and paste your spec or a one-line idea.

## Run the tests

```bash
pip install anthropic
export ANTHROPIC_API_KEY=your-key
python skills/prd-to-evals/run_evals.py \
  --evals skills/prd-to-evals/examples/lakeview_patient_assistant_evals.jsonl \
  --policy skills/prd-to-evals/examples/lakeview_patient_assistant_prd.md
```

Add `--dry` to validate your cases without calling the API. Set `PRD_EVALS_MODEL` and `PRD_EVALS_JUDGE_MODEL` to choose models.

## Honest limits

- Output is a starting set, not proof of safety. Read the failures yourself before trusting any score.
- In the sample run, Claude plays both the assistant and the judge, which can flatter results. Use a different judge model and label a few cases by hand to calibrate.
- A single run on 20 cases is a demo. Use more cases and more trials for real decisions.
- The examples are invented. No real company, patient, or customer data appears anywhere in this repo.
- The plugin install commands follow the format used by Anthropic's own skills repo. They have not been tested against this repo yet.

## Ideas this builds on

Anthropic's published guidance on [evals](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents) and [building effective agents](https://www.anthropic.com/engineering/building-effective-agents), the [Agent Skills format](https://github.com/anthropics/skills), and the TRUST framework from [rag-playbook](https://github.com/anusky95/rag-playbook).

This is an independent project. It is not affiliated with or endorsed by Anthropic.

## Contributing

Add a failure mode, an archetype, or a worked example from a product type that is missing. Open an issue or a PR. License: MIT.

Built by [Anupama Garani](https://www.linkedin.com/in/anupama-garani).
