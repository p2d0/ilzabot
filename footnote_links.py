#!/usr/bin/env python3
import re
from typing import List, Tuple

def parse_text_with_footnote_links(text):
    # Find all footnote links in the text
    pattern = r"\[\^(\d+)\^\]\[(\d+)\]"
    matches = re.findall(pattern, text)

    # Extract the URLs and descriptions from the footnote links
    links = []
    for match in matches:
        footnote_number = match[0]
        link_number = match[1]
        link_pattern = rf"\[{link_number}\]:\s*(\S+)\s*\"(.+?)\""
        link_match = re.search(link_pattern, text)
        if link_match:
            url = link_match.group(1)
            description = link_match.group(2)
            links.append((url, description))

    return links

def replace_footnotes_with_html_url(links, text):
    text = re.sub(r"\[\d\]","",text)
    for i, (url, desc) in enumerate(links):
        text = text.replace(f"[^{i+1}^]", f'<a href="{url}">[{i+1}]</a>')
    return text

def remove_footnotes(text: str) -> str:
    return re.sub(r'\[\d+\]:\s+\S+\s+"[^"]+"\s*', '', text)

if __name__ == '__main__':
    text = '''
    [1]: https://daily.afisha.ru/infoporn/15912-prohod-putina-po-koridoru-pered-inauguraciey-vnezapno-stal-abstraktnym-memom/ "Проход Путина перед инаугурацией превратился в абстрактный мем - Афиша ..."
    [2]: https://memes.fandom.com/ru/wiki/Wide_Putin_Walking "Wide Putin Walking | Мемопедия вики | Fandom"
    [3]: https://ru.wikipedia.org/wiki/%D0%A8%D0%B8%D1%80%D0%BE%D0%BA%D0%B8%D0%B9_%D0%9F%D1%83%D1%82%D0%B8%D0%BD_%D0%B8%D0%B4%D1%91%D1%82 "Широкий Путин идёт — Википедия"
    [4]: https://devsday.ru/news/details/195179 "Thicc Putin Walking: как появился мем про «широкого Путина»"
    [5]: https://www.youtube.com/watch?v=W58CjT1f6dI "сборник мемов про путина (putin memes compilation) - YouTube"

    Хорошо, вот пример мема про широкого путина[^1^][1] [^2^][2] [^3^][3]:

    ```markdown
    Видео: Путин идет по коридору в растянутом формате под музыку Song for Denise Piano Fantasia. На экране появляется надпись "IT HIM".
    ```

    Это видео стало вирусным в интернете и породило множество пародий и ремиксов[^4^][4] [^5^][5]. Вам понравился этот мем?
    '''

    print(replace_footnotes_with_html_url(parse_text_with_footnote_links(text),text))
    # print(remove_footnotes(text))
