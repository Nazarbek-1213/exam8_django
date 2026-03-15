from io import BytesIO
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from django.template.loader import get_template
from django.utils import timezone
from xhtml2pdf import pisa
from .models import Contract
from Projects.models import Project
from Users.models import User

def render_to_pdf(template_src, context_dict=None):
    context_dict = context_dict or {}
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None


def create_contract(request, project_id, freelancer_id):
    project = get_object_or_404(Project, id=project_id)
    freelancer = get_object_or_404(User, id=freelancer_id)
    client = request.user

    if client.role != 'client':
        messages.error(request, "Faqat client contract yaratadi.")
        return redirect('home')

    if hasattr(project, 'client'):
        if project.client != client:
            messages.error(request, "Siz faqat o'zingizning projectingiz uchun contract yaratishingiz mumkin.")
            return redirect('home')

    if request.method == 'POST':
        if Contract.objects.filter(project=project).exists():
            messages.error(request, "Bu project uchun allaqachon contract mavjud.")
            return redirect('client_contract_list')

        agreed_price = request.POST.get('agreed_price', '').strip()
        if not agreed_price:
            messages.error(request, "Narx kiritilishi shart.")
            return render(request, 'create_contract.html', {
                'project': project,
                'freelancer': freelancer
            })

        Contract.objects.create(
            project=project,
            client=client,
            freelancer=freelancer,
            agreed_price=agreed_price,
            status=Contract.ACTIVE
        )
        messages.success(request, "Contract muvaffaqiyatli yaratildi.")
        return redirect('client_contract_list')

    return render(request, 'create_contract.html', {
        'project': project,
        'freelancer': freelancer
    })

def contract_detail(request, contract_id):
    contract = get_object_or_404(Contract, id=contract_id)

    if request.user != contract.client and request.user != contract.freelancer:
        messages.error(request, "Siz bu contractni ko'ra olmaysiz.")
        return redirect('main_client')
    context = {
        'contract': contract,
        'user': request.user,
        'is_client': request.user == contract.client,
        'is_freelancer': request.user == contract.freelancer,
        'done_milestones': contract.milestones.filter(status='done').count() if hasattr(contract, 'milestones') else 0,
        'total_milestones': contract.milestones.count() if hasattr(contract, 'milestones') else 0,
    }
    return render(request, 'contract_detail.html', context)

def client_contract_list(request):
    if request.user.role != 'client':
        messages.error(request, "Faqat client contractlarni ko‘ra oladi.")
        return redirect('home')
    contracts = Contract.objects.filter(client=request.user).order_by('-created_at')
    return render(request, 'client_contract_list.html', {'contracts': contracts})

@login_required(login_url='login')
def freelancer_contract_list(request):
    if request.user.role != 'freelancer':
        messages.error(request, "Faqat freelancer contractlarni ko‘ra oladi.")
        return redirect('home')
    contracts = Contract.objects.filter(freelancer=request.user).order_by('-created_at')
    return render(request, 'freelancer_contract_list.html', {'contracts': contracts})


def all_contracts(request):
    contracts = Contract.objects.all().order_by('-created_at')
    return render(request, 'all_contracts.html', {'contracts': contracts})


def active_contracts(request):
    if request.user.role == 'client':
        contracts = Contract.objects.filter(client=request.user,status=Contract.ACTIVE).order_by('-created_at')
    elif request.user.role == 'freelancer':
        contracts = Contract.objects.filter(freelancer=request.user,status=Contract.ACTIVE).order_by('-created_at')
    else:
        contracts = Contract.objects.none()
    return render(request, 'active_contracts.html', {'contracts': contracts})

def finished_contracts(request):
    if request.user.role == 'client':
        contracts = Contract.objects.filter(client=request.user,status=Contract.FINISHED).order_by('-created_at')
    elif request.user.role == 'freelancer':
        contracts = Contract.objects.filter(freelancer=request.user,status=Contract.FINISHED).order_by('-created_at')
    else:
        contracts = Contract.objects.none()
    return render(request, 'finished_contracts.html', {'contracts': contracts})


def cancelled_contracts(request):
    if request.user.role == 'client':
        contracts = Contract.objects.filter(client=request.user,status=Contract.CANCELLED).order_by('-created_at')
    elif request.user.role == 'freelancer':
        contracts = Contract.objects.filter(freelancer=request.user,status=Contract.CANCELLED).order_by('-created_at')
    else:
        contracts = Contract.objects.none()
    return render(request, 'cancelled_contracts.html', {'contracts': contracts})

def finish_contract(request, contract_id):
    contract = get_object_or_404(Contract, id=contract_id)
    if request.user != contract.client:
        messages.error(request, "Faqat client contractni tugata oladi.")
        return redirect('contract_detail', contract_id=contract.id)
    if contract.status != Contract.ACTIVE:
        messages.error(request, "Faqat active contract tugatiladi.")
        return redirect('contract_detail', contract_id=contract.id)
    contract.status = Contract.FINISHED
    contract.finished_at = timezone.now()
    contract.save()
    messages.success(request, "Contract tugatildi.")
    return redirect('contract_detail', contract_id=contract.id)

def cancel_contract(request, contract_id):
    contract = get_object_or_404(Contract, id=contract_id)
    if request.user != contract.client:
        messages.error(request, "Faqat client contractni bekor qila oladi.")
        return redirect('contract_detail', contract_id=contract.id)
    if contract.status != Contract.ACTIVE:
        messages.error(request, "Faqat active contract bekor qilinadi.")
        return redirect('contract_detail', contract_id=contract.id)
    contract.status = Contract.CANCELLED
    contract.finished_at = timezone.now()
    contract.save()
    messages.success(request, "Contract bekor qilindi.")
    return redirect('contract_detail', contract_id=contract.id)

