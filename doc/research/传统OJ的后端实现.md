# 传统OJ的后端实现调研

这里调研了传统OJ（指面向ACM、OI等竞赛的在线评测平台）的后端实现。
一般来说后端会包括web服务和评测两部分的内容，并且这两部分通常是分开实现的。**这里我们主要关注web服务的后端功能**。

主要参考Github上开源的两个OJ平台：[QDUOJ](https://github.com/QingdaoU/OnlineJudge)和[LPOJ](https://github.com/Linzecong/LPOJ)。
这两个OJ的前端使用Vue.js而后端使用Django+Django REST Framework，符合我们的技术选型。

## 后端包括的主要功能

一般来说，后端需要实现的功能会划分为若干部分，每个部分由一个Django应用来实现。

QDUOJ的后端包括的Django应用有：account账号管理 announcement公告 conf配置 contest比赛 problem题库 submission提交 options utils

LPOJ的后端包括的Django应用有：problem题库 judgestatus评测状态 user用户管理 contest比赛 board榜单 blog博客（也有留言） wiki item事项（如补题） classes班级

由此可见，OJ后端一般包括的功能有以下几种：

- 用户管理
- 题目数据
- 提交（评测）
- 其他扩展性功能，如比赛、博客等

我们对用户管理以及提交评测功能的实现比较感兴趣，所以深入调研了一下这两个功能在QDUOJ/LPOJ中的实现方式。

## 用户管理的实现

在QDUOJ中，用户主要就分为普通用户和管理员两种，实现在[account应用](https://github.com/QingdaoU/OnlineJudge/tree/master/account)中。
普通用户实现的功能主要包括基本信息、登录、双重验证、邮箱验证、注册、邮箱/密码修改、排名等。
管理员主要是可以管理用户，包括用户列表、获取/修改用户属性、创建新用户、删除用户等。

在LPOJ中，用户管理在[user应用](https://github.com/Linzecong/LPOJ/blob/master/Backend/user)中实现，并且以普通用户为主。
其功能包括基本信息、修改信息、登入登出、排名更新、注册等。

考虑到我们的Verilog OJ面向课程实验使用，这些传统OJ的用户管理和我们需要的用户管理存在一定差距。
经过之前的组内讨论，我们对用户管理的需求应该会包括：

- 普通用户和管理员
- 普通用户可以通过邮箱注册，或者使用统一身份认证登录
- 基本的功能，如用户信息、登入登出
- 班级功能，管理员可以建立班级，添加或者删除其中的用户

## 提交评测的实现

QDUOJ的网页服务器和判题服务器是分开的。评测的执行环境（沙箱）在 https://github.com/QingdaoU/Judger 用C写成，并有python等的接口。其实现原理见 https://docs.onlinejudge.me/#/judger/how_it_works 。

评测的环境是放在独立的docker容器里的，这个docker的代码在 https://github.com/QingdaoU/JudgeServer ，它使用gunicorn运行一个web服务器，通过接收URL的方式获取评测任务（普通评测/SPJ），进行编译和运行。

后端里关于评测功能涉及两个django应用。submission模块在 https://github.com/QingdaoU/OnlineJudge/tree/master/submission/views 中实现了用户的提交功能和管理员的重判功能。[提交过程](https://github.com/QingdaoU/OnlineJudge/blob/master/submission/views/oj.py#L50)包括基本的权限检查、在数据库（Model）中创建提交数据、执行评测任务。

执行评测任务这一步是通过dramatiq完成异步任务分配的（旧版用的是celery），会调用一个[judge模块中的函数](https://github.com/QingdaoU/OnlineJudge/blob/master/judge/tasks.py#L10)，进一步将评测任务分配给某个评测环境（服务器）、执行评测，将评测结果以及其他信息保存到数据库（Model）中。

在LPOJ中，不再是由web后端主动分配评测任务、调用评测服务器，而是由评测服务器主动查询尚未完成的评测，将其加入自己的判题队列中进行评测。LPOJ的评测环境则直接使用了QDUOJ的评测环境。