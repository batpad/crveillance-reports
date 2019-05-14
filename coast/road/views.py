from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from datetime import datetime
from .models import Place, ReportCategory, Video, VideoReport
from django.views.decorators.csrf import ensure_csrf_cookie

def home(request):
    return render(request, 'home.html')

def places(request):
    return render(request, 'places.html', {
        'places': Place.objects.all()
    })

def place(request, slug):
    place = get_object_or_404(Place, slug=slug)
    #TODO: add counts for month: https://stackoverflow.com/questions/8746014/django-group-by-date-day-month-year
    months = Video.objects.filter(place=place).dates('start_time', 'month', order='DESC')
    return render(request, 'place.html', {
        'months': months,
        'place': place
    })

def month(request, place_slug, year, month):
    place = get_object_or_404(Place, slug=place_slug)
    videos_for_month = Video.objects.filter(place=place, start_time__year=year, start_time__month=month)
    days = videos_for_month.dates('start_time', 'day', order='DESC')
    dt = datetime(year, month, 1)
    return render(request, 'month.html', {
        'days': days,
        'place': place,
        'year': year,
        'month': month,
        'month_dt': dt
    })


def day(request, place_slug, year, month, day):
    place = get_object_or_404(Place, slug=place_slug)
    videos = Video.objects.filter(place=place, start_time__year=year, start_time__month=month, start_time__day=day).order_by('start_time')
    dt = datetime(year, month, day)
    return render(request, 'day.html', {
        'videos': videos,
        'day': dt,
        'place': place
    })

@ensure_csrf_cookie
def video(request, id):
    video = get_object_or_404(Video, id=id)
    return render(request, 'video.html', {
        'video': video,
        'previous_video': video.get_previous_video(),
        'next_video': video.get_next_video(),
        'existing_reports': VideoReport.objects.filter(video=video)
    })

def reports(request):
    #TODO: add filtering for reports, add image reports
    return render(request, 'reports.html', {
        'reports': VideoReport.objects.all()
    })

def report(request, typ, id):
    rep = get_object_or_404(VideoReport, id=id)
    return render(request, 'report.html', {
        'report': rep,
        'previous_report': rep.get_previous_report(),
        'next_report': rep.get_next_report()
    })

def add_report(request):
    description  = request.POST['description']
    title = request.POST['title']
    if description == '' or title == '':
        return JsonResponse({
            'error': 'Title or description cannot be empty'
        }, status=400)
    reporter_name = request.POST['reporter_name']
    frame_base64 = request.POST['frame_base64']
    video = request.POST['video']
    timecode = request.POST['timecode']        
    vr = VideoReport()
    vr.title = title
    vr.description  = description
    vr.reporter_name = reporter_name
    vr.frame_base64 = frame_base64
    vr.video_id = int(video)
    vr.timecode = timecode
    if ('point_x' in request.POST):
        vr.point_x = request.POST['point_x']
        vr.point_y = request.POST['point_y']
        vr.point_radius = request.POST['point_radius']
    vr.save()
    return JsonResponse({
        'report_id': vr.id
    })
    

