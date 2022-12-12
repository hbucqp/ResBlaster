import os
import sys
import argparse
import subprocess
import shutil
import pandas as pd
from Bio import SeqIO
from cvmblaster.blaster import Blaster


def args_parse():
    "Parse the input argument, use '-h' for help."
    parser = argparse.ArgumentParser(
        usage='ResBlaster -i <genome assemble directory> -db <reference database> -o <output_directory> \n\nAuthor: Qingpo Cui(SZQ Lab, China Agricultural University)\n')
    parser.add_argument(
        "-i", help="<input_path>: the PATH to the directory of assembled genome files")
    parser.add_argument("-o", help="<output_directory>: output PATH")
    parser.add_argument('-db', default='resfinder',
                        help='<database>: resfinder or others, You colud check database list using -list parameter')
    parser.add_argument('-minid', default=90,
                        help="<minimum threshold of identity>, default=90")
    parser.add_argument('-mincov', default=60,
                        help="<minimum threshold of coverage>, default=60")
    parser.add_argument('-list', action='store_true',
                        help='<show database list>')
    parser.add_argument(
        '-t', default=8, help='<number of threads>: default=8')
    parser.add_argument("-store_arg_seq", default=False, action="store_true",
                        help='<save the nucleotide and amino acid sequence of find genes on genome>')
    # parser.add_argument("-p", default=True, help="True of False to process something",
    #                     type=lambda x: bool(strtobool(str(x).lower())))
    parser.add_argument('-v', '--version', action='version',
                        version='Version: ' + get_version("__init__.py"), help='<display version>')
    group = parser.add_mutually_exclusive_group(required=False)
    group.add_argument('-updatedb', help="<add input fasta to BLAST database>")
    group.add_argument('-init', action='store_true',
                        help='<initialize the reference database>')
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
    try:
        with open(file, "r") as handle:
            fasta = SeqIO.parse(handle, "fasta")
            # False when `fasta` is empty, i.e. wasn't a FASTA file
            return any(fasta)
    except:
        return False


# def join(f):
#     """
#     Get the path of database file which was located in the scripts dir
#     """
#     return os.path.join(os.path.dirname(__file__), f)


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


def initialize_db():
    database_path = os.path.join(
        os.path.dirname(__file__), f'db')
    for file in os.listdir(database_path):
        if file.endswith('.fsa'):
            file_path = os.path.join(database_path, file)
            file_base = os.path.splitext(file)[0]
            out_path = os.path.join(database_path, file_base)
            Blaster.makeblastdb(file_path, out_path)

def update_db(fasta_file):
    database_path = os.path.join(
        os.path.dirname(__file__), f'db')
    fpath, fname = os.path.split(fasta_file)
    fbase, fsuffix = os.path.splitext(fname)
    if fsuffix == '.fsa':
        if fname not in os.listdir(database_path):
            dest_file = os.path.join(database_path, fname)
            shutil.copy(fasta_file, dest_file)
            blastdb_out = os.path.join(database_path, os.path.splitext(fname)[0])
            print(f"Add {fname} to database...")
            Blaster.makeblastdb(dest_file,  blastdb_out)
        else:
            print(f"{fname} already exist in database, Please make sure or rename your .fsa file")
            sys.exit(1)
    else:
        print("Wrong suffix with input fasta file")
        sys.exit(1)


def main():
    df_all = pd.DataFrame()
    args = args_parse()
    if args.list:
        show_db_list()
    elif args.init:
        initialize_db()
    elif args.updatedb:
        newdbfile = os.path.abspath(args.updatedb)
        if is_fasta(newdbfile):
            update_db(newdbfile)
    else:
        # threads
        threads = args.t
        # print(threads)

        minid = args.minid
        mincov = args.mincov

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
                    print(f'Processing {file}')
                    df, result_dict = Blaster(file_path, database_path,
                                              output_path, threads, minid, mincov).biopython_blast()
                    print(
                        f"Finishing process {file}: writing results to " + str(outfile))
                    df.to_csv(outfile, sep='\t', index=False)
                    # change all tab results to pivot table fomat
                    df_all = pd.concat([df_all, df])

                if args.store_arg_seq:
                    Blaster.get_arg_seq(file_base, result_dict, output_path)

        # output final pivot dataframe to outpu_path
        summary_file = os.path.join(output_path, 'ResBlaster_summary.csv')
        df_pivot = df_all.pivot_table(
            index='FILE', columns=['CLASSES', 'GENE'], values='%IDENTITY',
            aggfunc=lambda x: ','.join(map(str, x)))
        df_pivot.to_csv(summary_file, index=True)


if __name__ == '__main__':
    main()
