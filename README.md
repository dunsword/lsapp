#一、开发环境配置
##1、开发环境
1. python2.7
2. 需要的包：MySQL_python\PIL
3. Django1.4
4. 安装nginx
 静态文件路径改为：http://static.lsapp.com, 具体见settings文件的改动

	nginx配置:
	<pre><code>
 	server {
        listen       80;
        server_name static.lsapp.com;
 
        location / {
            root   /workspace/myhome/static; #你的项目路径下的static目录
            index  index.html index.htm;
        }
    }
 	</code></pre>

	本地host绑定
	127.0.0.1 static.lsapp.com
5. 安装sae本地开发包
  <pre><code>
  $ git clone http://github.com/saepython/saepythondevguide.git
  $ cd saepythondevguide/dev_server
  $ python setup.py install
  </code></pre>
  *一般情况下不需要用sae开发环境。但代码中有import，不安装可能会导致页面错误。
  
##2、配置过程
1. 下载项目到本地（废话）
2. 编辑myhome/settings.py, 修改数据库链接等参数
3. 在项目目录下，执行 ./cleardb (windows下执行cleardb.bat)
4. 启动项目：python manage.py runserver 127.0.0.1:8000 --noreload
