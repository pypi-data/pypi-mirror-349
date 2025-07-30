# FFmpeg Converter

基于 FFmpeg 的音视频格式转换工具，支持异步操作和进度监控。

[![CI Status](https://github.com/ospoon/ffmpeg-converter/workflows/CI/badge.svg)](https://github.com/ospoon/ffmpeg-converter/actions)
[![Coverage](https://codecov.io/gh/ospoon/ffmpeg-converter/branch/main/graph/badge.svg)](https://codecov.io/gh/ospoon/ffmpeg-converter)
[![Python Version](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![PyPI version](https://badge.fury.io/py/ffmpeg-converter.svg)](https://badge.fury.io/py/ffmpeg-converter)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 特性

- 支持异步操作
- 实时进度监控
- 支持音频和视频格式转换
- 丰富的转换参数配置
- 类型提示支持

## 安装

1. 安装 FFmpeg（必需）

   ```bash
   # Windows (使用 chocolatey)
   choco install ffmpeg

   # Linux (Ubuntu/Debian)
   sudo apt-get update && sudo apt-get install ffmpeg
   ```

2. 安装 ffmpeg-converter
   
   ```bash
   pip install ffmpeg-converter
    ```

## 快速开始
### 音频转换

```python
import asyncio
from ffmpeg_converter import AudioConverter

async def main():
    converter = AudioConverter()
    
    def progress_callback(progress, time_remaining, info):
        print(f"进度: {progress:.2f}%, 剩余时间: {time_remaining}")
    
    success = await converter.convert(
        input_file="input.mp3",
        output_file="output",
        output_format="wav",
        sample_rate=44100,
        channels=2,
        progress_callback=progress_callback,
    )
    
    if success:
        print("转换完成")
    else:
        print("转换失败")

if __name__ == "__main__":
    asyncio.run(main())
```

### 视频转换

```python
import asyncio
from ffmpeg_converter import VideoConverter

async def main():
    converter = VideoConverter()
    
    def progress_callback(progress, time_remaining, info):
        print(f"进度: {progress:.2f}%, 剩余时间: {time_remaining}")
        if "conversion_speed" in info:
            print(f"转换速度: {info['conversion_speed']}")
    
    success = await converter.convert(
        input_file="input.mp4",
        output_file="output",
        output_format="mkv",
        video_codec="h264",
        video_bitrate="5M",
        resolution="1920x1080",
        fps=30,
        audio_codec="aac",
        audio_bitrate="192k",
        preset="fast",
        crf=23,
        progress_callback=progress_callback,
    )
    
    if success:
        print("转换完成")
    else:
        print("转换失败")

if __name__ == "__main__":
    asyncio.run(main())
```

## 开发
1. 克隆仓库
   
   ```bash
   git clone https://github.com/ospoon/ffmpeg-converter.git
   cd ffmpeg-converter
   ```

2. 安装开发依赖
   
   ```bash
   pip install uv
   uv venv
   uv sync
   ```

3. 运行测试
   
   ```bash
   uv run pytest
   ```

## 贡献指南
欢迎贡献！请遵循以下步骤：

1. Fork 本仓库
2. 创建功能分支 ( git checkout -b feature/amazing-feature )
3. 提交更改 ( git commit -m 'Add amazing feature' )
4. 推送到分支 ( git push origin feature/amazing-feature )
5. 开启 Pull Request
## 许可证
本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件