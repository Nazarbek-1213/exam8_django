from django.contrib.auth import login, authenticate, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.db.models import Avg, Q
from django.shortcuts import render, redirect, get_object_or_404

from Bid.models import Bid
from Contracts.models import Contract
from Projects.models import Project
from Review.models import Review
from Users.models import FreelancerProfile

User = get_user_model()


def LoginView(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            if user.role == 'freelancer':
                return redirect('main_freelancer')
            else:
                return redirect('main_client')
        else:
            return render(request, "login.html", {"message": "Username yoki parol noto‘g‘ri"})

    return render(request, "login.html")


def RegisterView(request):
    if request.method == "POST":
        username = request.POST.get("username")
        role = request.POST.get("role")
        password = request.POST.get("password")
        password2 = request.POST.get("password2")
        email = request.POST.get("email")
        major = request.POST.get("major", "")

        if not role:
            return render(request, "register.html", {"message": "Rol tanlash kerak"})

        if password != password2:
            return render(request, "register.html", {"message": "Parollar mos kelmadi"})

        if User.objects.filter(email=email).exists():
            return render(request, "register.html", {"message": "Bu email allaqachon mavjud"})

        if User.objects.filter(username=username).exists():
            return render(request, "register.html", {"message": "Username mavjud"})

        user = User.objects.create_user(
            username=username,
            password=password,
            email=email,
            role=role,
        )

        if role == "freelancer":
            FreelancerProfile.objects.create(
                user=user,
                major=major,
                username=username,
                email=email,
            )

        login(request, user)
        if role == 'freelancer':
            return redirect('main_freelancer')
        else:
            return redirect('main_client')

    return render(request, "register.html")


def LogoutView(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
def ProfileView(request):
    user = request.user
    profile = FreelancerProfile.objects.filter(user=user).first()

    context = {
        "username": user.username,
        "email": user.email,
        "role": user.role,
        "profile_user": user,
        "freelancer_profile": profile,
    }
    return render(request, "profile.html", context)


@login_required(login_url='login')
def EditProfile(request):
    user = request.user
    profile = FreelancerProfile.objects.filter(user=user).first()

    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        bio = request.POST.get('bio')
        avatar = request.FILES.get('avatar')

        if username:
            user.username = username
        if email:
            user.email = email
        user.bio = bio or ''
        if avatar:
            user.avatar = avatar
        user.save()

        if user.role == 'freelancer':
            if not profile:
                profile = FreelancerProfile.objects.create(user=user, major='')
            profile.major = request.POST.get('major', profile.major) or profile.major
            profile.skills = request.POST.get('skills', '')
            hourly = request.POST.get('hourly_rate')
            if hourly:
                try:
                    profile.hourly_rate = float(hourly)
                except ValueError:
                    pass
            exp = request.POST.get('experience_years')
            if exp:
                try:
                    profile.experience_years = int(exp)
                except ValueError:
                    pass
            profile.portfolio_url = request.POST.get('portfolio_url', '')
            profile.bio = bio or ''
            profile.save()

        return redirect('profile')

    return render(request, 'edit_profile.html', {'profile': profile})


@login_required(login_url='login')
def SearchView(request):
    user = request.user
    q = request.GET.get('q', '')

    context = {'query': q}

    if user.role == 'freelancer':
        projects = Project.objects.filter(
            Q(title__icontains=q) | Q(description__icontains=q)
        )
        context['projects'] = projects

    elif user.role == 'client':
        freelancers = FreelancerProfile.objects.filter(
            Q(major__icontains=q) | Q(bio__icontains=q)
        )
        context['freelancers'] = freelancers

    return render(request, 'search.html', context)


def main_redirect(request):
    if not request.user.is_authenticated:
        return redirect('login')

    if request.user.role == 'freelancer':
        return redirect('main_freelancer')
    return redirect('main_client')


@login_required(login_url='login')
def liveProView(request):
    user = request.user

    if user.role == 'client':
        live_projects = Project.objects.filter(client=user, status='open').count()
        finished_projects = Project.objects.filter(client=user, status='completed').count()
        freelancer_count = Contract.objects.filter(
            client=user
        ).values('freelancer').distinct().count()

        avg_rating = Review.objects.filter(
            client=user
        ).aggregate(avg=Avg('rating'))['avg'] or 0

        my_projects = Project.objects.filter(client=user).order_by('-created_at')[:10]
        top_freelancers = FreelancerProfile.objects.all()[:5]

        return render(request, 'main_client.html', {
            'live_projects': live_projects,
            'finished_projects': finished_projects,
            'freelancer_count': freelancer_count,
            'avg_rating': avg_rating,
            'my_projects': my_projects,
            'top_freelancers': top_freelancers,
        })

    return redirect('main_freelancer')


@login_required(login_url='login')
def AllProview(request):
    user = request.user
    category = request.GET.get('category', '')
    projects = Project.objects.all().order_by('-created_at')

    if user.role == 'freelancer':
        if category:
            projects = projects.filter(category=category)
    else:
        projects = Project.objects.none()

    my_bids_list = Bid.objects.filter(
        freelancer=user
    ).select_related('project').order_by('-created_at')[:10]

    total_bids = Bid.objects.filter(freelancer=user).count()
    accepted_bids = Bid.objects.filter(freelancer=user, status='accepted').count()

    avg_rating = 0
    try:
        profile = FreelancerProfile.objects.get(user=user)
        avg = Review.objects.filter(freelancer=profile).aggregate(avg=Avg('rating'))
        avg_rating = avg['avg'] or 0
    except FreelancerProfile.DoesNotExist:
        avg_rating = 0

    return render(request, 'main_freelancer.html', {
        'projects': projects,
        'active_category': category,
        'avg_rating': avg_rating,
        'my_bids_list': my_bids_list,
        'total_bids': total_bids,
        'accepted_bids': accepted_bids,
    })


@login_required(login_url='login')
def logo_redirect(request):
    user = request.user
    if user.role == 'freelancer':
        return redirect('main_freelancer')
    return redirect('main_client')


@login_required(login_url='login')
def UserProfileView(request, pk):
    profile_user = get_object_or_404(User, pk=pk)
    profile = FreelancerProfile.objects.filter(user=profile_user).first()

    avg_rating = 0
    review_count = 0
    if profile:
        agg = Review.objects.filter(freelancer=profile).aggregate(avg=Avg('rating'))
        avg_rating = agg['avg'] or 0
        review_count = Review.objects.filter(freelancer=profile).count()

    context = {
        'profile_user': profile_user,
        'username': profile_user.username,
        'email': profile_user.email,
        'role': profile_user.role,
        'freelancer_profile': profile,
        'avg_rating': avg_rating,
        'review_count': review_count,
    }
    return render(request, 'profile.html', context)
