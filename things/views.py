# from django.views.generic.edit import CreateView, UpdateView, DeleteView
# from django.urls import reverse_lazy
from django.core.files.base import ContentFile, StringIO
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login 
from django.contrib.auth import logout
# from django.views.generic import View
from .forms import UserForm, CategoryForm, ThingForm
from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from django.http import JsonResponse
from .models import Thing, Category


AUDIO_FILE_TYPES = ['wav', 'mp3', 'ogg']
IMAGE_FILE_TYPES = ['png', 'jpg', 'jpeg']

# class IndexView(generic.ListView):
# 	template_name = 'things/index.html'
# 	context_object_name = 'all_things'

# 	def get_queryset(self):
# 		return Thing.objects.all()

def create_category(request):
	# user = request.user
    if not request.user.is_authenticated:
        return render(request, 'things/login.html')
    else:
        form = CategoryForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            category = form.save(commit=False)
            category.user = request.user
            # category.category_picture = request.FILES['catgegory_picture']
            # file_type = category.category_picture.url.split('.')[-1]
            # file_type = file_type.lower()
            # if file_type not in IMAGE_FILE_TYPES:
            #     context = {
            #         'category': category,
            #         'form': form,
            #         'error_message': 'Image file must be PNG, JPG, or JPEG',
            #     }
            # return render(request, 'things/create_category.html', context)
            category.save()
            return render(request, 'things/detail.html', {'category': category})
        context = {
            "form": form,
        }
        return render(request, 'things/create_category.html', context)


def create_thing(request, category_id):
    form = ThingForm(request.POST or None, request.FILES or None)
    category = get_object_or_404(Category, pk=category_id)
    if form.is_valid():
        # original_photo = StringIO.StringIO(form.thing_picture.file.read())
        # rotated_photo = StringIO.StringIO()
        # image = Image.open(original_photo)
        # image = image.rotate(-90)
        # image.save(rotated_photo, 'JPEG')

        # form.thing_picture.file.save(image.file.path, ContentFile(rotated_photo.getvalue()))
        categorys_things = category.thing_set.all()
        for s in categorys_things:
            if s.thing_title == form.cleaned_data.get("thing_title"):
                context = {
                    'category': category,
                    'form': form,
                    'error_message': 'You already added that thing',
                }
                return render(request, 'things/create_thing.html', context)
        thing = form.save(commit=False)
        thing.category = category
        thing.thing_picture = request.FILES['thing_picture']
        file_type = thing.thing_picture.url.split('.')[-1]
        file_type = file_type.lower()
        if file_type not in IMAGE_FILE_TYPES:
            context = {
                'category': category,
                'form': form,
                'error_message': 'Image File must be PNG, JPG, or JPEG',
            }
            return render(request, 'things/create_thing.html', context)

        thing.save()
        return render(request, 'things/detail.html', {'category': category})
    context = {
        'category': category,
        'form': form,
    }
    return render(request, 'things/create_thing.html', context)



def index(request):
    if not request.user.is_authenticated:
        return render(request, 'things/login.html')
    else:
        categorys = Category.objects.filter(user=request.user)
        thing_results = Thing.objects.all()
        query = request.GET.get("q")
        if query:
            categorys = categorys.filter(
                Q(category_title__icontains=query) 
            ).distinct()
            thing_results = thing_results.filter(
                Q(thing_title__icontains=query)  |
                Q(location__icontains=query)
            ).distinct()
            return render(request, 'things/index.html', {
                'categorys': categorys,
                'things': thing_results,
            })
        else:
            return render(request, 'things/index.html', {'categorys': categorys})


def logout_user(request):
    logout(request)
    form = UserForm(request.POST or None)
    context = {
        "form": form,
    }
    return render(request, 'things/login.html', context)


def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                categorys = Category.objects.filter(user=request.user)
                return render(request, 'things/index.html', {'categorys': categorys})
            else:
                return render(request, 'things/login.html', {'error_message': 'Your account has been disabled'})
        else:
            return render(request, 'things/login.html', {'error_message': 'Invalid login'})
    return render(request, 'things/login.html')



def register(request):
    form = UserForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user.set_password(password)
        user.save()
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                categorys = Category.objects.filter(user=request.user)
                return render(request, 'things/index.html', {'categorys': categorys})
    context = {
        "form": form,
    }
    return render(request, 'things/register.html', context)

# class DetailView(generic.DetailView):
# 	model = Thing 
# 	template_name = 'things/detail.html'

# class ThingCreate(CreateView):
# 	model = Thing
# 	fields = ['thing_title','description', 'category','thing_picture','location','notes']

def detail(request, category_id):
    if not request.user.is_authenticated:
        return render(request, 'things/login.html')
    else:
        user = request.user
        category = get_object_or_404(Category, pk=category_id)
        return render(request, 'things/detail.html', {'category': category, 'user': user})




	

def delete_category(request, category_id):
    category = Category.objects.get(pk=category_id)
    category.delete()
    categorys = Category.objects.filter(user=request.user)
    return render(request, 'things/index.html', {'categorys': categorys})


def delete_thing(request, category_id, thing_id):
    category = get_object_or_404(Category, pk=category_id)
    thing = Thing.objects.get(pk=thing_id)
    thing.delete()
    return render(request, 'things/detail.html', {'category': category})


def things(request, filter_by):
    if not request.user.is_authenticated():
        return render(request, 'things/login.html')
    else:
        try:
            thing_ids = []
            for category in Category.objects.filter(user=request.user):
                for thing in category.thing_set.all():
                    thing_ids.append(thing.pk)
            users_things = Thing.objects.filter(pk__in=thing_ids)
            if filter_by == 'favorites':
                users_things = users_things.filter(is_favorite=True)
        except Category.DoesNotExist:
            users_things = []
        return render(request, 'things/things.html', {
            'thing_list': users_songs,
            'filter_by': filter_by,
        })




		