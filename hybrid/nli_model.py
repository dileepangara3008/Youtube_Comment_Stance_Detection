from transformers import pipeline

nli = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

labels = ["favor", "against", "neutral"]

def predict_nli(text, topic):
    hypothesis_template = "The stance of the text towards {} is {}."

    result = nli(
        text,
        candidate_labels=labels,
        hypothesis_template=hypothesis_template.format(topic, "{}")
    )

    return result["labels"][0].lower()