from django.shortcuts import redirect, render
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .forms import ProfileForm
from .models import Movie, Profile

class Home(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('core:profile_list')
        return render(request, 'index.html')

@method_decorator(login_required, name='dispatch')
class ProfileList(View):
    def get(self, request, *args, **kwargs):
        profiles=request.user.profiles.all()
        return render(request, 'profilelist.html', {'profiles':profiles})

@method_decorator(login_required, name='dispatch')
class ProfileCreate(View):
    def get(self, request, *args,**kwargs):
        form = ProfileForm()
        return render(request, 'profilecreate.html', { 'form': form })

    def post(self, request, *args, **kwargs):
        form = ProfileForm(request.POST or None)
        if form.is_valid():
            profile = Profile.objects.create(**form.cleaned_data)
            if profile:
                request.user.profiles.add(profile)
                return redirect('core:profile_list')
        return render(request, 'profilecreate.html', { 'form': form })

@method_decorator(login_required, name="dispatch")
class Watch(View):
    def get(self, request, profile_id, *args, **kwargs):
        try:
            profile = Profile.objects.get(uuid=profile_id)
            movies = Movie.objects.filter(age_limit=profile.age_limit)

            try:
                showcase = movies[0]
            except:
                showcase = None

            if profile not in request.user.profiles.all():
                return redirect(to='core:profile_list')
            return render(request, 'movielist.html', {
                'movies': movies,
                'show_case': showcase
            })
        except Profile.DoesNotExist:
            return redirect(to='core:profile_list')

@method_decorator(login_required, name="dispatch")
class MovieDetail(View):
    def get(self, request, movie_id, *args, **kwargs):
        try:
            movie = Movie.objects.get(uuid=movie_id)
            print(vars(movie))
            return render(request, 'moviedetail.html', { 'movie': movie })
        except Exception as e:
            return redirect('core:profile_list')

@method_decorator(login_required, name="dispatch")
class PlayMovie(View):
    def get(self, request, movie_id, *args, **kwargs):
        try:
            movie = Movie.objects.get(uuid=movie_id)
            movie = movie.videos.values()

            return render(request, 'showmovie.html', { 'movie': list(movie) })
        except Exception as e:
            print(vars(e))
            return redirect('core:profile_list')
