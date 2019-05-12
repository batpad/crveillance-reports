from django.contrib import admin
from .models import Place, ReportCategory, Video, VideoReport, Image, ImageReport 

admin.site.register(Place)
admin.site.register(ReportCategory)
admin.site.register(Video)
admin.site.register(VideoReport)
admin.site.register(Image)
admin.site.register(ImageReport)

