from django.views import View
from django.http import HttpResponse
from django.core.cache import cache


# Constants
CACHE_KEY_HELLO = "hello"
CACHE_TIMEOUT_SECOND = 30


class HelloView(View):
    def get(self, request, *args, **kwargs):
        """호출된 시점부터 30초동안 유효한 캐쉬를 설정한다."""
        initial_value = 1
        cache.set(CACHE_KEY_HELLO, initial_value, timeout=CACHE_TIMEOUT_SECOND)
        return HttpResponse(get_text(initial_value))


class HelloAgainView(View):
    def get(self, request, *args, **kwargs):
        """후촐될 때 마다 유효한 캐쉬가 있을 경우 캐쉬의 값을 1 증가한 후 반환한다."""
        try:
            cache.incr(CACHE_KEY_HELLO)
            count = cache.get(CACHE_KEY_HELLO)
            # 캐쉬 키가 없을 경우 incr에서 ValueError 발생하여 따로 count의 유효성을 확인하지 않음
            return HttpResponse(get_text(count))
        except ValueError:
            return HttpResponse("Expired!")


def get_text(value) -> str:
    """정상 처리되는 응답 메세지 생성"""
    return HttpResponse(f"Hello ELECLE {value}")
