import itertools
import os
import cv2

from video_manager import VideoManager

get_your_config_from_env_var = os.environ.get('CONFIG_NAME', 'default_value_if_not_set')

if __name__ == '__main__':
    # vidManager = VideoManager(camNames='RTSP'.split(','),
    #                           streams='rtsp://wowzaec2demo.streamlock.net/vod/mp4:BigBuckBunny_115k.mov'.split(','),
    #                           isVideoFile=False, queueSize=2, writeDir='./output',
    #                           reconnectThreshold=1, max_height=1080, method='cv2')

    vidManager = VideoManager(camNames=['File', 'RTSP'],
                              streams=['/data/datasets/drone/macritchie-reservoir.mp4',
                                       'rtsp://wowzaec2demo.streamlock.net/vod/mp4:BigBuckBunny_115k.mov'],
                              isVideoFile=True, queueSize=2, writeDir='./output',
                              reconnectThreshold=1, max_height=1080, method='cv2')

    vidManager.start()
    print(f'Sources: {vidManager.videos} Details: {vidManager.getAllInfo()}')

    for frame_count in itertools.count():
        statuses, frames = vidManager.read()  # frames is list of arrays from 0 - 255, dtype uint8
        for i, video_stream_information in enumerate(vidManager.videos):
            if len(frames[i]) != 0:
                cv2.imshow(video_stream_information['camName'], frames[i])
        if cv2.waitKey(1) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break

    vidManager.stop()