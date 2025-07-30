import shutil
from pathlib import Path
from typing import Any

from nrp_devtools.config.config import OARepoConfig

from ..utils import run_cmdline


def copy_translations(config: OARepoConfig, **kwargs: Any):
    # copy translations from site_packages' oarepo/collected_translations to site_packages,
    # overwriting any existing ones
    site_packages_dir = run_cmdline(
        "python",
        "-c",
        "import site; print(site.getsitepackages()[0])",
        grab_stdout=True,
    ).strip()

    collected_translations_dir = (
        Path(site_packages_dir) / "oarepo" / "collected_translations"
    )
    if not collected_translations_dir.exists():
        print(
            f"Warning: {collected_translations_dir} does not exist, "
            "skipping copying translations"
        )
        return
    for translation_file in collected_translations_dir.glob("**/*"):
        relative_path = translation_file.resolve().relative_to(
            collected_translations_dir.resolve()
        )
        source_path = translation_file.resolve()
        target_path = Path(site_packages_dir) / relative_path
        target_path.parent.mkdir(parents=True, exist_ok=True)
        print(f"Copying translations file {translation_file} to {target_path}")
        shutil.copy(source_path, target_path)
