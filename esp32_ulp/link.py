"""
The ESP32_ULP linker. 

This does not link a bunch of object files together
but only builds the final binary.
"""

import log_sys
from uctypes import struct, addressof, LITTLE_ENDIAN, UINT16, UINT32


def make_binary(text, data, bss_size):
    if not isinstance(text, bytes):
        log_sys.log_e("ulp_ld", "Invalid .text region: .text section must be binary bytes.")
    if not isinstance(data, bytes):
        log_sys.log_e("ulp_ld", "Invalid .data region: .data section must be binary bytes.")
    binary_header_struct_def = dict(
        magic = 0 | UINT32,
        text_offset = 4 | UINT16,
        text_size = 6 | UINT16,
        data_size = 8 | UINT16,
        bss_size = 10 | UINT16,
    )
    header = bytearray(12)
    h = struct(addressof(header), binary_header_struct_def, LITTLE_ENDIAN)
    # https://github.com/espressif/esp-idf/blob/master/components/ulp/ld/esp32.ulp.ld
    # ULP program binary should have the following format (all values little-endian):
    h.magic = 0x00706c75  # (4 bytes)
    h.text_offset = 12  # offset of .text section from binary start (2 bytes)
    h.text_size = len(text)  # size of .text section (2 bytes)
    h.data_size = len(data)  # size of .data section (2 bytes)
    h.bss_size = bss_size  # size of .bss section (2 bytes)
    
    # Log the binary size.
    log_sys.log_i("ulp_ld", ".text region size: " + str(len(text)) + " B")
    log_sys.log_i("ulp_ld", ".data region size: " + str(len(text)) + " B")
    
    # Return the final image.
    return bytes(header) + text + data

