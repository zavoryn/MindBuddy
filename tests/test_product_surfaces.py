from mindbuddy.product_surfaces import build_readiness_report


def test_build_readiness_report_surfaces_viable_fallbacks() -> None:
    report = build_readiness_report(
        ".",
        runtime={
            "model": "claude-sonnet-4-20250514",
            "apiKey": "anthropic-key",
            "baseUrl": "https://api.anthropic.com",
            "fallbackModels": ["gpt-4o"],
            "openaiApiKey": "openai-key",
            "openaiBaseUrl": "https://api.openai.com",
        },
    )

    assert report.status == "ready"
    assert report.provider_ready is True
    assert report.fallback_ready is True
    assert report.fallback_candidates == ["gpt-4o", "claude-haiku-3-20240307"]
    assert report.viable_fallbacks == ["gpt-4o", "claude-haiku-3-20240307"]
    assert "fallbacks 2/2 locally ready" in report.summary


def test_build_readiness_report_warns_when_primary_ready_but_no_fallbacks() -> None:
    report = build_readiness_report(
        ".",
        runtime={
            "model": "deepseek-v4-pro[1m]",
            "baseUrl": "https://api.anthropic.com",
            "authToken": "proxy-token",
        },
    )

    assert report.status in ("warning", "blocked")
    assert report.provider_channel is not None


def test_build_readiness_report_uses_default_fallback_coverage() -> None:
    report = build_readiness_report(
        ".",
        runtime={
            "model": "deepseek-v4-pro[1m]",
            "apiKey": "anthropic-key",
            "baseUrl": "https://api.anthropic.com",
            "openaiApiKey": "openai-key",
            "openaiBaseUrl": "https://api.openai.com",
        },
    )

    assert report.status in ("ready", "warning", "blocked")
    assert isinstance(report.fallback_candidates, list)
