from fuzzywuzzy import fuzz


def delete_typos(token_list, lang_model, typo_threshold):
    to_delete = set()
    # сортирую, тк опечатки скорее всего будут менее частотными, чем правильное написание
    token_list = sorted(token_list, key=lambda x: lang_model.words.index(x) if x in lang_model.words else 10 ** 10)
    for i in range(len(token_list)):
        for j in range(i + 1, len(token_list)):
            if fuzz.ratio(token_list[i], token_list[j]) > typo_threshold:
                to_delete.add(token_list[j])
    return set(token_list) - to_delete


def clean_substitutes(substitutes: list, lang_model, typo_threashold=80):
    """
    Deletes typos and unnecessary punctuation
    :param typo_threshold: tokens with similarity more than given threshold will be assumed as a typos of the same word
    """

    unique_substitutes = set()
    for t in substitutes:
        t = t.lower().split('.')[0]
        unique_substitutes.add(t)
    cleaned_substitutes = delete_typos(list(unique_substitutes), lang_model, typo_threashold)
    if '' in cleaned_substitutes:
        cleaned_substitutes.remove('')
    return cleaned_substitutes
