from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator

from .models import Notification


@login_required(login_url='login')
def notification_list(request):
    qs = request.user.notifications.all()
    paginator = Paginator(qs, 20)
    page = paginator.get_page(request.GET.get('page'))
    return render(request, 'notifications.html', {'notifications': page, 'page_obj': page})


@login_required(login_url='login')
def mark_read(request, pk):
    n = get_object_or_404(Notification, pk=pk, user=request.user)
    n.is_read = True
    n.save(update_fields=['is_read'])
    if n.url:
        return redirect(n.url)
    return redirect('notifications')


@login_required(login_url='login')
def mark_all_read(request):
    request.user.notifications.filter(is_read=False).update(is_read=True)
    return redirect('notifications')
