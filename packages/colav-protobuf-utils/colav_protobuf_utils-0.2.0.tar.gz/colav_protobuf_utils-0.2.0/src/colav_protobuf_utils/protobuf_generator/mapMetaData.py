from colav_protobuf import MapMetaData
from typing import Tuple
from .stamp import Stamp

def gen_map_metadata(
    map_load_time: Stamp,
    resolution: float,
    width: float,
    height: float,
    origin_position: Tuple[float, float, float],
    origin_quaternium: Tuple[float, float, float, float] 
):
    metadata = MapMetaData()

    metadata.map_load_time.sec = map_load_time.sec
    metadata.map_load_time.nanosec = map_load_time.nanosec
    metadata.resolution = resolution
    metadata.width = width
    metadata.height = height
    
    metadata.origin.position.x = origin_position[0]
    metadata.origin.position.y = origin_position[1]
    metadata.origin.position.z = origin_position[2]

    metadata.origin.orientation.x = origin_quaternium[0]
    metadata.origin.orientation.y = origin_quaternium[1]
    metadata.origin.orientation.z = origin_quaternium[2]
    metadata.origin.orientation.w = origin_quaternium[2]

    return metadata
