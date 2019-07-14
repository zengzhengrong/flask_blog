# flask_blog
[test-link](http://47.106.195.247:800)
```
username：admin@163.com
pw: admin123
```
### Docker deploy already
 - nginx+gunicorn+postgresql

## Usage

### Download repo
```
git clone https://github.com/zengzhengrong/flask_blog.git
```

### Edit 
flask_nginx.conf：  

```server_name your-domainname or ip```

### Run

```
cd flask_blog
docker-compose up
```
test your-domainname or ip:800

### Remove

```
./flask_blog
docker-compose down -v --rmi all
```
