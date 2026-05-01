# Chunking Strategy Recommendations

## For PDF Documents
- **Recommended Strategy**: Recursive Character Chunking
- **Reasoning**:
  - PDFs have headers, numbered sections, and multi-sentence paragraphs preserved by `\n\n` separator priority.
  - Semantic sections stay intact; retrieval picks up full arguments rather than fragments.
- **Optimal Settings**: `chunk_size=1000`, `chunk_overlap=200`, separators `["\n\n", "\n", ". ", " ", ""]`.

## For Podcast Transcripts
- **Recommended Strategy**: Recursive Character Chunking (with sentence-level separators prioritized)
- **Reasoning**:
  - Transcripts lack paragraph breaks; sentence-ending separators (`. `) become the primary boundary.
  - Conversational turns are short, so a smaller `chunk_size` (~600–800 chars) better isolates topic shifts.
- **Optimal Settings**: `chunk_size=800`, `chunk_overlap=150`, separators `[". ", "! ", "? ", "\n", " ", ""]`.

## Trade-offs Summary
- **Fixed-Size**:
  - Pros: Simple, predictable, fast
  - Cons: Breaks sentences & context
  - Best For: Uniform / pre-cleaned text
- **Recursive**:
  - Pros: Respects structure & sentences
  - Cons: Slightly more tuning needed
  - Best For: Structured docs, transcripts
- **Token-Based**:
  - Pros: Exact LLM context-window budget
  - Cons: May still break sentences
  - Best For: Token-sensitive pipelines
- **Semantic**:
  - Pros: Meaning-driven splits
  - Cons: Slow, requires ML model
  - Best For: Dense / argumentative content