import asyncio
from ffmpeg import FFmpeg  # python-ffmpeg==1.0.11
from ffprobe import FFProbe  # ffprobe-python==1.0.3


async def run(_video_filename, _size, _index, _current_duration):
    ffmpegProcess = FFmpeg().input(_video_filename, {
        'ss': _current_duration
    }).option('-y').output(f'test_{_index}.mp4', {
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


if __name__ == '__main__':
    metadata = FFProbe('test.mp4')
    duration_seconds = 0
    current_duration = 0
    index = 1

    for stream in metadata.streams:
        if stream.is_video():
            print(f'Video last for {stream.duration_seconds()} seconds.')
            duration_seconds = stream.duration_seconds()
    # 60fps: 1fps = 0.01667 小于一帧就算了.jpg
    while abs(current_duration - duration_seconds) >= 0.01667:
        split_video('test.mp4', '20M', index, current_duration)
        nextMetadata = FFProbe(f'test_{index}.mp4')
        for nextStream in nextMetadata.streams:
            if nextStream.is_video():
                print(
                    f'CLip {index} last for {nextStream.duration_seconds()} seconds.'
                )
                current_duration += nextStream.duration_seconds()
        index += 1
