from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny, IsAuthenticated
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.throttling import AnonRateThrottle
from django.http import HttpResponse
from django.shortcuts import render
import os


def config_js(request):
    # Cloudtype에서 설정한 환경 변수들을 가져옵니다.
    langsmith_api_key = os.getenv('LANGSMITH_API_KEY')
    moviedata_api_key = os.getenv('MOVIEDATA_API_KEY')
    moviedata_token = os.getenv('MOVIEDATA_TOKEN')
    openai_api_key = os.getenv('OPENAI_API_KEY')
    the_film_council_api_key = os.getenv('the_Film_Council_API_KEY')
       # MOVIEDATA_TOKEN이 제대로 로드되었는지 확인
    print(f"MOVIEDATA_TOKEN: {moviedata_token}")  # 여기에서 값 출력 확인
    print(f"moviedata_api_key: {moviedata_api_key}")  
    print(f"openai_api_key: {openai_api_key}")  
    print(f"the_film_council_api_key: {the_film_council_api_key}")  
    
    # JavaScript로 출력할 config.js 내용 작성
    config_js_content = f"""
    window.CONFIG = {{
        LANGSMITH_API_KEY: "{langsmith_api_key}",
        MOVIEDATA_API_KEY: "{moviedata_api_key}",
        MOVIEDATA_TOKEN: "{moviedata_token}",
        OPENAI_API_KEY: "{openai_api_key}",
        the_Film_Council_API_KEY: "{the_film_council_api_key}",
    }};
    """
    

    # JavaScript 파일로 반환
    response = HttpResponse(config_js_content, content_type='application/javascript')
    response['Content-Disposition'] = 'inline; filename=config.js'
    return response



class Main(APIView):
    permission_classes = [AllowAny]  # 인증이 필요하지 않음
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'Main/Home.html'
    throttle_classes = [AnonRateThrottle]  # Rate limiting 적용

    def get(self, request):
        '''홈 페이지 렌더링'''
        context = {
            "MOVIEDATA_TOKEN": os.getenv("MOVIEDATA_TOKEN", ""),
            "THE_FILM_COUNCIL_API_KEY": os.getenv("THE_FILM_COUNCIL_API_KEY", "")
        }
        return Response(context)
    
class Movie(APIView):

    permission_classes = [AllowAny]  # 인증이 필요하지 않음
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'Main/movie.html'
    throttle_classes = [AnonRateThrottle]  # Rate limiting 적용

    def get(self,request, movie_id):
        '''리뷰 목록 폼'''
        context = {
            "MOVIEDATA_TOKEN": os.getenv("MOVIEDATA_TOKEN", ""),
            "THE_FILM_COUNCIL_API_KEY": os.getenv("THE_FILM_COUNCIL_API_KEY", "")
        }
        return Response(context)






