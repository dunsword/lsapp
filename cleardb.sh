./manage.py sqlclear album base  sessions auth contenttypes sites > clear_sql/clear.sql
mysql -upaul -ppassword -Dapp_weibols < clear_sql/drop_custom.sql
mysql -upaul -ppassword -Dapp_weibols < clear_sql/clear.sql
