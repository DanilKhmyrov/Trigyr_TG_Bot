import requests
from bs4 import BeautifulSoup


def format_meaning(meaning, index):
    text = meaning.text.strip()
    if 'Отсутствует пример употребления (см. рекомендации).' in text:
        text = text.replace(
            'Отсутствует пример употребления (см. рекомендации).', '').strip()
        text = text.replace('◆', '').strip()
    else:
        text = text.replace('◆', '\n<b>Пример :</b>').strip()
    text = text.replace('//', '\n')
    if text:
        return f'{index + 1}. <b>Значение :</b> {text}'
    else:
        return ''


def fetch_random_russian_word():
    while True:
        # Получаем случайную страницу
        url = 'https://ru.wiktionary.org/wiki/Служебная:Случайная_страница'
        # url = "https://ru.wiktionary.org/wiki/малопродуктивность"
        try:
            response = requests.get(url)
        except requests.exceptions.RequestException:
            return 'Произошла ошибка\nПопробуйте снова'
        soup = BeautifulSoup(response.text, 'html.parser')

        # Получаем заголовок страницы (слово)
        word = soup.find('h1', {'id': 'firstHeading'}).text

        # Проверяем, что это русское слово
        if "Викисловарь:Общие сведения" not in word:  # Фильтрация случайных справочных страниц
            lang_section = soup.find('span', {'id': 'Русский'})
            if lang_section:
                href = f'<a href="https://ru.wiktionary.org/wiki/{
                    word}">Подробнее</a>'
                word = f'<b>Слово - </b><i>{word.title()}</i>' + '\n'
                definition_block = soup.find(
                    'div', {'class': 'mw-body-content'})
                if not definition_block:
                    return f"Error: Unable to find definitions for {word}"
                try:
                    meanings = definition_block.find('ol').find_all(
                        'li', class_=lambda x: x != 'mw-empty-elt')
                except AttributeError:
                    return f"{word}\nНет значения\n{href}"
                if len(meanings) == 1:
                    all_meanings = format_meaning(
                        meanings[0], 0).replace('1. ', '')
                else:
                    all_meanings = '\n'.join(
                        [format_meaning(meaning, i) for i, meaning in enumerate(meanings[:3])])

                result = word + all_meanings + '\n' + href
                result_lines = filter(bool, result.split('\n'))
                result = '\n'.join(result_lines)
                return result


# TODO: ConnectTimeout MaxRetryError ConnectTimeoutError TimeoutError
if __name__ == '__main__':
    print(fetch_random_russian_word())
