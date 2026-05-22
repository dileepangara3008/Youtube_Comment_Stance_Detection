from hybrid.nli_model import predict_nli
from hybrid.llm_model import predict_llm

def predict_stance(text, target):
    try:
        nli_result = predict_nli(text, target)
        llm_result = predict_llm(text, target)

        # agreement → strong result
        if nli_result == llm_result:
            final = nli_result
        else:
            final = llm_result  # prefer LLM

        return {
            "nli": nli_result,
            "llm": llm_result,
            "final": final
        }

    except Exception as e:
        print("Pipeline Error:", e)
        return {
            "final": "neutral"
        }