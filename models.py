from transformers import pipeline
from functools import lru_cache

@lru_cache()
def get_summarizer(model_name: str = "facebook/bart-large-cnn", device: int = -1):
    # device=-1 for CPU, device=0 for GPU
    return pipeline("summarization", model=model_name, device=device)

@lru_cache()
def get_translator_en_bn(model_name: str = "Helsinki-NLP/opus-mt-en-bn"):
    return pipeline("translation_en_to_bn", model=model_name)

@lru_cache()
def get_translator_bn_en(model_name: str = "Helsinki-NLP/opus-mt-bn-en"):
    return pipeline("translation_bn_to_en", model=model_name)

def summarize_text(text, summarizer, max_length=150, min_length=40):
    from utils import chunk_text
    chunks = chunk_text(text, max_chars=2500)
    summaries = []
    for c in chunks:
        out = summarizer(c, max_length=max_length, min_length=min_length, do_sample=False)
        summaries.append(out[0].get('summary_text') or out[0].get('generated_text') or '')
    joined = '\n'.join(summaries)
    if len(chunks) > 1:
        final = summarizer(joined, max_length=max_length, min_length=min_length, do_sample=False)
        return final[0].get('summary_text') or final[0].get('generated_text') or joined
    return joined

def translate_text(text, translator):
    out = translator(text)
    if isinstance(out, list):
        return ' '.join([o.get('translation_text') or o.get('text') or '' for o in out])
    return out[0].get('translation_text') or out[0].get('text') or ''
