import os

import pytest

from ffmpeg_converter.video import VideoConverter

# 测试文件路径
TEST_DIR = os.path.dirname(os.path.abspath(__file__))
SAMPLE_VIDEO = os.path.join(TEST_DIR, "samples", "test_video.mov")

# 创建测试所需的目录
os.makedirs(os.path.join(TEST_DIR, "samples"), exist_ok=True)
os.makedirs(os.path.join(TEST_DIR, "output"), exist_ok=True)


@pytest.fixture(scope="session")
def video_converter() -> VideoConverter:
    return VideoConverter()


@pytest.mark.asyncio
@pytest.mark.parametrize("fmt", ["mp4", "mkv"])
async def test_video_format_conversion(video_converter: VideoConverter, fmt):
    """测试主要视频格式转换"""
    output_file = os.path.join(TEST_DIR, "output", f"test_output.{fmt}")
    result = await video_converter.convert(
        input_file=SAMPLE_VIDEO, output_file=output_file, output_format=fmt
    )
    assert result is True
    assert os.path.exists(output_file)


@pytest.mark.asyncio
@pytest.mark.parametrize("res", ["1280x720", "1920x1080"])
async def test_video_resolution_conversion(video_converter: VideoConverter, res):
    """测试主要分辨率转换"""
    output_file = os.path.join(TEST_DIR, "output", f"test_output_{res}.mp4")
    result = await video_converter.convert(
        input_file=SAMPLE_VIDEO,
        output_file=output_file,
        output_format="mp4",
        resolution=res,
    )
    assert result is True
    assert os.path.exists(output_file)


@pytest.mark.asyncio
async def test_video_basic_conversion(video_converter: VideoConverter):
    """测试基本视频转换功能"""
    output_file = os.path.join(TEST_DIR, "output", "test_output.mkv")

    progress_data = []

    def progress_callback(progress, time_remaining, info):
        progress_data.append(
            {"progress": progress, "time_remaining": time_remaining, "info": info}
        )

    result = await video_converter.convert(
        input_file=SAMPLE_VIDEO,
        output_file=output_file,
        output_format="mkv",
        video_codec="h264",
        video_bitrate="5M",
        resolution="1280x720",
        fps=30,
        audio_codec="aac",
        audio_bitrate="192k",
        preset="fast",
        progress_callback=progress_callback,
    )

    assert result is True
    assert os.path.exists(output_file)
    assert len(progress_data) > 0
    assert progress_data[-1]["progress"] == 100.0


@pytest.mark.asyncio
async def test_video_conversion_errors(video_converter: VideoConverter):
    """测试视频转换错误处理"""
    # 测试不存在的输入文件
    result = await video_converter.convert(
        input_file="nonexistent.mp4", output_file="output.mkv", output_format="mkv"
    )
    assert result is False


@pytest.mark.asyncio
async def test_video_audio_params(video_converter: VideoConverter):
    """测试视频音频参数设置"""
    output_file = os.path.join(TEST_DIR, "output", "test_output_audio.mp4")
    result = await video_converter.convert(
        input_file=SAMPLE_VIDEO,
        output_file=output_file,
        output_format="mp4",
        audio_codec="aac",
        audio_bitrate="192k",
    )
    assert result is True
    assert os.path.exists(output_file)


# @pytest.mark.asyncio
# async def test_video_conversion_interrupt(video_converter: VideoConverter):
#     """测试视频转换中断处理"""
#     output_file = os.path.join(TEST_DIR, "output", "test_output_interrupt.mp4")

#     def progress_callback(progress, time_remaining, info):
#         if progress > 50:  # 当进度超过50%时中断
#             if video_converter.process and video_converter.process.returncode is None:
#                 video_converter.process.terminate()

#     result = await video_converter.convert(
#         input_file=SAMPLE_VIDEO,
#         output_file=output_file,
#         output_format="mp4",
#         progress_callback=progress_callback,
#     )
#     assert result is False
