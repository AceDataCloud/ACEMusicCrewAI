import os
from typing import Any, Literal

from acedatacloud import AceDataCloud
from crewai.tools import tool

Model = Literal["acemusic-v1.1", "acemusic-v1"]


def _task_id(task: Any) -> dict[str, str]:
    if not task.id:
        raise ValueError(
            "Submission returned no task ID. Check usage history before retrying."
        )
    return {"task_id": task.id}


@tool("acemusic_generate_music")
def acemusic_generate_music(
    prompt: str, model: Model = "acemusic-v1.1"
) -> dict[str, Any]:
    """Submit one paid idea-to-song task. Save the returned task ID."""
    with AceDataCloud(
        api_token=os.environ["ACEDATACLOUD_API_TOKEN"], max_retries=0
    ) as client:
        return _task_id(
            client.acemusic.generate(
                action="generate", prompt=prompt, model=model, async_=True
            )
        )


@tool("acemusic_generate_custom_music")
def acemusic_generate_custom_music(
    lyric: str, style: str, title: str, model: Model = "acemusic-v1.1"
) -> dict[str, Any]:
    """Submit one paid song task with original lyrics, style and title."""
    with AceDataCloud(
        api_token=os.environ["ACEDATACLOUD_API_TOKEN"], max_retries=0
    ) as client:
        return _task_id(
            client.acemusic.generate(
                action="generate",
                custom=True,
                lyric=lyric,
                style=style,
                title=title,
                model=model,
                async_=True,
            )
        )


@tool("acemusic_upload_audio")
def acemusic_upload_audio(audio_url: str, name: str | None = None) -> dict[str, Any]:
    """Import one authorized public HTTPS MP3 as a separately priced reference."""
    if not audio_url.startswith("https://"):
        raise ValueError("Use a public HTTPS MP3 URL.")
    with AceDataCloud(
        api_token=os.environ["ACEDATACLOUD_API_TOKEN"], max_retries=0
    ) as client:
        return _task_id(
            client.acemusic.generate(
                action="upload", audio_url=audio_url, name=name, async_=True
            )
        )


@tool("acemusic_cover_audio")
def acemusic_cover_audio(
    audio_id: str, lyric: str, style: str, title: str | None = None
) -> dict[str, Any]:
    """Submit one paid cover using an owned audio ID, lyrics and style."""
    with AceDataCloud(
        api_token=os.environ["ACEDATACLOUD_API_TOKEN"], max_retries=0
    ) as client:
        return _task_id(
            client.acemusic.generate(
                action="cover",
                model="acemusic-v1.1",
                audio_id=audio_id,
                lyric=lyric,
                style=style,
                title=title,
                async_=True,
            )
        )


@tool("acemusic_mashup_audio")
def acemusic_mashup_audio(
    first_audio_id: str,
    second_audio_id: str,
    lyric: str,
    style: str,
    title: str | None = None,
) -> dict[str, Any]:
    """Blend two distinct owned audio IDs in one paid mashup task."""
    if first_audio_id == second_audio_id:
        raise ValueError("Choose two distinct owned audio IDs.")
    with AceDataCloud(
        api_token=os.environ["ACEDATACLOUD_API_TOKEN"], max_retries=0
    ) as client:
        return _task_id(
            client.acemusic.generate(
                action="mashup",
                model="acemusic-v1.1",
                mashup_audio_ids=[first_audio_id, second_audio_id],
                lyric=lyric,
                style=style,
                title=title,
                async_=True,
            )
        )


@tool("acemusic_generate_lyrics")
def acemusic_generate_lyrics(prompt: str, style: str | None = None) -> dict[str, Any]:
    """Request paid lyrics. Return the draft or the original task ID when pending."""
    with AceDataCloud(
        api_token=os.environ["ACEDATACLOUD_API_TOKEN"], max_retries=0
    ) as client:
        return client.acemusic.lyrics(prompt=prompt, style=style)


@tool("acemusic_get_task")
def acemusic_get_task(task_id: str) -> dict[str, Any]:
    """Read the original ACE Music task. Check group status and response before using audio URLs."""
    with AceDataCloud(
        api_token=os.environ["ACEDATACLOUD_API_TOKEN"], max_retries=0
    ) as client:
        return client.acemusic.tasks(action="retrieve", id=task_id)


tools = [
    acemusic_generate_music,
    acemusic_generate_custom_music,
    acemusic_upload_audio,
    acemusic_cover_audio,
    acemusic_mashup_audio,
    acemusic_generate_lyrics,
    acemusic_get_task,
]
