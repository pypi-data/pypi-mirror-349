import importlib.util
import argparse
from pathlib import Path
from jumla.dataset import Dataset
from jumla.log import logger
from os.path import join
import traceback


def main():
    parser = argparse.ArgumentParser(
        description="Jumla: Generate Lean tasks from Python specs."
    )
    parser.add_argument("path", help="Path to example .py file OR folder of examples")
    parser.add_argument("--log", action="store_true", help="Print debug logs")
    parser.add_argument(
        "--out", default="dataset", help="Base output directory for generated tasks"
    )
    args = parser.parse_args()

    path = Path(args.path)

    if not path.exists():
        logger.error(f"[✗] Not found: {path}")
        return

    if path.is_dir():
        py_files = list(path.glob("*.py"))
        logger.info(f"Processing {len(py_files)} files in {path}")
        if not py_files:
            logger.warn(f"[!] No .py files found in {path}")
            return
        for i, py_file in enumerate(py_files):
            task_id = f"task_id_{i}"
            logger.info(f"[{task_id}] {py_file.name}")
            write_to_dataset(py_file, task_id=task_id, log=args.log, base_dir=args.out)
        logger.finish()
    elif path.suffix == ".py":
        write_to_dataset(path, "task_id_0", log=args.log, base_dir=args.out)
        logger.finish()
    else:
        logger.error(f"[✗] Invalid file type: {path.name} (expected .py or directory)")


def create_dataset(path: Path, dir_name: str) -> Dataset:
    """Load a Dataset object or construct one from raw fields in a Python file."""
    spec = importlib.util.spec_from_file_location("example", path)

    if spec is None:
        raise ImportError(f"Could not create import spec for {path}")

    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None, f"No loader for module {path}"
    spec.loader.exec_module(module)

    required = ["function", "description_doc", "input_doc", "output_doc", "test_cases"]
    if not all(hasattr(module, key) for key in required):
        raise AttributeError(
            f"{path} must define either `dataset` or all of: {', '.join(required)}"
        )

    return Dataset(
        function=module.function,
        description_doc=module.description_doc,
        input_doc=module.input_doc,
        output_doc=module.output_doc,
        test_cases=module.test_cases,
        dir=dir_name,
    )


def write_to_dataset(path: Path, task_id: str, log=False, base_dir="dataset"):
    try:
        full_dir = join(base_dir, task_id) + "/"
        dataset = create_dataset(path, dir_name=full_dir)
        dataset.write_all(log=log)
    except Exception as e:
        logger.error(f"{path.name}: Failed on {e}")
        traceback.print_exc()
