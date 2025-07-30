import os

import pytest

from ffmpeg_converter.audio import AudioConverter

# 测试文件路径
TEST_DIR = os.path.dirname(os.path.abspath(__file__))
SAMPLE_AUDIO = os.path.join(TEST_DIR, "samples", "test_audio.mp3")

# 创建测试所需的目录
os.makedirs(os.path.join(TEST_DIR, "samples"), exist_ok=True)
os.makedirs(os.path.join(TEST_DIR, "output"), exist_ok=True)


@pytest.fixture(scope="session")
def audio_converter() -> AudioConverter:
    return AudioConverter()


@pytest.mark.asyncio
@pytest.mark.parametrize("fmt", ["mp3", "wav"])
async def test_audio_format_conversion(audio_converter: AudioConverter, fmt):
    """测试主要音频格式转换"""
    output_file = os.path.join(TEST_DIR, "output", f"test_output.{fmt}")
    result = await audio_converter.convert(
        input_file=SAMPLE_AUDIO, output_file=output_file, output_format=fmt
    )
    assert result is True
    assert os.path.exists(output_file)


@pytest.mark.asyncio
@pytest.mark.parametrize("rate", [44100, 48000])
async def test_audio_sample_rate_conversion(audio_converter: AudioConverter, rate):
    """测试关键采样率转换"""
    output_file = os.path.join(TEST_DIR, "output", f"test_output_{rate}.wav")
    result = await audio_converter.convert(
        input_file=SAMPLE_AUDIO,
        output_file=output_file,
        output_format="wav",
        sample_rate=rate,
    )
    assert result is True
    assert os.path.exists(output_file)


@pytest.mark.asyncio
async def test_audio_basic_conversion(audio_converter: AudioConverter):
    """测试基本音频转换功能"""
    output_file = os.path.join(TEST_DIR, "output", "test_output.wav")

    progress_data = []

    def progress_callback(progress, time_remaining, info):
        progress_data.append(
            {"progress": progress, "time_remaining": time_remaining, "info": info}
        )

    result = await audio_converter.convert(
        input_file=SAMPLE_AUDIO,
        output_file=output_file,
        output_format="wav",
        sample_rate=44100,
        channels=2,
        progress_callback=progress_callback,
    )

    assert result is True
    assert os.path.exists(output_file)
    assert len(progress_data) > 0
    assert progress_data[-1]["progress"] == 100.0


@pytest.mark.asyncio
async def test_audio_conversion_errors(audio_converter: AudioConverter):
    """测试音频转换错误处理"""
    # 测试不存在的输入文件
    result = await audio_converter.convert(
        input_file="nonexistent.mp3", output_file="output.wav", output_format="wav"
    )
    assert result is False


@pytest.mark.asyncio
@pytest.mark.parametrize("channels", [1, 2])
async def test_audio_channels_conversion(audio_converter: AudioConverter, channels):
    """测试音频声道数转换"""
    output_file = os.path.join(TEST_DIR, "output", f"test_output_{channels}ch.wav")
    result = await audio_converter.convert(
        input_file=SAMPLE_AUDIO,
        output_file=output_file,
        output_format="wav",
        channels=channels,
    )
    assert result is True
    assert os.path.exists(output_file)


# @pytest.mark.asyncio
# async def test_audio_conversion_interrupt(audio_converter: AudioConverter):
#     """测试音频转换中断处理"""
#     output_file = os.path.join(TEST_DIR, "output", "test_output_interrupt.wav")

#     def progress_callback(progress, time_remaining, info):
#         if progress > 5:  # 当进度超过5%时中断
#             if audio_converter.process and audio_converter.process.returncode is None:
#                 audio_converter.process.terminate()

#     result = await audio_converter.convert(
#         input_file=SAMPLE_AUDIO,
#         output_file=output_file,
#         output_format="wav",
#         progress_callback=progress_callback,
#         sample_rate=44100,
#         channels=2,
#     )
#     assert result is False
