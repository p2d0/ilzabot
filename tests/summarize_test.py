import sys
import os
import pytest
import glob
sys.path.append(os.getcwd())
from summarize import *
# from giga import Bot
from hug import Bot

@pytest.mark.skip()
def test_find_first_file():
    assert find_first_file() == "./out.ru.ttml"


@pytest.mark.skip()
def test_summarize_ilza():
    text = parse_xml_file(find_first_file())
    print(text)
    bot = Bot()
    answer = bot.ask(f'(Отвечай по русски!) Извлеки суть: "{text}"')
    assert answer == ""

def test_main():
    print(get_transcript("https://youtube.com/shorts/y8lMSMoqbps?si=u7XN1hG3HWWEllNE"))
    # assert "hands can work" in get_transcript("https://www.youtube.com/shorts/D1dv39-ekBM")

@pytest.mark.skip()
def test_no_subs():
    assert None == get_transcript("https://youtube.com/shorts/y8lMSMoqbps?si=u7XN1hG3HWWEllNE")
