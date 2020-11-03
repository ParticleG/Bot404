# Have to run under python3.8 with latest requirements.
import asyncio
from ffmpeg import FFmpeg  # python-ffmpeg==1.0.11
from ffprobe import FFProbe  # ffprobe-python==1.0.3

MINIMUM_ONE_FRAME = 0.01667


def if_end(current_duration, duration_seconds):
    return abs(current_duration - duration_seconds) >= MINIMUM_ONE_FRAME


async def run(_video_filename, _size, _index, _current_duration):
    video_name = _video_filename[:-4]
    ffmpegProcess = FFmpeg().input(_video_filename, {
        'ss': _current_duration
    }).option('-y').output(f'{video_name}_{_index}.mp4', {
        'fs': _size,
        'c': 'copy'
    })

    @ffmpegProcess.on('terminated')
    def on_terminated():
        print('Terminated!')

    @ffmpegProcess.on('error')
    def on_error(code):
        print('Error:', code)

    await ffmpegProcess.execute()


def split_video(video_filename, size, index, current_duration):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(
        run(_video_filename=video_filename,
            _size=size,
            _index=index,
            _current_duration=current_duration))
    loop.close()


def execute_split(video):
    # LOAD
    video_metadata = FFProbe(video)
    video_name = video[:-4]
    # INIT
    duration_seconds = 0
    current_duration = 0
    index = 1
    # GET VIDEO STREAM
    for stream in video_metadata.streams:
        if stream.is_video():
            print(f'[Origin Video] "{video}" last for {stream.duration_seconds()} seconds.')
            duration_seconds = stream.duration_seconds()
    # SPLIT
    while abs(current_duration - duration_seconds) >= 0.01667:
        split_video(video, '1G', index, current_duration)
        nextMetadata = FFProbe(f'{video_name}_{index}.mp4')
        for nextStream in nextMetadata.streams:
            if nextStream.is_video():
                print(
                    f'Clip{index} last for {nextStream.duration_seconds()} seconds.'
                )
                current_duration += nextStream.duration_seconds()
        index += 1
    # COUNT
    return index
