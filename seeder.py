import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "web_interface.settings")
django.setup()

from harvester.models import Query

initial_queries = [
    "हिंदी भाषा सीखने",
    "हिंदी व्याकरण सीखने",
    "हिंदी वर्णमाला सीखने",
    "बेहतरीन हिंदी भाषा सीखने",
    "हिंदी भाषा के शब्द सीखने",
    "हिंदी बोलना सीखने",
    "हिंदी में संवाद सीखने",
    "हिंदी में लिखना सीखने",
    "हिंदी भाषा के बेहतरीन शिक्षण",
]

for query in initial_queries:
    new_query = Query(query=query)
    new_query.save()

print("Seeding Completed!")
