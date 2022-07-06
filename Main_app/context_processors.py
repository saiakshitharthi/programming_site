def pass_user(request):
    print(request)
    print('I came inside atleast this time')
    return {'user_context': request.user}