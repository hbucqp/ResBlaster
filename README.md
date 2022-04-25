# ResBlaster

![PYPI](https://img.shields.io/pypi/v/ResBlaster)

## Installation
pip3 install ResBlaster==0.1.4

## Dependency
- BLAST+ >2.7.0
- cvmblaster (v0.1.3)

**you should add blast in your PATH**


## Blast installation
### Windows
waiting...

### Linux/Mac
The easyest way to install blast is:

```
conda install -c bioconda blast
```

## Usage
```
usage: ResBlaster -i <genome assemble directory> -db <reference database> -o <output_directory>

Author: Qingpo Cui(SZQ Lab, China Agricultural University)

optional arguments:
  -h, --help      show this help message and exit
  -i I            <input_path>: genome assembly path
  -o O            <output_directory>: output path
  -db DB          <database>: resfinder or othersoutfile
  -minid MINID    <minimum threshold of identity>
  -mincov MINCOV  <minimum threshold of coverage>
  -list           <show database>
  -t T            <number of threads>: threads
  -v, --version   Display version
  ```


