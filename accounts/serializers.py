# accounts/serializers.py
from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from .models import Follow, UserProfile
from articles.models import Article, Comment
from AI.models import AI
from django.core.exceptions import ValidationError
User = get_user_model()


class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = (
            "email",
            "password",
            "password2",
            "username",
        )
           
    def validate_email(self, value):
        """이메일 중복 체크"""
        if User.objects.filter(email=value).exists():
            raise ValidationError("이미 사용 중인 이메일 주소입니다.")
        return value

    def validate(self, data):
        if data["password"] != data["password2"]:
            raise serializers.ValidationError(
                {"password": "비밀번호가 일치하지 않습니다."}
            )
        # 비밀번호 강도 체크
        try:
            validate_password(data['password'])  # Django의 비밀번호 강도 체크 함수
        except Exception as e:
            raise serializers.ValidationError({
                "password": list(e.messages)
            })

        return data

    def create(self, validated_data):
        validated_data.pop("password2")  # password2 제거
        return User.objects.create_user(**validated_data)


class UserProfileSerializer(serializers.ModelSerializer):

    class FollowSerializer(serializers.ModelSerializer):
        class Meta:
            model = User
            fields = ("id", "email", "username", "profile_image",)

    followers = FollowSerializer(many=True, read_only=True)
    followings = FollowSerializer(many=True, read_only=True)
    follower_count = serializers.IntegerField(source="followers.count", read_only=True)
    following_count = serializers.IntegerField(source="followings.count", read_only=True)

    # 추가된 챗봇 대화 기록 부분
    class TimovingbotSerializer(serializers.ModelSerializer):
        author_username = serializers.CharField(source='author.username', read_only=True)  # 작성자의 username을 가져옴
        class Meta:
            model = AI
            fields = ("user_question", "bot_response", "created_at", "author_username")  # 정확한 필드명으로 수정

    # 챗봇 대화 기록을 사용자 프로필에 포함
    bot_Conversation_List = TimovingbotSerializer(
        many=True, 
        read_only=True,
        source="questions"  # AI 모델의 author 필드와 연결된 질문 목록 (related_name='questions' 사용)
    ) 

    # 좋아요 한 게시글 정보를 사용자 프로필에 포함
    class article_likeSerializer(serializers.ModelSerializer): 
        author_username = serializers.CharField(source='author.username', read_only=True)  # 작성자의 username을 가져옴
        class Meta:
            model = Article
            fields = ("Article_title", "movie_title", "image", "rating", "author_username")

    Favorite_articles = article_likeSerializer(
        many=True, 
        read_only=True, 
        source="liked_articles"  # Article 모델의 author 필드와 연결된 게시글 좋아요 목록 (related_name='liked_articles' 사용)
    )
    Favorite_articles_count = serializers.IntegerField(
        source="liked_articles.count", read_only=True  # 개수 필드도 source 수정
    )
    
    # 좋아요 한 댓글 정보를 사용자 프로필에 포함
    class comment_likeSerializer(serializers.ModelSerializer): 
        Article_title = serializers.CharField(source='article.Article_title', read_only=True)  # Article의 title을 가져옴
        author_username = serializers.CharField(source='author.username', read_only=True)  # 작성자의 username을 가져옴

        class Meta:
            model = Comment
            fields = ("content", "created_at", "Article_title", "author_username")

    Favorite_comments = comment_likeSerializer(
        many=True, 
        read_only=True, 
        source="liked_comments"  # Comment 모델의 author 필드와 연결된 댓글 좋아요 목록 (related_name='liked_comments' 사용)
    )
    Favorite_comments_count = serializers.IntegerField(
        source="liked_comments.count", read_only=True  # 개수 필드도 source 수정
    )
    
    # 추가된 작성한 게시글 및 댓글 정보
    class articleSerializer(serializers.ModelSerializer):  # 작성한 게시글 정보
        author_username = serializers.CharField(source='author.username', read_only=True)  # 작성자의 username을 가져옴
        class Meta:
            model = Article
            fields = ("id", "Article_title", "movie_title", "image", "rating", "author_username")

    written_articles = articleSerializer(
        many=True, 
        read_only=True, 
        source="articles"  # User 모델의 작성한 게시글 목록 (related_name='articles' 사용)
    )
    written_articles_count = serializers.IntegerField(
        source="articles.count", read_only=True  # 작성한 게시글 수
    )

    class commentSerializer(serializers.ModelSerializer):  # 작성한 댓글 정보
        Article_title = serializers.CharField(source='article.Article_title', read_only=True)  # 게시글 제목
        author_username = serializers.CharField(source='author.username', read_only=True)  # 댓글 작성자 이름

        class Meta:
            model = Comment
            fields = ("id", "content", "created_at", "Article_title", "author_username")

    written_comments = commentSerializer(
        many=True, 
        read_only=True, 
        source="comments"  # User 모델의 작성한 댓글 목록 (related_name='comments' 사용)
    )
    written_comments_count = serializers.IntegerField(
        source="comments.count", read_only=True  # 작성한 댓글 수
    )
    
    # 프로필 이미지
    profile_image = serializers.SerializerMethodField()

    # 성별, 주민등록번호, 전화번호
    gender = serializers.CharField(source='get_gender_display', read_only=True)
    ssn = serializers.CharField(read_only=True)
    phone_number = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = [
            "email",
            "username",
            "profile_image",
            "followings",
            "followers",
            "follower_count",
            "following_count",
            "profile_image",
            "gender",        # 성별 필드 추가
            "ssn",           # 주민등록번호 필드 추가
            "phone_number",  # 전화번호 필드 추가
            "Favorite_articles",  # 좋아요 한 게시글 정보
            "Favorite_articles_count",  # 좋아요 한 게시글 수
            "Favorite_comments",  # 좋아요한 댓글 정보
            "Favorite_comments_count",  # 좋아요 한 댓글 수
            "written_articles",  # 작성한 게시글 목록
            "written_articles_count",  # 작성한 게시글 수
            "written_comments",  # 작성한 댓글 목록
            "written_comments_count",  # 작성한 댓글 수
            "bot_Conversation_List"  # 챗봇 대화 리스트
        ]  # 반환할 필드

    def get_profile_image(self, obj):
        request = self.context.get("request")
        if obj.profile_image:
            return request.build_absolute_uri(obj.profile_image.url)
        return None



class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "email","profile_image")  # 수정 가능한 필드

class passwordchangeSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["password"]  # 수정 가능한 필드
        
        
    def validate_password(self, value):
        """비밀번호 유효성 검사"""
        if len(value) < 8:
            raise serializers.ValidationError("비밀번호는 8자리 이상이어야 합니다.")
        # 다른 비밀번호 강도 관련 검사를 추가할 수도 있습니다.
        return value
    
    def update(self, instance, validated_data):
        instance.set_password(validated_data['password'])  # 비밀번호 해시화
        instance.save()
        return instance

