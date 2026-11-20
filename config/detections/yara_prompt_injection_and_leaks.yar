rule PromptInjection_UnicodeTag_Smuggling {
    meta:
        description = "Detects UTF-8 encoded Unicode Tag characters (U+E0000-U+E007F) used to hide prompt injections"
        author = "llm-sec-studio"
        severity = "high"
    strings:
        $utag_utf8_prefix = { F3 A0 ( 80 | 81 ) }
    condition:
        $utag_utf8_prefix
}

rule PromptInjection_ControlToken_Smuggling {
    meta:
        description = "Detects ChatML and tool-call control tokens in untrusted external artifacts"
        author = "llm-sec-studio"
        severity = "high"
    strings:
        $im_start = "<|im_start|>" ascii nocase
        $im_end = "<|im_end|>" ascii nocase
        $tool_call = "<|tool_call|>" ascii nocase
        $endoftext = "<|endoftext|>" ascii nocase
    condition:
        any of them
}
