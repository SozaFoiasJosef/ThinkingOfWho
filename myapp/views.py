from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse

from django.forms import modelformset_factory
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.contrib.contenttypes.models import ContentType
from django.db.models import OuterRef, Subquery, IntegerField, Value
from django.db.models.functions import Coalesce
from hitcount.models import HitCount
from hitcount.views import HitCountMixin
from .forms import ImageForm, RoomForm
from .models import Image, Room, RoomHitTarget

# Create your views here.
def home(request):
    return render(request, 'home.html', {'title': 'Thinking of Who - Free Online Deduction Game'})

def joingame(request):
    return render(request, 'joingame.html', {'title': 'Play Thinking of Who'})

def creategame(request):
    ImageFormSet = modelformset_factory(Image, form=ImageForm, extra=24)
    #'extra' means the number of photos that you can upload   ^
    if request.method == 'POST':
    
        formset = ImageFormSet(request.POST, request.FILES,
                               queryset=Image.objects.none())
        roomForm = RoomForm(request.POST)
    
    
        if formset.is_valid() and roomForm.is_valid():
            roomName = roomForm.cleaned_data.get('name')
            isSearchableBool = roomForm.cleaned_data.get('isSearchable')
            room = Room.objects.create(name=roomName, isSearchable=isSearchableBool)
            for form in formset.cleaned_data:
                #this helps to not crash if the user   
                #do not upload all the photos
                if form:
                    title = form['title']
                    image = form['image']
                    photo = Image(room=room,image=image, title=title)
                    photo.save()
            # use django messages framework
            messages.success(request,
                             "Yeeew, check it out on the home page!")
            # If this was an AJAX request, return the new room id as JSON
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'room_id': str(room.id)})
            # otherwise redirect to the game page for the created room
            return redirect(reverse('game', args=[room.id]))
        else:
            messages.error(request,
                             "oopsie!")
            print(formset.errors)
    else:
        formset = ImageFormSet(queryset=Image.objects.none())
        roomForm = RoomForm()
    return render(request, 'creategame.html',
                  {'formset': formset, 'roomForm': roomForm, 'title': 'Create Game'})

# Used for searching rooms by name
def _with_room_popularity(rooms_queryset, rank_queryset=None):
    room_hit_target_type = ContentType.objects.get_for_model(RoomHitTarget)
    hit_count_subquery = HitCount.objects.filter(
        content_type=room_hit_target_type,
        object_pk=OuterRef('hit_target__id')
    ).values('hits')[:1]

    def with_visits(queryset):
        return queryset.annotate(
            visit_count=Coalesce(
                Subquery(hit_count_subquery, output_field=IntegerField()),
                Value(0, output_field=IntegerField())
            )
        )

    rooms_queryset = with_visits(rooms_queryset)
    rank_queryset = with_visits(rank_queryset) if rank_queryset is not None else rooms_queryset

    ranked_ids = list(rank_queryset.order_by('-visit_count', '-created_at').values_list('id', flat=True))
    rank_by_id = {room_id: index + 1 for index, room_id in enumerate(ranked_ids)}

    rooms = list(rooms_queryset.order_by('-created_at'))
    for room in rooms:
        room.popularity_rank = rank_by_id.get(room.id, 0)

    return rooms


def gamelist(request,room_name):
    rooms_queryset = Room.objects.filter(
        name__icontains=room_name,
        isSearchable=True,
        image__isnull=False
    ).distinct()
    global_rank_queryset = Room.objects.filter(isSearchable=True, image__isnull=False).distinct()
    rooms = _with_room_popularity(rooms_queryset, rank_queryset=global_rank_queryset)
    return render(request, 'gamelist.html', {'title': 'Game List', 'rooms': rooms, 'search_name': room_name})

# Used for showing all rooms
def gamelistall(request):
    rooms_queryset = Room.objects.filter(isSearchable=True, image__isnull=False).distinct()
    rooms = _with_room_popularity(rooms_queryset)
    
    return render(request, 'gamelist.html', {'title': 'Game List', 'rooms': rooms})


def game(request, room_id):
    room = get_object_or_404(Room, pk=room_id)
    ImageFormSet = modelformset_factory(Image, form=ImageForm, extra=8)
    room_hits = None

    if request.method == 'POST':
        add_formset = ImageFormSet(
            request.POST,
            request.FILES,
            queryset=Image.objects.none(),
            prefix='add'
        )
        if add_formset.is_valid():
            for form in add_formset.cleaned_data:
                if form:
                    title = form.get('title')
                    image = form.get('image')
                    if image:
                        Image.objects.create(room=room, image=image, title=title)
            messages.success(request, "Photos added!")
            return redirect(reverse('game', args=[room.id]))
        else:
            messages.error(request, "Unable to add photos. Please check your files and try again.")
    else:
        room_hit_target, _ = RoomHitTarget.objects.get_or_create(room=room)
        hit_count = HitCount.objects.get_for_object(room_hit_target)
        HitCountMixin.hit_count(request, hit_count)
        hit_count.refresh_from_db()
        room_hits = hit_count.hits
        add_formset = ImageFormSet(queryset=Image.objects.none(), prefix='add')

    images = Image.objects.filter(room=room)
    return render(request, 'game.html', {
        'title': 'Game Room',
        'room': room,
        'images': images,
        'add_formset': add_formset,
        'room_hits': room_hits,
    })

def tos(request):
    return render(request, 'tos.html', {'title': 'Terms of Service'})