# Импортируй свой LazyModelManager как он у тебя уже есть
from lazymodelmanager import LazyModelManager  # или просто из текущего файла

max_loaded_memory=1024*6
# Глобальный экземпляр
_lazy_model_manager = LazyModelManager(max_memory_mb=max_loaded_memory)

# Основная обёртка
def lazy_model_transformer(model_name: str, task: str = None, tokenizer: bool = False):
    """
    Умная ленивая загрузка модели transformers по имени.
    Использует глобальный LazyModelManager.
    """
    return _lazy_model_manager.load_transformer_smart(model_name, task=task, tokenizer=tokenizer)

# Явная загрузка с указанием класса модели
def lazy_model_transformer_explicit(model_name: str, model_cls: str, tokenizer: bool = False):
    """
    Явная загрузка модели transformers по имени и типу класса.
    Например: model_cls = "AutoModelForCausalLM"
    """
    key = f"transformers::{model_cls}::{model_name}::with_tokenizer={tokenizer}"

    def loader():
        tr = __import__("transformers")
        model_class = getattr(tr, model_cls)
        model = model_class.from_pretrained(model_name)
        if tokenizer:
            tok = tr.AutoTokenizer.from_pretrained(model_name)
            return model, tok
        return model

    _lazy_model_manager.register(key, loader, imports=["transformers"])
    return _lazy_model_manager.get(key)

# Явный доступ к текущему менеджеру, если вдруг нужно
def get_lazy_model_manager():
    return _lazy_model_manager
