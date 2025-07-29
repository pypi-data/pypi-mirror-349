# ndtiler

A lightweight Python package for iterative tiling over N-dimensional arrays.

## Overview

`ndtiler` is a simple, efficient library that generates tile coordinates for processing large N-dimensional arrays in smaller chunks. This approach is particularly useful for operations on large images, volumetric data, or any N-dimensional matrix that's too large to process at once.

While available as a package, the entire implementation is contained in a single file that can be easily copy-pasted into your project as a "header-only" style Python module.

The library offers two tiling strategies:
- **Static tiling**: Requires even sampling of the input matrix (default)
- **Minimally Dynamic tiling**: Adjusts the final tiles in each dimension to fit the matrix size exactly

## Installation

```bash
pip install ndtiler
```

## Basic Usage

```python
import numpy as np
from ndtiler import tile_nd, dynamic_tile_nd

# Create a sample 2D array
data = np.zeros((512, 512))

# Define tile size and overlap
tile_size = (128, 128)
overlap = (32, 32)

# Generate tile coordinates using static tiling
for ((y0, y1), (x0, x1)) in tile_nd(data.shape, tile_size, overlap):
    tile = data[y0:y1, x0:x1]  # Extract the tile

    #
    # Process the tile...
    #
    
# Generate tile coordinates using dynamic tiling
for ((y0, y1), (x0, x1)) in dynamic_tile_nd(data.shape, tile_size, overlap):
    tile = data[y0:y1, x0:x1]  # Extract the tile
    
    #
    # Process the tile...
    #
```

## Key Functions

### Tiling Functions

- `tile_nd(size, tile_size, overlap)`: Static tiling that requires even division of the input shape.
- `dynamic_tile_nd(size, tile_size, overlap)`: Dynamic tiling that adjusts the final tiles in each dimension.

### Utility Functions

- `get_stride(tile_size, overlap)`: Calculate the step size between tiles.
- `get_overlap_from_stride(tile_size, stride)`: Calculate overlap given tile size and stride.
- `get_overflow(size, tile_size, overlap)`: Calculate the adjustment needed for even tiling.
- `get_tile_count(size, tile_size, overlap)`: Calculate the number of tiles needed in each dimension.

More in-depth examples can be seen in the `examples/` directory.


## License

MIT License

## Author

Ryan 'RyanIRL' Peters 


