import logging
import time
from collections.abc import Callable
from datetime import timedelta
from typing import Any

from .base import BaseConverter


class VideoConverter(BaseConverter):
    def _parse_progress(self, line: str, duration: float) -> dict[str, Any] | None:
        """解析FFmpeg进度输出"""
        progress_info: dict[str, Any] = {}
        try:
            for item in line.strip().split():
                if "=" in item:
                    key, value = item.split("=", 1)
                    progress_info[key] = value

            if "out_time_ms" in progress_info:
                time_ms = int(progress_info["out_time_ms"])
                progress = (time_ms / 1000000 / duration) * 100
                progress_info["progress"] = progress

                if "frame" in progress_info:
                    progress_info["current_frame"] = int(progress_info["frame"])

                if "speed" in progress_info:
                    progress_info["conversion_speed"] = progress_info["speed"]

                return progress_info

        except Exception as e:
            logging.error("Error parsing progress: %s", str(e))
            pass

        return None

    def _estimate_time_remaining(self, progress: float, duration: float) -> str:
        """根据当前进度估算剩余时间"""
        if progress <= 0:
            return "计算中..."

        elapsed_time = time.time() - (self.start_time or time.time())
        total_time = (elapsed_time * 100) / progress
        remaining_seconds = total_time - elapsed_time

        remaining_time = timedelta(seconds=int(remaining_seconds))
        return str(remaining_time)

    async def convert(
        self,
        input_file: str,
        output_file: str,
        output_format: str,
        video_codec: str | None = None,
        video_bitrate: str | None = None,
        resolution: str | None = None,
        fps: int | None = None,
        audio_codec: str | None = None,
        audio_bitrate: str | None = None,
        preset: str = "medium",
        crf: int | None = None,
        progress_callback: Callable[[float, str, dict[str, Any]], None] | None = None,
        **kwargs,
    ) -> bool:
        """使用FFmpeg转换视频文件到指定格式，并提供进度监控

        Args:
            input_file (str): 输入视频文件路径
            output_file (str): 输出视频文件路径
            output_format (str): 目标输出格式（如'mp4', 'mkv'等）
            video_codec (str, optional): 视频编码器（如'h264', 'h265'等）
            video_bitrate (str, optional): 视频比特率（如'5M'）
            resolution (str, optional): 视频分辨率（如'1920x1080'）
            fps (int, optional): 视频帧率
            audio_codec (str, optional): 音频编码器（如'aac'）
            audio_bitrate (str, optional): 音频比特率（如'192k'）
            preset (str, optional): 编码器预设值（如'fast', 'medium'等）。默认为'medium'
            crf (int, optional): 恒定速率因子，控制视频质量（0-51，值越小质量越好）
            progress_callback (callable, optional): 进度回调函数，接收进度百分比、
                剩余时间和详细信息
            **kwargs: 其他可选参数

        Returns:
            bool: 转换成功返回True，否则返回False
        """
        if not self._check_input_file(input_file):
            return False

        probe = await self._get_file_info(input_file)
        duration = float(probe["format"]["duration"])

        command = ["ffmpeg", "-i", input_file]

        if video_codec:
            command.extend(["-c:v", video_codec])

        if video_bitrate:
            command.extend(["-b:v", video_bitrate])

        if resolution:
            command.extend(["-s", resolution])

        if fps:
            command.extend(["-r", str(fps)])

        if audio_codec:
            command.extend(["-c:a", audio_codec])

        if audio_bitrate:
            command.extend(["-b:a", audio_bitrate])

        if video_codec in ["h264", "h265", "hevc"]:
            command.extend(["-preset", preset])
            if crf is not None:
                command.extend(["-crf", str(crf)])

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
