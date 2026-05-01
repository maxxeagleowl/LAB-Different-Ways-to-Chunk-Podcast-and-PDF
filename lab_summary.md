# Generated Not Tested

Due expensive Model setting in Codey I exceded my API limit. Rewerting the Code to anthopic not possible. I need Whsiper SST vi aOpenAI. 

'RateLimitError: Error code: 429 I wasn´t able to proceed an test 'chunking-strategies.ipynp''


# Lab Summary – Different Ways to Chunk Podcast and PDF

For **PDF documents** (structured, section-based content), Recursive Character Chunking with `chunk_size=1000` and `chunk_overlap=200` is the recommended strategy: the priority-ordered separator list (`\n\n` → `\n` → `. `) keeps headers and paragraphs intact, so retrieved chunks contain full arguments rather than fragments — a direct win for RAG answer quality. For **podcast transcripts** (flat, conversational text without paragraph breaks), the same recursive strategy works best but tuned smaller (`chunk_size=800`, `chunk_overlap=150`) with sentence-level separators prioritised (`. `, `! `, `? `), since conversational turns are short and topic shifts happen at sentence boundaries rather than paragraph breaks. Fixed-size chunking is the simplest to implement but consistently breaks sentences mid-thought for both content types; token-based chunking is indispensable when you need strict context-window budgeting for a specific LLM, but still requires a structure-aware separator to avoid broken context; semantic chunking produces the most meaning-faithful splits but is computationally expensive and best reserved for dense, argumentative content where size-based boundaries would obscure the reasoning chain.
