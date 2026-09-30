# catsHTM
`catsHTM` 是一个用于快速访问与交叉匹配大型天文星表的工具包，最初由 Eran O. Ofek 用 `Matlab` 编写，此处给出其 Python 版本。

[![PyPI](https://img.shields.io/pypi/v/catsHTM.svg?style=flat-square)](https://pypi.python.org/pypi/catsHTM)

```python
>>> import catsHTM
>>> catsHTM.cone_search('ATLASREFCAT2',0,0,500)
```

## 文档

HDF5/HTM 格式用于存储并快速访问大型天文星表（行数超过 10^6），其设计见 [preliminary documentation](https://webhome.weizmann.ac.il/home/eofek/matlab/doc/catsHTM.html)，该页面同时给出 `Matlab` 版本。

`catsHTM` 工具包另见 [Soumagnac & Ofek 2018](https://arxiv.org/abs/1805.02666)。

## Credit
If you are using one of the large catalogs, or this tool, please give the specific reference and acknowledgments to the catalogs you used (see [list](https://webhome.weizmann.ac.il/home/eofek/matlab/doc/catsHTMcredit.html)) and add the following acknowledgment:

*The XXX catalog we use was formatted into the HDF5/HTM large catalog format as described in Soumagnac & Ofek (2018) and was developed as part of the Matlab Astronomy & Astrophysics Toolbox (Ofek 2014; ascl.soft 07005).*

[Bibtex entry for Soumagnac & Ofek 2018](http://adsabs.harvard.edu/cgi-bin/nph-bib_query?bibcode=2018arXiv180502666S&data_type=BIBTEX&db_key=PRE&nocookieset=1)

## 如何安装 `catsHTM` 代码？

以下说明仅用于安装 catsHTM **代码**，不包含 HDF5 格式星表本身的安装。

### pip

`pip install catsHTM`

### Python 版本
* `Python 3`（要求 `>=3.9`）

### 依赖的 Python 包
* `numpy`
* `scipy`
* `h5py`
* `tqdm`
* `hdf5storage`

详细的接口用法见 [USAGE.md](USAGE.md)。

## 快速开始

首先指定 HDF5 格式星表所在目录（默认是 `./data`）：

```python
>>> import catsHTM
>>> path='path/to/directory'
```

调用 `cone_search` 进行 cone 检索。例如在星表中搜索以 RA=0 rad、DEC=0 rad 为中心、半径 100 arcsec 的 cone 内天体：

```python
>>> cat,colcell,colunits=catsHTM.cone_search('ATLASREFCAT2',0,0,100,catalogs_dir=path)
```

cone 内天体保存在 `numpy` 数组 `cat` 中；列名保存在 `colcell` 中；列单位保存在 `colunits` 中。

把可选参数 `verbose` 设为真值，会额外打印本次检索的摘要：

```python
>>> cat,colcell,colunits=catsHTM.cone_search('ATLASREFCAT2',0,0,100,catalogs_dir=path,verbose=True)
>>> print(cat)
*************
Catalog: ATLASREFCAT2; cone radius: 100 arcsec; cone center: (RA,DEC)=(0,0)
*************
```

## 许可

见 [LICENSE.txt](LICENSE.txt)。
