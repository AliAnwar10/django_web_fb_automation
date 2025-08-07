from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Credential, GroupLink, Post, PostSelection
from .forms import CredentialForm, GroupLinkForm, PostForm
from .automation_runner import run_automation
import asyncio
import json
from django.http import JsonResponse
from asgiref.sync import sync_to_async

def dashboard(request):
    credentials = Credential.objects.all()
    groups = GroupLink.objects.all()
    posts = Post.objects.all()
    context = {
        'credentials': credentials,
        'groups': groups,
        'posts': posts,
        'credential_form': CredentialForm(),
        'group_form': GroupLinkForm(),
        'post_form': PostForm(),
    }
    return render(request, 'autoapp/dashboard.html', context)

def add_credential(request):
    if request.method == 'POST':
        form = CredentialForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Credential added successfully!')
            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({'status': 'error', 'errors': form.errors}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)

def delete_credential(request, pk):
    credential = Credential.objects.get(pk=pk)
    credential.delete()
    messages.success(request, 'Credential deleted successfully!')
    return redirect('dashboard')

def add_group(request):
    if request.method == 'POST':
        form = GroupLinkForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Group added successfully!')
            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({'status': 'error', 'errors': form.errors}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)

def delete_group(request, pk):
    group = GroupLink.objects.get(pk=pk)
    group.delete()
    messages.success(request, 'Group deleted successfully!')
    return redirect('dashboard')

def add_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Post added successfully!')
            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({'status': 'error', 'errors': form.errors}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)

def delete_post(request, pk):
    post = Post.objects.get(pk=pk)
    post.delete()
    messages.success(request, 'Post deleted successfully!')
    return redirect('dashboard')

def load_data(request):
    if request.method == 'POST':
        credential_id = request.POST.get('credential')
        PostSelection.objects.filter(credential_id=credential_id).delete()
        groups = GroupLink.objects.all()
        posts = Post.objects.all()
        for post in posts:
            for group in groups:
                checkbox_name = f"selection_{post.id}_{group.id}"
                if checkbox_name in request.POST:
                    PostSelection.objects.create(
                        credential_id=credential_id,
                        group=group,
                        post=post,
                        selected=True
                    )
        messages.success(request, 'Selections saved successfully!')
        return redirect('dashboard')
    return redirect('dashboard')

async def run_automation_view(request):
    if request.method == 'POST':
        credential_id = request.POST.get('credential')
        if not credential_id:
            return JsonResponse({'status': 'error', 'message': 'No credential selected.'}, status=400)
        success, logs = await run_automation(int(credential_id))
        return JsonResponse({'status': 'success' if success else 'error', 'logs': logs})
    return redirect('dashboard')

def custom_404(request, exception):
    return render(request, 'autoapp/404.html', status=404)