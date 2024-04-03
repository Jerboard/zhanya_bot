import re
import typing as t


def remove_punctuation(text: t.Optional[str]) -> list:
    if text:
        cleaned_text = re.sub(r'[^\w\s]', '', text.lower())
    else:
        cleaned_text = ''
    return cleaned_text.split(' ')
