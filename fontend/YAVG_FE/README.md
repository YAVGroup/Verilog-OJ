# 前端



## 本地运行

```
npm install
npm run dev
```



## 部署


编译完毕后，网站文件保存在dist目录中，接下来部署到服务器中

+ 推荐使用Nginx

```
sudo apt-get install nginx
```

将dist文件夹中的文件复制到Web服务器目录中（默认根目录 **/var/www/html/**）
接下来修改Nginx配置文件（不同版本可能在不同的地方）

```
sudo nano /etc/nginx/nginx.conf
```

主要修改如下几个配置

1. 路由重定向
2. API重定向

将如下配置复制到http{}中

```
server{
    listen 80;
    server_name www.lpoj.cn;  # 此处填写你的域名或IP地址
    root /var/www/html;   # 此处填写你的网页根目录
    location /api {  # 将API重定向到后台服务器（如果你修改了前端中的代理配置，这里需要对应的修改）
        rewrite ^.*api/?(.*)$ /$1 break;
        proxy_pass http://localhost:8000; # 填写你的后端地址和端口
    }
    location / {  # 路由重定向以适应Vue中的路由
        index index.html;
        try_files $uri $uri/ /index.html;
    }
}
```

其他配置请自行参考Nginx配置



## 项目框架

### src：

```
./
├── App.vue       网站的入口
├── components		
│   ├── admin/    网站主要的控件
│   ├── chart/    网站后台相关的控件
│   ├── contest/  网站比赛页面相关的控件
│   ├── main.vue  网站的首页
│   ├── mainpage/ 网站主要的页面的相关控件
│   ├── problem/  网站题目相关的控件
│   ├── utils/    网站一些有用的控件
│   └── wiki/     网站Wiki页相关的控件
├── login.vue     登录控件
├── main.js       网站的Js入口
├── register.vue  注册控件
└── router
    └── index.js  网站的路由信息

```

### admin（管理员控件）:

```
./
├── adminaddchoiceproblem.vue
├── adminaddcontest.vue
├── adminaddproblem.vue
├── adminboard.vue
├── adminchangechoiceproblem.vue
├── adminchangecontest.vue
├── adminchangepro.vue
├── adminclassmanage.vue
├── adminmanageuser.vue
├── adminrejudge.vue
├── adminsetting.vue
├── admintrainning.vue
└── givechoiceproblemscore.vue
```

#### mainpage

```
./
├── admin.vue							//管理员界面
├── billboard.vue
├── blog.vue							//博客界面
├── classdetail.vue				//班级细节
├── classes.vue						//班级界面
├── contest.vue						//竞赛界面（暂不用）
├── homework.vue					//作业界面
├── problem.vue						//问题主界面
├── rank.vue							//排名界面
├── setting.vue						//设置界面
├── statue.vue						//Status页面
├── user.vue							//用户界面修改
└── wiki.vue							//wiki界面
```

### problem:

```
./
└── problemdetail.vue            //单个problem的详细界面
```



### utils:

```
./
├── acrank.vue							//主页用AC排名控件（暂不用）
├── algorithmselect.vue
├── blogmini.vue
├── cfrate.vue							//主页用 CF排名控件（暂不用）
├── contestmini.vue					//主页用的竞赛信息（暂不用）
├── description.vue					//主页的描述OJ信息控件
├── languageselect.vue			//语言选择控件（应不用，暂未改）
├── ojmessage.vue						//主页用留言控件（暂不用）
├── prostatistice.vue				//问题界面的题目信息统计（（应不用，暂未改））
├── ratingrule.vue					//主页用排名规则
├── soulrow.vue							//主页最上层的一些小部件，搜索和新闻类似的东西
├── statusmini.vue					//问题界面的当前提交记录状态栏控件
├── todolist.vue					//Todo控件
├── topuser.vue						//主页用前10排名控件
├── welcomemessage.vue		//主页的欢迎控件
└── wikidetail.vue
```

### admin（管理员控件）:

```
./
├── adminaddchoiceproblem.vue
├── adminaddcontest.vue
├── adminaddproblem.vue
├── adminboard.vue
├── adminchangechoiceproblem.vue
├── adminchangecontest.vue
├── adminchangepro.vue
├── adminclassmanage.vue
├── adminmanageuser.vue
├── adminrejudge.vue
├── adminsetting.vue
├── admintrainning.vue
└── givechoiceproblemscore.vue
```

### Chart 

```
./
├── echarts.js
├── rankchart.vue			//主页排名图控件（暂不用）
├── ratingchart.vue
└── teamchart.vue
```

### wiki（暂不用）:

```
./                //暂时不用
├── algorithm.vue
├── algorithmpages
│   ├── basic.vue
│   ├── dp.vue
│   ├── ds.vue
│   ├── editalgorithm.vue
│   ├── geometry.vue
│   ├── graph.vue
│   ├── intro.vue
│   ├── math.vue
│   ├── misc.vue
│   ├── search.vue
│   └── string.vue
├── code.vue
├── mbcode
│   ├── codeedit.vue
│   ├── viewcode.vue
│   └── viewcodedetail.vue
├── newalgorithm.vue
├── trainning
│   └── trainningdetail.vue
└── trainning.vue
```

### contest（暂不用）

```
./
├── contestannounce.vue
├── contestchoiceproblem.vue
├── contestcomment.vue
├── contestdetail.vue
├── contestoverview.vue
├── contestproblem.vue
├── contestrank.vue
├── contestsubmit.vue
└── contesttutorial.vue
```



## TODO

- soulrow中的新闻部件没有后端对应
- soulrow中的Search可以改成教学的wiki

