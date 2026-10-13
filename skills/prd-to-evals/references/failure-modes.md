# Universal failure modes

Weight these by archetype and stakes. Name each case with the tag in backticks.

1. `confident_wrong`: states a wrong fact fluently, or accepts a false premise from the user.
2. `missing_info_not_hedged`: the answer is not in the sources, and the product guesses instead of saying so.
3. `stale_source`: answers from outdated information.
4. `over_refusal`: blocks a legitimate request. Unhelpfulness has a cost too.
5. `under_refusal`: answers something it should not.
6. `out_of_scope`: handles a request outside its job badly.
7. `injection`: obeys instructions hidden in user input or documents, or reveals internal rules.
8. `data_leak`: exposes sensitive or another person's data.
9. `inconsistent`: gives different answers to the same question across runs.
10. `format_break`: output shape breaks the next step.
11. `unauthorized_commitment`: promises something it cannot grant (refund, waiver, outcome).
12. `unauthorized_action` / `tool_misuse` (agents only): takes a consequential action without approval, or uses a tool wrongly.
13. `bias_or_unfair` (rankers): systematically disadvantages a group.

Design notes taken from Anthropic's published eval guidance: balance should-happen and should-not-happen cases, grade outputs rather than exact paths, give model judges an "Unknown" option, start with 20 to 50 cases from real failures when you have them.
