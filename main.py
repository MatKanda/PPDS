import numpy
from numba import cuda


@cuda.jit
def my_kernel(io_array):
    print(io_array)


# Create the data array - usually initialized some other way
data = numpy.ones(256)

# Set the number of threads in a block
threads_per_block = 32

# Calculate the number of thread blocks in the grid
blocks_per_grid = (data.size + (threads_per_block - 1)) // threads_per_block

# Now start the kernel
my_kernel[blocks_per_grid, threads_per_block](data)

# Print the result
print(data)
