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

###数据库更新：
1.2012-05-09
Document： 
<pre><code>
  source_updated_at=models.DateTimeField(u'原文章最后更新时间', default=datetime.now(),db_index=True)
  
  ALTER TABLE  `ls_document` ADD  `source_updated_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP AFTER  `topic_id` ,
  ADD INDEX (  `source_updated_at` )
</code></pre>

2.添加数据表：用于记录收录过的来源站点document信息。
cron_documentmapping
<pre><code>
CREATE TABLE `cron_documentmapping` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `document_id` bigint(20) NOT NULL,
  `source_document_id` bigint(20) NOT NULL,
  `source_id` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
/*!40101 SET character_set_client = @saved_cs_client */;
</code></pre>

3.添加数据库表：用户记录每个分类下相应的作者uid和name,有初始化数据cron-0509.json
cron_categoryauthor
<pre><code>
CREATE TABLE `cron_categoryauthor` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `uid` bigint(20) NOT NULL,
  `authorName` varchar(256) COLLATE utf8_bin NOT NULL,
  `cid` bigint(20) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=512 DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
</code></pre>

4.Topic，添加last_reply_at
<pre><code>
ALTER TABLE  `ls_topic` ADD  `last_reply_at` DATETIME NULL AFTER  `reply_count` ,
ADD INDEX (  `last_reply_at` );
update ls_topic set last_reply_at=updated_at;
</code></pre>

5.2013-5-17
Topic,TopicReply，扩展content长度
<pre><code>
alter table ls_topic change content content text null;
alter table ls_topic_reply change content content text null;
</code></pre>

5.2013-5-19
User,添加bind字段
<pre><code>
ALTER TABLE  `base_user` ADD  `email_bind` tinyint(1)  default 0 not NULL AFTER  `email`;
ALTER TABLE  `base_user` ADD  `is_bind` tinyint(1)  default 0 not NULL AFTER  `is_active`;
</code></pre>

6.2013-5-21
base.EmailBindRecord
<pre></code>
CREATE TABLE `base_emailbindrecord` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `created_at` datetime NOT NULL,
    `updated_at` datetime NOT NULL,
    `userid` integer NOT NULL,
    `email` varchar(75) NOT NULL,
    `active_code` varchar(128) NOT NULL,
    `is_used` bool NOT NULL
)
;
CREATE INDEX `base_emailbindrecord_3b1c9c31` ON `base_emailbindrecord` (`created_at`);
CREATE INDEX `base_emailbindrecord_f84f7de6` ON `base_emailbindrecord` (`updated_at`);
CREATE INDEX `base_emailbindrecord_7444f637` ON `base_emailbindrecord` (`userid`);
COMMIT;
</code></pre>
