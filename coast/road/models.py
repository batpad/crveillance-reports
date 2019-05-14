from datetime import timedelta
from django.db import models
from django.contrib.auth.models import User
from model_utils.models import TimeStampedModel

class Place(models.Model):
    name = models.CharField(max_length=512)
    slug = models.SlugField(max_length=256, db_index=True, help_text='URL Friendly name for the place, eg. worli-dairy')
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)

    def __str__(self):
        return self.name

class Video(models.Model):
    place = models.ForeignKey(Place, on_delete=models.PROTECT)
    start_time = models.DateTimeField(db_index=True)
    end_time = models.DateTimeField()
    video = models.FileField()
    thumbnail = models.ImageField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    def get_title(self):
        return '%s: %s' % (self.place.name, self.start_time.strftime('%d/%m/%Y, %H:%M:%S'))

    def get_day_link(self):
        return '/place/%s/%d/%d/%d' % (self.place.slug, self.start_time.year, self.start_time.month, self.start_time.day)

    def get_next_video(self):
        video_class = type(self)
        next_video = video_class.objects.filter(place=self.place, start_time__gt=self.start_time).order_by('start_time')[0:1]
        if (len(next_video) > 0):
            return next_video[0]
        else:
            return None

    def get_previous_video(self):
        video_class = type(self)
        previous_video = video_class.objects.filter(place=self.place, start_time__lt=self.start_time).order_by('-start_time')[0:1]
        if (len(previous_video) > 0):
            return previous_video[0]
        else:
            return None        
    class Meta:
        unique_together = ['start_time', 'end_time']
        
    def __str__(self):
        return self.get_title()

class Image(models.Model):
    place = models.ForeignKey(Place, on_delete=models.PROTECT)
    time = models.DateTimeField()
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return str(self.time)

class ReportCategory(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

SEVERITY_CHOICES = (
    (0, 'Not Relevant'),
    (1, 'Minor'),
    (2, 'Medium'),
    (3, 'Heavy'),
    (4, 'Severe'),
    (5, 'Critical')
)

class VideoReport(TimeStampedModel):
    video = models.ForeignKey(Video, on_delete=models.PROTECT)
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)
    timecode = models.IntegerField(help_text='timecode of incident, saved in ms')
    frame_base64 = models.TextField(blank=True, null=True)
    title = models.CharField(blank=True, null=True, max_length=512)
    reporter_name = models.CharField(blank=True, null=True, max_length=255)
    description = models.TextField()
    category = models.ForeignKey(ReportCategory, on_delete=models.PROTECT, null=True, blank=True)
    point_x = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    point_y = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    point_radius = models.IntegerField(blank=True, null=True)
    severity_level = models.IntegerField(choices=SEVERITY_CHOICES, db_index=True, null=True, blank=True)
    is_verified = models.BooleanField(default=False, db_index=True)

    def get_timestamp(self):
        video_start = self.video.start_time
        return video_start + timedelta(seconds = self.timecode / 1000.0)

    def get_next_report(self):
        report_class = type(self)
        next_report = report_class.objects.filter(created__gt=self.created).order_by('created')[0:1]
        if (len(next_report) > 0):
            return next_report[0]
        else:
            return None

    def get_previous_report(self):
        report_class = type(self)
        previous_report = report_class.objects.filter(created__lt=self.created).order_by('-created')[0:1]
        if (len(previous_report) > 0):
            return previous_report[0]
        else:
            return None 

    def get_absolute_url(self):
        return '/report/video/%d' % self.id
        
    def __str__(self):
        return self.description

class ImageReport(TimeStampedModel):
    image = models.ForeignKey(Image, on_delete=models.PROTECT)
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)
    description = models.TextField()
    category = models.ForeignKey(ReportCategory, on_delete=models.PROTECT, null=True, blank=True)
    severity_level = models.IntegerField(choices=SEVERITY_CHOICES, db_index=True, blank=True, null=True)
    is_verified = models.BooleanField(default=False, db_index=True)

    def __str__(self):
        return self.description    


