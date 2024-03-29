from bs4 import BeautifulSoup
import yt_dlp
import argparse
import glob
import shutil
import os


def download_subtitles(video_url):
    ydl_opts = {
        'skip_download': True,
        'writesubtitles': True,
        'writeautomaticsub': True,
        'subtitleslangs': ['(?:ru|en)(?:-orig)?'],
        'subtitlesformat': 'ttml',
        "overwrites": True,
        'outtmpl': 'out.%(ext)s'
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_url])


def parse_xml_file(filename='out.en.ttml'):
    with open(filename, 'r') as f:
        xml_data = f.read()

    soup = BeautifulSoup(xml_data, 'xml')

    paragraphs = soup.find_all('p')
    text = '';
    for p in paragraphs:
        text += p.get_text() + ' '
    return text


def find_first_file():
    for file_name in ["out.ru-orig.ttml", "out.ru.ttml", "out.en-orig.ttml","out.en.ttml"]:
        file_path = os.path.join("./", file_name)
        if os.path.exists(file_path):
            return file_path
    return None

def remove_old_ttmls():
    files = glob.glob('out.*.ttml')
    # if there are any matching files
    if files:
        for file_path in files:
            os.remove(file_path)

def get_transcript(video_url):
    remove_old_ttmls()

    download_subtitles(video_url);
    f = find_first_file()
    if f:
        transcript = parse_xml_file(f);
        return transcript

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Download subtitles for a given YouTube video URL.')

    parser.add_argument('video_url', type=str, help='YouTube video URL')

    args = parser.parse_args()

    print(get_transcript(args.video_url))
