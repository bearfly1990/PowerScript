# Header 1
## Header 2
### Header 3
**Bold** __Bold2__  
_Italic_ *Italic2*

`code`  
``` python
print("Hello World!")
```
* Item1
    * Item1.1
    * Item1.2
* Item2
* Item3
1. List1
2. List2
3. List3
> This is Blockquotes
Horizotal Rules
***
![Chartjs](http://www.chartjs.org/img/chartjs-logo.svg)

[Baidu](www.baidu.com)

[Link to Baidu][1]
[Link to Google][2]  
[Link to Baidu again][1]

[1]:https://www.baidu.com  
[2]:https://www.google.com  
- MainList1
- MainList2
  1. Second List1
  2. Second List2
+ MainList3

- [x] Task1
- [ ] Task2
- [ ] Task3

emoji1: :+1:, emoji2: :o:
:smile:

使用svn用的好好的，为什么要用git？git有哪些优势？又有哪些劣势？在日常使用中两者明显的差异是什么？
```SQL
select * from table;
```
```js
$(document).ready(function() {
     //var md = window.markdownit().use(window.markdownitEmoji);
    //<script>hljs.initHighlightingOnLoad();
   //hljs.initHighlightingOnLoad();
    // Actual default values
    //hljs.initHighlightingOnLoad();
    var md = window.markdownit({
        highlight: function (str, lang) {
                       if (lang && hljs.getLanguage(lang)) {
                         try {
                           return '<pre class="hljs"><code>' +
                                  hljs.highlight(lang, str, true).value +
                                  '</code></pre>';
                         } catch (__) {}
                       }
                       return '<pre class="hljs"><code>' + md.utils.escapeHtml(str) + '</code></pre>';
                   },
        html: true,
        linkify: true,
        typographer: true,
        }).use(window.markdownitEmoji);
    
     $.ajax({
            url : "22.md",
            dataType: "text",
            success : function (data) {
                        var result = md.render(data);
                        $("#markdownArea").html("<article class='markdown-body'>"+result+"</article>");
                      }
           });
       
   
});
```
```js
var a = 0;
a += 1;
```
```
nothing serious
```
`sssss`

（关于 svn 的使用，一起来回顾一下 [How To Use Svn in Daily Work](using-svn.md)）

- [Why is Git better than Subversion?](http://stackoverflow.com/questions/871/why-is-git-better-than-subversion)  stackoverflow 上关于svn和git的区别的讨论，说的很详细。
- [What are the differences between SVN and Git? ](https://help.github.com/articles/what-are-the-differences-between-svn-and-git/)  github 上通过版本库结构、历史、子项目（submudle）的不同来对比两者。
- [蒋鑫：为什么 Git 比 SVN 好？](http://www.worldhello.net/2012/04/12/why-git-is-better-than-svn.html "蒋鑫 - Why `Git` is better than `SVN`")

以下内容出自 [@oldratlee](https://github.com/oldratlee) 的 [repo](https://github.com/oldratlee/software-practice-miscellany/blob/master/git/README.md)。

SVN 和 Git 在日常使用中的明显差异
=========================

![git vs svn](http://static.ixirong.com/pic/mygit/why-git.png)

:point_right: 自己在使用`git`过程中相对`svn`的感受强烈的变化。

:beer: 合并对提交过程的保留
-------------------

- `git`：合并操作保留原有的提交过程（即保留了合并来源的作者、提交次数、分离提交的内容）。
- `svn`：合并操作把来源多个提交合并成了一个合并提交，即在提交历史中Crash了自然的提交过程。

保留原有的提交过程，可以无需繁琐追踪历史就方便的

1. 跟踪修改过程。
1. 直接从提交中就可以看到原提交的作者信息，体现了对作者的尊重。
1. 自然的提交过程。这极大方便了代码细节演进过程的查看。
1. 极大方便查出那行提交是什么时间、谁做出的。  
`svn`因为合并Crash了自然的提交过程，要追踪很痛苦。

:beer: 修正提交
-------------------

- `git`：可以修正提交。  
使用功能分支工作流，在自己的分支可以方便修正提交而不会影响大家。
- `svn`：一旦提交就到服务器上，实际使用中就是不能修改。  
（`svn`可以在服务器上修改，因为过程复杂需要权限实际上从不会这样做。）

实际使用中会有误提交的情况（如提交了一个不该提交的日志文件），对于`svn`来说，就是让大家一遍又一遍看到这个垃圾文件。

没有干净的提交，严重影响了`Code Review`，增加成本。

另外对于想了解演进过程的同学，垃圾提交影响了了解效果。

:beer: 廉价好用的本地分支
-------------------

- `git`：有本地分支
- `svn`：无本地分支

`git`可以方便创建本地分支，且创建分支的时间是`O(1)`，即瞬间就创建好了。由于分支可以是本地的，也就不存在`svn`目录权限的问题。

可以从想要工作点闪电般创建本地分支，本地实验不确定的修改，创建分支如此之廉价，`git`推荐创建分支来隔离修改。

:beer: 更强大智能的合并能力
----------------

- `git`：重命名（无论文件还有目录）提交 可以合并上 文件重命名前的这些文件的提交。
- `svn`：重命名（无论文件还有目录）提交后，你本地/或是分支上 有文件重命名前的这些文件的修改或提交，在做合并操作时，恭喜:see_no_evil:，你会碰上传说中难搞的***树冲突***！

因为惧怕`svn`***树冲突***，在包名调整（重命名目录）或类名调整（重命名文件）前，我不得不先向一起开发的组员广播：

1. 提交你的修改
1. 暂停相关类的修改
1. 我开始做调整
1. 等我修改好后:scream:，你再开始修改

OMG～ :confounded:～～

因为这个过程烦琐，结果就是影响了大家去做这样重构操作的积极性，进而影响项目的代码质量改进！

别忘了，如果你的项目是开源的，全球的人可以给你提交，可没有办法向全球的同学广播 :kissing:

:beer: 一等公民支持`tag`
-------------------

- `svn`在模型上是没有分支和`tag`的。`tag`是通过目录权限限制（对开发只读）来保证不变。
- `git`模型上一等公民支持`tag`，保证只读。

内心是不是有强烈的安全感？ :sparkles:

:beer: 完整配套的开发过程设施
-------------------

与`git`配套的`github`、`gitlab`（我们公司搭建了）提供了：

- `Markdown`：高效的文档编写和查看。
- `Issue` & `Milestone`：问题记录&跟踪，任务分配，版本规划&管理
- `Wiki`系统：体系的文档
- 评论：可以对代码提交（即是Code Review）& Issue做评论。  
这个有记录交流的过程。

记住，上面的一切和代码一起集中管理，是以代码为中心的，可以方便的工程中的代码。

可运行并完成功能的代码（且叫目标代码） 才是整体项目真正生效的产出。

一切不为 目标代码 服务 的东东都是 **流氓**！  
\# 是不是想到很多东西（比如下压式的排期计划）会觉得自己是生效的产出，好像剩下的事就是 码农搬砖一样把代码码好。

:beer: 热操作有闪电般的速度
-------------------

### 提交

- `git`提交是个本地操作，相对`svn`闪电一般。
- `git`提供了暂存区，可以方便指定提交内容，而不是全部。  
PS： `git`可以只提交一个文件修改的一部分而非全部（`git add –p`），使用相对繁琐些。（实际上开发中我很少这么做 :grin:）

这让开发者更愿意整理提交，让每个提交更内聚自包含。进而有利于

- `Code Review`
- 线上`Bug`的快速准确的回滚式修复

### 查看日志

查看日志是个频繁的操作。

- `git`：本地包含了完整的日志，闪电的速度（并且无需网络）。
- `svn`：需要从服务拉取。

一旦用了`git`后，等待`svn`日志（包括查看2个版本间的`diff`）过程简直让我发狂。
duide


---
__Advertisement :)__

- __[pica](https://nodeca.github.io/pica/demo/)__ - high quality and fast image
  resize in browser.
- __[babelfish](https://github.com/nodeca/babelfish/)__ - developer friendly
  i18n with plurals support and easy syntax.

You will like those projects!

---

# h1 Heading 8-)
## h2 Heading
### h3 Heading
#### h4 Heading
##### h5 Heading
###### h6 Heading


## Horizontal Rules

___

---

***


## Typographic replacements

Enable typographer option to see result.

(c) (C) (r) (R) (tm) (TM) (p) (P) +-

test.. test... test..... test?..... test!....

!!!!!! ???? ,,  -- ---

"Smartypants, double quotes" and 'single quotes'


## Emphasis

**This is bold text**

__This is bold text__

*This is italic text*

_This is italic text_

~~Strikethrough~~


## Blockquotes


> Blockquotes can also be nested...
>> ...by using additional greater-than signs right next to each other...
> > > ...or with spaces between arrows.


## Lists

Unordered

+ Create a list by starting a line with `+`, `-`, or `*`
+ Sub-lists are made by indenting 2 spaces:
  - Marker character change forces new list start:
    * Ac tristique libero volutpat at
    + Facilisis in pretium nisl aliquet
    - Nulla volutpat aliquam velit
+ Very easy!

Ordered

1. Lorem ipsum dolor sit amet
2. Consectetur adipiscing elit
3. Integer molestie lorem at massa


1. You can use sequential numbers...
1. ...or keep all the numbers as `1.`

Start numbering with offset:

57. foo
1. bar


## Code

Inline `code`

Indented code

    // Some comments
    line 1 of code
    line 2 of code
    line 3 of code


Block code "fences"

```
Sample text here...
```

Syntax highlighting

``` js
var foo = function (bar) {
  return bar++;
};

console.log(foo(5));
```

## Tables

| Option | Description |
| ------ | ----------- |
| data   | path to data files to supply the data that will be passed into templates. |
| engine | engine to be used for processing templates. Handlebars is the default. |
| ext    | extension to be used for dest files. |

Right aligned columns

| Option | Description |
| ------:| -----------:|
| data   | path to data files to supply the data that will be passed into templates. |
| engine | engine to be used for processing templates. Handlebars is the default. |
| ext    | extension to be used for dest files. |


## Links

[link text](http://dev.nodeca.com)

[link with title](http://nodeca.github.io/pica/demo/ "title text!")

Autoconverted link https://github.com/nodeca/pica (enable linkify to see)


## Images

![Minion](https://octodex.github.com/images/minion.png)
![Stormtroopocat](https://octodex.github.com/images/stormtroopocat.jpg "The Stormtroopocat")

Like links, Images also have a footnote style syntax

![Alt text][id]

With a reference later in the document defining the URL location:

[id]: https://octodex.github.com/images/dojocat.jpg  "The Dojocat"


## Plugins

The killer feature of `markdown-it` is very effective support of
[syntax plugins](https://www.npmjs.org/browse/keyword/markdown-it-plugin).


### [Emojies](https://github.com/markdown-it/markdown-it-emoji)

> Classic markup: :wink: :crush: :cry: :tear: :laughing: :yum:
>
> Shortcuts (emoticons): :-) :-( 8-) ;)

see [how to change output](https://github.com/markdown-it/markdown-it-emoji#change-output) with twemoji.


### [Subscript](https://github.com/markdown-it/markdown-it-sub) / [Superscript](https://github.com/markdown-it/markdown-it-sup)

- 19^th^
- H~2~O


### [\<ins>](https://github.com/markdown-it/markdown-it-ins)

++Inserted text++


### [\<mark>](https://github.com/markdown-it/markdown-it-mark)

==Marked text==


### [Footnotes](https://github.com/markdown-it/markdown-it-footnote)

Footnote 1 link[^first].

Footnote 2 link[^second].

Inline footnote^[Text of inline footnote] definition.

Duplicated footnote reference[^second].

[^first]: Footnote **can have markup**

    and multiple paragraphs.

[^second]: Footnote text.


### [Definition lists](https://github.com/markdown-it/markdown-it-deflist)

Term 1

:   Definition 1
with lazy continuation.

Term 2 with *inline markup*

:   Definition 2

        { some code, part of Definition 2 }

    Third paragraph of definition 2.

_Compact style:_

Term 1
  ~ Definition 1

Term 2
  ~ Definition 2a
  ~ Definition 2b


### [Abbreviations](https://github.com/markdown-it/markdown-it-abbr)

This is HTML abbreviation example.

It converts "HTML", but keep intact partial entries like "xxxHTMLyyy" and so on.

*[HTML]: Hyper Text Markup Language

### [Custom containers](https://github.com/markdown-it/markdown-it-container)

::: warning
*here be dragons*
:::


[https://www.webpagefx.com/tools/emoji-cheat-sheet/](https://www.webpagefx.com/tools/emoji-cheat-sheet/)

\*\* Cancel Markdown Key Word

