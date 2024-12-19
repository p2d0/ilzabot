# import sys
# import os
# import pytest
# import glob
# import yt_dlp

# # def test_format():
# # 	with yt_dlp.YoutubeDL({'outtmpl': 'video.mp4',"overwrites": True, 'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]', 'cookiefile': '../instacookie'}) as ydl:
# # 		ydl.download(["https://www.reddit.com/r/SipsTea/comments/180fy79/warning_this_is_gonna_hurt/?utm_source=share&utm_medium=web2x&context=3"])

# @pytest.mark.skip()
# def test_format2():
# 	with yt_dlp.YoutubeDL({'outtmpl': 'video.%(ext)s',"overwrites": True,"format":"bv*[ext=mp4]+ba[ext=m4a]/b[ext=mp4] / bv*+ba/b", 'cookiefile': './instacookie',
# 				'postprocessors': [{
# 					"key": "FFmpegVideoRemuxer",
# 					"preferedformat": "mp4"
# 				}]
# 				}) as ydl:
# 		ydl.download(["https://www.youtube.com/shorts/ehCW4YHHtu0"])

# if __name__ == '__main__':
# 	with yt_dlp.YoutubeDL({'outtmpl': 'video.%(ext)s',"overwrites": True,"format":"bv*[ext=mp4]+ba[ext=m4a]/b[ext=mp4] / bv*+ba/b", 'cookiefile': './instacookie',
# 				'postprocessors': [{
# 					"key": "FFmpegVideoRemuxer",
# 					"preferedformat": "mp4"
# 				}]
# 				}) as ydl:
# 		ydl.download(["https://www.youtube.com/shorts/ehCW4YHHtu0"])
