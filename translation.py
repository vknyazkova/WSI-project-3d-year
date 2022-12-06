import os
import uuid
from enum import Enum
from pathlib import Path
from Naked.toolshed.shell import muterun_js
from googletrans import Translator


def get_official_google_translate(
    text: str,
    source_lang: Enum,
    target_lang: Enum
) -> str:
    home_path = Path().resolve()
    translations_folder = str(Path(home_path, "translation_files"))
    if not os.path.exists(translations_folder):
      os.makedirs(translations_folder, exist_ok=True)
    file_translation = str(Path(translations_folder, f"{uuid.uuid4().hex}.js"))
    text = text.replace('\n', ' ').replace('\'', '\"')

    template = f"""const translate = require('@iamtraction/google-translate');
    translate(
        '{text}',
        {{from: '{source_lang}', to: '{target_lang}' }}).then(res => {{
    console.log(res.text); }}).catch(err => {{
    console.error(err);
    }});
    """
    with open(file_translation, "w", encoding="utf-8") as f:
        f.write(template)
    response = muterun_js(file_translation)

    os.remove(file_translation)
    return response.stdout.decode("utf-8")


def get_unofficial_google_translate(
        text: str,
        source_lang: Enum,
        target_lang: Enum
) -> str:
    """
    We advise not to translate using this function in multiprocessing manner.
    """
    return Translator().translate(text, src=source_lang, dest=target_lang).text
