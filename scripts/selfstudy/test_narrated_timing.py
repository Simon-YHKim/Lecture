"""The audio/container duration must not hide a shortened video track."""
import json
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

from render_narrated import concat_text, VIDEO_FILTER, validate_video_timing


class NarratedTimingTests(unittest.TestCase):
    def test_rejects_short_video_even_when_container_and_audio_are_complete(self):
        probe={'format':{'duration':'34.233333'},'streams':[
            {'codec_type':'video','duration':'24.066667','nb_frames':'722','start_time':'0'},
            {'codec_type':'audio','duration':'34.233333','start_time':'0'}]}
        with self.assertRaisesRegex(ValueError,'Video track'):
            validate_video_timing(probe,1027/30)
        probe['streams'][0].update(duration='34.233333',nb_frames='1027')
        self.assertEqual(validate_video_timing(probe,1027/30)['frames'],1027)

    @unittest.skipUnless(shutil.which('ffmpeg') and shutil.which('ffprobe'),'FFmpeg is optional in source CI')
    def test_sparse_last_still_reaches_the_last_scheduled_frame(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp)
            # PPM avoids a graphics dependency and makes the last frame distinct.
            for color,rgb in [('red',(255,0,0)),('blue',(0,0,255))]:
                (root/(color+'.ppm')).write_bytes(b'P6\n32 18\n255\n'+bytes(rgb)*32*18)
            shots=[{'imagePath':str(root/'red.ppm'),'duration':18.7},
                   {'imagePath':str(root/'blue.ppm'),'duration':15.533333333}]
            concat=root/'images.ffconcat';concat.write_text(concat_text(shots))
            video=root/'test.mp4'
            subprocess.run(['ffmpeg','-nostdin','-v','error','-f','concat','-safe','0','-i',str(concat),
                '-f','lavfi','-i','anullsrc=r=24000:cl=mono','-vf',VIDEO_FILTER,
                '-r','30','-fps_mode','cfr','-t','34.233333333','-c:v','libx264','-threads','1',
                '-preset','ultrafast','-pix_fmt','yuv420p','-c:a','aac',str(video)],check=True)
            probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams',
                '-show_format','-of','json',str(video)]))
            validate_video_timing(probe,1027/30)
            last=subprocess.check_output(['ffmpeg','-nostdin','-v','error','-ss',str(1026/30),
                '-i',str(video),'-frames:v','1','-pix_fmt','rgb24','-f','rawvideo','-'])
            self.assertEqual(len(last),32*18*3)
            self.assertGreater(last[2],240)
            self.assertLess(last[0],15)


if __name__=='__main__':unittest.main()
