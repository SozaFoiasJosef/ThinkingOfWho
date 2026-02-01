import uuid
from django.db import models
from .utils.image_processing import compress_image


# Create your models here.
class Room(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=63, default='Unnamed Room')
    isSearchable = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    #host = models.ForeignKey('Players', on_delete=models.CASCADE, null=True, blank=True)
    #opponent = models.ForeignKey('Player', on_delete=models.CASCADE, null=True, blank=True)


class Player(models.Model):
    name = models.CharField(max_length=63, default='TestPlayer')

def room_images_path(instance, filename):
    return "room_images/%s-%s" % (instance.room.id, filename)

class Image(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, null=True, blank=True)
    image = models.ImageField(upload_to=room_images_path, verbose_name='Image')
    title = models.CharField(max_length=63, blank=True)

    def save(self, *args, **kwargs):
        # Compress the image before saving
        if self.image:
            self.image = compress_image(self.image)
        super().save(*args, **kwargs)
