from django.contrib import admin

from .models import Question
from .models import Video

admin.site.register(Question)
admin.site.register(Video)
