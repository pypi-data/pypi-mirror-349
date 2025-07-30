import importlib
from collections import OrderedDict

# Внутреннее состояние (глобальное)
_lazy_model_cache = OrderedDict()
_lazy_model_limit = 2

def _lazy_model_resolve_class(model_name: str, task: str = None) -> str:
    name = model_name.lower()
    if task == "causal-lm" or any(k in name for k in ["gpt", "llama", "mistral", "rwkv", "opt"]):
        return "AutoModelForCausalLM"
    if task == "seq2seq" or any(k in name for k in ["t5", "bart", "mbart"]):
        return "AutoModelForSeq2SeqLM"
    if task == "token-class" or "ner" in name:
        return "AutoModelForTokenClassification"
    if task == "qa":
        return "AutoModelForQuestionAnswering"
    if "mini" in name or "paraphrase" in name or "sentence" in name or task == "embedding":
        return "SentenceTransformer"
    return "AutoModel"

def lazy_model_transformer(model_name: str, task: str = None, tokenizer: bool = False):
    global _lazy_model_cache, _lazy_model_limit

    model_cls = _lazy_model_resolve_class(model_name, task)
    key = f"{model_cls}::{model_name}::with_tokenizer={tokenizer}"

    if key in _lazy_model_cache:
        _lazy_model_cache.move_to_end(key)
        return _lazy_model_cache[key]

    # Lazy import
    tr = importlib.import_module("transformers")
    model_class = getattr(tr, model_cls)
    model = model_class.from_pretrained(model_name)

    if tokenizer:
        tok = tr.AutoTokenizer.from_pretrained(model_name)
        obj = (model, tok)
    else:
        obj = model

    # Выгрузка старых
    if len(_lazy_model_cache) >= _lazy_model_limit:
        old_key, old_obj = _lazy_model_cache.popitem(last=False)
        print(f"[lazy_model_transformer] Unloading: {old_key}")
        del old_obj

    print(f"[lazy_model_transformer] Loading: {key}")
    _lazy_model_cache[key] = obj
    return obj
# # GPT2 — генерация
# model = lazy_model_transformer("gpt2")
#
# # T5 + токенизатор
# model, tokenizer = lazy_model_transformer("t5-small", tokenizer=True)
#
# # Явная задача
# model = lazy_model_transformer("bert-base-cased", task="token-class")