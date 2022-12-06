from collections import defaultdict
from tqdm import tqdm
from sklearn.metrics.pairwise import cosine_similarity

from substitution_preprocessing import clean_substitutes


def target_substitutes(target: str, lang_model, n_substitutes=200, translator=None, lang='en'):
    """
    Generation of substitutes closest to the target (no context info)
    If translator is not None targets will be translated to the given lang
    """

    if translator:
        target = translator(target, 'en', lang).strip('\n')
    target_substitutes = lang_model.get_nearest_neighbors(target, k=n_substitutes)
    target_substitutes = [s[1] for s in target_substitutes]
    return target_substitutes


def substitutes_generator(lang_model, lang, target_context_info, similarity_metric=cosine_similarity, translator=None):
    """
    :param target_context_info: {target: {context_id: context_emb}},
            target = lemma.POS
            context_id = lemma.POS.context_id
            context_emb.shape = (300,)
    """

    subst_dict = defaultdict(dict)
    for i, target in enumerate(tqdm(target_context_info)):
        target_lemma = target.split('.')[0]
        all_substitutes = target_substitutes(target_lemma, lang_model, translator=translator, lang=lang)
        cleaned_substitutes = clean_substitutes(all_substitutes, lang_model)
        target_closest_emb = [(substitute, lang_model.get_word_vector(substitute)) for substitute in cleaned_substitutes]
        for context in target_context_info[target]:
            context_emb = lang_model.get_sentence_vector(context)
            sorted_substitutes = sorted(target_closest_emb, key=lambda x: similarity_metric(x[1].reshape(1, -1), context_emb.reshape(1, -1)), reverse=True)
            substitutes = [s[0] for s in sorted_substitutes]
            subst_dict[target][context] = ' '.join(substitutes)
    return subst_dict