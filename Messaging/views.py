from django.contrib import messages as flash
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Max
from django.shortcuts import render, redirect, get_object_or_404

from .models import Conversation, Message
from Projects.models import Project

User = get_user_model()


def _build_conv_list(user, active=None):
    convs = Conversation.for_user(user).select_related('user1', 'user2', 'project')
    items = []
    for c in convs:
        last = c.messages.last()
        unread = c.messages.filter(is_read=False).exclude(sender=user).count()
        items.append({
            'pk': c.pk,
            'other_user': c.other_user(user),
            'project': c.project,
            'last_message': last.text if last else '',
            'last_time': last.created_at if last else c.updated_at,
            'unread_count': unread,
        })
    return items


@login_required(login_url='login')
def inbox(request):
    conv_id = request.GET.get('conv')
    active = None
    msgs = []
    if conv_id:
        active = get_object_or_404(
            Conversation.objects.filter(Q(user1=request.user) | Q(user2=request.user)),
            pk=conv_id,
        )
        msgs = list(active.messages.select_related('sender').all())
        active.messages.filter(is_read=False).exclude(sender=request.user).update(is_read=True)

    if request.method == 'POST':
        text = request.POST.get('text', '').strip()
        target_conv_id = request.POST.get('conv_id') or conv_id
        if text and target_conv_id:
            conv = get_object_or_404(
                Conversation.objects.filter(Q(user1=request.user) | Q(user2=request.user)),
                pk=target_conv_id,
            )
            Message.objects.create(conversation=conv, sender=request.user, text=text)
            conv.save(update_fields=['updated_at'])
            return redirect(f"{request.path}?conv={conv.pk}")

    active_dict = None
    if active:
        active_dict = {
            'pk': active.pk,
            'other_user': active.other_user(request.user),
            'project': active.project,
        }

    return render(request, 'messages.html', {
        'conversations': _build_conv_list(request.user),
        'active_conv': active_dict,
        'messages': msgs,
    })


@login_required(login_url='login')
def conversation_detail(request, conv_id):
    return redirect(f"/messages/?conv={conv_id}")


@login_required(login_url='login')
def start_conversation(request, user_id, project_id=None):
    other = get_object_or_404(User, pk=user_id)
    if other == request.user:
        flash.error(request, "O'zingiz bilan suhbat ocha olmaysiz.")
        return redirect('inbox')

    project = None
    if project_id:
        project = Project.objects.filter(pk=project_id).first()

    conv = Conversation.get_or_create_between(request.user, other, project=project)
    return redirect(f"/messages/?conv={conv.pk}")
