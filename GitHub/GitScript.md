<font size=12>**Git**</font> is the same with SVN/CSV as a source code management system. But it's differnt with them, could work at distributed. we could commit at local and will not affect the shared code repository. Git has a lot of features and I list some common usage:
##### 自动使用github用户名和密码提交
```vim
git config --global credential.helper store
```
##### 创建SSH Key
```vim
$ ssh-keygen -t rsa -C "youremail@example.com"
```
如果一切顺利的话，可以在用户主目录里找到.ssh目录，里面有id_rsa和id_rsa.pub两个文件，这两个就是SSH Key的秘钥对，id_rsa是私钥，不能泄露出去，id_rsa.pub是公钥，可以放心地告诉任何人。

第2步：登陆GitHub，打开“Account settings”，“SSH Keys”页面

然后，点“Add SSH Key”，填上任意Title，在Key文本框里粘贴id_rsa.pub文件的内容

##### Config editor:
```vim
$ export GIT_EDITOR=vim
or
$ git config --global core.editor vim
```
##### Compare tools:
```vim
$ git config --global merge.tool vimdiff
$ git config --global diff.tool vimdiff
$ git config --global difftool.prompt No
```

##### Ignore file priority：
```vim
$ git config core.filemode false
```

##### Config personal information：
```vim
$ git config user.name "bearfly1990"
$ git config user.email "bearfly1990@163.com"
```
these `git config` command is writen into `~/.gitconfig`, it's the same to edit this file. e.g. in oreder to hight the output of git command, we could add text like:
```
[color]
	ui=auto
```
##### Create a new Git Repository:
```vim
$ git init
```
##### Check config information
```vim
$ git config --list
```

##### Check repository status
```vim
$ git status
```
##### Check difference between two versions
```vim
$ git diff
```
Because git using `index`, so compare with svn, `git diff` have two types: with `--cached` and without it:
```vim
$ git diff  # show local change but no stage change
$ git diff --cached # show staged local chagne, in other world, the changes will be commited
$ git diff master..test # diff between two branch
$ git diff --stat  # show summary information
```
##### History information
```vim
$ git log
$ git log -p # show patch
$ git log --stat  #s show commit log line by line
$ git log --topo-order --graph # show commit relations by graph
$ git log -n # show top n
$ git show-branch  --more=n # top n commit history
```vim
##### check changs
```vim
$ git show <sha> # check changes for wich commit
```
另外，对工作目录中文件操作有`git ls-files`，`git grep`等命令。
#### 提交(`commit`)
和SVN不同的是，Git中的Checkin分两步，即`stage`和`commit`。如：
```vim
$ git add a.c  # stage改动，更改index（index是一个临时动态文件，描述了整个工程目录，并记录了作了哪些改动）。stage过的改动会在git diff --cached中显示出来。
$ git commit -m "comments" # 提交改动
```
加`-a`参数可以将前面两步合二为一：
```vim
$ git commit -a
```
但它仅限于tracked的文件。比如新建一个文件但没有`git add`过，它还是`untracked`状态，那加`-a`也没用。
#### 补丁(`patch`)
##### 生成补丁
```vim
$ git format-patch -n  master # 生成最近n次commit的patch
$ git format-patch master~4..master~2 # 生成master~4和master~2之间差异的patch
$ git format-patch -s <sha> # 生成指定commit的patch，加签名
```
##### 应用补丁
`git am` 用了`git apply`，用它打补丁会生成commit信息。如果出现错误
`previous rebase directory ../.git/rebase-apply still exists but mbox given`
可以用
```vim
$ git am --abort
```
前面方法用于已经commit的更改，如果是用`git diff`生成的本地修改的patch，则可以用下面方法：
##### 生成本地修改的patch：
```vim
$ git diff | tee diff.patch
```
##### 应用patch时用：
```vim
$ git apply --ignore-space-change --ignore-whitespace diff.patch
```
或者
```vim
$ patc -p1 < diff.patch
```

当然这更像Svn中的习惯，在git里反正是本地提交，提交的成本很低，所以可以先提交再生成patch。
branch之间打patch用：
```vim
$ git cherry-pick
```
##### 撤消(undo)
和撤消相关的有三个命令：git checkout, git revert和git reset。
如取消本地没有stage过的改动（即没有通过git add等命令记录到index中的改动）：
```vim
$ git checkout . # index不变，工作目录改变
```
再如
```vim
$ git checkout HEAD^  # 返档到前一次commit的版本
$ git checkout <sha>  # 返档到指定commit版本
```

`git reset` 不仅作用于工作目录，而且作用于index文件。`git reset`有三种方式，分别为`soft`, `hard`和`mixed`方式。
```vim
$ git reset --soft <sha> # 既不影响index也不影响工作目录，也就是说用git diff --cached还是可以看到撤消的改动
$ git reset --mixed <sha> # index改变，但工作目录不变
$ git reset --hard <sha>，# 将index和工作目录都恢复到指定版本。相当于svn revert -R *
```
撤消后，git log无法看到撤消的commit历史，但可以用下面命令看到：
```vim
$ git reflog
```
`git checkout` 和 `git reset --hard`的区别在于：
```vim
git checkout .  # 清除本地更改，但不清除index。举例来说，之前git add但没commit的作用还在。
git reset --hard HEAD  # 清除本地更改，包括index。所以git add过的也清除了。
```
`git revert` 进行一次与指定版本相反的commit。如：
```vim
$ git revert <sha> # commit一次和<sha>指定commit相反的改动
$ git revert -n <sha> # 和前一命令一样，但不提交
```
`git revert`可以把中间的commit作用消除，且`git revert`不会改变已有的历史记录。当项目是基于已有Git仓库时这很有用。
如果只是想修改commit时的提交信息，可以用：
```vim
$ git commit --amend
```
#### 分支(branch)
##### 新建
```vim
$ git branch new_branch
```
或
```vim
$ git checkout -b new_branch
```
##### 查看
```vim
$ git show-branch
```
##### 提取
```vim
$ git checkout new_branch
```
##### 删除
```vim
$ git branch -d new_branch
```
##### 归并其它分支
```vim
$ git merge branchname
```
##### 将新分支推送到github
```vim
git push origin [branch name]
```
##### 删除github远程分支, 分支名前的冒号代表删除。
```vim
git push origin :[branch name]
```
```vim
git branch -r -d origin/branch-name  
git push origin :branch-name

```
#### 杂项：
某些文件不需要让Git去track，可以在`.gitignore`中设置忽略这些文件。
##### 指定特定文件用--，如：
```vim
$ git checkout -- dir/main.c
```
##### Git有几个内置的符号索引指针：
**HEAD**：永远指向当前分支的最近一次commit
**ORIG_HEAD**：git reset或git merge后，原来的HEAD被存在这里
**FETCH_HEAD**：git fetch后所有分支的头索引指针
**MERGE_HEAD**：git merge时另一分支的头索引指针
**相对索引**：HEAD^ HEAD^^ HEAD~2 HEAD@{2}等

如果手头的工作做了一半，但有一个小的但紧急的bug要fix，可以用git stash。它像一个栈一样将当前的工作上下文push到栈中，当bug fix完了再pop出来。
```vim
$ git stash "current work"
$ git commit -a -m "trivial bug fix"
$ git stash apply
```
##### gitk：图形化的git diff
当碰到regression时，可以用`git bisect`和`git blame`。前者用来查找问题从哪个版本开始出现，后者列出每行代码的修改者和时间。
#### 分布式管理
##### 复制代码仓库
```vim
$ git clone /tmp/repo repo # 在当前目录下创建/tmp/repo的代码仓库拷贝
```
##### 复制远程代码仓库（如用户名zjin，主机名zjin-machine）
```vim
$ git clone zjin@zjin-machine:/home/zjin/repo
```
##### 向远程代码仓库提交
```vim
$ git push /tmp/repo master # 将本地master分支中的改动提交到/tmp/repo中
```
##### 从远程代码仓库同步
```vim
$ git pull /tmp/repo master # 将/tmp/repo中的改动同步到本地的master分支中
```
该命令相当于git fetch 加 git merge
#### 其他(Others)
##### 拷贝别人的Repository给自己用(Clone other's repository as own)
1. Create a new repository at github.com. (this is your repository)
```
    Give it the same name as as the other repository.
    Don't initialize it with a README, .gitignore, or license.
```
2. Clone the other repository to your local machine. (if you haven't done so already)
```
    git clone https://github.com/other-account/other-repository.git
```
3. Rename the local repository's current 'origin' to 'upstream'.
```
    git remote rename origin upstream
```
4. Give the local repository an 'origin' that points to your repository.
```
    git remote add origin https://github.com/your-account/your-repository.git
```
5. Push the local repository to your repository on github.
```
    git push origin master
```
