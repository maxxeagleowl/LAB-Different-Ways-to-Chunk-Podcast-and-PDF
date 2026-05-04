## Chunking Strategy Recommendations

### For PDF Documents:
**Recommended Strategy:** Recursive Character Chunking
**Reasoning:**
- PDFs have headers, numbered sections, and multi-sentence paragraphs that are preserved by `\n\n` separator priority.
- Key advantages: semantic sections stay intact; retrieval picks up full arguments rather than fragment.
- Optimal: `chunk_size=1000`, `chunk_overlap=200`, separators `["\n\n", "\n", ". ", " ", ""]`.

### For Podcast Transcripts:
**Recommended Strategy:** Recursive Character Chunking (with sentence-level separators prioritised)
**Reasoning:**
- Transcripts lack paragraph breaks; sentence-ending separators (`. `) become the primary boundary.
- Conversational turns are short, so a smaller `chunk_size` (~600–800 chars) better isolates topic shifts.
- Optimal: `chunk_size=800`, `chunk_overlap=150`, separators `[". ", "! ", "? ", "\n", " ", ""]`.

### Trade-offs Summary:
| Strategy    | Pros                              | Cons                            | Best For                 |
|-------------|-----------------------------------|---------------------------------|--------------------------|
| Fixed-Size  | Simple, predictable, fast         | Breaks sentences & context      | Uniform / pre-cleaned text |
| Recursive   | Respects structure & sentences    | Slightly more tuning needed     | Structured docs, transcripts |
| Token-Based | Exact LLM context-window budget   | May still break sentences       | Token-sensitive pipelines |
| Semantic    | Meaning-driven splits             | Slow, requires ML model         | Dense / argumentative content |