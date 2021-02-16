import imageio
import win_unicode_console
win_unicode_console.enable()
import os
from moviepy.video.io.VideoFileClip  import VideoFileClip
from moviepy.video.compositing.concatenate import concatenate_videoclips
from moviepy.editor import VideoFileClip, clips_array, vfx, CompositeVideoClip
import glob

if __name__=="__main__":
    output_folder = './output'
    files = glob.glob('**/*.mp4', recursive=True)
    video_list = []
    start_sec = 0
    for file in files:
        try:
            source = file
            target = os.path.join(output_folder, source) #拼接文件名路径
            if not os.path.exists(os.path.dirname(target)): #os.path.isdir(os.path.join(root, output)) os.path.join(root, output)
                os.makedirs(os.path.dirname(target))
            video = VideoFileClip(source)
            total_seconds = video.duration
            start_time = 0
            stop_time = total_seconds - 3
            video = video.subclip(int(start_time), int(stop_time))#执行剪切操作
            video.to_videofile(target, fps=20, remove_temp=True)#输出文件
            # os.remove(source)
            print(video.size[0],video.size[1])
            print(video.size[0]/1300,video.size[1]/720)
            rate_x = video.size[0]/1300
            rate_y = video.size[1]/720
            rate_max = max(rate_x, rate_y)
            if rate_max > 1:
                rate_max = 1/rate_max
            else:
                rate_max = 1
            video = video.set_start(start_sec).set_pos("center").resize(rate_max)
            print('-=====>', rate_max)
            start_sec = start_sec + video.duration
            video_list.append(video)#将加载完后的视频加入列表
        except Exception as e:
            print('have error:',e)
        finally:
            print(file, 'done')
    final_clip = CompositeVideoClip(video_list, size=(1300, 720))
    final_clip.to_videofile(os.path.join(output_folder, 'combined.mp4'), fps=20, remove_temp=True)
    # final_clip = concatenate_videoclips(video_list)#进行视频合并
    # final_clip.write_videofile(os.path.join(output_folder, 'combined.mp4'), fps=20, remove_temp=True)
    # final_clip.to_videofile(os.path.join(output_folder, 'combined.mp4'), fps=20, remove_temp=True)#将合并后的视频输出