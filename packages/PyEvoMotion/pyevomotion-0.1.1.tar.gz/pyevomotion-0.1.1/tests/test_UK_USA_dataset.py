import os
import pytest
import subprocess
from datetime import datetime
from .helpers.test_UK_USA_dataset_helpers import check_data_exists, download_data_zip, extract_data_zip, generate_sampled_df, generate_figure_df

# Setup
@pytest.fixture
def setup():
    if not check_data_exists():
        download_data_zip()
        extract_data_zip()
    return datetime.now().strftime('%Y%m%d%H%M%S')


# General helper function for testing dataset parsing
def run_dataset_test(setup, meta_file_path, seq_file_path, output_prefix):
    """Abstracted logic to test PyEvoMotion on a dataset."""
    
    _date = setup
    _dt = "7D"
    _size = 100  # Feel free to change this value
    os.makedirs(f"tests/data/test3/output/{_date}", exist_ok=True)

    _filename = generate_sampled_df(
        meta_file_path,
        _date,
        _dt,
        _size
    )

    # Invoke PyEvoMotion as if it were a command line tool
    result = subprocess.run(
        [
            "PyEvoMotion",
            seq_file_path,
            _filename,
            f"tests/data/test3/output/{_date}/{output_prefix}",
            "-k", "total",
            "-dt", _dt,
            "-dr", "2020-10-01..2021-08-01",
            "-ep",
            "-xj",
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    # Check for known errors that happen when random sampling is defficient
    if ("ValueError: No groups with at least 2 observations" in result.stderr) or ("ValueError: The dataset is (almost) empty at this point of the analysis." in result.stderr):
        pytest.skip("Skipped due to insufficient observations in random input. Consider re-running this particular test.")

    assert os.path.exists(f"tests/data/test3/output/{_date}/{output_prefix}_plots.pdf")

def run_fig_test(setup, set, meta_file_path, seq_file_path, output_prefix, dt="7D"):
    _date = setup
    _dt = dt
    os.makedirs(f"tests/data/test3/output/{_date}", exist_ok=True)

    _filename = generate_figure_df(
        meta_file_path,
        _date,
        set
    )

    # Invoke PyEvoMotion as if it were a command line tool
    result = subprocess.run(
        [
            "PyEvoMotion",
            seq_file_path,
            _filename,
            f"tests/data/test3/output/{_date}/{output_prefix}",
            "-k", "total",
            "-dt", _dt,
            "-dr", "2020-10-01..2021-08-01",
            "-ep",
            "-xj",
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    # Check for known errors that happen when random sampling is defficient
    if ("ValueError: No groups with at least 2 observations" in result.stderr) or ("ValueError: The dataset is (almost) empty at this point of the analysis." in result.stderr):
        pytest.skip("Skipped due to insufficient observations in random input. Consider re-running this particular test.")
    if result.stderr:
        print(result.stdout)
        print(result.stderr)
    assert os.path.exists(f"tests/data/test3/output/{_date}/{output_prefix}_plots.pdf")

def test_UK_dataset(setup):
    """Tests that PyEvoMotion can parse the UK dataset correctly.
    """
    run_dataset_test(
        setup,
        "tests/data/test3/test3UK.tsv",
        "tests/data/test3/test3UK.fasta",
        "UKout"
    )

def test_USA_dataset(setup):
    """Tests that PyEvoMotion can parse the USA dataset correctly.
    """
    run_dataset_test(
        setup,
        "tests/data/test3/test3USA.tsv",
        "tests/data/test3/test3USA.fasta",
        "USAout"
    )

def test_UK_figure_dataset(setup):
    """Tests that PyEvoMotion can generate the UK corresponding figure from the manuscript.
    """
    run_fig_test(
        setup,
        "UK",
        "tests/data/test3/test3UK.tsv",
        "tests/data/test3/test3UK.fasta",
        "UKout_fig"
    )

def test_USA_figure_dataset(setup):
    """Tests that PyEvoMotion can generate the USA corresponding figure from the manuscript.
    """
    run_fig_test(
        setup,
        "USA",
        "tests/data/test3/test3USA.tsv",
        "tests/data/test3/test3USA.fasta",
        "USAout_fig"
    )

def test_UK_5D_dataset(setup):
    """Tests that PyEvoMotion runs correctly with a 5D time-window (for example).
    """
    run_fig_test(
        setup,
        "UK",
        "tests/data/test3/test3UK.tsv",
        "tests/data/test3/test3UK.fasta",
        "UKout_5D",
        dt="5D"
    )

def test_UK_10D_dataset(setup):
    """Tests that PyEvoMotion runs correctly with a 5D time-window (for example).
    """
    run_fig_test(
        setup,
        "UK",
        "tests/data/test3/test3UK.tsv",
        "tests/data/test3/test3UK.fasta",
        "UKout_10D",
        dt="10D"
    )

def test_UK_14D_dataset(setup):
    """Tests that PyEvoMotion runs correctly with a 14D time-window (for example).
    """
    run_fig_test(
        setup,
        "UK",
        "tests/data/test3/test3UK.tsv",
        "tests/data/test3/test3UK.fasta",
        "UKout_14D",
        dt="14D"
    )