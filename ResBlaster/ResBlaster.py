import os
import sys
import argparse
import subprocess
from Bio import SeqIO
from cvmblaster.blaster import Blaster


def args_parse():
    "Parse the input argument, use '-h' for help."
    parser = argparse.ArgumentParser(
        usage='ResBlaster -i <genome assemble directory> -db <reference database> -o <output_directory> \n\nAuthor: Qingpo Cui(SZQ Lab, China Agricultural University)\n')
    parser.add_argument("-i", help="<input_path>: genome assembly path")
    parser.add_argument("-o", help="<output_directory>: output path")
    parser.add_argument('-db', default='resfinder',
                        help='<database>: resfinder or othersoutfile')
    parser.add_argument('-list', action='store_true', help='<show database>')
    parser.add_argument('-t', default=8, help='<number of threads>: threads')
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


def show_db_list():
    print('Datbase' + '\t' + 'Num_of_Sequence')
    db_path = os.path.join(os.path.dirname(__file__), 'db')
    for file in os.listdir(db_path):
        file_path = os.path.join(db_path, file)
        if file_path.endswith('.fsa'):
            fasta_file = os.path.basename(file_path)
            file_base = os.path.splitext(fasta_file)[0]
            num_seqs = len(
                [1 for line in open(file_path) if line.startswith(">")])
            print(file_base + '\t' + str(num_seqs))


def main():
    args = args_parse()
    if args.list:
        show_db_list()
    else:
        # threads
        threads = args.t
        # print(threads)

        # get the input path
        input_path = os.path.abspath(args.i)

        # check if the output directory exists
        if not os.path.exists(args.o):
            os.mkdir(args.o)

        output_path = os.path.abspath(args.o)

        # get the database path
        database = args.db
        database_path = os.path.join(
            os.path.dirname(__file__), f'db/{args.db}')
        # print(database_path)

        for file in os.listdir(input_path):
            file_base = str(os.path.splitext(file)[0])
            output_filename = file_base + '_tab.txt'
            outfile = os.path.join(output_path, output_filename)
            # print(file_base)
            file_path = os.path.join(input_path, file)
            if os.path.isfile(file_path):
                # print("TRUE")
                if is_fasta(file_path):
                    df = Blaster(file_path, database_path,
                                 output_path, threads).biopython_blast()
                    df.to_csv(outfile, index=False)


if __name__ == '__main__':
    main()
