import requests
from bs4 import BeautifulSoup


def get_word(word):
    return f'<b>Слово - </b><i>{word.title()}</i>'


def get_href(word):
    return f'<a href="https://ru.wiktionary.org/wiki/{word}">Подробнее</a>'


def fetch_page(word):
    url = f'https://ru.wiktionary.org/wiki/{word}'
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException:
        return None


def fetch_random_page():
    url = 'https://ru.wiktionary.org/wiki/Служебная:Случайная_страница'
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException:
        return None


def parse_word_page(url):
    soup = BeautifulSoup(url, 'html.parser')
    word = soup.find('h1', {'id': 'firstHeading'}).text
    return word, soup


def is_russian_word(word, soup):
    if "Викисловарь:Общие сведения" in word:
        return False
    lang_section = soup.find('span', {'id': 'Русский'})
    return bool(lang_section)


def is_any_lang_word(lang, soup):
    languages = {
        'ru': 'Русский',
        'en': 'Английский',
        'uk': 'Украинский',
        'de': 'Немецкий',
        'es': 'Испанский',
        'fr': 'Французский',
    }
    return soup.find('span', {'id': languages.get(lang)})


def extract_rus_meanings(soup):
    definition_block = soup.find('div', {'class': 'mw-body-content'})
    if not definition_block:
        return None
    try:
        meanings = definition_block.find('ol').find_all(
            'li', class_=lambda x: x != 'mw-empty-elt')
        return meanings
    except AttributeError:
        return None


def extract_eng_meanings(soup):
    try:
        meanings = soup.find_next('ol').find_all(
            'li', class_=lambda x: x != 'mw-empty-elt')
        return meanings
    except AttributeError:
        return None


def format_meaning(meaning, index):
    text = meaning.text.strip()
    if 'Отсутствует пример употребления (см. рекомендации).' in text:
        text = text.replace(
            'Отсутствует пример употребления (см. рекомендации).', '').replace('◆', '').strip()
    else:
        text = text.replace('◆', '\n<b>Пример :</b>')
    text = text.replace('//', '\n')
    if text:
        return f'{index + 1}. <b>Значение :</b> {text}'
    else:
        return ''


def format_meanings(meanings):
    if not meanings:
        return "Нет значения"
    if len(meanings) == 1:
        return format_meaning(meanings[0], 0).replace('1. ', '')
    return '\n'.join(format_meaning(meaning, i) for i, meaning in enumerate(meanings[:3]))


def fetch_random_russian_word():
    while True:
        url = fetch_random_page()
        if not url:
            return 'Произошла ошибка\nПопробуйте снова'

        word, soup = parse_word_page(url)

        if is_russian_word(word, soup):
            href = get_href(word)
            word = get_word(word)
            meanings = extract_rus_meanings(soup)

            if not meanings:
                return f"{word}\nНет значения\n{href}"

            all_meanings = format_meanings(meanings)
            result = f"{word}\n{all_meanings}\n{href}"
            result_lines = filter(bool, result.split('\n'))
            return '\n'.join(result_lines)


def get_word_search(word, lang):
    page_content = fetch_page(word)
    if not page_content:
        return 'Произошла ошибка\nПопробуйте снова'

    soup = BeautifulSoup(page_content, 'html.parser')
    lang_section = is_any_lang_word(lang, soup)

    if not lang_section:
        return 'Нет значений для данного слова'

    href = get_href(word)
    word = get_word(word)

    meanings = extract_eng_meanings(lang_section)

    if not meanings:
        return f"{word}\nНет значения\n{href}"

    all_meanings = format_meanings(meanings)
    result = f"{word}\n{all_meanings}\n{href}"
    result_lines = filter(bool, result.split('\n'))

    return '\n'.join(result_lines)


# TODO: ConnectTimeout MaxRetryError ConnectTimeoutError TimeoutError
if __name__ == '__main__':
    # print(fetch_random_russian_word())
    print(get_word_search('ban', 'en'))
