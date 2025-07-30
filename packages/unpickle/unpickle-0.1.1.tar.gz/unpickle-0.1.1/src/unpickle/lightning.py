import sys
import torch
import types
from torch.serialization import get_unsafe_globals_in_checkpoint, safe_globals


def stub(fullname: str) -> tuple[type, str]:
    """
    Creates a stub class to safely load PyTorch checkpoints with missing dependencies.

    When loading a PyTorch checkpoint that references classes from modules that are no longer
    available, this function creates minimal placeholder classes to allow loading the weights
    without requiring the original dependencies.

    Args:
        fullname: Fully qualified name of the class to stub (e.g. "module.submodule.MyClass")

    Returns:
        A tuple containing:
        - The created stub class
        - The fully qualified name of the original class

    This is useful when you want to load weights from a checkpoint but don't need or can't
    access the original model architecture/classes, only caring about the parameter values.
    """
    modpath, _, clsname = fullname.rpartition(".")

    # Ensure the parent module can be imported even if it's not present
    module = sys.modules.setdefault(modpath, types.ModuleType(modpath))

    # Create an inert placeholder class
    Dummy = type(clsname, (), {})

    setattr(module, clsname, Dummy)

    return (Dummy, fullname)  # (<object>, "qualified.path")


def load_ckpt_robustly(ckpt_path: str) -> dict:
    unsafe = get_unsafe_globals_in_checkpoint(ckpt_path)
    if not unsafe:
        return torch.load(ckpt_path, weights_only=True)

    with safe_globals([stub(name) for name in unsafe]):
        return torch.load(ckpt_path, weights_only=True)


def extract_state_dict_from_lightning_ckpt(ckpt_path: str) -> dict:
    return load_ckpt_robustly(ckpt_path)["state_dict"]