import importlib
from collections import OrderedDict
from typing import Callable, Literal


class LazyModelManager:
    def __init__(self, max_memory_mb: int = None, device: Literal["auto", "cpu", "cuda"] = "auto"):
        self.device = self._resolve_device(device)
        self.max_memory_mb = max_memory_mb or self._get_available_memory_mb()
        self.models = OrderedDict()
        self.loaders = {}
        self.import_map = {}

    def _resolve_device(self, d):
        if d == "auto":
            try:
                import torch
                return "cuda" if torch.cuda.is_available() else "cpu"
            except ImportError:
                return "cpu"
        return d

    def _get_memory_usage_mb(self):
        if self.device == "cuda":
            try:
                import torch
                return torch.cuda.memory_allocated() / (1024 * 1024)
            except ImportError:
                print("[LazyModelManager] torch не установлен — не могу измерить VRAM.")
                return 0
        else:
            try:
                import psutil
                process = psutil.Process()
                mem = process.memory_info().rss
                return mem / (1024 * 1024)
            except ImportError:
                print("[LazyModelManager] psutil не установлен — пропускаю контроль памяти.")
                return 0

    def _get_available_memory_mb(self):
        if self.device == "cuda":
            try:
                import torch
                free, total = torch.cuda.mem_get_info()
                return int(free / (1024 * 1024))
            except Exception as e:
                print(f"[LazyModelManager] Cannot get CUDA memory: {e}")
                return 2000  # fallback
        else:
            try:
                import psutil
                available = psutil.virtual_memory().available
                return int(available / (1024 * 1024))
            except Exception as e:
                print(f"[LazyModelManager] Cannot get CPU memory: {e}")
                return 2000  # fallback

    def register(self, name: str, loader: Callable, imports: list[str] = None):
        self.loaders[name] = loader
        if imports:
            self.import_map[name] = imports

    def _lazy_import(self, name):
        for module_name in self.import_map.get(name, []):
            if module_name not in globals():
                globals()[module_name] = importlib.import_module(module_name)

    def _try_unload(self, model):
        try:
            del model
        except Exception:
            pass

    def get(self, name: str):
        if name in self.models:
            self.models.move_to_end(name)
            return self.models[name]

        if name not in self.loaders:
            raise ValueError(f"Model '{name}' not registered.")

        self._lazy_import(name)

        # Выгрузка моделей по памяти (CPU или GPU)
        while self._get_memory_usage_mb() > self.max_memory_mb and self.models:
            old_name, old_model = self.models.popitem(last=False)
            print(f"[LazyModelManager] Unloading: {old_name} (memory control)")
            self._try_unload(old_model)

        print(f"[LazyModelManager] Loading: {name}")
        model = self.loaders[name]()
        self.models[name] = model
        return model

    def list_loaded(self):
        return list(self.models.keys())

    def _resolve_transformer_class(self, model_name: str, task: str = None) -> str:
        name = model_name.lower()
        if task == "causal-lm" or any(k in name for k in ["gpt", "llama", "mistral", "rwkv", "opt"]):
            return "AutoModelForCausalLM"
        if task == "seq2seq" or any(k in name for k in ["t5", "bart", "mbart"]):
            return "AutoModelForSeq2SeqLM"
        if task == "token-class" or "ner" in name:
            return "AutoModelForTokenClassification"
        if task == "qa":
            return "AutoModelForQuestionAnswering"
        if "paraphrase" in name or "sentence" in name or task == "embedding":
            return "SentenceTransformer"
        return "AutoModel"

    def load_transformer_smart(self, model_name: str, task: str = None, tokenizer: bool = False):
        model_cls = self._resolve_transformer_class(model_name, task)
        key = f"transformers::{model_cls}::{model_name}::with_tokenizer={tokenizer}"

        def loader():
            if model_cls == "SentenceTransformer":
                st = importlib.import_module("sentence_transformers")
                return st.SentenceTransformer(model_name)

            tr = importlib.import_module("transformers")
            model_class = getattr(tr, model_cls)
            model = model_class.from_pretrained(model_name).to(self.device)
            if tokenizer:
                tok = tr.AutoTokenizer.from_pretrained(model_name)
                return (model, tok)
            return model

        # Выбираем правильные импорты
        imports = ["sentence_transformers"] if model_cls == "SentenceTransformer" else ["transformers"]

        self.register(key, loader, imports=imports)
        return self.get(key)

# manager = LazyModelManager(max_memory_mb=3000, device="auto")
#
# # GPT на GPU (если есть), иначе на CPU
# model = manager.load_transformer_smart("gpt2")
#
# # Список текущих моделей
# print(manager.list_loaded())