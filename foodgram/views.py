from django.shortcuts import render


def page_not_found(request, exception):
    return render(
        request,
        'misc/page_not_found.html',
        {'path': request.path},
        status=404
    )


def server_error(request):
    return render(
        request,
        'misc/server_error.html',
        status=500
    )
