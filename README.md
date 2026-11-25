# ACE Music for CrewAI

Install from a source checkout with `pip install .` and set `ACEDATACLOUD_API_TOKEN` to your private [application key](https://platform.acedata.cloud/console/applications).

```python
from acemusic_crewai import tools

# Supply tools to a CrewAI Agent with Agent(..., tools=tools).
```

The package exposes native tools for ideas, custom lyrics and titles, reference MP3 import, cover, two-reference mashup, lyrics, and task retrieval. Each paid operation is attempted once. Save the task ID and call `acemusic_get_task` with that ID until the group reaches a terminal state. Use completed tracks from the returned task. [API contract](https://github.com/AceDataCloud/ACEMusicAPI) · [中文](readme/README_zh_Hans.md)

## Distribution

Publishing a reviewed GitHub release with a matching `vX.Y.Z` tag builds and attaches the wheel and source archive after the offline tests pass. The package can also be built from the checkout.
