import time
from collections.abc import Callable
from datetime import timedelta
from typing import Any

from .base import BaseConverter


class AudioConverter(BaseConverter):
    def _parse_progress(self, line: str, duration: float) -> dict[str, Any] | None:
        """解析FFmpeg进度输出"""
        if "time=" in line:
            try:
                time_str = line.split("time=")[1].split()[0]
                if ":" in time_str:
                    h, m, s = time_str.split(":")
                    time_seconds = float(h) * 3600 + float(m) * 60 + float(s)
                else:
                    time_seconds = float(time_str)
                progress = (time_seconds / duration) * 100
                return {
                    "progress": progress,
                    "time": time_seconds,
                    "duration": duration,
                }
            except (ValueError, IndexError):
                return None
        return None

    def _estimate_time_remaining(self, progress: float, duration: float) -> str:
        """根据当前进度估算剩余时间"""
        if progress <= 0:
            return "计算中..."

        elapsed_time = time.time() - (
            self.start_time if self.start_time is not None else time.time()
        )
        total_time = (elapsed_time * 100) / progress
        remaining_seconds = total_time - elapsed_time

        remaining_time = timedelta(seconds=int(remaining_seconds))
        return str(remaining_time)

    async def convert(
        self,
        input_file: str,
        output_file: str,
        output_format: str,
        sample_rate: int | None = None,
        channels: int | None = None,
        progress_callback: Callable[[float, str, dict[str, Any]], None] | None = None,
        **kwargs,
    ) -> bool:
        """使用FFmpeg将音频文件转换为指定格式，并提供进度监控

        Args:
            input_file (str): 输入音频文件路径
            output_file (str): 输出音频文件路径
            output_format (str): 目标输出格式（如'mp3', 'wav', 'ogg'等）
            sample_rate (int, optional): 采样率（Hz，如44100）
            channels (int, optional): 音频通道数（如2表示立体声）
            progress_callback (callable, optional): 进度回调函数，接收进度百分比和
            剩余时间
            **kwargs: 其他可选参数

        Returns:
            bool: 转换成功返回True，否则返回False
        """
        if not self._check_input_file(input_file):
            return False

        probe = await self._get_file_info(input_file)
        duration = float(probe["format"]["duration"])

        command = ["ffmpeg", "-i", input_file]

        if sample_rate:
            command.extend(["-ar", str(sample_rate)])

        if channels:
            command.extend(["-ac", str(channels)])

        command.extend(["-progress", "pipe:1"])
        output_file = self._ensure_output_format(output_file, output_format)
        command.extend(["-y", output_file])

        success = await self._execute_ffmpeg_command(
            command, duration, self._parse_progress, progress_callback
        )

        if success and progress_callback:
            progress_callback(100, "完成", {"status": "finished"})
            print(f"\nSuccessfully converted {input_file} to {output_file}")

        return success
