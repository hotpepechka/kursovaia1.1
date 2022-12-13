from django.shortcuts import render
from django.views.generic import ListView, DetailView
from . import models
from django.shortcuts import render, redirect
# imported our models
from django.core.paginator import Paginator
from . models import Song
from . models import Loved
from django.views.generic import TemplateView
from django.views.generic.edit import UpdateView, DeleteView, CreateView
from .forms import NewSonger
from django.urls import reverse_lazy  # new


class MusicHome(TemplateView):
    template_name = 'index.html'


class SongList(ListView):
    model = Song
    template_name = 'personal_area.html'


class LovedList(ListView):
    model = Song
    template_name = 'Loved.html'


class AllSongList(ListView):
    model = Song
    template_name = 'AllSong.html'

    def get_queryset(self):
        if self.request.GET.get('q') != None:
            query = self.request.GET.get('q')
            object_list = Song.objects.filter(genre__name__icontains=query)
            return object_list
        else:
            object_list = Song.objects.all()
            return object_list


def index(request):
    paginator = Paginator(Song.objects.all(), 1)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {"page_obj": page_obj}
    return render(request, "index.html", context)


def index1(request, pk):
    users = Loved.objects.filter(user=request.user.id).all()
    return render(request, "Loved.html", {"users": users})

class MusicDetail(DetailView):
    model = Song
    template_name = "MusicDetail.html"

class ButtonLoved(ListView):
    model = models.Loved
    template_name = 'SureToLove.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class NewMusic(CreateView):
    model = Song
    form_class = NewSonger
    template_name = 'NewMusic.html'
    success_url = reverse_lazy("index")


class MusicDelete(DeleteView):
    model = Song
    template_name = 'deleteMusic.html'
    success_url = reverse_lazy('index')


class EditMusic(UpdateView):
    model = Song
    form_class = NewSonger
    template_name = 'editMusic.html'
    success_url = reverse_lazy('index')


