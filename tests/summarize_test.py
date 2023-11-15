import sys
import os
import glob
sys.path.append(os.getcwd())
from summarize import *

def test_find_first_file():
    assert find_first_file() == "./out.en-orig.ttml"

def test_main():
    assert "hands can work" in get_transcript("https://www.youtube.com/shorts/D1dv39-ekBM")
