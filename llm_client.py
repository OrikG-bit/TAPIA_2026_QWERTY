"""Shared LLM call wrapper -- everyone imports from here.

Calls OpenRouter through its OpenAI-compatible API, so we use the `openai`
package regardless of which model slug MODEL points at. Reads the API key from
LLM_API_KEY, the variable name the README setup steps tell everyone to export.

Contract for the rest of the pipeline: `call_llm(prompt) -> str`. Keep that
signature stable; swap the endpoint or model underneath it as needed.
"""

import os

from dotenv import load_dotenv

# Load .env into the environment before anything reads os.environ.
load_dotenv()

BASE_URL = "https://openrouter.ai/api/v1"
# Slug verified against https://openrouter.ai/api/v1/models.
MODEL = "anthropic/claude-sonnet-5"
MAX_TOKENS = 16000

_client = None


def _get_client():
    """Lazily build and reuse one OpenRouter client, keyed off LLM_API_KEY."""
    global _client
    if _client is None:
        try:
            from openai import OpenAI
        except ImportError as exc:
            raise RuntimeError(
                "The 'openai' package is not installed. Run: pip install -r requirements.txt"
            ) from exc

        # Try to get API key from environment or Streamlit secrets
        api_key = os.environ.get("LLM_API_KEY")

        # If not in env, try Streamlit secrets (for cloud deployment)
        if not api_key:
            try:
                import streamlit as st
                api_key = st.secrets.get("LLM_API_KEY")
            except:
                pass

        if not api_key:
            raise RuntimeError(
                'LLM_API_KEY is not set.\n'
                'Local: export LLM_API_KEY="your-key-here" (or add to .env)\n'
                'Streamlit Cloud: Add LLM_API_KEY to secrets in dashboard'
            )

        _client = OpenAI(base_url=BASE_URL, api_key=api_key)
    return _client


def call_llm(prompt: str) -> str:
    """Send a single prompt to the LLM and return the response text."""
    response = _get_client().chat.completions.create(
        model=MODEL,
        max_tokens=MAX_TOKENS,
        messages=[{"role": "user", "content": prompt}],
    )
    content = response.choices[0].message.content
    if not content:
        raise RuntimeError(
            f"{MODEL} returned an empty response "
            f"(finish_reason={response.choices[0].finish_reason!r})"
        )
    return content


if __name__ == "__main__":
    # Connection smoke test -- README tells everyone to run `python llm_client.py`.
    print(call_llm("Reply with exactly: LLM connection OK"))
