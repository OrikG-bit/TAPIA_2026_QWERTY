"""Shared Claude API wrapper for the pipeline.

STUB: created by Pair B because this file did not exist yet. Whoever owns the
shared LLM layer should review/replace it -- the rest of the pipeline only
depends on `call_llm(prompt) -> str`, so keep that signature stable.
"""

MODEL = "claude-opus-5"
MAX_TOKENS = 16000

_client = None


def _get_client():
    """Lazily build and reuse one Anthropic client (credentials come from the environment)."""
    global _client
    if _client is None:
        try:
            import anthropic
        except ImportError as exc:
            raise RuntimeError(
                "The 'anthropic' package is not installed. Run: pip install anthropic"
            ) from exc
        # Reads ANTHROPIC_API_KEY (or an `ant auth login` profile). Never hardcode a key.
        _client = anthropic.Anthropic()
    return _client


def call_llm(prompt: str) -> str:
    """Send a single prompt to Claude and return the response text."""
    response = _get_client().messages.create(
        model=MODEL,
        max_tokens=MAX_TOKENS,
        messages=[{"role": "user", "content": prompt}],
    )
    return "".join(block.text for block in response.content if block.type == "text")
