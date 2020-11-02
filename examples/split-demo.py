import asyncio
from ffmpeg import FFmpeg  # python-ffmpeg==1.0.11
from ffprobe import FFProbe  # ffprobe-python==1.0.3


async def run(_index, _current_duration):
    ffmpegProcess = FFmpeg().input(
        'test.mp4',
        {'ss': _current_duration}
    ).option(
        '-y'
    ).output(
        f'test_{_index}.mp4',
        {'fs': '10M', 'c': 'copy'}
    )

    # @ffmpegProcess.on('start')
    # def on_start(arguments):
    #     print('Arguments:', arguments)

    # @ffmpegProcess.on('stderr')
    # def on_stderr(line):
    #     print('stderr:', line)

    # @ffmpegProcess.on('progress')
    # def on_progress(progress):
    #     print('progress:', progress)

    # @ffmpegProcess.on('completed')
    # def on_completed():
    #     print('Completed!')

    @ffmpegProcess.on('terminated')
    def on_terminated():
        print('Terminated!')

    @ffmpegProcess.on('error')
    def on_error(code):
        print('Error:', code)

    await ffmpegProcess.execute()


def split_video(_index, _current_duration):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(run(_index, _current_duration))
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

    while current_duration < duration_seconds:
        split_video(index, current_duration)
        nextMetadata = FFProbe(f'test_{index}.mp4')
        for nextStream in nextMetadata.streams:
            if nextStream.is_video():
                print(f'CLip {index} last for {nextStream.duration_seconds()} seconds.')
                current_duration += nextStream.duration_seconds()
        index += 1
