from __future__ import annotations
from dataclasses import dataclass, asdict, field
from typing import Dict, Any, Optional


@dataclass
class PlaNetConfig:
    hidden_dim: int = 128
    nr: int = 64
    nz: int = 64
    n_measures: int = 302

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    def __repr__(self) -> str:
        s = f"{self.__class__.__name__} with arguments: \n"
        for attr in vars(self).keys():
            s += f"    {attr}: {getattr(self, attr)}\n"
        return s


@dataclass
class Config:
    is_physics_informed: bool = True
    dataset_path: str = ""
    batch_size: int = 64
    epochs: int = 10
    planet_config: Dict[str, int] = field(default_factory=dict)
    planet: PlaNetConfig = field(default_factory=PlaNetConfig)
    log_to_wandb: bool = False
    wandb_project: Optional[str] = None
    save_checkpoints: bool = False
    save_path: str = "tmp/"
    resume_from_checkpoint: bool = False
    num_workers: int = 0
    do_super_resolution: bool = False

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, config_dict: Dict[str, Any]) -> Config:

        cls_instance = cls()
        for k, v in config_dict.items():
            if k in cls_instance.__dict__.keys():
                setattr(cls_instance, k, v)

        if hasattr(cls_instance, "planet"):
            assert (
                cls_instance.planet is not None
            ), "must provide valid config.planet, got None"
            cls_instance.planet = PlaNetConfig(**cls_instance.planet_config)

        return cls_instance

    def __repr__(self) -> str:
        s = f"{self.__class__.__name__} with arguments: \n"
        for attr in vars(self).keys():
            s += f"    {attr}: {getattr(self, attr)}\n"
        return s.replace("\n\n", "\n")
