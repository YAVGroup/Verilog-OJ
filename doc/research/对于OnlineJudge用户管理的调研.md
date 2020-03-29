# 对于OnlineJudge用户管理的调研

## 传统OJ的做法

在一般的OJ系统中，我们一般不会对用户的做额外的分组管理，用户和用户直接的独立性较强，且没有过多关联。除了一些整合了社交性质的OJ，会有简单的好友关系。

这些OJ的单位结构是权限，用通俗的语言描述一下：我们对于每一个用户，我们有各种权限，例如——做题权限，发布题目权限，新增测试数据权限。

而我们希望我们的OJ是组别管理，用户会被分为教师组，学生组，或者助教组。我们对学生用户也会做一些特殊处理，除了之前的信息，我们还会维护班级信息。

## Vue-excel

这里，为了给教师提供方便的操作处理，我觉得我们的用户管理需要支持以下的特性：

1. 简单易懂的用户增删
2. 方便的信息变更
3. 信息的批量导入导出

在调研的时候，我发现Vue2.0的Element组件满足了我们的这些需求

Link:[Element](https://element.eleme.io/)



至于数据的上传，我们可以用Element的Upload组件进行

Link:[Element-Upload](https://element.eleme.io/#/en-US/component/upload)

之后和数据库进行求并集进行维护



一些Excel的交互，我们可以使用[vue-element-admin](https://panjiachen.github.io/vue-element-admin-site/feature/component/excel.html)进行处理:

- Install

  ```bash
  npm install xlsx file-saver -S
  npm install script-loader -S -D
  ```

- Upload Excel Demo

  [Online-Demo-Link](https://panjiachen.github.io/vue-element-admin/#/excel/upload-excel)

- Export Excel Demo

  [Online-Demo-Link](https://panjiachen.github.io/vue-element-admin/#/excel/export-excel)



## 数据库系统的选择

由于vue-element-admin的处理方式，我个人建议我们数据库采用MariaDB

选择理由是我们对于Json的处理有较高的需求，为其单独设置处理组件会需要Ajex，处理方法不是很优雅

[Json Database](https://mariadb.com/resources/blog/the-best-of-both-worlds-relational-json/)

这里我还有一个相关的例子：

[Example](https://go.mariadb.com/JSON-Relational-How-to-use-hybrid-data-models-2019-11-12.html?_ga=2.197860075.531382662.1585446580-181680767.1585446580)



