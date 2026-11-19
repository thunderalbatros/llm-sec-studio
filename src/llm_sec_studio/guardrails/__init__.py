"""Zero-Trust guardrails package (Spotlighting input sanitizer & fast prompt/trace sanitizer)."""
from llm_sec_studio.guardrails.input_sanitizer import SpotlightingSession, sanitize_untrusted_input
from llm_sec_studio.guardrails.prompt_sanitizer import compress_trace, sanitize_text

__all__ = ["SpotlightingSession", "compress_trace", "sanitize_text", "sanitize_untrusted_input"]
