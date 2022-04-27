# ResBlaster

![PYPI](https://img.shields.io/pypi/v/ResBlaster)

## Installation
pip3 install ResBlaster==0.2.1

## Dependency
- BLAST+ >2.7.0
- cvmblaster (v0.2.3)

**you should add blast in your PATH**


## Blast installation
### Windows


Following this tutorial:
http://115.28.184.56:22300/shares/rCE8EfUqL5xTn4cdg6rHfE3wxpOQxNNe

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
  -i I            <input_path>: genome assembly path
  -o O            <output_directory>: output path
  -db DB          <database>: resfinder or others
  -minid MINID    <minimum threshold of identity>, default=90
  -mincov MINCOV  <minimum threshold of coverage>, default=60
  -list           <show database>
  -init           <initialize the reference database>
  -t T            <number of threads>: default=8
  -v, --version   Display version
  ```


**Following database are currently under development and will be available soon:**
|Database|Description|
|---|---|
|vfdb| virulence factor|
|ssuis_sero| The serotype database for Streptococcus suis|
|hps| The serotype database for Haemophilus parasuis|
...

