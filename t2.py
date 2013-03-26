from ls.models import Topic

topics=Topic.objects.all()
for topic in topics:
    print topic.title

quit()