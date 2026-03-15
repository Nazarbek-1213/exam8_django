from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from Contracts.models import Contract
from .models import Review



def write_review(request, contract_id):
    contract = get_object_or_404(Contract, id=contract_id)

    if request.user != contract.client:
        messages.error(request, "Faqat mijoz sharh yoza oladi.")
        return redirect('contract_detail', contract_id=contract.id)

    if hasattr(contract, 'review'):
        messages.info(request, "Siz allaqachon sharh yozgansiz.")
        return redirect('contract_detail', contract_id=contract.id)

    if contract.status != 'finished':
        messages.error(request, "Faqat yakunlangan shartnomaga sharh yozish mumkin.")
        return redirect('contract_detail', contract_id=contract.id)

    if request.method == 'POST':
        rating  = request.POST.get('rating', '0')
        comment = request.POST.get('comment', '').strip()

        if not rating or not (1 <= int(rating) <= 5):
            messages.error(request, "Reyting 1 dan 5 gacha bo'lishi kerak.")
            return render(request, 'write.html', {
                'contract': contract,
                'reviewee': contract.freelancer
            })

        Review.objects.create(
            client=contract.client,
            freelancer=contract.freelancer,
            contract=contract,
            rating=int(rating),
            comment=comment
        )
        messages.success(request, "Sharh muvaffaqiyatli qoldirildi")
        return redirect('contract_detail', contract_id=contract.id)

    return render(request, 'write.html', {
        'contract': contract,
        'reviewee': contract.freelancer
    })

class ReviewListView(LoginRequiredMixin, ListView):
    model = Review
    template_name = 'review_list.html'
    context_object_name = 'reviews'
    ordering = ['-created_at']

class FreelancerReviewListView(LoginRequiredMixin, ListView):
    model = Review
    template_name = 'freelancer_review_list.html'
    context_object_name = 'reviews'

    def get_queryset(self):
        freelancer_id = self.kwargs['freelancer_id']
        return Review.objects.filter(freelancer_id=freelancer_id).order_by('-created_at')


class ReviewDetailView(LoginRequiredMixin, DetailView):
    model = Review
    template_name = 'review_detail.html'
    context_object_name = 'review'

class ReviewUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Review
    fields = ['rating', 'comment']
    template_name = 'review_form.html'
    success_url = reverse_lazy('review_list')

    def test_func(self):
        review = self.get_object()
        return self.request.user == review.client


class ReviewDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Review
    template_name = 'review_confirm_delete.html'
    success_url = reverse_lazy('review_list')

    def test_func(self):
        review = self.get_object()
        return self.request.user == review.client