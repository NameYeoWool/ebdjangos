from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from .models import Room, SeatInfo, Event, FoodInfo, Coment
from django.http import HttpResponse, JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
from .forms import RoomForm, FoodForm
from django.forms import formset_factory
from django.forms import modelformset_factory
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
import logging
import random
import os
from django.utils import timezone
from django.conf import settings
from PIL import Image
from django.contrib import messages
from django.http import HttpResponseRedirect

logger_seatInfo = logging.getLogger('seatInfo')
logger = logging.getLogger('watcher')

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

dic_name = {
    "프리미엄 PC방_혜화역":0,"1% PC 아레나_혜화역":1,"3POP PC카페_혜화역":2,"닥필 PC존_혜화역":3,
    "세븐 PC방_혜화역":4,"이스포츠센터 PC방_혜화역":5,"웹투나잇 PC방_혜화역":6,
    "헌터 PC방_성대역":10,"탑플레이어 PC방_성대역":11,"아라크네 PC방_성대역":12,"시티파크 PC방_성대역":13,
    "스토리 PC LAB_성대역":14,"라이또 PC방_성대역":15,"LET'S PC_성대역":16,"Gallery PC방_성대역":17,"3POP PC카페_성대역":18,
}

list_error=["zero-size array",
            "'NoneType' object is not subscriptable",
            "'NoneType' object has no attribute 'shape'",
            "OpenCV(4.0.0)"]

# def room_food(request,name):
#     room = Room.objects.filter(name__contains=name)
#     foodInfos = room[0].foodInfo_set.filter(room=room)
#     name_list = []
#     # for foodInfo in foodInfos:
#         # if foodInfo.food_name_1

@csrf_exempt
def review_new(request):
    if request.method == 'POST':
        print(request.POST.get('name'))
        room = get_object_or_404(Room,name=request.POST.get('name'))
        coments = room.coment_set.all()
        cnt_coment = len(coments)

        title = request.POST.get('title')
        content = request.POST.get('content')
        rating = int(request.POST.get('rating'))

        coment = Coment(room = room, title=title,star=rating,content=content)
        coment.save()

        if cnt_coment == 0:
            room.rating = rating
            room.save()
        else:
            room.rating = (room.rating + rating ) / ( cnt_coment + 1 )
            room.save()

        return HttpResponse("ok")








def review_list(request,name):
    room = get_object_or_404(Room,name=name)
    coments = room.coment_set.order_by('created_date')

    res = {"cnt_all":0,
           "rating_mean":room.rating}

    coment_info = []
    if coments:
        res['cnt_all']= len(coments)
        for coment in coments:
            temp = {
                "title":coment.title,
                "rating": coment.star,
                "time": coment.created_date,
                "content":coment.content,
            }
            coment_info.append(temp)
        res['reviews']=coment_info

    return JsonResponse(res, safe=False, json_dumps_params={'ensure_ascii': False})


def room_image(request,name):
    room = get_object_or_404(Room,name=name)
    image = room.image
    return HttpResponse(image, content_type="image/jpeg")

def food_list(request, name):
    room = get_object_or_404(Room,name=name)
    foods = room.foodinfo_set.order_by('rank')

    res = {"cnt_all":0}
    food_info = []
    if foods:
        res['cnt_all']= len(foods)
        for food in foods:
            temp = {
                "foodName":food.foodName,
                "rank":food.rank,
            }
            food_info.append(temp)
        res['food']=food_info

    return JsonResponse(res,safe=False,json_dumps_params = {'ensure_ascii': False})


def food_image(request,name,number):
    room = get_object_or_404(Room,name=name)
    # seatInfos = room[0].seatinfo_set.filter(created_date__lt=timezone.now()).order_by('-created_date')
    foods = room.foodinfo_set.order_by('rank')
    try:
        image = foods[int(number)].image
        return HttpResponse(image, content_type="image/jpeg")
    except Exception as e:
        return HttpResponse("OK")


@login_required
def foodUpload(request,name):
    room = get_object_or_404(Room,name=name)
    FoodFormSet = modelformset_factory(FoodInfo,form=FoodForm,extra=10,max_num=10)
    # 'extra' means the number of photos that you can upload

    if request.method == 'POST':

        formset = FoodFormSet(request.POST, request.FILES)

        if formset.is_valid():
            for form in formset:
                if form:
                    image=form.cleaned_data['image']
                    image = rescale(image,100,100)
                    rank = form.cleaned_data['rank']
                    foodName = form.cleaned_data['foodName']
                    foodInfo= FoodInfo(room=room,foodName= foodName,rank = rank,image=image)
                    foodInfo.save()

            # return HttpResponse(im,content_type="image/jpeg")
            # messages.success(request, " chceck it out on the home page!")
            # return HttpResponseRedirect('/')
            return redirect('room_detail', name=room.name)
        else:
            print(formset.errors)
    else:
        formset = FoodFormSet()
        return render(request, 'watcher/room_food.html',{'formset':formset})
    # formset = FoodForm()

def rescale(data, width, height):
    from io import BytesIO
    from PIL import Image as pil
    input_file = BytesIO(data.read())
    img = pil.open(input_file)
    img = img.resize((width,height))
    image = BytesIO()
    img.save(image,'JPEG')
    data.file= image
    return data


def logs(request):

    #
    if settings.OFF:
        f_log_seatInfo = open(os.path.join(BASE_DIR, 'logs','log_seatInfo'),'rb')
        f_log_django = open(os.path.join(BASE_DIR, 'logs','log'),'rb')
    else:
        f_log_seatInfo = open("/var/log/app_logs/log_seatInfo.txt",'rb')
        f_log_django = open("/var/log/app_logs/django_debug.txt",'rb')
    #
    #
    response = HttpResponse(f_log_seatInfo.read(), content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename=' + str(timezone.now()) + 'log_seatInfo'

    return response
    # # return HttpResponse(f_log_seatInfo,content_type='text/plain',charset='utf8')



def eventInfo(request):
    events = Event.objects.filter(startDate__lt=timezone.now(),endDate__gt=timezone.now())
    if len(events) == 0 :
        return HttpResponse("No events")
    else:
        index = random.randrange(0, len(events))
        eventImage = events[index].eventImage
        return HttpResponse(eventImage,content_type="image/png")




def room_seat(request,pcname):
    room = Room.objects.filter(name__contains=pcname)
    seatInfos = room[0].seatinfo_set.filter(created_date__lt=timezone.now()).order_by('-created_date')
    image_data = seatInfos[0].seatImage

    return HttpResponse(image_data, content_type="image/gif")

def room_info(reqeust,pcname):
    room = Room.objects.filter(name__contains=pcname)
    room = room[0]
    # notice = room[0].notice

    cnt_empty = 0
    seatInfos = room.seatinfo_set.filter(created_date__lt=timezone.now()).order_by('-created_date')
    if len(seatInfos) > 0:
        seatInfo = seatInfos[0]
        seat_data = seatInfo.data
        cnt_empty = json.loads(seat_data)['empty_seats']
    # seat_data = json.dumps(seat_data, ensure_ascii=False)

    content_contact = {'name': room.name,
                       'address': room.address,
                       'latitude': room.latitude,
                       'longitude': room.longitude,
                       'contact': room.contact,
                       'notice': room.notice,
                       'spec': room.spec,
                       'cnt_empty': cnt_empty,
                       }
    return JsonResponse(content_contact,safe=False,json_dumps_params = {'ensure_ascii': False})



def room_region(request,region):
    rooms_contact = Room.objects.filter(name__contains=region,contact=True).order_by('created_date')
    rooms_non_contact = Room.objects.filter(name__contains=region,contact=False).order_by('created_date')

    cnt_contact = len(rooms_contact)
    cnt_non_contact = len(rooms_non_contact)
    cnt_all = cnt_contact + cnt_non_contact

    contact=[]
    for room in rooms_contact:
        cnt_empty = 0
        seatInfos = room.seatinfo_set.filter(created_date__lt=timezone.now()).order_by('-created_date')
        if len(seatInfos) >0:
            seatInfo = seatInfos[0]
            seat_data = seatInfo.data
            cnt_empty = json.loads(seat_data)['empty_seats']
        # seat_data = json.dumps(seat_data, ensure_ascii=False)
        content_contact = {'name': room.name,
                           'address': room.address,
                           'latitude': room.latitude,
                           'longitude': room.longitude,
                           'contact': room.contact,
                           'notice': room.notice,
                           'spec': room.spec,
                           'cnt_empty': cnt_empty,
                           'rating': room.rating,
                           }

        contact.append(content_contact)
        content_contact={}

    contact_non = []
    for room in rooms_non_contact:
        content_non_contact = {'name': room.name,
                           'address': room.address,
                           'latitude': room.latitude,
                           'longitude': room.longitude,
                           'contact': room.contact,
                           'notice': room.notice,
                           'spec': room.spec
                           }

        contact_non.append(content_non_contact)

    res= {'cnt_all':cnt_all,
          'cnt_contact':cnt_contact,
          'cnt_non_contact':cnt_non_contact,
          'contact':contact,
          'contact_non':contact_non
        }


    # if not json shape, set safe parameter False
    # if contain korean, set ensure_ascil: False
    return JsonResponse(res,safe=False,json_dumps_params = {'ensure_ascii': False})

    return



@login_required
def room_remove(request,name):
    room = get_object_or_404(Room,name=name)
    try:
        pcCode = dic_name[room.name]
    except Exception as e:
        pcCode = 99
    logger.debug('room_remove Method : %s , PcName : %d '% (request.method, pcCode) )
    room.delete()
    return redirect('room_list')

@login_required
def room_edit(request, name):
    room = get_object_or_404(Room, name=name)
    try:
        pcCode = dic_name[room.name]
    except Exception as e:
        pcCode = 99
    logger.debug('room_edit Method : %s , PcName : %d '% (request.method, pcCode) )
    if request.method == "POST":

        form = RoomForm(request.POST or None, request.FILES or None,instance=room)
        if form.is_valid():
            room = form.save(commit=False)
            image = form.cleaned_data['image']
            image= rescale(image,100,100)
            room.image= image
            room.save()
            return redirect('room_detail', name=room.name)
    else:
        form = RoomForm(instance=room)
    return render(request, 'watcher/room_edit.html', {'form': form})

def room_detail(request, name):

    room = get_object_or_404(Room, name=name)
    try:
        pcCode = dic_name[room.name]
    except Exception as e:
        pcCode = 99
    logger.debug('room_detail Method : %s , PcName : %d '% (request.method, pcCode) )

    foods = room.foodinfo_set.all().order_by('rank')
    if foods:
        return render(request, 'watcher/room_detail.html', {'room':room,
                                                            'foods':foods})
    return render(request,'watcher/room_detail.html', {'room':room} )

@login_required
def room_new(request):
    if request.method == "POST":
        form = RoomForm(request.POST)
        if form.is_valid():
            room = form.save(commit=False)
            # room.created_date = timezone.now()
            room.save()
            try:
                pcCode = dic_name[room.name]
            except Exception as e:
                pcCode = 99
            logger.debug('room_new Method : %s , PcName : %d '% (request.method, pcCode) )
            return redirect('room_detail', name=room.name)
    else:
        form = RoomForm()

    return render(request, 'watcher/room_edit.html',{'form':form})

def room_list(request):
    logger.debug('room_list Method : %s '% (request.method) )
    rooms = Room.objects.filter(created_date__lte=timezone.now()).order_by('created_date')
    return render(request, 'watcher/room_list.html', {'rooms':rooms})

def room_seat(request,name):
    room = Room.objects.filter(name__contains=name)
    try:
        pcCode = dic_name[room.name]
    except Exception as e:
        pcCode = 99
    logger.debug('room_seatImage Method : %s , PcName : %d '% (request.method, pcCode) )

    seatInfos = room[0].seatinfo_set.filter(created_date__lt=timezone.now()).order_by('-created_date')
    image_data = seatInfos[0].seatImage

    return HttpResponse(image_data, content_type="image/gif")

@csrf_exempt
def seatInfo_save(request):
    # data = json.loads(request)

    if request.method == 'POST':
        data = request.POST.get("data")
        pcName = request.POST.get("pc_room")
        file = request.FILES['seat_image']
        room = Room.objects.filter(name__contains=pcName)
        try:
            pcCode = dic_name[pcName]
        except Exception as e:
            pcCode = 99

        logger_seatInfo.info("%d save the images\n"%pcCode)
        # pcName = pcName.encode('utf8') # to avoid aws unicode error
        # logger_seatInfo.info("%s save the images\n"%pcName)
        seatInfo = SeatInfo(room=room[0],data=data,seatImage=file)
        seatInfo.save()
        res = {"response":"ok"}
        return JsonResponse(json.dumps(res, ensure_ascii=False),safe=False)

    if request.method == 'GET':
        pcName = request.GET["pc_room"]
        msg=request.GET['msg']
        room = Room.objects.filter(name__contains=pcName)

        try:
            pcCode = dic_name[pcName]
        except Exception as e:
            pcCode = 99

        found = False
        for i in range(0,len(list_error)):
            if list_error[i] in msg:
                msg_type = i
                logger_seatInfo.info("%d    %d\n"%(pcCode, msg_type))
                found = True
                break

        if not found:
            logger_seatInfo.info("%d    %s\n"%(pcCode, msg))
        # pcName = pcName.encode('utf8') # to avoid aws unicode error
        # msg = msg.encode('utf8') # to avoid aws uncidoe error
        # logger_seatInfo.info("%s    %s\n"%(pcName, msg))
        return HttpResponse("ok", content_type="image/gif")


