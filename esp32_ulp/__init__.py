import log_sys

from .util import garbage_collect

from .preprocess import preprocess
from .assemble import Assembler
from .link import make_binary
garbage_collect('after import')


# Store version in a global for easy editing.
version = "1.2.0"


# This makes the binary and returns it to the caller.
def src_to_binary(src):
    # Create the assembler object and prepare it for the source.
    assembler = Assembler()
    
    # Preprocess the input assembly. Remove macros, strip comments,
    # etc...
    log_sys.log_i("esp32_ulp", "Preprocessing assembly code.")
    src = preprocess(src)
    
    # Now assemble the preprcessed code.
    log_sys.log_i("esp32_ulp", "Assembling the preprocessed assembly code.")
    assembler.assemble(src, remove_comments=False)  # comments already removed by preprocessor
    
    # Clean up used memory.
    garbage_collect('before symbols export')
    
    # Report the linker step.
    log_sys.log_i("esp32_ulp", "Linking the binary.")
    
    # Fetch the symbol table from the assembler.
    addrs_syms = assembler.symbols.export()
    for addr, sym in addrs_syms:
        print('%04d %s' % (addr, sym))

    # Grab the executable code, the data, and the .bss segment
    # from the assembler.
    text, data, bss_len = assembler.fetch()
    
    # Link the ASM object into a binary file.
    return make_binary(text, data, bss_len)


# Assemble a provided file. Must be a vaild assembly file with .S extension.
def assemble_file(filename):
    # Print out compiler and target information.
    log_sys.log_i("esp32_ulp", "Compiler version: " + version)
    log_sys.log_i("esp32_ulp", "Compiling ULP binary from file " + filename)
    log_sys.log_i("esp32_ulp", "Compile target: SP Co-processor.")
    
    # Read the data from disk and prepare it for compilation.
    with open(filename) as f:
        src = f.read()

    # Compile the assembly file.
    binary = src_to_binary(src)

    # Remove the file extension and write out the linked object file
    # as a .bin file (used to be .ulp but I prefer .bin).
    if filename.endswith('.s') or filename.endswith('.S'):
        filename = filename[:-2]
    with open(filename + '.bin', 'wb') as f:
        f.write(binary)
        
    # Inform the user that compilation is complete.
    log_sys.log_i("esp32_ulp", "Compilation of ULP binary " + filename + ".bin successful.")

