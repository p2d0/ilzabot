from bs4 import BeautifulSoup
import yt_dlp
import glob
import shutil
import os


def download_subtitles(video_url):
    ydl_opts = {
        'skip_download': True,
        'writesubtitles': True,
        'writeautomaticsub': True,
        'subtitleslangs': ['..-orig'],
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

def get_transcript(video_url):
    download_subtitles(video_url);

    files = glob.glob('out.*.ttml')
    # if there are any matching files
    if files:
        # get the first matching file
        first_file = files[0]
        # get the extension of the first matching file
        extension = os.path.splitext(first_file)[-1]
        # get the base name of the file without the extension
        base_name = os.path.splitext(os.path.basename(first_file))[0].split('.')[0]
        # create a new file name "out.ttml"
        new_file_name = f"{base_name}.ttml"
        # loop through all matching files
        print(new_file_name)
        for file in files:
            # move each file to the new file name
            shutil.move(file, new_file_name)
    transcript = parse_xml_file("out.ttml");
    return transcript
