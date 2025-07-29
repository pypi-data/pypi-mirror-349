import xarray as xr
from .icsv_file import iCSVFile, VERSIONS
import pandas as pd
import datetime
from typing import Optional
import warnings

FIRSTLINES_2DTIMESERIES = [f"# iCSV {version} UTF-8 2DTIMESERIES" for version in VERSIONS]

class iCSV2DTimeseries(iCSVFile):
    """
    Class to represent an iCSV file containing 2D timeseries data.

    The iCSV2DTimeseries extends the iCSVFile class to handle the specific structure
    and requirements of 2D timeseries data, which includes multiple timestamped
    measurements.

    Attributes (additional to iCSVFile):
        dates (list): List of datetime objects representing measurement dates in the file.
        date_lines (list): List of line numbers where date entries begin in the file.
        data (dict): Dictionary mapping datetime objects to pandas DataFrames containing
                    the 2D timeseries data for that timestamp.

    Key Features:
        - Handles multiple time-stamped 2D timeseries in a single file
        - Can convert to xarray Dataset for multi-dimensional data analysis

    The 2D timeseries format follows the iCSV specification with the addition of
    [DATE=timestamp] markers in the data section to separate measurements from
    different dates. Each profile can include a 'layer_index' field to identify
    profile layers.
    """
    def __init__(self, filename: str = None):
        self.dates = []
        self.date_lines = []
        super().__init__(filename)

    def _parse_comment_line(self, line, section, line_number):
        if line == "[METADATA]":
            return "metadata"
        elif line == "[FIELDS]":
            self.metadata.check_validity()  # to parse fields we need valid metadata
            return "fields"
        elif line == "[DATA]":
            return "data"
        else:
            return self._parse_section_line(line, section, line_number)

    def _parse_section_line(self, line, section, line_number):
        if not section:
            raise ValueError("No section specified")
        line_vals = line.split("=")
        if len(line_vals) != 2:
            raise ValueError(f"Invalid {section} line: {line}, got 2 assignment operators \"=\"")

        if section == "metadata":
            self.metadata.set_attribute(line_vals[0].strip(), line_vals[1].strip())
        elif section == "fields":
            fields_vec = [field.strip() for field in line_vals[1].split(self.metadata.get_attribute("field_delimiter"))]
            self.fields.set_attribute(line_vals[0].strip(), fields_vec)
        elif section == "data":
            if "[DATE=" in line:
                date_str = line.split('[DATE=')[1].split(']')[0].strip()
                self.dates.append(datetime.datetime.fromisoformat(date_str))
                self.date_lines.append(line_number)
            else:
                raise ValueError(f"Invalid data line: {line}")

        return section

    def load_file(self, filename: str = None):
        """Loads an iCSV file and parses its contents, extracting the dates and data lines for a 2D timeseries.

        Args:
            filename (str, optional): The path to the iCSV file. If not provided, the previously set filename will be used.

        Raises:
            ValueError: If the file is not a valid iCSV file or if the data section is not specified.

        Returns:
            None
        """
        self.data = dict()
        if filename:
            self.filename = filename

        section = ""
        with open(self.filename, 'r') as file:
            first_line = file.readline().rstrip()  # rstrip() is used to remove the trailing newline
            if first_line not in FIRSTLINES_2DTIMESERIES:
                raise ValueError("Not an iCSV file with the 2D timeseries application profile")

            line_number = 1 # need to find the line number where the data starts
            for line in file:
                line_number += 1
                if line.startswith("#"):
                    line = line[1:].strip()
                    section = self._parse_comment_line(line.strip(), section, line_number)
                else:
                    if section != "data":
                        raise ValueError("Data section was not specified")


        for (i, date) in enumerate(self.dates):
            first_data_line = self.date_lines[i]
            last_data_line = self.date_lines[i+1] if i+1 < len(self.dates) else line_number + 1
            self.data[date] = pd.read_csv(self.filename, skiprows=first_data_line, nrows=last_data_line-first_data_line-1, header=None, sep=self.metadata.get_attribute("field_delimiter"))
            self.data[date].columns = self.fields.fields

        self.fields.check_validity(self.data[self.dates[0]].shape[1]) # check if the number of fields match the number of columns
        self.parse_geometry()

    def info(self):
        """
        Prints information about the object and its data.

        This method prints the object itself and the head of its data.

        Args:
            None

        Returns:
            None
        """
        print(self)
        print("\nDates:")
        print(self.dates)
        print("\nFirst Profile:")
        print(self.data[self.dates[0]].head())

    def to_xarray(self):
        """
        Converts the data to a single 3D xarray Dataset with 'time' as one dimension.

        Returns:
            xarray.Dataset: The combined xarray dataset.
        """

        # Convert each DataFrame to xarray DataArray
        arrays = []
        for date in self.dates:
            df = self.data[date].copy()
            if "layer_index" in df.columns:
                df.set_index("layer_index", inplace=True)
            arrays.append(df.to_xarray())
        # Concatenate along new time dimension
        ds = xr.concat(arrays, dim="time")
        ds = ds.assign_coords(time=self.dates)
        # Optionally add metadata
        ds.attrs = self.metadata.metadata
        return ds

    def setData(self, timestamp: datetime.datetime, data: pd.DataFrame, colnames: Optional[list] = None):
        if not self.data:
            self.data = dict()
        self.dates.append(timestamp)
        self.data[timestamp] = data

    def write(self, filename: str = None):
        """
        Writes the metadata, fields, and data to a CSV file.

        Args:
            filename (str, optional): The name of the file to write. If not provided, the current filename will be used.

        Returns:
            None
        """

        if filename:
            self.filename = filename

        self.metadata.check_validity()
        if "source" not in self.metadata.metadata:
            warnings.warn("source is a recommended metadata for the 2D timeseries application profile, but could not be found")
        first_key = self.dates[0]
        self.fields.check_validity(self.data[first_key].shape[1])
        if "layer_index" not in self.fields.fields:
            warnings.warn("layer_index is a recommended field for the 2D timeseries application profile, but could not be found")
            
        with open(self.filename, 'w') as file:
            file.write(f"{FIRSTLINES_2DTIMESERIES[-1]}\n")
            file.write("# [METADATA]\n")
            for key, val in self.metadata.metadata.items():
                file.write(f"# {key} = {val}\n")
            file.write("# [FIELDS]\n")
            for key, val in self.fields.all_fields.items():
                fields_string = self.metadata.get_attribute("field_delimiter").join(str(value) for value in val)
                file.write(f"# {key} = {fields_string}\n")
            file.write("# [DATA]\n")
            for date in self.dates:
                file.write(f"# [DATE={date.isoformat()}]\n")
                self.data[date].to_csv(file, mode='a', index=False, header=False, sep=self.metadata.get_attribute("field_delimiter") )


def append_timepoint(filename: str, timestamp: datetime.datetime, data: pd.DataFrame, field_delimiter: str = ","):
    """
    Appends a new timepoint to the iCSV file.

    Args:
        filename (str): The name of the file to append to.
        timestamp (datetime.datetime): The timestamp of the new timepoint.
        data (pd.DataFrame): The data to append.

    Returns:
        None
    """
    with open(filename, 'a') as file:
        file.write(f"# [DATE={timestamp.isoformat()}]\n")
        data.to_csv(file, mode='a', index=False, header=False, sep=field_delimiter)
