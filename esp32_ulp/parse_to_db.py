import sys
import log_sys

from .preprocess import Preprocessor
from .definesdb import DefinesDB


def parse(files):
    db = DefinesDB()

    p = Preprocessor()
    p.use_db(db)

    for f in files:
        log_sys.log_i("ulp_pp", "Processing file: " + f)

        p.process_include_file(f)

    log_sys.log_i("ulp_pp", "Preprocessing finished.")


if __name__ == '__main__':
    parse(sys.argv[1:])

