from django.http import HttpResponseForbidden


def group_required(group_name):
    def group_required(func):
        def res(request, *args, **kwargs):
            if request.user.groups.filter(name=group_name).exists():
                return func(request, *args, **kwargs)
            else:
                return HttpResponseForbidden()
        return res
    return group_required