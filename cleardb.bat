mysql -upaul -ppassword   < clear_sql/recreatedb.sql
python manage.py syncdb
manage.py loaddata base_user1.json
manage.py loaddata ls_books1.json