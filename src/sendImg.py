import cv2
import numpy as np
# File names
in_name = 'lixo.png'
out_name = 'square_out.png'

# Read data and convert to a list of bits
data = list(in_bits)

# Convert the list of bits back to bytes and save
out_bits = np.array(data)
print(np.all(out_bits == in_bits))
out_bytes = np.packbits(out_bits)
print(np.all(out_bytes == in_bytes))
out_bytes.tofile(out_name)
