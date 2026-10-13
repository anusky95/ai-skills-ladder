# Archetypes

| Archetype | Example | Output | Usual top failure modes |
|---|---|---|---|
| Answer from documents (RAG Q&A) | HR benefits assistant | Free text with sources | confident_wrong, missing_info_not_hedged, stale_source |
| Extract or summarize | Contract summarizer | Fields or text | confident_wrong, format_break, injection |
| Classify or route | Email triage | A label | confident_wrong, inconsistent, over/under_refusal |
| Generate or draft | Reply writer, code helper | Text or code | confident_wrong, data_leak, inconsistent |
| Conversational assistant | Support chatbot | Multi-turn text | missing_info_not_hedged, out_of_scope, unauthorized_commitment |
| Agent that takes actions | Refund or booking bot | Actions in a system | unauthorized_action, tool_misuse, injection |
| Rank or recommend | Job matcher | Ordered list | bias_or_unfair, inconsistent, confident_wrong |

Products can be several at once (a support chatbot that answers from documents and can open cases is conversational + RAG + a thin action layer). List all that apply.

Out of scope for this skill: voice, image, and video products. Say so and ask questions instead of guessing.
