import asyncio
import json
import os
import time
from abc import ABC, abstractmethod
from typing import Any


class BaseConverter(ABC):
    def __init__(self):
        self.process = None
        self.start_time = None

    async def _get_file_info(self, file_path: str) -> dict:
        """使用ffprobe获取媒体文件信息"""
        try:
            probe = await asyncio.create_subprocess_exec(
                "ffprobe",
                "-v",
                "quiet",
                "-print_format",
                "json",
                "-show_format",
                "-show_streams",
                file_path,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
            stdout, _ = await probe.communicate()
            return json.loads(stdout.decode())
        except Exception as e:
            print(f"Error probing file: {str(e)}")
            return {"format": {"duration": "0"}}

    async def _execute_ffmpeg_command(
        self,
        command: list,
        duration: float,
        parse_progress_func,
        progress_callback=None,
    ) -> bool:
        """执行FFmpeg命令并监控进度"""
        try:
            self.start_time = time.time()
            self.process = await asyncio.create_subprocess_exec(
                *command, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
            )

            while True:
                if not self.process or self.process.returncode is not None:
                    break

                if self.process.stdout:
                    try:
                        line = await self.process.stdout.readline()
                        if not line:
                            break

                        progress_info = parse_progress_func(line.decode(), duration)
                        if progress_info and progress_callback:
                            if isinstance(progress_info, dict):
                                progress = progress_info["progress"]
                                time_remaining = self._estimate_time_remaining(
                                    progress, duration
                                )
                                progress_callback(
                                    progress, time_remaining, progress_info
                                )
                            else:
                                time_remaining = self._estimate_time_remaining(
                                    progress_info, duration
                                )
                                progress_callback(progress_info, time_remaining)
                    except asyncio.CancelledError:
                        if self.process:
                            self.process.terminate()
                        raise

            if self.process:
                await self.process.wait()
                if self.process.returncode != 0:
                    error = (
                        await self.process.stderr.read() if self.process.stderr else b""
                    )
                    print(f"Error executing command: {error.decode()}")
                    return False

            return True

        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return False
        finally:
            self.process = None

    def _check_input_file(self, input_file: str) -> bool:
        """检查输入文件是否存在"""
        if not os.path.exists(input_file):
            print(f"Error: Input file '{input_file}' does not exist")
            return False
        return True

    def _ensure_output_format(self, output_file: str, output_format: str) -> str:
        """确保输出文件具有正确的扩展名"""
        if not output_file.endswith(f".{output_format}"):
            output_file = f"{output_file}.{output_format}"
        return output_file

    @abstractmethod
    def _parse_progress(self, line: str, duration: float) -> Any:
        """解析FFmpeg进度输出的抽象方法"""
        pass

    @abstractmethod
    def _estimate_time_remaining(self, progress: float, duration: float) -> str:
        """根据当前进度估算剩余时间的抽象方法"""
        pass

    @abstractmethod
    async def convert(
        self, input_file: str, output_file: str, output_format: str, **kwargs
    ) -> bool:
        """转换媒体文件的抽象方法"""
        pass
