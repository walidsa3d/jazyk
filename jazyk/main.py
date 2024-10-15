import asyncio
import click
from deep_translator import GoogleTranslator
from rich.console import Console
from rich.panel import Panel
from rich.align import Align
import uroman as ur
from jazyk.langs import *
import time 
uroman = ur.Uroman()
console = Console()

async def translate_language(text, code, lang, max_lang_length):
    """Translate text to a specific language asynchronously."""
    jlang = lang.ljust(max_lang_length)
    try:
        translator = GoogleTranslator(source='auto', target=code)
        translation = await asyncio.to_thread(translator.translate, text)
        if code in dict(NON_LATIN_LANGS).keys():
            translit = await asyncio.to_thread(uroman.romanize_string, translation)
            return lang, jlang, translation, None, translit
        else:
            return lang, jlang, translation, None
    except Exception as e:
        return lang, jlang, None, str(e)

async def generate_translations(text):
    """Generate translations for a given text in all European languages asynchronously."""
    ALL_LANGS = LATIN_LANGS + NON_LATIN_LANGS
    max_lang_length = max(len(lang) for _, lang in ALL_LANGS)

    tasks = [translate_language(text, code, lang, max_lang_length) for code, lang in ALL_LANGS]
    return await asyncio.gather(*tasks)

def display_translation(translation):
    """Display a single translation."""
    if len(translation) == 4:  # Latin script language
        lang, jlang, trans, error = translation
        if error:
            console.print(Align.left(f"[bold]{jlang}:[/bold] [red]Error: {error}[/red]"), end="")
        else:
            console.print(Align.left(f"[bold][yellow]{jlang}:[/yellow][/bold] [magenta]{trans}[/magenta]"), end="")
    else:  # Non-Latin script language
        lang, jlang, trans, error, translit = translation
        if error:
            console.print(Align.left(f"[bold]{jlang}:[/bold] [red]Error: {error}[/red]"), end="")
        else:
            console.print(Align.left(f"[bold][yellow]{jlang}:[/yellow][/bold] [magenta]{trans}/{translit}[/magenta]"), end="")

@click.command()
@click.argument('text', nargs=-1)
def translate_text(text):
    """Translate a word or phrase to all languages."""
    text = ' '.join(text)
    console.print(Panel(Align.center(f"[bold]Translating '[cyan]{text}[/cyan]' to All languages[/bold]")))

    # Generate all translations asynchronously
    translations = asyncio.run(generate_translations(text))
    
    # Sort translations alphabetically by language name
    sorted_translations = sorted(translations, key=lambda x: x[0])
    
    # Display sorted translations
    for translation in sorted_translations:
        time.sleep(0.5)
        display_translation(translation)

if __name__ == '__main__':
    translate_text()