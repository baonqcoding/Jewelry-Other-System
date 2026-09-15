class DisableCSRFOnAPIMiddleware:
    """
    Tắt CSRF check cho toàn bộ request có path bắt đầu bằng /api/
    (và /update_item/ nếu cần), vì đây là JSON API gọi từ Postman/
    frontend riêng, không phải form HTML có {% csrf_token %}.
    Các route khác (vd /admin/) vẫn được CSRF bảo vệ bình thường.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith('/api/') or request.path.startswith('/update_item/'):
            setattr(request, '_dont_enforce_csrf_checks', True)
        return self.get_response(request)