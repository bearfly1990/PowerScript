import imageio
import win_unicode_console
win_unicode_console.enable()
import os
from moviepy.video.io.VideoFileClip  import VideoFileClip
from moviepy.video.compositing.concatenate import concatenate_videoclips
from moviepy.editor import VideoFileClip, clips_array, vfx, CompositeVideoClip
import glob
from concurrent.futures import ThreadPoolExecutor, wait, ALL_COMPLETED, FIRST_COMPLETED
from datetime import datetime
"""
author: bearfly1990
create at: 02/01/2021
description:
    Utils for send email
Change log:
Date          Author      Version    Description
02/17/2021    bearfly1990 1.0.1      update combine video hight/width resize logic to adapt all videos.
02/21/2021    bearfly1990 1.0.2      Get max hight/max width from all the input videos, not hard code
                                     
"""
class TiktokUtil(object):
    output_folder = './output'
    max_workers = 6
   
    def __init__(self, remove_watermark=True, input_folder='', output_name='combined.mp4'):
        self.remove_watermark = remove_watermark
        self.output_name = output_name
        self.input_folder=input_folder
        self.video_list = []
        self.max_x_list = []
        self.max_y_list = []

    def convert_video(self, file):
        try:
            target = os.path.join(self.output_folder, file) # 拼接文件名路径
            try:
                if not os.path.exists(os.path.dirname(target)): # os.path.isdir(os.path.join(root, output)) os.path.join(root, output)
                    os.makedirs(os.path.dirname(target))
            except Exception as e:
                print('have error when create subfolder:',e)
            video = VideoFileClip(file)
            if self.remove_watermark:
                total_seconds = video.duration
                start_time = 0
                stop_time = total_seconds - 3
                video = video.subclip(int(start_time), int(stop_time))# 执行剪切操作
            # video.to_videofile(target, fps=20, remove_temp=True)# 输出文件
            # os.remove(source)
            self.max_x_list.append(video.size[0])
            self.max_y_list.append(video.size[1])
            self.video_list.append(video)# 将加载完后的视频加入列表
        except Exception as e:
            print('have error:',e)
        finally:
            print(file, 'done')

    def combine_videos(self):
        self.max_x = max(self.max_x_list)
        self.max_y = max(self.max_y_list)
        start_sec = 0
        for i, video in enumerate(self.video_list):
            # print(video.size[0],video.size[1])
            # print(video.size[0]/1300,video.size[1]/720)
            rate_x = video.size[0]/self.max_x
            rate_y = video.size[1]/self.max_y
            rate_max = max(rate_x, rate_y)
            if rate_max > 1:
                rate_max = 1/rate_max
            else:
                rate_max = 1
            self.video_list[i] = video.set_start(start_sec).set_pos("center").resize(rate_max)
            start_sec = start_sec + video.duration
        print(self.max_x, self.max_y)
        final_clip = CompositeVideoClip(self.video_list, size=(self.max_x, self.max_y))   
        final_clip.to_videofile(os.path.join(self.output_folder, self.input_folder, self.output_name), fps=20, remove_temp=True)
        final_clip.close()
        # final_clip = concatenate_videoclips(VIDEO_LIST)#进行视频合并
        # final_clip.write_videofile(os.path.join(OUTPUT_FOLDER, 'combined.mp4'), fps=20, remove_temp=True)
        # # final_clip.to_videofile(os.path.join(output_folder, 'combined.mp4'), fps=20, remove_temp=True)#将合并后的视频输出

    def preprocess_videos(self):
        files = glob.glob(f'{self.input_folder}/*.mp4', recursive=True)
        # print(files)
        # print(len(self.video_list))
        # exit()
        executor = ThreadPoolExecutor(max_workers=self.max_workers)
        all_task = [executor.submit(self.convert_video, (file)) for file in files]
        wait(all_task, return_when=ALL_COMPLETED)
        
if __name__=="__main__":
    start_time = datetime.now()
    
    files = glob.glob('**/*.mp4', recursive=True)
    if not files:
        print('no files found')
        exit(0)
    dirs = list(set(['.' if os.path.dirname(file)=='' else os.path.dirname(file) for file in files]))
    for dir in dirs:
        tiktok_util = TiktokUtil(input_folder=dir)
        tiktok_util.preprocess_videos()
        tiktok_util.combine_videos()

    ended_time = datetime.now()
    print(f'time cost: {ended_time - start_time}')
    
        
        
        
        
        
        
        
        
# files = glob.glob('**/*.mp4', recursive=True)
# video_list = []
# start_sec = 0
# for file in files:
#     try:
#         source = file
#         target = os.path.join(output_folder, source) #拼接文件名路径
#         if not os.path.exists(os.path.dirname(target)): #os.path.isdir(os.path.join(root, output)) os.path.join(root, output)
#             os.makedirs(os.path.dirname(target))
#         video = VideoFileClip(source)
#         total_seconds = video.duration
#         start_time = 0
#         stop_time = total_seconds - 3
#         video = video.subclip(int(start_time), int(stop_time))#执行剪切操作
#         video.to_videofile(target, fps=20, remove_temp=True)#输出文件
#         # os.remove(source)
#         print(video.size[0],video.size[1])
#         print(video.size[0]/1300,video.size[1]/720)
#         rate_x = video.size[0]/1300
#         rate_y = video.size[1]/720
#         rate_max = max(rate_x, rate_y)
#         if rate_max > 1:
#             rate_max = 1/rate_max
#         else:
#             rate_max = 1
#         video = video.set_start(start_sec).set_pos("center").resize(rate_max)
#         print('-=====>', rate_max)
#         start_sec = start_sec + video.duration
#         video_list.append(video)#将加载完后的视频加入列表
#     except Exception as e:
#         print('have error:',e)
#     finally:
#         print(file, 'done')
# final_clip = CompositeVideoClip(video_list, size=(1300, 720))
# final_clip.to_videofile(os.path.join(output_folder, 'combined.mp4'), fps=20, remove_temp=True)
# # final_clip = concatenate_videoclips(video_list)#进行视频合并
# # final_clip.write_videofile(os.path.join(output_folder, 'combined.mp4'), fps=20, remove_temp=True)
# # final_clip.to_videofile(os.path.join(output_folder, 'combined.mp4'), fps=20, remove_temp=True)#将合并后的视频输出