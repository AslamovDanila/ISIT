import flet as ft
import aiohttp
import re
from __init__ import api_key

CYRILLIC_PATTERN = re.compile(r'[а-яА-ЯёЁ]')
ENGLISH_PATTERN = re.compile(r'[a-zA-Z]')


def is_russian(text: str) -> bool:
    return bool(CYRILLIC_PATTERN.search(text)) and not bool(ENGLISH_PATTERN.search(text))


def is_english(text: str) -> bool:
    return bool(ENGLISH_PATTERN.search(text)) and not bool(CYRILLIC_PATTERN.search(text))


async def fetch_english_definition(word: str) -> str:
    url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.json()
                return format_english_response(data)
            return "Слово не найдено"


async def fetch_russian_definition(word: str) -> str:
    url = f"https://dictionary.yandex.net/api/v1/dicservice.json/lookup?key={api_key}&lang=ru-ru&text={word}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.json()
                return format_russian_response(data)
            return "Ошибка при обращении к API"


def format_english_response(data: list) -> str:
    result = []
    for entry in data[:3]:
        word = entry.get('word', '')
        phonetics = entry.get('phonetics', [])
        phonetic_text = ""
        for p in phonetics:
            if p.get('text'):
                phonetic_text = p.get('text', '')
                break
        
        result.append(f"📖 {word.upper()} {phonetic_text}")
        
        for meaning in entry.get('meanings', [])[:2]:
            part_of_speech = meaning.get('partOfSpeech', '')
            definitions = meaning.get('definitions', [])[:2]
            
            result.append(f"\n🔤 {part_of_speech}")
            
            for i, defn in enumerate(definitions, 1):
                definition_text = defn.get('definition', '')
                example = defn.get('example', '')
                result.append(f"  {i}. {definition_text}")
                if example:
                    result.append(f"     Example: \"{example}\"")
            
            synonyms = meaning.get('synonyms', [])[:3]
            if synonyms:
                result.append(f"\n  🔗 Синонимы: {', '.join(synonyms)}")
            
            antonyms = meaning.get('antonyms', [])[:3]
            if antonyms:
                result.append(f"  🔄 Антонимы: {', '.join(antonyms)}")
        
        result.append("\n" + "="*40)
    
    return "\n".join(result)


def format_russian_response(data: dict) -> str:
    result = []
    defs = data.get('def', [])
    
    if not defs:
        return "Переводы не найдены"
    
    for def_entry in defs[:3]:
        text = def_entry.get('text', '')
        result.append(f"📖 {text.upper()}")
        
        tr_list = def_entry.get('tr', [])[:2]
        for tr in tr_list:
            translation = tr.get('text', '')
            part_of_speech = tr.get('pos', '')
            
            result.append(f"\n🔤 {part_of_speech}: {translation}")
            
            meanings = tr.get('mean', [])[:2]
            for mean in meanings:
                meaning_text = mean.get('text', '')
                result.append(f"  • {meaning_text}")
            
            examples = tr.get('ex', [])[:2]
            for ex in examples:
                ex_text = ex.get('text', '')
                result.append(f"  Example: \"{ex_text}\"")
            
            synonyms = [s.get('text', '') for s in tr.get('syn', [])[:3]]
            if synonyms:
                result.append(f"  🔗 Синонимы: {', '.join(synonyms)}")
        
        result.append("\n" + "="*40)
    
    return "\n".join(result)


def main(page: ft.Page):
    page.title = "Электронный словарь"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 20
    
    word_input = ft.TextField(
        label="Введите слово",
        width=400,
        height=50,
        autofocus=True
    )
    
    result_area = ft.TextField(
        value="",
        width=500,
        height=400,
        multiline=True,
        read_only=True,
        text_size=14
    )
    
    status_text = ft.Text("", size=14, color=ft.Colors.GREY)
    
    async def search_word(e):
        word = word_input.value.strip()
        if not word:
            return
        
        status_text.value = "Поиск..."
        page.update()
        result_area.value = ""
        
        try:
            if is_english(word):
                result_area.value = await fetch_english_definition(word)
                status_text.value = "✓ Найдено (английский)"
            elif is_russian(word):
                result_area.value = await fetch_russian_definition(word)
                status_text.value = "✓ Найдено (русский)"
            else:
                result_area.value = "Неподдерживаемый язык"
                status_text.value = "⚠ Невозможно определить язык"
        except Exception as ex:
            result_area.value = f"Ошибка: {str(ex)}"
            status_text.value = "✗ Ошибка соединения"
        
        page.update()
    
    search_button = ft.Button(
        "Найти",
        on_click=search_word,
        width=120,
        height=50
    )
    
    title = ft.Text("Электронный словарь", size=24, weight=ft.FontWeight.BOLD)

    input_row = ft.Row([word_input, search_button], alignment=ft.MainAxisAlignment.CENTER)
    
    page.add(
        ft.Container(title, margin=ft.Margin.only(bottom=20)),
        input_row,
        ft.Container(status_text, margin=ft.Margin.only(top=10, bottom=10)),
        ft.Container(
            result_area,
            border=ft.Border.all(1, ft.Colors.GREY_300),
            border_radius=10,
            padding=15
        )
    )


if __name__ == "__main__":
    ft.run(main, view = ft.AppView.WEB_BROWSER)
