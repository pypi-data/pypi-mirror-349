# mcp-video2text

Convert online video to text, read it quickly

![screenshoot](https://raw.githubusercontent.com/yanyaoer/mcp-video2text/refs/heads/main/screenshoot/example.png)

## Usage

```bash
## require
$ curl -LsSf https://astral.sh/uv/install.sh | sh  # install uv package manager
$ brew install ffmpeg  # or `sudo apt install ffmpeg` for linux

## install
$ uv pip install mcp-video2text[mlx]  # recommend with mlx for silicon machine
$ uv pip install mcp-video2text[cpp]  
```

for mcp client, pass `uv run mpc-video2text` to `command` field.

```json
{
  "mcpServers": {
    "mcp-video2text": {
      "command": "uv",
      "args": ["run", "mcp-video2text"],
    }
  }
}
```

The first run will download the Whisper model and may take a few minutes.  
It's recommended to update the timeout settings in your client.

or your can custom your own client, view example `test_mcp_client.py`

```python
import asyncio
import os

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def client():
  server_params = StdioServerParameters(
    command="uv", args=["run", "mcp-video2text"], env=os.environ
  )
  async with stdio_client(server_params) as (read, write):
    async with ClientSession(read, write) as session:
      await session.initialize()
      print(await session.list_tools())
      result = await session.call_tool(
        "video2text", {"url": "https://www.bilibili.com/video/BV1gdERzuEYB/"}
      )
      print(result.content[0].text)


if __name__ == "__main__":
  asyncio.run(client())
```

## Thanks
- https://github.com/yt-dlp/yt-dlp
- https://github.com/k2-fsa/sherpa-onnx
- https://github.com/ml-explore/mlx-examples/tree/main/whisper
- https://github.com/ggerganov/whisper.cpp
- https://github.com/absadiki/pywhispercpp
- https://github.com/pydantic/pydantic-ai
- https://github.com/yetone/avante.nvim
