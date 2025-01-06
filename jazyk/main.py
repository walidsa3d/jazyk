import asyncio
import click
from deep_translator import GoogleTranslator
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from dataclasses import dataclass
import uroman as ur
from jazyk.langs import LATIN_LANGS, NON_LATIN_LANGS
from rich.text import Text
import pyfiglet

uroman = ur.Uroman()
console = Console()

@dataclass
class TranslationResult:
    lang: str
    jlang: str
    translation: str
    error: str = None
    translit: str = None

def asciify(text:str, font='standard')->str:
    """Convert the given text into colorful and centered ASCII art using Rich.

    Args:
        text (str): The text to convert into ASCII art.
        font (str, optional): The font style to use for the ASCII art. Defaults to 'standard'.
        color (str, optional): The color to apply to the ASCII art. Defaults to 'green'.

    Returns:
        None: The function prints the ASCII art directly to the terminal.
    """
    # Generate ASCII art using pyfiglet
    ascii_art = pyfiglet.figlet_format(text, font=font)
    return ascii_art

def show_banner():
    ascii_text = asciify("Jazyk")
    rich_text = Text(ascii_text, style="orange")
    console.print(rich_text, justify="center")

async def translate_language(text, code, lang, max_lang_length):
    """Translate text to a specific language asynchronously."""
    jlang = lang.ljust(max_lang_length)
    try:
        translator = GoogleTranslator(source='auto', target=code)
        translation = await asyncio.to_thread(translator.translate, text)
        if code in dict(NON_LATIN_LANGS).keys():
            translit = await asyncio.to_thread(uroman.romanize_string, translation)
            return TranslationResult(lang, jlang, translation, None, translit)
        else:
            return TranslationResult(lang, jlang, translation)
    except Exception as e:
        return TranslationResult(lang, jlang, None, str(e))

async def generate_translations(text):
    """Generate translations for a given text in all European languages asynchronously."""
    ALL_LANGS = {**dict(LATIN_LANGS), **dict(NON_LATIN_LANGS)}
    max_lang_length = max(len(lang) for lang in ALL_LANGS.values())

    tasks = [translate_language(text, code, lang, max_lang_length) for code, lang in ALL_LANGS.items()]
    return await asyncio.gather(*tasks)

def display_translation(result):
    """Display a single translation result."""
    if result.error:
        console.print(f"[bold]{result.jlang}:[/bold] [red]Error: {result.error}[/red]")
    elif result.translit:
        console.print(f"[bold][yellow]{result.jlang}:[/yellow][/bold] [magenta]{result.translation}/{result.translit}[/magenta]")
    else:
        console.print(f"[bold][yellow]{result.jlang}:[/yellow][/bold] [magenta]{result.translation}[/magenta]")

@click.command()
@click.argument('text', nargs=-1)
def translate_text(text):
    """Translate a word or phrase to all languages."""
    show_banner()
    text = ' '.join(text)
    if not text:
        console.print("[red]Error: No text provided.[/red]")
        return

    # Show banner

    # Display the text being translated
    console.print(Panel.fit(f"[bold]Translating '[cyan]{text}[/cyan]' to All languages[/bold]"))

    # Show a spinner while generating translations
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,  # Hides the spinner after completion
    ) as progress:
        progress.add_task("[cyan]Translating...", total=None)
        # Generate all translations asynchronously
        translations = asyncio.run(generate_translations(text))
    
    # Sort translations alphabetically by language name
    sorted_translations = sorted(translations, key=lambda x: x.lang)
    
    # Display translations one by one
    for result in sorted_translations:
        display_translation(result)
        asyncio.run(asyncio.sleep(0.5))  # Add a slight delay between results

if __name__ == '__main__':
    translate_text()