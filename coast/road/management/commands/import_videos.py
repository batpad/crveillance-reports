import os
import datetime
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
import glob
from road.models import Video, Place

def get_int(s):
    num = s.lstrip('0')
    if num:
        return int(num)
    else:
        return 0

def get_time(t):
    year = int(t[0:4])
    month = get_int(t[4:6])
    day = get_int(t[6:8])
    hour = get_int(t[8:10])
    min = get_int(t[10:12])
    return datetime.datetime(year, month, day, hour, min)

'''
    Import videos
'''
class Command(BaseCommand):
    help = 'Run python manage.py fix_tags <path/to/file.csv>'

    def add_arguments(self, parser):
        parser.add_argument('dir')

    @transaction.atomic
    def handle(self, *args, **options):
        input_dir = options['dir']
        
        if not input_dir or not os.path.exists(input_dir):
            self.stderr.write('Please provide a valid path to a folder of videos to be imported')
            return
        place = Place.objects.get(slug='worli-dairy')
        for mp4_path in glob.glob(os.path.join(input_dir, '**/*.mp4'), recursive=True):
            base_path = mp4_path.replace(input_dir, '')
            print('base_path', base_path)
            video_path = os.path.join('videos', base_path)
            print('video_path', video_path)
            existing_videos = Video.objects.filter(video=video_path)
            if existing_videos.count() > 0:
                print('skipping', video_path)
                continue
            image_path = os.path.join('images', base_path.replace('.mp4', '.jpg'))
            filename = os.path.basename(base_path)
            start_time = filename.split('_')[0]
            end_time = filename.split('_')[1].replace('.mp4', '')
            v = Video()
            v.place = place
            v.start_time = get_time(start_time)
            v.end_time = get_time(end_time)
            v.video.name = video_path
            v.thumbnail.name = image_path
            v.description = ''
            print(v.start_time.strftime('%m/%d/%Y, %H:%M:%S'), v.end_time.strftime('%m/%d/%Y, %H:%M:%S'))
            print(v.video.name, v.thumbnail.name)
            v.save()
            
        print('done')

        


                

