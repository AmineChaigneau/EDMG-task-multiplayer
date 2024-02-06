from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Trial, Round, Calibration, Form
import json

# Create your views here.
@csrf_exempt
def create_trial(request):
    if request.method == "POST":
        data = json.loads(request.body)
        trial = Trial.objects.create(**data)
        trial.save()
        return JsonResponse({"status": "success", "trial_id": trial.id})
    else:
        return JsonResponse({"status": "error", "message": "Invalid request method"})

@csrf_exempt
def create_round(request):
    if request.method == "POST":
        data = json.loads(request.body)
        round_instance = Round.objects.create(**data)
        round_instance.save()
        return JsonResponse({"status": "success", "round_id": round_instance.id})
    else:
        return JsonResponse({"status": "error", "message": "Invalid request method"})

@csrf_exempt
def create_calibration(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        calibration = Calibration(id=data['id'], trajectories=data['trajectories'])
        calibration.save()
        return JsonResponse({'status': 'success'})

    return JsonResponse({'status': 'error'})

@csrf_exempt
def create_form(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        form = Form(
            subject_id=data['subject_id'],
            age=data['age'],
            genre=data['genre'],
            profession=data['profession'],
            main=data['main'],
            souris=data['souris'],
        )
        form.save()
        return JsonResponse({'status': 'success'})

    return JsonResponse({'status': 'error'})