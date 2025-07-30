from dataclasses import dataclass, field

from hydra.core.config_store import ConfigStore
from omegaconf import MISSING  # pyright: ignore


@dataclass
class VisualEncoderConfig:
    hf_name: str = MISSING
    output_layer: int | None = None
    use_cls_token: bool = False


@dataclass
class LanguageModelConfig:
    hf_name: str = MISSING
    max_seq_length: int | None = None
    use_start_end_tokens: bool = False
    use_image_patch_token: bool = False
    image_start_token: str = "<im_start>"
    image_end_token: str = "<im_end>"
    image_patch_token: str = "<im_patch>"
    ignore_index: int = -100
    image_token_index: int = -200
    padding_side: str = "left"


@dataclass
class ConnectorConfig:
    name: str = MISSING
    type: str = MISSING


@dataclass
class ModelConfig:
    name: str = MISSING
    visual_encoder: VisualEncoderConfig = field(default_factory=VisualEncoderConfig)
    language_model: LanguageModelConfig = field(default_factory=LanguageModelConfig)
    connector: ConnectorConfig = field(default_factory=ConnectorConfig)


@dataclass
class DatasetConfig:
    name: str = MISSING
    path: str = MISSING
    type: str = "json"
    lazy_preprocess: bool = True
    is_multimodal: bool = True
    early_mix_text: bool = False
    image_folder: str = MISSING
    image_aspect_ratio: str = "square"
    image_token: str = "<image>"


@dataclass
class UnfreezeConfig:
    train_vision_model: bool = True
    train_language_model: bool = True
    train_connector: bool = True


@dataclass
class LearningRateConfig:
    visual_encoder_learning_rate: float = 1e-4
    language_model_learning_rate: float = 1e-4
    connector_learning_rate: float = 1e-4
    default_lr: float = 1e-4


@dataclass
class WeightDecayConfig:
    visual_encoder_weight_decay: float = 0.0
    language_model_weight_decay: float = 0.0
    connector_weight_decay: float = 0.0
    default_wd: float = 0.0


@dataclass
class TrainerConfig:
    output_dir: str = "."
    unfreeze: UnfreezeConfig = field(default_factory=UnfreezeConfig)
    learning_rate: LearningRateConfig = field(default_factory=LearningRateConfig)
    weight_decay: WeightDecayConfig = field(default_factory=WeightDecayConfig)
    per_device_train_batch_size: int = 16
    per_device_eval_batch_size: int = 4
    bf16: bool = False
    fp16: bool = False
    tf32: bool = False
    deepspeed: str | None = None
    num_train_epochs: int = 1
    save_strategy: str = "steps"
    save_steps: int = 5000
    save_total_limit: int = 20
    logging_steps: int = 1
    warmup_ratio: float = 0.0
    lr_scheduler_type: str = "linear"
    gradient_accumulation_steps: int = 1
    report_to: str | None = None
    dataloader_num_workers: int = 0
    version: str = "v0"
    group_by_modality_length: bool = False
    gradient_checkpointing: bool = False
    run_name: str = "small-vlm"
    resume_from_checkpoint: str | None = None
    from_pretrained: str | None = None
    seed: int = 42
    attn_implementation: str | None = "flash_attention_2"


@dataclass
class InferenceConfig:
    checkpoint_path: str = MISSING
    num_inference_samples: int | None = None
    chat_template: str = "plain"


@dataclass
class AppConfig:
    is_training: bool = True
    model: ModelConfig = field(default_factory=ModelConfig)
    dataset: DatasetConfig = field(default_factory=DatasetConfig)
    trainer: TrainerConfig = field(default_factory=TrainerConfig)
    inference: InferenceConfig = field(default_factory=InferenceConfig)


def register_configs() -> None:
    cs: ConfigStore = ConfigStore.instance()
    cs.store(name="cfg", node=AppConfig)
