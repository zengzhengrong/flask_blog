# flask_blog
用flask 搭建的blog-[测试链接](http://47.106.195.247:800)
```
内置户名：admin@163.com
pw: admin123
```
### Docker deploy already
 - nginx+gunicorn+postgresql

## 一键部署

### 下载repo
```
git clone https://github.com/zengzhengrong/flask_blog.git
```

### 修改域名或IP
进入 flask_nginx.conf 修改：  

**server_name 成你的域名或者IP地址**  

==如果要修改监听端口,记得Dockerfile的ports也要改==

### 进入目录并运行docker-compose up

```
cd flask_blog
docker-compose up
```
尝试访问 IP:800

### 移除容器、挂载卷和镜像

依然在目录下执行
```
docker-compose down -v --rmi all
```


