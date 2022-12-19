from django.shortcuts import render

def core_base(request):
    return render(request, 'core/base.html')




