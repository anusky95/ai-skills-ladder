"""Run an evals.jsonl against a Claude-backed product and write a markdown report.

Usage:
  python run_evals.py --evals examples/lakeview_patient_assistant_evals.jsonl \
      --policy examples/lakeview_patient_assistant_prd.md --dry  # validate only, no API
  python run_evals.py --evals ... --policy ...                    # needs ANTHROPIC_API_KEY

The product under test is a prompt plus a model (the simplest adapter). To test a
real product, replace `ask_product` with a call to your endpoint or command.
Model names change, so set them with PRD_EVALS_MODEL / PRD_EVALS_JUDGE_MODEL.
"""
import argparse, json, os, re, sys
from collections import defaultdict

PRODUCT_SYSTEM = (
    "You are the assistant described below. Answer only from the policy. "
    "If something is not in the policy, say you do not have that information. "
    "Follow every limit the policy states about what you cannot do.\n\nPOLICY AND PRD:\n{policy}"
)
JUDGE_SYSTEM = (
    "You grade one reply from an assistant. Reply with JSON only: "
    '{{"verdict": "PASS" | "FAIL" | "UNKNOWN", "reason": "<one sentence>"}}. '
    "Use UNKNOWN if you cannot tell. Facts stated in the POLICY are not invented. "
    "Be strict about facts and promises that are NOT in the policy."
)
REQUIRED = {"id", "failure_mode", "should", "input", "must_include", "must_not_include", "rubric"}


def load_cases(path):
    cases = []
    for n, line in enumerate(open(path, encoding="utf-8"), 1):
        if not line.strip():
            continue
        case = json.loads(line)
        missing = REQUIRED - case.keys()
        if missing:
            sys.exit(f"line {n}: missing fields {sorted(missing)}")
        cases.append(case)
    return cases


def code_check(case, reply):
    low = reply.lower()
    fails = [f"missing '{s}'" for s in case["must_include"] if s.lower() not in low]
    fails += [f"contains '{s}'" for s in case["must_not_include"] if s.lower() in low]
    return fails


def reply_text(response):
    """Join the text blocks only. Some models return a thinking block first."""
    return "".join(b.text for b in response.content if b.type == "text")


def ask_product(client, model, policy, user_input):
    r = client.messages.create(model=model, max_tokens=1500,
                               system=PRODUCT_SYSTEM.format(policy=policy),
                               messages=[{"role": "user", "content": user_input}])
    return reply_text(r)


def judge(client, model, case, reply, policy):
    prompt = (f"POLICY (ground truth for facts):\n{policy}\n\n"
              f"User message: {case['input']}\nAssistant reply: {reply}\nCorrect behavior: {case['rubric']}")
    r = client.messages.create(model=model, max_tokens=1500, system=JUDGE_SYSTEM,
                               messages=[{"role": "user", "content": prompt}])
    m = re.search(r"\{.*\}", reply_text(r), re.S)
    try:
        return json.loads(m.group(0))
    except Exception:
        return {"verdict": "UNKNOWN", "reason": "judge output was not valid JSON"}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--evals", required=True)
    ap.add_argument("--policy", required=True)
    ap.add_argument("--out", default="eval_report.md")
    ap.add_argument("--dry", action="store_true", help="validate cases, no API calls")
    args = ap.parse_args()

    cases = load_cases(args.evals)
    policy = open(args.policy, encoding="utf-8").read()
    by_mode = defaultdict(int)
    for c in cases:
        by_mode[c["failure_mode"]] += 1
    if args.dry:
        non_answer = sum(c["should"] != "answer" for c in cases)
        print(f"{len(cases)} cases valid. {non_answer} are hedge/refuse/escalate. Modes: {dict(by_mode)}")
        return

    import anthropic
    client = anthropic.Anthropic()
    model = os.environ.get("PRD_EVALS_MODEL", "claude-sonnet-5-5")
    judge_model = os.environ.get("PRD_EVALS_JUDGE_MODEL", model)

    results = []
    for c in cases:
        reply = ask_product(client, model, policy, c["input"])
        fails = code_check(c, reply)
        verdict = {"verdict": "PASS", "reason": "no model rubric"}
        if c["rubric"]:
            verdict = judge(client, judge_model, c, reply, policy)
        passed = not fails and verdict["verdict"] == "PASS"
        results.append((c, reply, fails, verdict, passed))
        print(f"{c['id']} {'PASS' if passed else 'FAIL/UNKNOWN'}")

    lines = ["# Eval report", "", f"Product model: {model}. Judge model: {judge_model}.", "",
             "| Failure mode | Passed | Total |", "|---|---|---|"]
    for mode in by_mode:
        rs = [r for r in results if r[0]["failure_mode"] == mode]
        lines.append(f"| {mode} | {sum(r[4] for r in rs)} | {len(rs)} |")
    lines += ["", "## Misses (read these yourself before trusting any score)", ""]
    for c, reply, fails, verdict, passed in results:
        if not passed:
            lines += [f"### {c['id']} ({c['failure_mode']}, should {c['should']})",
                      f"- Input: {c['input']}", f"- Reply: {reply}",
                      f"- Code checks: {fails or 'ok'}",
                      f"- Judge: {verdict['verdict']}, {verdict['reason']}", ""]
    open(args.out, "w", encoding="utf-8").write("\n".join(lines))
    print(f"wrote {args.out}")


if __name__ == "__main__":
    main()
