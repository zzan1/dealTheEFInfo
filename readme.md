# 简单介绍
 
由于获取的英语资源来自于付费的某英语教育集团，出于尊重相关知识产权的考虑，相关的文档内容不能分享。望体谅。

这个仓库的主要目的是为了保存代码，以便日后进行回顾和复习，等进一步学习了更多编程思想和规范之后。 可以进一步的**迭代代码** 和 **规范化代码书写** 。

# 更新内容介绍

## 2020-05-10

**第一次创建仓库，上传第一版代码。**

其中包含到的学习的知识点：

### lxml

[主要参考文章](https://www.cnblogs.com/zhangxinqi/p/9210211.html) 

lxml 是 `python` 处理 `xml` 等标记语言的库。这里用来处理 `json` 中的 `html` 片段。

`lxml` 与 `javascript` 的 `Dom` 有一点类似，整体都是一个 `ElementTreeObject`, 利用 `xpath` 可以选取指定**元素节点** ，`xpath` 的相关规则如下：


| 表达式            | 描述                                       |
|-------------------|--------------------------------------------|
| nodename          | 选取此节点的所有子节点                     |
| /                 | 从当前节点选取直接子节点                   |
| //                | 从当前节点选取子孙节点                     |
| .                 | 选取当前节点                               |
| ..                | 选取当前节点的父节点                       |
| @                 | 选取属性                                   |
| *                 | 通配符，选择所有元素节点与元素名           |
| `@*`                | 选取所有属性                               |
| [@attrib]         | 选取具有给定属性的所有元素                 |
| [@attrib='value'] | 选取给定属性具有给定值的所有元素           |
| [tag]             | 选取所有具有指定元素的直接子节点           |
| [tag='text']      | 选取所有具有指定元素并且文本内容是 text 节点 |

建立 `dom` 树对象
```python
	import lxml.etree as let

	# build elemnet tree from str 
	newTree = let.HTML(content)

	# buile element tree from file
	newTree = let.parse(file, let.HTMLParser())
```

过程中发现一个点就是，lxml 默认选择的点从定义好的 `newTree` 这个 `elementTreeObj` 开始寻找. 类如下面一段代码

```html
<div>
	<em>test1<em>
</div>
<p>
	<em>test2</em>
</p>
```

我们想得到 `p` 标签下面的 `em` 标签，原来的想法是：

```python
pTag=newTree.xpath('//p')
test2=pTag.xpath('/em')
```

这样不会做到目的，选取到的仍然是所有的 `elementTreeObj` 即 `newTree` 中的所有 `em` 标签。因为，此时的 `pTag` 只是一个 `elementListObj` 不是一个树对象。可以从新利用这个 `p` 来新建立一个树对象。

```python 
# 用选出来的元素对象新建一个lxml的元素树对象
def buildNewElementTree(HTMLElement):
    content = let.tostring(HTMLElement, encoding='utf-8').decode("utf-8")
    newTree = let.HTML(content)
    return newTree
```

简单来说就是利用 `tostring` 函数将 `elementListObj` 中的一个元素单独拿出来，获取其中所有的内容，返回一个字符串。 利用这个字符串，重新建立一个树对象。

> 解决中文显示不全的问题，正确显示 lxml 的字符串：
> 解决方法就是上面的 `tostring` 函数，先进行编码，然后再进行解码。

## logging 模块的使用

[主要参考文章](https://www.cnblogs.com/Nicholas0707/p/9021672.html) 

**快速实现相关功能**

首先，配置 `log` 文档的格式：

```python
logging.basicConfig(level=logging.DEBUG,#控制台打印的日志级别
                    filename='new.log',
                    filemode='a',##模式，有w和a，w就是写模式，每次都会重新写日志，覆盖之前的日志
                    #a是追加模式，默认如果不写的话，就是追加模式
                    format=
                    '%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s'
                    #日志格式
                    )
```

然后利用不同的 logging 等级来查看消息。各个等级的语法和 `print` 差不多，这个项目中，我主要是把它当作一个 `print` 语句来使用。

**logging 的五个等级** 

| 日志等级（level） | 描述                                                                                        |
|-------------------|---------------------------------------------------------------------------------------------|
| DEBUG             | 最详细的日志信息，典型应用场景是 问题诊断                                                   |
| INFO              | 信息详细程度仅次于DEBUG，通常只记录关键节点信息，用于确认一切都是按照我们预期的那样进行工作 |
| WARNING           | 当某些不期望的事情发生时记录的信息（如，磁盘可用空间较低），但是此时应用程序还是正常运行的 |
| ERROR             | 由于一个更严重的问题导致某些功能不能正常运行时记录的信息                                    |
| CRITICAL          | 当发生严重错误，导致应用程序不能继续运行时记录的信息                                        |

- [ ] 学习使用 `logging` 的思想，明白什么时候该用 `logging` 的几个等级语句，可以快速定位 bug 位置。

# 练习点

流程控制，整体的设计思想，和字符串的控制
