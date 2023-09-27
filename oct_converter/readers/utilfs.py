from __future__ import annotations
import eyepy
from oct_converter.readers.BINReader import BINReader
import h5py
from tenpy.tools import hdf5_io # should be installed pip install physics-tenpy

'''
*1- Loading, creating and returting a .eye object  from a .bin path 
filepath: Path of the .bin file    
other parameters for opening .bin files
if the protocol is set as 'zeiss', then all of the parameters for our oct machine will be loaded automatically. 
otherwise, the parameters should be set based on image volumes
this function returns a .eye object
'''
def load_eye_from_bin(filepath, header_size=0, num_slices=2044, width=2048, height=1536, num_channels=1, prototype='zeiss'):
    bin_reader = BINReader(filepath,header_size, num_slices, width, height, num_channels, prototype)
    oct_volume = bin_reader.read_data()
    eye_volume = eyepy.KnotEyeVolume(data=oct_volume)
    return eye_volume


'''
*2- Saving a .bin file in a .eye file 
src_filepath: Source filepath-Path of the .bin file 
des_filepath: Destination filepath-Path of the desired .eye file 
other parameters for opening .bin files
if the protocol is set as 'zeiss', then all of the parameters for our oct machine will be loaded automatically. 
otherwise, the parameters should be set based on image volumes
'''
def save_bin2eye(src_filepath, des_filepath, header_size=0, num_slices=2044, width=2048, height=1536, num_channels=1, prototype='zeiss'):
    bin_reader = BINReader(src_filepath,header_size, num_slices, width, height, num_channels, prototype)
    oct_volume = bin_reader.read_data()
    eye_volume = eyepy.KnotEyeVolume(data=oct_volume)
    
    eye_volume.save(des_filepath)


'''
*3- Saving a .eye file to a .bin file 
eye_filepath: Name and path of the .eye file    
bin_filepath: Name and path of the desired .bin file    
'''  
def save_eye2bin(eye_filepath, bin_filepath):
    try:
        eye_object = eyepy.KnotEyeVolume.load(eye_filepath)
        
        parts = bin_filepath.rsplit('.', 1)
        if len(parts) == 2:
            characters_before_dot = parts[0]
        else:
            characters_before_dot = bin_filepath

        data_path = characters_before_dot + '_structure.bin'
        data_part = eye_object.data
        with open(data_path,'wb') as f:
            f.write(data_part)
            
    except Exception as e:
        print(f"Error: {e}")


'''
*4- Saving a .eye file to a .hdf5 file
eye_filepath:Name and path of the .eye file      
filepath: Name and path of the desired .hdf5 file    
'''      
def save_eye2hdf5(eye_filepath, hdf5_filepath):
    try:
        eye_object = eyepy.KnotEyeVolume.load(eye_filepath)
        # Open the HDF5 file
        with h5py.File(hdf5_filepath, 'w') as f:
            # Save the object to the HDF5 file
            hdf5_io.save_to_hdf5(f, eye_object)
    except Exception as e:
        print(f"Error: {e}")



'''
*5- Loading and returning a .eye object from a .hdf5 file
hdf5_filepath: Name and path of the .hdf5 file    
'''      
def load_eye_from_hdf5(hdf5_filepath):
    try:
        # Open the HDF5 file
        with h5py.File(hdf5_filepath, 'r') as f:
            # Load the object from the HDF5 file
            loaded_eye_object = hdf5_io.load_from_hdf5(f)
    except Exception as e:
        print(f"Error: {e}")
    
    return loaded_eye_object

