from django.db import models
from django.utils import timezone
from django.template.defaultfilters import slugify



class Room(models.Model):
    name = models.CharField(max_length=200,primary_key=True)
    address = models.CharField(max_length=255)
    latitude = models.FloatField(blank=False)
    longitude =models.FloatField(blank=False)
    contact = models.BooleanField(default=False,help_text="가맹점일 경우 체크하시오.")
    created_date = models.DateTimeField(default=timezone.now)
    notice = models.TextField(blank=True)
    spec = models.TextField(blank=True)
    image = models.ImageField(blank=True)
    rating = models.FloatField(default=0)


    def created(self):
        self.created_date = timezone.now()
        self.save()

    def __str__(self):
        return self.name


class SeatInfo(models.Model):
        room = models.ForeignKey(Room,on_delete=models.CASCADE)
        data = models.TextField(blank=True)
        # seatImage = models.ImageField(blank=True,upload_to="seat_images/")
        seatImage = models.ImageField(blank=True)
        created_date = models.DateTimeField(default=timezone.now)

        def __str__(self):
            return ("%s %s " %(self.room.name, self.created_date) )


def get_image_filename(instance, filename):
    room_name = instance.room.name
    slug = slugify(room_name)
    return "media/room_food_images/%s-%s" % (slug, filename)

class FoodInfo(models.Model):
    room = models.ForeignKey(Room,on_delete=models.CASCADE)
    image = models.ImageField(upload_to=get_image_filename,verbose_name="Image")
    foodName = models.CharField(max_length=255)
    rank = models.IntegerField(default=99)

    def __str__(self):
        return ("%s , Rank : %d"%(self.foodName,self.rank))




class Event(models.Model):
    name = models.CharField(max_length=255,primary_key=True)
    eventImage = models.ImageField(blank=False)
    startDate = models.DateTimeField(default=timezone.now)
    endDate = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return ("%s"%self.name)

class Coment(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    title = models.CharField(max_length=255,blank=True)
    rating = models.FloatField(default=0)
    content = models.TextField(blank=True)
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title