import os
import sys
import argparse
import subprocess
import shutil
import time
# import warnings
from tabulate import tabulate
import pandas as pd
from Bio import SeqIO
from cvmblaster.blaster import Blaster
from cvmcore.cvmcore import cfunc
from Bio import BiopythonDeprecationWarning

# warnings.simplefilter('ignore', BiopythonDeprecationWarning)


def args_parse():
    "Parse the input argument, use '-h' for help."
    parser = argparse.ArgumentParser(
        usage='ResBlaster -i <genome assemble directory> -db <reference database> -o <output_directory> \n\nAuthor: Qingpo Cui(SZQ Lab, China Agricultural University)\n')

    # Add subcommand
    subparsers = parser.add_subparsers(
        dest='subcommand', title='ResBlaster subcommand')
    show_database_parser = subparsers.add_parser(
        'show_db', help="<show the list of all available database>")

    init_db_parser = subparsers.add_parser(
        'init', help='<initialize the reference database>')

    add_db_parser = subparsers.add_parser(
        'updatedb', help='<add custome database, use ResBlaster updatedb -h for help>')

    add_db_parser.add_argument(
        '-file', help='<The fasta format reference file>')

    # Add options
    parser.add_argument(
        "-i", help="<input_path>: the PATH to the directory of assembled genome files")
    parser.add_argument("-o", help="<output_directory>: output PATH")
    parser.add_argument('-db', default='resfinder',
                        help='<database>: resfinder or others, You colud check database list using -list parameter')
    parser.add_argument('-minid', default=90,
                        help="<minimum threshold of identity>, default=90")
    parser.add_argument('-mincov', default=60,
                        help="<minimum threshold of coverage>, default=60")
    # parser.add_argument('-list', action='store_true',
    #                     help='<show database list>')
    parser.add_argument(
        '-t', default=8, help='<number of threads>: default=8')
    parser.add_argument("-store_arg_seq", default=False, action="store_true",
                        help='<save the nucleotide and amino acid sequence of find genes on genome>')
    # parser.add_argument("-p", default=True, help="True of False to process something",
    #                     type=lambda x: bool(strtobool(str(x).lower())))
    parser.add_argument('-v', '--version', action='version',
                        version='Version: ' + get_version("__init__.py"), help='<display version>')

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


# def get_rel_path():
#     """
#     Get the relative path
#     """
#     here = os.path.abspath(os.path.dirname(__file__))
#     return here


def get_version(rel_path: str) -> str:
    for line in read(rel_path).splitlines():
        if line.startswith("__version__"):
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]
    raise RuntimeError("Unable to find version string.")


def get_rel_path():
    """
    Get the relative path
    """
    here = os.path.abspath(os.path.dirname(__file__))
    return here


def show_db_list():
    """
    Convert the ResBlaster database to tidy dataframe
    Paramters
    ----------

    Returns
    ----------
    A tidy dataframe contains the blast database name and No. of seqs in database and the last modified date

    """
    here = get_rel_path()
    db_path = os.path.join(here, 'db')
    db_list = []
    for file in os.listdir(db_path):
        file_path = os.path.join(db_path, file)
        if file_path.endswith('.fsa'):
            db_dict = {}
            fasta_file = os.path.basename(file_path)
            file_base = os.path.splitext(fasta_file)[0]
            num_seqs = len(
                [1 for line in open(file_path) if line.startswith(">")])
            update_date = cfunc.get_mod_time(file_path)
            db_dict['DB_name'] = file_base
            db_dict['No. of seqs'] = num_seqs
            db_dict['Update_date'] = update_date
            db_list.append(db_dict)
        else:
            next

    db_df = pd.DataFrame(db_list)
    db_df = db_df.sort_values(by='DB_name', ascending=True)
    tidy_db_df = tabulate(db_df, headers='keys', showindex=False)
    return print(tidy_db_df)


def initialize_db():
    database_path = os.path.join(
        os.path.dirname(__file__), f'db')
    for file in os.listdir(database_path):
        if file.endswith('.fsa'):
            file_path = os.path.join(database_path, file)
            file_base = os.path.splitext(file)[0]
            out_path = os.path.join(database_path, file_base)
            seq_type = cfunc.check_sequence_type(file_path)
            if seq_type == 'DNA':
                Blaster.makeblastdb(file_path, out_path)
            elif seq_type == 'Amino Acid':
                Blaster.makeblastdb(file_path, out_path, 'prot')
            else:
                print('Unknown sequence type, exit ...')


def update_db(fasta_file):
    database_path = os.path.join(
        os.path.dirname(__file__), f'db')
    fpath, fname = os.path.split(fasta_file)
    fbase, fsuffix = os.path.splitext(fname)
    if fsuffix == '.fsa':
        if fname not in os.listdir(database_path):
            dest_file = os.path.join(database_path, fname)
            shutil.copy(fasta_file, dest_file)
            blastdb_out = os.path.join(
                database_path, os.path.splitext(fname)[0])
            print(f"Add {fname} to database...")
            Blaster.makeblastdb(dest_file,  blastdb_out)
        else:
            print(
                f"{fname} already exist in database, Please make sure or rename your .fsa file")
            sys.exit(1)
    else:
        print("Wrong suffix with input fasta file")
        sys.exit(1)


def check_db():
    """
    ruturn database list
    """
    db_list = []
    database_path = os.path.join(
        os.path.dirname(__file__), f'db')
    for file in os.listdir(database_path):
        if file.endswith('.fsa'):
            db_name = os.path.splitext(file)[0]
            db_list.append(db_name)
    return db_list


def main():
    df_all = pd.DataFrame()
    args = args_parse()
    if args.subcommand is None:
        # if args.list:
        #     show_db_list()
        # elif args.init:
        #     initialize_db()
        # elif args.updatedb:
        #     newdbfile = os.path.abspath(args.updatedb)
        #     if is_fasta(newdbfile):
        #         update_db(newdbfile)
        # else:
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

        # check if input db is in dblist
        exist_database = check_db()
        # print(exist_database)
        if database in exist_database:
            database_path = os.path.join(
                os.path.dirname(__file__), f'db/{args.db}')
            seq_type = cfunc.check_sequence_type(f'{database_path}.fsa')
        else:
            print(
                f'Could not found {database} in {exist_database}, Please check your input or view database list using "ResBlaster -list"')
            sys.exit(1)

        # decide blast type
        # print(f'The database type is {seq_type} \n')
        if seq_type == 'Amino Acid':
            blast_type = 'blastx'
        else:
            blast_type = 'blastn'

        # print(f'The blast type is {blast_type}')

        for file in os.listdir(input_path):
            file_base = str(os.path.splitext(file)[0])
            output_filename = file_base + '_tab.txt'
            outfile = os.path.join(output_path, output_filename)
            # print(file_base)
            file_path = os.path.join(input_path, file)
            if os.path.isfile(file_path):
                # print("TRUE")
                if cfunc.is_fasta(file_path):
                    print(f'Processing {file}')
                    df, result_dict = Blaster(file_path, database_path,
                                              output_path, threads, minid, mincov, blast_type).biopython_blast()
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
    elif(args.subcommand == 'show_db'):
        show_db_list()
    elif(args.subcommand == 'init'):
        initialize_db()
    elif(args.subcommand == 'updatedb'):
        custome_db_file = os.path.abspath(args.file)
        update_db(custome_db_file)
        print(f'Adding {args.file} to reference database...')
        print(f'Initializing reference data...')
        initialize_db()
    else:
        print(
            f'{args.subcommand} do not exists, please using "ResBlaster -h" to show help massage.')


if __name__ == '__main__':
    main()
