import importlib.resources as resources
from pathlib import Path

from src.cli.commands import cmd_demo


def test_sample_dataset_ships_inside_the_package():
    """The demo dataset must travel inside the installed package.

    Until issue #26 it lived in `examples/` at the repository root, which
    setuptools never copied into the wheel: `pip install msgram` produced a
    `msgram demo` that could not find its own data.
    """
    dataset = resources.files("src.cli.examples").joinpath("analytics-raw-data")

    assert dataset.is_dir()
    assert any(entry.name.endswith(".json") for entry in dataset.iterdir())


def test_find_raw_data_dir_resolves_inside_the_package():
    """The lookup must not depend on the repository layout.

    Walking up the parents of the module only works while the code sits in a
    checkout. Once installed in site-packages there is no `examples/` above it,
    so the resolved path has to live under the `src/cli` package itself.
    """
    package_root = Path(cmd_demo.__file__).resolve().parent.parent

    assert package_root in cmd_demo.find_raw_data_dir().resolve().parents
