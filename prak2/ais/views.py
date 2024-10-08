from django.shortcuts import render

from django.shortcuts import render, redirect
from .models import Students

from django.contrib import messages
from .forms import StudentsForm

def homepage(request):
    return render(request, 'homepage/index.html')

def about(request):
    return render(request, 'homepage/about.html')

def student_index(request):
    students = Students.objects.all()
    return render(request, 'student/index.html', {'students': students})

...
# CREATE Mahasiswa
def student_create(request):
    if request.method == 'POST':
        form = StudentsForm(request.POST)
        if form.is_valid():
            form.save() # Simpan data mahasiswa ke database
            messages.success(request, 'Mahasiswa berhasil dibuat!') # Pesan sukses
            return redirect('student_index') # Redirect ke halaman index mahasiswa
    else:
        form = StudentsForm()
    return render(request, 'student/create.html', {'form': form})

from django.shortcuts import render, redirect, get_object_or_404
from .models import Students

# UPDATE Mahasiswa
def student_update(request, student_id):
    student = get_object_or_404(Students, id=student_id)
    if request.method == 'POST':
        form = StudentsForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, 'Data mahasiswa berhasil diubah!')
            return redirect('student_index')
    else:
        form = StudentsForm(instance=student)
    return render(request, 'student/update.html', {'form': form, 'student': student})
from django.http import JsonResponse
# DELETE Mahasiswa
def student_delete(request, student_id):
    student = get_object_or_404(Students, id=student_id)
    student.delete()
    messages.success(request, 'Data mahasiswa berhasil dihapus')
    return JsonResponse({'success': True})



from django.db.models import Q
def student_index(request):
    query = request.GET.get('q')
    students = Students.objects.all()
    if query:
        students = Students.objects.filter(
            Q(name__icontains=query) |
            Q(nim__icontains=query) |
            Q(email__icontains=query) |
            Q(phone_number__icontains=query)
    )
    else:
        students = Students.objects.all()
    return render(request, 'student/index.html', {'students': students, 'query': query})