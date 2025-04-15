# prescriptions/views.py

import os
import shutil
from datetime import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.contrib import messages
from django.conf import settings
from django.http import JsonResponse, FileResponse
from django.urls import reverse
from django.utils.text import slugify

from .models import Scan, Medicine
from .forms import UserRegisterForm, ScanUploadForm
from .gemini_api import process_prescription_image

def index(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return redirect('login')

def register_view(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Account created successfully!')
            return redirect('dashboard')
        else:
            for error in form.errors.values():
                messages.error(request, error)
    else:
        form = UserRegisterForm()
    
    return render(request, 'prescriptions/login.html', {'form': form, 'register': True})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
        
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        from django.contrib.auth import authenticate
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password')
    
    return render(request, 'prescriptions/login.html', {'register': False})

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def dashboard(request):
    scans = Scan.objects.filter(user=request.user).order_by('-timestamp')
    return render(request, 'prescriptions/dashboard.html', {'scans': scans})

@login_required
def scan_view(request):
    if request.method == 'POST':
        form = ScanUploadForm(request.POST, request.FILES)
        
        if form.is_valid():
            # Clear uploads folder (optional in Django)
            upload_folder = settings.UPLOAD_FOLDER
            for file in os.listdir(upload_folder):
                file_path = os.path.join(upload_folder, file)
                if os.path.isfile(file_path):
                    os.remove(file_path)
            
            # Save the uploaded file
            uploaded_file = request.FILES['file']
            filename = f"{slugify(request.user.username)}_{uploaded_file.name}"
            filepath = os.path.join(upload_folder, filename)
            
            with open(filepath, 'wb+') as destination:
                for chunk in uploaded_file.chunks():
                    destination.write(chunk)
            
            # Process image with Gemini API
            extracted_text, medicine_info = process_prescription_image(filepath)
            
            # Save scan in past scans folder with timestamp
            timestamp_str = datetime.now().strftime("%Y%m%d_%H%M%S")
            past_scan_path = os.path.join(settings.PAST_SCANS_FOLDER, f"{timestamp_str}_{filename}")
            shutil.copy(filepath, past_scan_path)
            
            # Save to database
            scan = Scan.objects.create(
                user=request.user,
                image_path=os.path.relpath(past_scan_path, settings.MEDIA_ROOT),
                extracted_text=extracted_text
            )
            
            # Optional: Parse and save individual medicines from extracted text
            # This would require additional logic to extract medicine names, etc.
            
            context = {
                'form': form,
                'extracted_text': extracted_text,
                'medicine_info': medicine_info,
                'scan': scan,
                'image_path': os.path.join(settings.MEDIA_URL, os.path.relpath(past_scan_path, settings.MEDIA_ROOT))
            }
            return render(request, 'prescriptions/scan.html', context)
    else:
        form = ScanUploadForm()
    
    return render(request, 'prescriptions/scan.html', {'form': form})

@login_required
def view_scan(request, scan_id):
    scan = get_object_or_404(Scan, id=scan_id, user=request.user)
    return render(request, 'prescriptions/view_scan.html', {'scan': scan})

@login_required
def get_scan_json(request, scan_id):
    scan = get_object_or_404(Scan, id=scan_id, user=request.user)
    return JsonResponse({
        "timestamp": scan.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
        "extracted_text": scan.extracted_text,
    })

def media_file(request, path):
    """Serve media files in development"""
    return FileResponse(open(os.path.join(settings.MEDIA_ROOT, path), 'rb'))