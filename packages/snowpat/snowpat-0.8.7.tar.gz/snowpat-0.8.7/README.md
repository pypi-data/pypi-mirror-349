# SNOWPAT

This is a toolbox for handling file formates most often used in Snow Science.

There are 4 submodules:
pysmet: Used to read and write SMET files
snowpackreader: Used to read SNOWPACK output files (.pro) and handle profiles easily (soon also with visualization)
SnowLense: Plotting Framework for files that can be read with this module (SMET not yet available)
icsv: Read and write iCSV Files. (Next generation SMET)
([see Documentation](http://patrick.leibersperger.gitlab-pages.wsl.ch/snowpat))

## News

2025-03-13: It is now possible to write Snowpack objects to .pro files. (If necessary also a series of profiles, could be written to a .pro file, not implemented yet). Manual JSON profiles can be written to .pro files including stability calculations.

2025-01-06: Happy New Year! New year new bugs, please update snowpat, as a function used in the plotting is deprecated in the newest matplotlib.

2024-05-05: A module to read and write iCSV files.

2024-03-25: Installation via PyPi now possible

2024-03-08: Plotting of Snow Profiles is available with SnowLense module

2024-03-01: A simple merge function is now available to join to SMET Files: merge(SMETFile, override) and mergeFromFile(filename, override)

## Installation

Installation via pip and poetry is supported. 

It is as easy as:

```bash
pip install snowpat
```

You can also install from git (needs git to be installed) to always get the latest release:

```bash
pip install [--user] git+https://gitlabext.wsl.ch/patrick.leibersperger/snowpat.git
```

the --user option might be needed if you do not have admin rights.

### Upgrade

If you already have an installation of Sowpat, that is out of date, run:

```bash
pip install [--user] --upgrade snowpat
pip install [--user] --upgrade git+https://gitlabext.wsl.ch/patrick.leibersperger/snowpat.git
```

### Manually

Download the folder, and from the main directory run:

```bash
poetry install
```

or:

```bash
pip install [--user] .
```

## Documentation

The main documentation can be found under the respective module names, i.e. pySMET and SMET, as well as snowpackreader

Extensive Documentation is available [online](http://patrick.leibersperger.gitlab-pages.wsl.ch/snowpat), it uses http, so you might get a privacy error in your browser;
Or prepuilt in artifacts.zip, whic can be found in [job artifacts](https://gitlabext.wsl.ch/patrick.leibersperger/snowpat/-/artifacts): under (Number) files download the folder.

If you download the zip folder just open index.html in your browser.

Or you can build the docs yourself.

### MkDocs

To create the docs with MkDocs:
Install via

```bash
pip install mkdocs
```

run:

```bash
mkdocs serve
```

from the main directory and follow the link shown (localhost)


## License

This project is licensed under the terms of the GNU-GPL-3.0 license.

## Examples

Please see the Documentation for more Examples and information on the full capabilities

```python
from snowpat import pysmet as smet
from snowpat import snowpackreader as spr
```

### Examples iCSV

```python
from snowpat import icsv

file = icsv.read(filename)
data_pandas = file.data
data_xarray = file.to_xarray()
# metadata and fields can be accessed with get_attribute
field_delimiter = file.metadata.get_attribute("field_delimiter")
fields = file.fields.get_attribute("fields")
# required keys will always be present, as a sanity check is done. Any other might return None if it is not available.
# To see what metadata is available, you can print the information:
file.info() # prints information about the whole file
print(file.metadata) # prints information on the metadata only
print(file.fields) # print information on the fields section

# changing metadata
file.metadata.set_attribute("field_delimiter", ":")

# and for writing to an output again (if no output filename is provided, the given filename is used with an out flag):
file.write(out_filename)

# It is possible to convert SMET files to iCSV:
from snowpat import pysmet as smet
smet_file = smet.read(smet_filename)
icsv_file = from_smet(smet_file)
```

### Examples pySMET

```python
from snowpat import pysmet as smet

file = smet.read(filename)
data_pandas = file.data
data_numpy = file.toNumpy()
# meta_data only contains the mandatory SMET metadata
station_id = file.meta_data.station_id
lon = file.meta_data.location.longitude

# optional_meta_data according to the file format can be accessed like this:
timezone = file.optional_meta_data.tz

# acdd metadata (anything preceded with acdd_ or known acdd attributes are stored in acdd metadata)
acdd_creator_name = file.acdd_meta_data.get_attribute("creator_name")

# everything else is in other metadata
value = file.other_metadata["key"]

# changing metadata
file.meta_data.station_ID = "WFJ"
file.acdd_meta_data.set_attribute("creator_name", "SomeName")

# for easier access and visibility of metadata do:
file.all_meta_data # And access values by keys in this dictionary

# and for writing to an output again (if no output filename is provided, the given filename is used with an out flag):
file.write(out_filename)

# a summary is also available wih
file.info()

#UNTESTED:
# it is also possible to merge to SMET files, as long as they are compatible (metadata and fields)
other_file = smet.read(other_filename)
file.merge(other_file)

# or
list_of_files_to_merge = [filename1, filename2,filename3,...]
merged_file = smet.merge_files(list_of_files_to_merge)
```

### Examples snowpackreader

```python
from snowpat import snowpackreader as spr
pro = spr.readPRO("test.pro")

# print a summary of the file
pro.info()

# all available dates
dates = pro.get_all_dates()

# will only return data above the ground after this
pro.discard_below_ground(True)
# get a Snowpack object (internal data class for Profiles) on a specific date
profile = pro.get_profile_on(dates[0])
# convert it to a dataframe with minimum stability and surface hoar as metadata
# column names will be data codes, except for "0500"= height (layer boundaries)-> 2 columns: layer middle and layer thickness
profile.toDf().head()
wl = profile.weak_layer # or profile.get_param["0534"]
sh = profile.surface_hoar # pr profile.get_param["0514"]

# There is help, to deal with the DataCodes:
# per default, the names are as in the .pro Header (without units)
pro.update_name_of_code("0503", "Snow Density")
density_code = pro.name_to_code("Snow Density")

# read from JSON (as best as it can)
profile, metadata, date = spr.read_json_profile("test.json")

# write profile to .pro
metadata = {
    "StationName": "Test",
    "Latitude": 47.123,
    "Longitude": 8.123,
    "Altitude": 1234,
    "SlopeAngle": 12,
    "SlopeAzi": 123
}
date = datetime.datetime.now()
pro.write_pro_file("out.pro", metadata, date)

```

Logo was creaeted with: hotpot.ai/art-generator