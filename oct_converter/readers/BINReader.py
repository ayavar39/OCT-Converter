from __future__ import annotations
import numpy as np
from pathlib import Path


class BINReader(object):
    """Class for extracting data from a generic .bin file format.

    Attributes:
        filepath: path to the .bin file for reading.
        header_size: size of the header in bytes (if applicable).
        num_slices: number of slices in the data.
        width: width of each slice.
        height: height of each slice.
        num_channels: number of channels in each pixel.
    """

    def __init__(self, filepath: str, header_size: int = 0,
                 num_slices: int = 100, width: int = 1000, height: int = 512,
                 num_channels: int = 3, prototype: str='zeiss') -> None:
        self.filepath = Path(filepath)
        self.header_size = header_size
        self.num_slices = num_slices
        self.width = width
        self.height = height
        self.num_channels = num_channels
        self.prototype = prototype
        if not self.filepath.exists():
            raise FileNotFoundError(self.filepath)

    def read_data(self) -> np.ndarray:
        """Reads data from the .bin file.

        Returns:
            numpy.ndarray containing the data with the specified shape.
        """
        with open(self.filepath, "rb") as f:
            if self.header_size > 0:
                # Skip the header if it exists
                f.seek(self.header_size)
            
            if self.num_channels > 1: 
            
                # Calculate the total number of elements in the data array
                num_elements = self.num_slices * self.width * self.height * self.num_channels
    
                # Read the data into a numpy array with the specified shape and data type
                data = np.fromfile(f, dtype=np.uint8, count=num_elements)
                
                # Reshape the data to match the specified shape
                data = data.reshape(self.num_slices, self.width, self.height, self.num_channels)
            
            else:
                # Calculate the total number of elements in the data array
                num_elements = self.num_slices * self.width * self.height * self.num_channels
                # Read the data into a numpy array with the specified shape and data type
                data = np.fromfile(f, dtype=np.uint8, count=num_elements)
                
                # Reshape the data to match the specified shape
                data = data.reshape(self.num_slices, self.width, self.height)
                # data = data.reshape(-1, self.width, self.height)
                
                if self.prototype=='zeiss':
                    data = [np.rot90(x,k=-1) for x in data]
                    data = np.stack(data)
                    
            return data
