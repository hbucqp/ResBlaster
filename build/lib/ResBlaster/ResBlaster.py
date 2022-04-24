import os
import sys
import argparse
from Bio import SeqIO
from cvmblaster.blaster import Blaster


input = "/Users/cuiqingpo/Downloads/test_genome"
my_file = "/Users/cuiqingpo/Downloads/zdq_ecoli/jsE212.fa"
# db = "/Users/cuiqingpo/Downloads/blast_db/resfinder"
output = "./"


def args_parse():
    "Parse the input argument, use '-h' for help."
    parser = argparse.ArgumentParser(
        usage='ResBlaster -i <genome assemble directory> -db <reference database> -o <output_directory> \n\nAuthor: Qingpo Cui(SZQ Lab, China Agricultural University)\n')
    parser.add_argument("-i", help="<input_path>: genome assembly path")
    parser.add_argument("-o", help="<output_directory>: output path")
    parser.add_argument('-db', default='resfinder',
                        help='database <resfinder or others>')
    # parser.add_argument("-p", default=True, help="True of False to process something",
    #                     type=lambda x: bool(strtobool(str(x).lower())))
    parser.add_argument('-v', '--version', action='version',
                        version='Version: ' + get_version("__init__.py"), help='Display version')
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)
    return parser.parse_args()


def read(rel_path: str) -> str:
    here = os.path.abspath(os.path.dirname(__file__))
    # intentionally *not* adding an encoding option to open, See:
    #   https://github.com/pypa/virtualenv/issues/201#issuecomment-3145690
    with open(os.path.join(here, rel_path)) as fp:
        return fp.read()


def get_version(rel_path: str) -> str:
    for line in read(rel_path).splitlines():
        if line.startswith("__version__"):
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]
    raise RuntimeError("Unable to find version string.")


def is_fasta(file):
    """
    chcek if the input file is fasta format
    """
    with open(file, "r") as handle:
        fasta = SeqIO.parse(handle, "fasta")
        # False when `fasta` is empty, i.e. wasn't a FASTA file
        return any(fasta)


def join(f):
    """
    Get the path of database file which was located in the scripts dir
    """
    return os.path.join(os.path.dirname(__file__), f)


def main():
    args = args_parse()
    input_path = os.path.abspath(args.i)

    # check if the output directory exists
    if not os.path.exists(args.o):
        os.mkdir(args.o)

    print(args.db)


if __name__ == '__main__':
    main()
# db = join('db/resfinder')
# print(db)

# for file in os.listdir(input):
#     file_base = os.path.splitext(file)[0]
#     print(file_base)
#     file_path = os.path.join(input, file)
#     print(file_path)
#     df = Blaster(file_path, db, output, 8, 50, 50).biopython_blast()
#     print(df)


# df = Blaster(my_file, db, output, 8, 50, 50).biopython_blast()
# df.to_csv(r'test.csv', index=False)
# print(blast1.is_fasta())
