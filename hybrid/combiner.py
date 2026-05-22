labels = ["favor", "against", "neutral"]

def combine(nli, llm, w1=0.4, w2=0.6):
    scores = {}

    for label in labels:
        scores[label] = (
            w1 * nli.get(label, 0) +
            w2 * llm.get(label, 0)
        )

    final = max(scores, key=scores.get)

    # confidence check
    nli_label = max(nli, key=nli.get)
    llm_label = max(llm, key=llm.get)

    confidence = "high" if nli_label == llm_label else "medium"

    return final, scores, confidence