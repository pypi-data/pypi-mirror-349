# PyEvoMotion

A software to assess the evolution dynamics of a set of related DNA sequences.

_(See [Goiriz L, et al.](http://doi.org/10.1073/pnas.2303578120))_

## Installation

> **Note:**
> `PyEvoMotion` uses [mafft](https://mafft.cbrc.jp/alignment/software/) to do the sequence alignment. If it's not available in your system, on the first run of `PyEvoMotion`, it will ask to install it locally.
> 
> If so, ensure to restart your shell session or run `source ~/.bashrc` to update the PATH environment variable, so that the `mafft` executable is available in your shell.
>
> To install `PyEvoMotion` you may clone the repository and run `pip install`, or install it from PyPI:

```bash
pip install PyEvoMotion
```

This will install the package and its dependencies _(but not the tests nor the test data)_. To check if the installation was successful, you can run the following command:

```bash
PyEvoMotion
```

If the installation was successful, you should see the following output:

```bash
Welcome to Rodrigolab's
 _____       ______          __  __       _   _
|  __ \     |  ____|        |  \/  |     | | (_)
| |__) |   _| |____   _____ | \  / | ___ | |_ _  ___  _ __
|  ___/ | | |  __\ \ / / _ \| |\/| |/ _ \| __| |/ _ \| '_ \
| |   | |_| | |___\ V / (_) | |  | | (_) | |_| | (_) | | | |
|_|    \__, |______\_/ \___/|_|  |_|\___/ \__|_|\___/|_| |_|
        __/ |
       |___/

usage: PyEvoMotion [-h] [-dt DELTA_T] [-sh] [-ep] [-l LENGTH_FILTER] [-xj] [-ij IMPORT_JSON] [-k {all,total,substitutions,insertions,deletions,indels}] [-f FILTER [FILTER ...]] [-gp GENOME_POSITIONS] [-dr DATE_RANGE]
                   seqs meta out

PyEvoMotion

positional arguments:
  seqs                  Path to the input fasta file containing the sequences.
  meta                  Path to the corresponding metadata file for the sequences.
  out                   Path to the output filename prefix used to save the different results.

options:
  -h, --help            show this help message and exit
  -dt DELTA_T, --delta_t DELTA_T
                        Time interval to calculate the statistics. Default is 7 days (7D).
  -sh, --show           Show the plots of the analysis.
  -ep, --export_plots   Export the plots of the analysis.
  -l LENGTH_FILTER, --length_filter LENGTH_FILTER
                        Length filter for the sequences (removes sequences with length less than the specified value). Default is 0.
  -xj, --export_json    Export the run arguments to a json file.
  -ij IMPORT_JSON, --import_json IMPORT_JSON
                        Import the run arguments from a JSON file. If this argument is passed, the other arguments are ignored. The JSON file must contain the mandatory keys 'seqs', 'meta', and 'out'.
  -k {all,total,substitutions,insertions,deletions,indels}, --kind {all,total,substitutions,insertions,deletions,indels}
                        Kind of mutations to consider for the analysis. Default is 'all'.
  -f FILTER [FILTER ...], --filter FILTER [FILTER ...]
                        Specify filters to be applied on the data with keys followed by values. If the values are multiple, they must be enclosed in square brackets. Example: --filter key1 value1 key2 [value2 value3]
                        key3 value4. If either the keys or values contain spaces, they must be enclosed in quotes. keys must be present in the metadata file as columns for the filter to be applied. Use '*' as a
                        wildcard, for example Bio* to filter all columns starting with 'Bio'.
  -gp GENOME_POSITIONS, --genome_positions GENOME_POSITIONS
                        Genome positions to restrict the analysis. The positions must be separated by two dots. Example: 1..1000. Open start or end positions are allowed by omitting the first or last position,
                        respectively. If not specified, the whole reference genome is considered.
  -dr DATE_RANGE, --date_range DATE_RANGE
                        Date range to filter the data. The date range must be separated by two dots and the format must be YYYY-MM-DD. Example: 2020-01-01..2020-12-31. If not specified, the whole dataset is
                        considered. Note that if the origin is specified, the most restrictive date range is considered.

Error: the following arguments are required: seqs, meta, out
```

## Tests

This package has been developed using `pytest` for testing. To run the tests, you may install PyEvoMotion from the `sdist` archive, decompress it, install it and run the tests:

```bash
pip download --no-deps --no-binary :all: PyEvoMotion
tar -xvzf pyevomotion-*.tar.gz
cd pyevomotion-*/
pip install .
PyEvoMotion # To trigger mafft installation. Ensure afterwards that mafft is available in your PATH.
pytest
```

> [!WARNING]
> The first time the tests are run, they will automatically download the test data from `https://sourceforge.net/projects/pyevomotion/files/test_data.zip/download` and extract it in the appropriate directory.
>
> Given the size of the test data, this may take a while.


## Docker

A Docker image containing a virtual environment with `PyEvoMotion` pre-installed, its dependencies, the test data is available at `ghcr.io/luksgrin/pyevomotion:latest` and the manuscript's original figure script is available at `ghcr.io/luksgrin/pyevomotion-fig:latest`.

Pull the image from by running:

```bash
docker pull ghcr.io/luksgrin/pyevomotion:latest
```

Alternatively, to build the main image, run:

```bash
docker build -t ghcr.io/luksgrin/pyevomotion:latest -f docker/Dockerfile
```

### Running the container

To start an interactive container:

```bash
docker run -it ghcr.io/luksgrin/pyevomotion:latest
```

This will open a prompt that displays a welcome message and allows you to start using `PyEvoMotion` right away.

### Included data

The image includes (heavy) input files (FASTA and metadata) in:

```bash
/home/pyevomotion/pyevomotion-*/tests/data/test3
```

which are used by the test suite (and are automatically downloaded and extracted if not present, thereby using the containerized version is more convenient).

Also, the source script for figure generation (along with the pre-generated results of running `PyEvoMotion`) is already available under:

```bash
/home/pyevomotion/pyevomotion-*/share
```

Do note that if all the contents within

```bash
/home/pyevomotion/pyevomotion-*/share
```

are deleted except for the `manuscript_figure.py` script, it is still possible to generate the figure (although it will take much longer since the dataset's stats must be computed by `PyEvoMotion`).

### Running tests

Once inside the container, run:

```bash
cd pyevomotion-*
pytest
```

This will execute the test suite included with the source.

### Reproducing the Figure from the original manuscript

To reproduce the figure from the original manuscript, run:

```bash
cd pyevomotion-*
python share/manuscript_figure.py export
```

The figure will be saved in the `share` directory. Font warnings may appear — they are safe to ignore and do not affect the scientific content of the figure, only the styling.