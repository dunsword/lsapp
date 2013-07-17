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
alter table ls_topic change content content mediumtext null;
alter table ls_topicreply change content content mediumtext null;
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

5.2013-5-24
TopicReply,添加is_chapter字段
<pre><code>
ALTER TABLE  `ls_topicreply` ADD  `is_chapter` tinyint(1)  default 0 not NULL ;
ALTER TABLE  `ls_topicreply` ADD   `source_url` varchar(200) default  NULL;

</code></pre>

6.2013-5-27
Document，添加source_tid
<pre><code>
ALTER TABLE  `ls_document` ADD  `source_tid` bigint NOT NULL default 0;
</code></pre>

7.2013-5-31
TopicReply ，添加索引
<pre><code>
CREATE INDEX `ls_topicreply_27d438ea` ON `ls_topicreply` (`topicid`, `is_chapter`);
</code></pre>

8.2013-6-2
TopicReply ，添加字段
<pre><code>
alter table `ls_document` ADD  `source_uid` bigint NOT NULL default 0;
ALTER TABLE  `ls_topicreply` ADD  `source_pid` bigint NOT NULL default 0;
alter table `ls_topicreply` change  `source_url` `source_url` varchar(200);
</code></pre>

9.2013-6-16
Document
<pre><code>
alter table ls_document add column `source_cover_img` varchar(200);
</code></pre>

10.2013-06-29
保存大人列表
<pre><code>

CREATE TABLE `sync_source_author` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `created_at` datetime NOT NULL,
    `updated_at` datetime NOT NULL,
    `uid` bigint NOT NULL,
    `username` varchar(100) NOT NULL,
    `desc` varchar(1000) NOT NULL,
    `site_id` integer NOT NULL
)
;
CREATE INDEX `sync_source_author_96511a37` ON `sync_source_author` (`created_at`
);
CREATE INDEX `sync_source_author_a11a40ab` ON `sync_source_author` (`updated_at`
);
CREATE INDEX `sync_source_author_82ae9392` ON `sync_source_author` (`uid`);
CREATE INDEX `sync_source_author_66fec48f` ON `sync_source_author` (`site_id`);
CREATE INDEX `sync_source_author_47b71727` ON `sync_source_author` (`uid`, `site_id`);


</code></pre>


11.2013-07-04
在User表添加了用户信息，另外添加了version表
<pre><code>
alter table base_user add column `mobile` varchar(30) UNIQUE;
alter table base_user add column `mobile_bind` bool NOT NULL;
alter table base_user add column `reg_source` smallint NOT NULL;

alter table `base_user` ADD  `mobile` varchar(30) UNIQUE;
alter table `base_user` ADD  `mobile_bind` bool NOT NULL;
alter table `base_user` ADD  `reg_source` smallint NOT NULL;

CREATE TABLE `lsapp_version` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `version` varchar(30) UNIQUE not null,
    `desc` varchar(200),
    `created_at` timestamp NOT NULL default CURRENT_TIMESTAMP
);
insert into `lsapp_version` (`version`,`desc`) values('2013-07-04','add mobile and reg_source for user');


CREATE TABLE `ls_bookmark` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `created_at` datetime NOT NULL,
    `updated_at` datetime NOT NULL,
    `uid` integer NOT NULL,
    `tid` integer NOT NULL,
    `rid` integer NOT NULL,
    `title1` varchar(255) NOT NULL,
    `title2` varchar(255) NOT NULL
);
CREATE INDEX `ls_bookmark_96511a37` ON `ls_bookmark` (`created_at`);
CREATE INDEX `ls_bookmark_a11a40ab` ON `ls_bookmark` (`updated_at`);
CREATE INDEX `ls_bookmark_82ae9392` ON `ls_bookmark` (`uid`);

</code></pre>

12. 20130707
<pre><code>
CREATE TABLE `ls_comment` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `status` integer NOT NULL,
    `created_at` datetime NOT NULL,
    `updated_at` datetime NOT NULL,
    `uid` integer NOT NULL,
    `username` varchar(256) NOT NULL,
    `topicid` integer NOT NULL,
    `replyid` integer NOT NULL,
    `content` longtext NOT NULL,
    `source_uid` integer NOT NULL
)
;
CREATE INDEX `ls_comment_48fb58bb` ON `ls_comment` (`status`);
CREATE INDEX `ls_comment_96511a37` ON `ls_comment` (`created_at`);
CREATE INDEX `ls_comment_a11a40ab` ON `ls_comment` (`updated_at`);
CREATE INDEX `ls_comment_a9db1261` ON `ls_comment` (`topicid`);
CREATE INDEX `ls_comment_7cc7297e` ON `ls_comment` (`replyid`);
insert into `lsapp_version` (`version`,`desc`) values('2013-07-07','add comment table');
</code></pre>

12. 20130707
<pre><code>
CREATE TABLE `base_userloginlog` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `uid` integer NOT NULL,
    `src` smallint NOT NULL,
    `src_uuid` varchar(256),
    `login_time` datetime NOT NULL,
    `raw_pass` varchar(256),
    `ip` varchar(20),
    `port` smallint NOT NULL
);

CREATE INDEX `base_userloginlog_82ae9392` ON `base_userloginlog` (`uid`);
insert into `lsapp_version` (`version`,`desc`) values('2013-07-09','add login log table');
</code></pre>


12. 201307011
<pre><code>
alter table `ls_comment` ADD  `source_id` bigint unique;
alter table `ls_comment` change `uid` `uid` bigint NOT NULL;
alter table `ls_comment` change `topicid` `topicid` bigint NOT NULL;
alter table `ls_comment` change `replyid` `replyid` bigint NOT NULL;
alter table `ls_comment` change `source_uid` `source_uid` bigint NOT NULL;
CREATE INDEX `ls_comment_48fb58cc` ON `ls_comment` (`source_id`);
insert into `lsapp_version` (`version`,`desc`) values('2013-07-11','add source rate id in comment table');
</code></pre>

13.20130717
<pre><code>
CREATE INDEX `ls_topicreply_topicid_source_pid_ea` ON `ls_topicreply` (`topicid`,`source_pid`);
insert into `lsapp_version` (`version`,`desc`) values('2013-07-17','index for ls_topicreply for performance');
</code></pre>