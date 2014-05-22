from django.contrib.auth.models import User
from DP.models import Project, CurrentProject


def myprojects(request):
    projects = Project.objects.filter(investigator=request.user.pk)
    return {'projects': projects}


def curproject(request):
    if request.user.is_authenticated():
        s = User.objects.filter(pk=request.user.pk)[0]
        current = CurrentProject.objects.filter(user=s)
        if not current.exists():
            return {'project': None}
        return {'project': current[0].project}
    else:
        return {'project': None}