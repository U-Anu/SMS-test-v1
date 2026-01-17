from functools import wraps
from django.shortcuts import redirect, render


# def user_type_required(user_type):
#     def decorator(view_func):
#         @wraps(view_func)
#         def _wrapped_view(request, *args, **kwargs):
#             if not request.user.is_authenticated or request.user.user_type != user_type:
#                 # Redirect or raise PermissionDenied as needed
#                 return render(request, "page_not_found.html")
#                 # Or raise PermissionDenied("You don't have access to this page.")
#             return view_func(request, *args, **kwargs)

#         return _wrapped_view

#     return decorator


# from functools import wraps
# from django.shortcuts import redirect, render


def user_type_required(user_type):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            print('=======')
            # print('the request user is',request.user )
            if not request.user.is_superuser and not request.user.is_school_admin:
                if request.user.user_type != user_type:
                    return render(request, "page_not_found.html")
                return view_func(request, *args, **kwargs)
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator
