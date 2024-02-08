from django.http import HttpResponse

def errorResponse(code, message) -> HttpResponse:
    res = HttpResponse()
    res.status_code = code
    res.content = f"{{'error':'{message}'}}"
    res['Content-Type'] = 'application/json'
    return res

def errorInvalidMethod():
    return  errorResponse(405, 'Invalid method')