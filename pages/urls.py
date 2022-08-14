from django.urls import path

from .views import FindFriendView, FollowUnfollowView, FriendProfileView, HomeView, LikeUnlikeView, PostAddView, PostCommentView, ProfileView ,ProfileEditView
from accounts.middlewares import auth_middleware,auth_middleware_w_slug

app_name="pages"
urlpatterns=[
    path("",auth_middleware(HomeView.as_view()),name="home"),
    path("profile/",auth_middleware(ProfileView.as_view()),name='profile'),
    path("profile/edit/",auth_middleware(ProfileEditView.as_view()),name="edit-profile"),
    path("add/post/",auth_middleware(PostAddView.as_view()),name="add-post"),

    path("profile/<slug:url>/",auth_middleware_w_slug(FriendProfileView.as_view()),name="friend-profile"),
    path("follow-unfollow/",auth_middleware(FollowUnfollowView.as_view()),name="follow-unfollow"),
    path("like-unlike/",auth_middleware(LikeUnlikeView.as_view()),name="like-unlike"),
    path("post-comment/",auth_middleware(PostCommentView.as_view()),name="post-comment"),
    path("suggestion/",auth_middleware(FindFriendView.as_view()),name="find-friend"),

]