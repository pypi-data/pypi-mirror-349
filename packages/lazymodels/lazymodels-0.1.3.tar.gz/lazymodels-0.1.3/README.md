# lazymodels

**LazyModels** is a lightweight utility for lazy-loading HuggingFace Transformers and managing memory automatically, both on CPU and GPU.

It keeps only the models you need in memory and unloads older ones when memory limits are exceeded. Works out of the box in one line of code:

```python
from lazymodels import lazy_model_transformer

model = lazy_model_transformer("gpt2")
````

## 🔥 Features

* ✅ Lazy loading of models by name
* ✅ Smart task detection: causal-lm, seq2seq, token classification, etc.
* ✅ Automatic unloading when RAM or VRAM usage exceeds the limit
* ✅ One global manager to control all memory
* ✅ Transformers support out of the box

## 📦 Example

```python
from lazymodels import lazy_model_transformer

# Load a causal LM model
model = lazy_model_transformer("gpt2")

# Load a seq2seq model with tokenizer
model2, tokenizer = lazy_model_transformer("t5-small", tokenizer=True)
```

## ⚙️ Requirements

* `torch`
* `transformers`
* `psutil`

---

Licensed under MIT.