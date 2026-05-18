from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Bid
from Projects.models import Project


@login_required(login_url='login')
def place_bid(request, pk):
    project = get_object_or_404(Project, pk=pk)

    if request.user.role != 'freelancer':
        messages.error(request, "Faqat freelancer bid yuborishi mumkin.")
        return redirect('main-redirect')

    if Bid.objects.filter(project=project, freelancer=request.user).exists():
        messages.warning(request, "Siz bu loyihaga allaqachon ariza yuborgansiz.")
        return redirect('project_detail', id=project.pk)

    if request.method == 'POST':
        price = request.POST.get('amount') or request.POST.get('price')
        text = request.POST.get('xabar', '').strip()
        delivery_days = request.POST.get('delivery_days', '7')
        attachment = request.FILES.get('attachment')

        if not price:
            messages.error(request, "Iltimos, summani kiriting.")
            return render(request, 'place_bid.html', {'project': project})

        try:
            Bid.objects.create(
                project=project,
                freelancer=request.user,
                price=float(price),
                xabar=text,
                delivery_days=int(delivery_days or 7),
                attachment=attachment,
            )
            messages.success(request, "Ariza muvaffaqiyatli yuborildi!")
        except Exception as e:
            messages.error(request, f"Xato: {str(e)}")
            return render(request, 'place_bid.html', {'project': project})

        return redirect('project_detail', id=project.pk)

    return render(request, 'place_bid.html', {'project': project})


@login_required(login_url='login')
def accept_bid(request, bid_id):
    bid = get_object_or_404(Bid, id=bid_id)

    if request.user != bid.project.client:
        messages.error(request, "Ruxsat yo'q.")
        return redirect('project_detail', id=bid.project.pk)

    if bid.status != 'pending':
        messages.warning(request, "Bu ariza allaqachon ko'rib chiqilgan.")
        return redirect('project_detail', id=bid.project.pk)

    bid.status = 'accepted'
    bid.save()

    Bid.objects.filter(
        project=bid.project,
    ).exclude(id=bid.id).update(status='rejected')

    messages.success(request, f"{bid.freelancer.username} arizasi qabul qilindi!")
    return redirect(
        'create_contract',
        project_id=bid.project.id,
        freelancer_id=bid.freelancer.id,
    )


@login_required(login_url='login')
def reject_bid(request, bid_id):
    bid = get_object_or_404(Bid, id=bid_id)

    if request.user != bid.project.client:
        messages.error(request, "Ruxsat yo'q.")
        return redirect('project_detail', id=bid.project.pk)

    if request.method == 'POST':
        reason = request.POST.get('reason', '').strip()
        bid.status = 'rejected'
        if reason:
            bid.xabar = bid.xabar + f"\n\n[Rad etish sababi: {reason}]"
        bid.save()
        messages.success(request, "Ariza rad etildi.")
        return redirect('project_detail', id=bid.project.pk)

    return render(request, 'reject_bid.html', {'bid': bid})


@login_required(login_url='login')
def my_bids(request):
    bids = Bid.objects.filter(freelancer=request.user).select_related('project')
    return render(request, 'my_bids.html', {'bids': bids})
