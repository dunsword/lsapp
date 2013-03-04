manage.py sqlclear album base auth contenttypes sessions  sites > clear_sql/clear.sql
mysql -upaul -ppassword -Dmyhome < clear_sql/drop_custom.sql
mysql -upaul -ppassword -Dmyhome < clear_sql/clear.sql