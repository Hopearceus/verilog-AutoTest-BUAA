# Verilog Auto Test 说明文档

<!-- TODO: 自动化测评 -->

## 基于代码块的数据生成器

### 模板文件语法及含义

模板文件需为拓展名是 `.template` 的 UTF-8 编码的文本文件。

在模板文件中，空行没有任何特殊含义，仅用于分隔。每条语句独占一行，由空格指示缩进层次，每层缩进严格为 4 个空格，不能越级缩进。

相同缩进层级的语句（包括内部有更多缩进的语句）会被视为同一语句块，和 Python 的缩进思路类似。

对于每条语句，应遵循如下格式：

```text
<indent-spaces><ClassName> [<key1>=<value1>[ <key2>=<value2>[ ...]]]
```

`<ClassName>` 在 `blocks` 中定义，后续有若干可选的，用键值对标注的，空格隔开的参数。可选项及其含义与参数列表如下：

<table style="text-align: center">

<thead>
    <th><code>ClassName</code></th>
    <th>语句含义</th>
    <th>参数</th>
    <th>参数含义</th>
</thead>

<tbody>
    <tr>
        <td rowspan="1"><code>Init</code></td>
        <td rowspan="1">将全部寄存器初始化为随机值</td>
        <td></td>
        <td></td>
    </tr>
    <tr>
        <td rowspan="1"><code>Endless</code></td>
        <td rowspan="1">生成一个死循环的跳转块</td>
        <td><code>label</code></td>
        <td>指定使用的标签，默认为 "_e"</td>
    </tr>
    <tr>
        <td rowspan="3"><code>Calc</code></td>
        <td rowspan="3">随机生成基本的与计算相关语句</td>
        <td><code>pick</code></td>
        <td>指定选取的指令，由<code>|</code>隔开多项</td>
    </tr>
    <tr>
        <td><code>reg</code></td>
        <td>指定可供选用的寄存器<sup>*</sup>（默认选用 "vats"）</td>
    </tr>
    <tr>
        <td><code>repeat</code></td>
        <td>指定生成指令的条数（默认为 1）</td>
    </tr>
    <tr>
        <td rowspan="2"><code>Beq</code><sup>#</sup></td>
        <td rowspan="2">随机生成一个跳转块，保证不生成死循环</td>
        <td><code>end</code></td>
        <td>指定循环终量使用的寄存器<sup>**</sup>（默认选用 $s*）</td>
    </tr>
    <tr>
        <td><code>var</code></td>
        <td>指定循环变量使用的寄存器<sup>**</sup>（默认选用 $t*）</td>
    </tr>
    <tr>
        <td rowspan="1"><code>Procedure</code><sup>#</sup></td>
        <td rowspan="1">生成一个过程调用块，保证不会出现死循环</td>
        <td></td>
        <td></td>
    </tr>
    <tr>
        <td rowspan="5"><code>SwLw</code><sup>#</sup></td>
        <td rowspan="5">生成一组配套的字存取指令，地址由随机生成的立即数与寄存器值计算得到</td>
        <td><code>reg_s</code></td>
        <td>需要保存的寄存器<sup>*</sup>（默认随机生成）</td>
    </tr>
    <tr>
        <td><code>reg_l</code></td>
        <td>需要写入的寄存器<sup>*</sup>（默认随机生成）</td>
    </tr>
    <tr>
        <td><code>low</code></td>
        <td>读写的最低地址（以字为单位，默认为 0）</td>
    </tr>
    <tr>
        <td><code>high</code></td>
        <td>读写的最高地址（以字为单位，默认为 3071）</td>
    </tr>
    <tr>
        <td><code>repeat</code></td>
        <td>重复生成的次数</td>
    </tr>
    <tr>
        <td rowspan="4"><code>DataRW</code></td>
        <td rowspan="4">产生连续地址的读写代码</td>
        <td><code>AddrStart</code></td>
        <td>起始地址（以字节为单位，默认为 0）</td>
    </tr>
    <tr>
        <td><code>AddrEnd</code></td>
        <td>结束地址（以字节为单位，默认为 12284）</td>
    </tr>
    <tr>
        <td><code>AddrStep</code></td>
        <td>地址遍历步长（以字节为单位，默认为 4）</td>
    </tr>
    <tr>
        <td><code>SL</code></td>
        <td>指定方向（默认为 <code>load</code>，另一个可选项为 <code>store</code>）</td>
    </tr>
</tbody>

</table>


#：该指令接受块的嵌套，可通过增加一个缩进层次进行代码块的嵌套

*：此处通过字符串指定选取的寄存器范围，如字母 'v' 表示允许选用 $v0 和 $v1 这两个寄存器，全部可选的范围是 "vats0"

**：此处需要指定完整的寄存器的名字，包括 '$'


### 自定义语句块

在 `blocks` 包中新建一个 `.py` 文件，创建一个类，继承 `blocks.BlockBase.BlockBase` 类，实现其 `spawn` 方法即可。

在新增模块中，需要提供全局方法 `instance`，然后新增类的一个实例即可。
