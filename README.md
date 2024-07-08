# CloudSatiPy
Read CloudSat HDF files into xarray datasets

This package is designed to be a lightweight but versatile method for loading Cloudsat data products produced by the Cloudsat DPC ([(https://www.cloudsat.cira.colostate.edu/)](https://www.cloudsat.cira.colostate.edu/)).

The minimal requirements can be installed from conda using the following:

```conda install -c conda-forge --yes --file conda-requirements.txt```

Alternatively, a complete environment for running the examples can be created by running:

```conda env create -f environment.yml --yes```

The cloudsatipy module contains a single function, `open_cloudsat`, which can be used to read Cloudsat HDF files:

```
from cloudsatipy import open_cloudsat
ds = open_cloudsat(cloudsat_filename, [variables=optional_list_of_vars_to_read])
```

Under the hood, it utilises a reader class, which can be used if you need to load variables in later in processing:

```
from cloudsatipy.reader import CloudsatReader
reader = CloudsatReader(cloudsat_filename)
ds = reader.data
...do some processing...
reader.read_data(requested_variable)
new_ds = reader.data
```

A number of jupyter notebooks showing different applications can be found in the `examples` folder
