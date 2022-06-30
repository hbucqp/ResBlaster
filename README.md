# ResBlaster

![PYPI](https://img.shields.io/pypi/v/ResBlaster)

```
 ____           ____  _           _
|  _ \ ___  ___| __ )| | __ _ ___| |_ ___ _ __
| |_) / _ \/ __|  _ \| |/ _` / __| __/ _ \ '__|
|  _ <  __/\__ \ |_) | | (_| \__ \ ||  __/ |
|_| \_\___||___/____/|_|\__,_|___/\__\___|_|

```




## Installation
pip3 install ResBlaster

## Dependency
- BLAST+ >2.7.0
- cvmblaster (v0.3.4)

**you should add BLAST in your PATH**


## Blast installation
### Windows


Following this tutorial:
http://82.157.185.121:22300/shares/BevQrP0j8EXn76p7CwfheA

### Linux/Mac
The easyest way to install blast is:

```
conda install -c bioconda blast
```



## Usage

### Initialize reference database

After finish installation, you should first initialize the reference database using following command
```
ResBlaster -init
```



```
Usage: ResBlaster -i <genome assemble directory> -db <reference database> -o <output_directory> -minid 90 -mincov 60 -t 4


optional arguments:
  -h, --help      show this help message and exit
  -i I            <input_path>: the PATH to the directory of assembled genome files
  -o O            <output_directory>: output PATH
  -db DB          <database>: resfinder or others, You colud check database list using -list parameter
  -minid MINID    <minimum threshold of identity>, default=90
  -mincov MINCOV  <minimum threshold of coverage>, default=60
  -list           <show database list>
  -init           <initialize the reference database>
  -t T            <number of threads>: default=8
  -store_arg_seq  save the nucleotide and amino acid sequence of find genes on genome
  -v, --version   Display version
  ```


**Following database are currently under development and will be available soon:**
|Database|Description|
|---|---|
|vfdb_core| The core dataset of vfdb|
|vfdb_full| The full database of vfdb |
|ncbi| Bacterial Antimicrobial Resistance Reference Gene Database from NCBI |
|resfinder | ARGs from ResFinder|
|ssuis_sero| The serotype database for Streptococcus suis|
|hps| The serotype database for Haemophilus parasuis|
...

