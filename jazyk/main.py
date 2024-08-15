import click
from deep_translator import GoogleTranslator
from rich.console import Console
from rich.panel import Panel
from rich.align import Align
import uroman as ur
from langs import *

uroman = ur.Uroman()
console = Console()

@click.command()
@click.argument('text', nargs=-1)
def translate_word(word):
    """Translate a word to all European languages."""
    text = ' '.join(text)
    console.print(Panel(Align.center(f"[bold]Translating '[cyan]{word}[/cyan]' to European languages[/bold]")))
    ALL_LANGS = LATIN_LANGS + NON_LATIN_LANGS
    max_lang_length = max(len(lang) for _, lang in ALL_LANGS)
    for code, lang in LATIN_LANGS:
        try:
            jlang = lang.ljust(max_lang_length)
            translator = GoogleTranslator(source='auto', target=code)
            translation = translator.translate(word)
            console.print(Align.left(f"[bold][yellow]{jlang}:[/yellow][/bold] [magenta]{translation}[/magenta]"))
        except Exception as e:
            console.print(Align.left(f"[bold]{lang}:[/bold] [red]Error: {str(e)}[/red]"))
    for code, lang in NON_LATIN_LANGS:
        try:
            jlang = lang.ljust(max_lang_length)
            translator = GoogleTranslator(source='auto', target=code)
            translation = translator.translate(word)
            translit = uroman.romanize_string(translation)
            console.print(Align.left(f"[bold][yellow]{jlang}:[/yellow][/bold] [magenta]{translation}/{translit}[/magenta]"))
        except Exception as e:
            console.print(Align.right(f"[bold]{jlang}:[/bold] [red]Error: {str(e)}[/red]"))
if __name__ == '__main__':
    translate_word()