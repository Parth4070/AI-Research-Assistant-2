from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from projects.models import Projects
from datasets.models import Dataset
from ml_engine.models import MLExpriment

# Create your views here.
def home(request):
    return render(request, "home.html")

@login_required
def dashboard(request):
    user_projects = Projects.objects.filter(owner=request.user)
    projects_count = user_projects.count()
    
    # Count datasets belonging to projects owned by the user
    datasets_count = Dataset.objects.filter(project__owner=request.user).count()
    
    # Count experiments belonging to datasets in user projects
    experiments_count = MLExpriment.objects.filter(dataset__project__owner=request.user).count()
    
    # Query latest projects and experiments
    recent_projects = user_projects.order_by("-created_at")[:5]
    recent_experiments = MLExpriment.objects.filter(dataset__project__owner=request.user).order_by("-created_at")[:5]

    context = {
        "projects_count": projects_count,
        "datasets_count": datasets_count,
        "experiments_count": experiments_count,
        "recent_projects": recent_projects,
        "recent_experiments": recent_experiments,
    }
    return render(request, "dashboard/dashboard.html", context)

