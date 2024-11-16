import os
import importlib.util
from inspect import signature
import numpy as np

QUALITY_CHECKS = "QUALITY_CHECKS"
BASE_DIR = "BASE_DIR"

def load_quality_checkers(config):
    directory = config[QUALITY_CHECKS][BASE_DIR]

    quality_checkers = {}

    for file in os.listdir(directory):
        if file.endswith(".py") and file != os.path.basename(__file__):
            module_name = file[:-3]  # Remove ".py" extension
            module_path = os.path.join(directory, file)

            # Dynamically import the module (the file)
            spec = importlib.util.spec_from_file_location(module_name, module_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            # Inspect module for functions with the expected inputs/outputs (this allows to have >1 function per file also)
            for attr_name in dir(module):
                attr = getattr(module, attr_name)
                if callable(attr):
                    sig = signature(attr)
                    params = list(sig.parameters.values())
                    if (len(params) >= 1 and params[0].name == "img" and params[1].name == "args" and sig.return_annotation == bool):
                        quality_checkers[attr_name] = attr

    return quality_checkers


if __name__ == "__main__":
    config = {}
    config[QUALITY_CHECKS] = {}
    config[QUALITY_CHECKS][BASE_DIR] = './backend/quality_checker'

    quality_checkers = load_quality_checkers(config)

    print("Loaded Quality Checkers:")
    for func_name, func in quality_checkers.items():
        print(f"  Function: {func_name}, From File: {func.__module__}.py")

    dummy_image = np.zeros((100, 100, 3), dtype=np.uint8)

    test_args = {
        "check_black_white": (10,),
        "check_random": (70,),
    }

    print("\nTesting Quality Checkers:")
    for func_name, func in quality_checkers.items():
        try:
            args = test_args.get(func_name, ())
            result = func(dummy_image, *args)
            print(f"  {func_name}: Returned {result} with args {args}")
        except Exception as e:
            print(f"  {func_name}: Error - {e}")