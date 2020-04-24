from django.test import TestCase

# Create your tests here.
import os
import sys
import django

sys.path.append(r'E:\PycharmProjects\DRMDEMO')

os.chdir(r'E:\PycharmProjects\DRMDEMO')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "DRMDEMO.settings")
django.setup()

from apps.operations.models import UserMusic
str = UserMusic.objects.get(id=321).projectname
print(str.encode().decode("unicode-escape"))