# ResBlaster

![PYPI](https://img.shields.io/pypi/v/ResBlaster)
![Static Badge](https://img.shields.io/badge/OS-_Windows_%7C_Mac_%7C_Linux-steelblue)

```
 ____           ____  _           _
|  _ \ ___  ___| __ )| | __ _ ___| |_ ___ _ __
| |_) / _ \/ __|  _ \| |/ _` / __| __/ _ \ '__|
|  _ <  __/\__ \ |_) | | (_| \__ \ ||  __/ |
|_| \_\___||___/____/|_|\__,_|___/\__\___|_|

```

## Installation
```shell
pip3 install ResBlaster
```

## Dependency

*   BLAST+ >2.7.0

*   cvmblaster (v0.4.1)

**you should add BLAST in your PATH**

## Blast installation

### Windows

Following this tutorial: [Add blast into your windows PATH](http://82.157.185.121:22300/shares/BevQrP0j8EXn76p7CwfheA)

### Linux/Mac

The easyest way to install blast is:
```shell
conda install -c bioconda blast
```

## Usage

### 1. Initialize reference database

After finish installation, you should first initialize the reference database using following command
```shell
ResBlaster init
```

```shell
Usage: ResBlaster -i <genome assemble directory> -db <reference database> -o <output_directory>

Author: Qingpo Cui(SZQ Lab, China Agricultural University)

optional arguments:
  -h, --help            show this help message and exit
  -i I                  <input_path>: the PATH to the directory of assembled genome files
  -o O                  <output_directory>: output PATH
  -db DB                <database>: resfinder or others, You colud check database list using -list parameter
  -minid MINID          <minimum threshold of identity>, default=90
  -mincov MINCOV        <minimum threshold of coverage>, default=60
  -t T                  <number of threads>: default=8
  -store_arg_seq        <save the nucleotide and amino acid sequence of find genes on genome>
  -v, --version         <display version>
  -updatedb UPDATEDB    <add input fasta to BLAST database>

ResBlaster subcommand:
  {show_db,init,updatedb}
    show_db             <show the list of all available database>
    init                <initialize the reference database>
    updatedb            <add custome database, use ResBlaster updatedb -h for help>


```

### 2. Show available database
```shell
ResBlaster show_db
```
|DB_name|No. of seqs|Update_date|
|---|---|---|
|ESBL|1101|2024-10-09|
|LGI|1255|2024-07-31|
|bacmet1|578|2024-10-09|
|bacmet2_exp|753|2024-10-09|
|bacmet2_pred|155512|2024-10-09|
|lmo|20195|2024-10-09|
|ncbi|6146|2024-10-09|
|resfinder|3154|2024-10-09|
|rpoB|1|2024-10-09|
|ssuis_vf|111|2024-10-09|
|vf_hps|49|2024-10-09|
|vfdb_core|4329|2024-10-09|
|vfdb_full|32164|2024-10-09|
|vibrio_vf|5|2024-08-25|



### 2. Making your own database

Let's say you want to make your own database called `owndb`. All you need is a FASTA file of nucleotide sequences, say `owndb.fsa`(**note: the fasta file must end with .fsa**). Ideally the sequence IDs would have the format `>GENE___ID___ACC___CATEGORY` where `GENE` is the name of `GENE`, `ID` is the `allele ID` of `GENE`, `ACC` is an accession number of the sequence source, `CATEGORY` is the `CATEGORY of this GENE belongs to`.

**Your final** `owndb.fsa` should like this:
```shell
>blaOXA-62___1___AY423074___Beta-lactam
ATGAATACGATAATCTCTCGCCGGTGGCGTGCCGGCCTGTGGCGGCGGCTGGTCGGCGCG
GTCGTCTTGCCCGCAACGCTCGCCGCCACCCCTGCGGCCTATGCGGCCGACGTGCCGAAA
GCCGCGTTGGGGCGCATCACCGAGCGCGCCGACTGGGGCAAGCTGTTCGCCGCGGAGGGC
GTGAAGGGCACGATCGTGGTGCTCGACGCACGCACGCAAACCTATCAGGCCTACGACGCC
GCACGTGCCGAGAAGCGCATGTCGCCGGCGTCGACCTACAAGATATTCAACAGCCTGCTG
GCGCTCGACTCCGGGGCGCTGGACAACGAACGCGCGATCATTCCCTGGGATGGCAAGCCG
CGACGCATCAAGAACTGGAACGCGGCGATGGACCTGAGGACCGCGTTTCGCGTGTCATGC
CTGCCCTGCTATCAGGTCGTCTCGCACAAGATCGGGCGCCGGTACGCGCAGGCGAAGCTG
AACGAGGTCGGGTATGGCAACCGCACCATTGGCGGCGCGCCGGACGCCTATTGGGTCGAC
GACAGTCTGCAGATTTCGGCGCGTGAGCAGGTGGACTTCGTGCAGCGTCTCGCGCGTGGC
ACGTTGCCGTTCTCTGCGCGCTCGCAGGACATCGTGCGCCAGATGTCGATCGTCGAAGCC
ACGCCGGACTATGTGCTTCACGGCAAGACGGGTTGGTTCGTCGACAAGAAGCCCGATATC
GGCTGGTGGGTAGGGTGGATCGAGCGCGACGGCAACATCACCAGCGTCGCGATCAACATC
GACATGCTGTCGGAGGCGGACGCCCCGAAACGGGCACGCATCGTGAAGGCGGTGCTGAAG
GACCTGAAGCTGATCTGA
```
**Run following command will add** `owndb.fsa` to blast database

```shell
ResBlaster -updatedb owndb.fsa
```



