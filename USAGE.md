# catsHTM 使用说明

本文档给出 `catsHTM` 的详细接口用法。安装步骤见 [README.md](README.md)。

所有示例假定已经指定星表所在目录：

```python
>>> import catsHTM
>>> path='path/to/directory'
```

## cone 检索：`cone_search`

在本地 HDF5/HTM 星表上，围绕给定 RA/Dec 执行cone 检索。

主要参数：

* `CatName`：星表名。
* `RA`：J2000.0 赤经，单位 rad。
* `Dec`：J2000.0 赤纬，单位 rad。
* `Radius`：检索半径，默认单位 arcsec。
* `catalogs_dir`：星表目录，默认 `./data`。
* `RadiusUnits`：半径单位，默认 `arcsec`，请勿修改默认值。
* `OnlyCone`：为真时只返回cone 内天体，为假时会同时返回cone 外部分天体，默认真。
* `verbose`：为真时打印检索摘要。

例如，在星表中搜索以 RA=0 rad、DEC=0 rad 为中心、半径 100 arcsec 的cone 内天体：

```python
>>> cat,colcell,colunits=catsHTM.cone_search('ATLASREFCAT2',0,0,100,catalogs_dir=path)
```

cone 内天体保存在 `numpy` 数组 `cat` 中，每行对应星表的一行：

```python
>>> print(cat)
[[  6.28300408e+00  -7.24311612e-05   1.68128476e-01   7.59999990e-01
    6.70588255e-01   9.23669338e-02   4.30000019e+00   0.00000000e+00
    6.20000000e+01   7.13999987e+00   4.32999992e+00   5.32000008e+01
    2.45002071e+06   2.45247496e+06]]
```

列名保存在 `colcell`，列单位保存在 `colunits`：

```python
>>> print(colcell)
['RA' 'Dec' 'col3' 'col4' 'col5' 'col6' 'col7' 'col8'
 'col9' 'col10' 'col11' 'col12' 'col13' 'col14']
>>> print(colunits)
['rad' 'rad' ' ' 'mJy' 'mJy' 'mJy' 'arcsec' 'arcsec' 'deg'
 'arcsec' 'arcsec' 'deg' 'MJD' 'MJD']
```

若设置 `verbose=True`，会额外打印检索摘要：

```python
>>> cat,colcell,colunits=catsHTM.cone_search('ATLASREFCAT2',0,0,100,catalogs_dir=path,verbose=True)
*************
Catalog: ATLASREFCAT2; cone radius: 100 arcsec; cone center: (RA,DEC)=(0,0)
*************
```

## 交叉匹配两个星表：`xmatch_2cats`

对第一个星表中的每个源，在指定距离内找出第二个星表中最近的对应体。

主要参数：

* `Catname1`、`Catname2`：两个星表名。
* `Search_radius`：检索半径，默认 2 arcsec。
* `QueryAllFun`：作用在交叉匹配结果上的自定义函数。
* `QueryAllFunPar`：传给 `QueryAllFun` 的附加参数。
* `catalogs_dir`：星表目录，默认 `./data`。
* `Verbose`：为真时打印各步骤的中间输出。
* `save_results`：为真时保存结果，**默认为假，需显式开启**。
* `save_in_one_file`：为真时把两个星表的结果合并保存到一个文件。
* `save_in_separate_files`：为真时分别保存两个星表的结果文件。
* `output`：输出目录，默认 `./cross-matching_results`。
* `time_it`、`Debug`：计时与调试开关。

例如，对两个星表执行交叉匹配：

```python
>>> catsHTM.xmatch_2cats('Cat1','Cat2',catalogs_dir=path)

Catalog_1 is Cat1 (43688 trixels)
Catalog_2 is Cat2 (43688 trixels)
************** I am building all the trixels relevant to our search **************
The number of trixels in the highest level, for Cat1 is 32768
The number of trixels in the highest level, for Cat2 is 32768
************** I am looking for overlapping trixels **************
...
```

**若要保存结果，必须设置 `save_results=True`。**

默认会在 `./cross-matching_results` 下生成三个文件：

1. `cross-matching_result_Cat1.txt`：第一个星表中存在一个或多个第二星表对应体的条目。
2. `cross-matching_result_Cat2.txt`：每个对应体在第二星表中最近的条目。
3. `cross-matching_result_full.txt`：上面两个文件的合并结果。

这些文件的表头标明了各列含义。

输出位置可通过 `output` 关键字修改：

```python
>>> catsHTM.xmatch_2cats('Cat1','Cat2',catalogs_dir=path,output='./my_results')
```

若不需要保存，保持 `save_results` 的默认值（`False`），可加快运行速度，并把交叉匹配算法的输出直接交给自定义函数处理。

也可以通过 `save_in_one_file=False` 只保存两个分开的文件，或通过 `save_in_separate_files=False` 只保存合并的大文件：

```python
>>> catsHTM.xmatch_2cats('Cat1','Cat2',catalogs_dir=path,save_in_one_file=False)
```

检索半径默认 2 arcsec，可用 `Search_radius` 修改：

```python
>>> catsHTM.xmatch_2cats('Cat1','Cat2',Search_radius=5)
```

### 在交叉匹配输出上运行自定义函数

`QueryAllFun` 与 `QueryAllFunPar` 允许在交叉匹配算法的输出上运行自定义函数。`QueryAllFun` 接收以下输入参数：

1. `Cat1`：第一个星表某个 trixel 的内容。
2. `Cat2`：与 `Cat1` 重叠的第二个星表某个 trixel 的内容。
3. `Ind`：一个字典列表，每个字典对应 `Cat1` 中有一个或多个对应体的对象：
* `Ind[i]["IndRef"]`：第 i 个存在对应体的 `Cat1` 源的下标。
* `Ind[i]["IndCat"]`：`Cat2` 中对应体的下标列表。
* `Ind[i]["Dist"]`：第 i 个 `Cat1` 源与其 `Cat2` 对应体之间的角距离向量（rad）。
4. `IndCatMinDist`：长度与 `Cat1` 行数相同的向量，无对应体处为 `nan`，有对应体处为最近对应体在 `Cat2` 中的下标。

自定义函数按如下形式编写：

```python
def Your_QueryAllFun(Cat1,Ind,Cat2,IndCatMinDist,i,additionnal_args=[1,2,'hi']):
    return [your output]
```

`QueryAllFunPar` 若非 `None`，须为一个元组，会被传给 `Your_QueryAllFun` 的 `additional_args` 参数。

代码内置一个示例函数 `Example_QueryAllFun`。例如用 `QueryAllFun=Example_QueryAllFun`、`QueryAllFunPar=['test']` 运行，会打印 `Cat1`、`Cat2`、`Ind`、`IndCatMinDist`，并把 `Cat1` 的内容保存到 `test` 目录：

```python
>>> import catsHTM
>>> from catsHTM import Example_QueryAllFun
>>> catsHTM.xmatch_2cats('Cat1','Cat2',catalogs_dir=path,QueryAllFun=Example_QueryAllFun,QueryAllFunPar=['test'])
```

### 示例：交叉匹配两个星表并按两个星表的条件筛选

下面的示例对两个星表做交叉匹配，并依据第一个星表某量的信噪比与第二个星表某两列之差筛选天体。

```python
import catsHTM
import math
import numpy as np
import pandas as pd
import os

def query_function_example(Cat1,Ind,Cat2,IndCatMinDist,i,additionnal_args):

    columns_in_crossmatchfile=additionnal_args[0]+additionnal_args[1]
    Verbose=additionnal_args[2]

    Nind=len(Ind)
    if Verbose==True:
        print('Nind',Nind)

    data_list=[]
    for si in range(Nind):
        if Verbose==True:
            print('Ind',Ind)
        I1=Ind[si]['IndRef']
        I2 = int(Ind[si]['IndCat'][np.argmin(Ind[si]['Dist'])])
        if Verbose==True:
            print('IndCatMinDist',IndCatMinDist)
            print("Ind[si]['IndRef']",Ind[si]['IndRef'])
            print("Ind[si]['IndCat']",Ind[si]['IndCat'])
            print('I2, the index of the closest is',I2)

        col1     = cat1_cols.index('col1')
        col1_err = cat1_cols.index('col1_err')
        col2_a   = cat2_cols.index('col2_a')
        col2_b   = cat2_cols.index('col2_b')

        snr_constraint   = 15   # 信噪比约束：col1/col1_err > 15
        color_constraint = -0.5 # 颜色约束：(col2_a-col2_b) < -0.5

        # 筛选条件：
        cond=(Cat1[I1,col1]/Cat1[I1,col1_err] > snr_constraint) & \
             (Cat2[I2,col2_a]-Cat2[I2,col2_b] < color_constraint) & \
             (Cat2[I2,col2_a]-Cat2[I2,col2_b] > -5.0 )

        if cond:
            if Verbose==True:
                print('Success.')
            data_line = {}
            for bli,blu in enumerate(np.hstack((Cat1[I1,:],Cat2[I2,:]))):
                data_line[columns_in_crossmatchfile[bli]]=blu
            data_list.append(data_line)
    data = pd.DataFrame(data_list)

    if len(data)>0:
        data['RA_cat1'] *= 180./np.pi # 保存前把 RA、Dec 转回十进制度。
        data['Dec_cat1'] *= 180./np.pi
        data['RA_cat2'] *= 180./np.pi
        data['Dec_cat2'] *= 180./np.pi
        if not os.path.isfile("data_xmatch.csv"):
            # 输出文件不存在时，写入表头和数据。
            data.to_csv('data_xmatch.csv'.format(i),index=False, mode='a', header=True)
        else:
            # 输出文件已存在时，只写数据不写表头。
            data.to_csv('data_xmatch.csv'.format(i),index=False, mode='a', header=False)
    return data
```

然后以该函数运行 `xmatch_2cats`：

```python
    cat_path = "the/directory/where/you/have/your/HDF5/catalogs"
    verbose=False

    cat1_cols = ['RA', 'Dec', 'col1', 'col1_err']
    cat2_cols = ['RA', 'Dec', 'col2_a', 'col2_b']

    catsHTM.xmatch_2cats('Cat1','Cat2',Search_radius=4,QueryAllFun=query_function_example,QueryAllFunPar=[cat1_cols, cat2_cols, verbose],
                     catalogs_dir=cat_path,Verbose=verbose,save_results=False,save_in_one_file=False,
                     save_in_separate_files=False,output='./cross-matching_results',time_it=False,Debug=False)
```

### 修改其他默认参数

其他默认参数（如文件名与数据集命名格式）可在 Python 文件 `params.py` 中修改（在命令行输入 `pip show catsHTM` 可查看 `params.py` 的位置）。
