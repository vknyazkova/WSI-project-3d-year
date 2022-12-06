import ast
from collections import defaultdict


def extract_target_context(context_info, delete_target=True, window=3):
    """
    Retrieves context with a given window size

    :param context_info: a row from dataframe with target position in 'target_id'
            column and list of parsed sentence written in 'sentence' column
    """

    target_id = context_info['target_id']
    context = ast.literal_eval(context_info['sentence'])
    if delete_target:
        context.pop(target_id)
    return ' '.join(context[target_id - window: target_id + window + 1])


def get_context_embeddings(dataset, lang_model, window=3):
    """
    :return: {target: {context id: context embedding}}
    """

    by_targets = dataset.groupby(['group_by'])
    context_embeddings = defaultdict(dict)
    for target in by_targets.groups:
        for context in by_targets.groups[target]:
            context_info = dataset.loc[context]
            extracted_context = extract_target_context(context_info, window=window)
            cont_emb = lang_model.get_sentence_vector(extracted_context)
            context_embeddings[target][context_info['context_id']] = cont_emb
    return context_embeddings
