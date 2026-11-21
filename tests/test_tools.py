from unittest.mock import MagicMock, patch

from acemusic_crewai import tools


def test_native_tool_discovery_and_original_task(monkeypatch):
    monkeypatch.setenv("ACEDATACLOUD_API_TOKEN", "offline-example")
    collection = tools
    named = {t.name: t for t in collection}
    assert set(named) == {
        "acemusic_generate_custom_music",
        "acemusic_cover_audio",
        "acemusic_generate_music",
        "acemusic_get_task",
        "acemusic_upload_audio",
        "acemusic_generate_lyrics",
        "acemusic_mashup_audio",
    }
    with patch("acemusic_crewai.tools.AceDataCloud") as constructor:
        api = constructor.return_value.__enter__.return_value.acemusic
        api.generate.return_value = MagicMock(id="original")
        api.tasks.return_value = {"status": "partial_failed", "response": {"data": []}}
        result = named["acemusic_generate_music"].run(prompt="sample")
        assert result == {"task_id": "original"}
        api.generate.assert_called_once_with(
            action="generate", prompt="sample", model="acemusic-v1.1", async_=True
        )
        record = named["acemusic_get_task"].run(task_id="original")
        assert record["status"] == "partial_failed"
        api.tasks.assert_called_once_with(action="retrieve", id="original")
        assert constructor.call_args.kwargs["max_retries"] == 0
