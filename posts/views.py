from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.utils import timezone

from posts.models import Posts, Content, Comment
from posts.serializers import PostSerializer, CommentSerializer
from sign.models import Users
from posts.push_alarm import PushSend


# Create your views here.
def test(request):
    if request.method == 'GET':
        return HttpResponse('test')



#######################################
#   게시글 리스트 페이지     /post/
# GET : 게시글 리스트
# POST : X
# PATCH : X
# DELETE : X
#######################################
@csrf_exempt
@api_view(('GET', 'POST', 'PATCH', 'DELETE'))
def posts(request):
    if request.method == "GET":
        posts = Posts.objects.filter(deleted=0).order_by('-created_date')
        serializer = PostSerializer(posts, many=True)
        return JsonResponse(serializer.data, safe=False)

    if request.method == "POST":
        return HttpResponse("post list post")

    if request.method == "PATCH":
        return HttpResponse("post list patch")

    if request.method == "DELETE":
        return HttpResponse("post list delete")

#######################################
#   게시글 상세페이지   /post/detail
# GET : 게시글 조회
# POST : 게시글 작성
# PATCH : 게시글 수정
# DELETE : 게시글 삭제
#######################################
@csrf_exempt
@api_view(('GET', 'POST', 'PATCH', 'DELETE'))
def detail(request):
    if request.method == "GET":
        post_id = request.GET.get('post_id')
        post = Posts.objects.filter(id=post_id).first()
        content = Content.objects.filter(post_id=post_id).first()
        d = dict(
            title=post.title,
            content=content.content,
        )
        data = dict(
            content=d,
            code='000'
        )
        return Response(data=data)

    if request.method == "POST":
        title = request.POST.get('title', None)
        content = request.POST.get('content', None)
        user = request.POST.get('user_id')
        if (len(content) > 7):
            brief_description = str(content)[0:7] + "..."
        else:
            brief_description = content
        if (Users.objects.filter(id=user).first().username == "test"):
            post = Posts.objects.create(title=title, brief_description=brief_description,
                                        user_id=Users.objects.filter(id=user).first(), deleted=1, comment_count=0)
        else:
            post = Posts.objects.create(title=title, brief_description=brief_description,
                                        user_id=Users.objects.filter(id=user).first(), deleted=0, comment_count=0)
        Content.objects.create(post_id=Posts.objects.filter(id=post.id).first(), content=content, )
        data = dict(
            # msg='글작성 성공',
            code='000'
        )
        push_title = '게시판'
        push_body = '새로운 게시물이 올라왔어요! \n' + '확인해보세요'
        token_list = list(Users.objects.filter(token__isnull=False).exclude(id=user).values_list('token'))[:99]
        tokens = [x[0] for x in token_list]
        # logger = logging.getLogger('test')
        # logger.error('token : '+str(token))
        tokenNotNull = []
        for i in tokens:
            if i not in tokenNotNull and (i is not None and i != ""):
                tokenNotNull.append(i)
        if tokenNotNull and (
                Users.objects.get(id=user).username == "suhun" or Users.objects.get(id=user).username == "hogil"):
            # logger = logging.getLogger('test')
            # logger.error('suhun : '+token)
            PushSend.send_new_post(push_title, push_body, tokenNotNull)
        return Response(data=data)

    if request.method == "PATCH":
        post_id = request.GET.get('post_id')
        user_id = request.GET.get('user_id')
        post = Posts.objects.filter(id=post_id).first()
        user = Users.objects.filter(id=user_id).first()
        if (user_id == post.user_id.id or user.username == "suhun"):
            postdata = Posts.objects.get(id=post_id)
            contentdata = Content.objects.get(post_id=post_id)
            title = request.GET.get('title', None)
            content = request.GET.get('content', None)
            if (len(content) > 7):
                brief_description = str(content)[0:7] + "..."
            else:
                brief_description = content
            postdata.title = title
            postdata.brief_description = brief_description
            postdata.updated_date = timezone.now()
            contentdata.content = content
            contentdata.save()
            postdata.save()
            a = dict(
                title=title,
                content=content,
                updated_date=postdata.updated_date,
                id=postdata.id
            )
            data = dict(
                content=a,
                code='000'
            )
        else:
            data = dict(
                # msg='작가 불일치',
                code='001'
            )
        return Response(data=data)

    if request.method == "DELETE":
        post_id = request.GET.get('post_id')
        user_id = request.GET.get('user_id')
        post = Posts.objects.filter(id=post_id).first()
        user = Users.objects.filter(id=user_id).first()
        postdata = Posts.objects.get(id=post_id)
        if (user_id == post.user_id.id or user.username == "suhun"):
            postdata.deleted = 1
            postdata.save()
            data = dict(
                # msg='글 삭제 완료',
                code='000'
            )
        else:
            data = dict(
                # msg='작가 불일치',
                code='001'
            )
        return Response(data=data)

#######################################
#   댓글  /post/comments
# GET : 댓글 조회
# POST : 댓글 달기
# PATCH : 댓글 수정 (미구현)
# DELETE : 댓글 삭제
#######################################
@csrf_exempt
@api_view(('GET', 'POST', 'PATCH', 'DELETE'))
def comments(request):
    if request.method == "GET":     # GET : 댓글 조회
        post_id = request.GET.get('post_id')
        comment = Comment.objects.filter(post_id=post_id, deleted=0).all()
        comment_serializer = CommentSerializer(comment, many=True)
        data = dict(
            comments=comment_serializer.data,
            code='000',
        )
        return Response(data=data)

    if request.method == "POST":        # POST : 댓글 달기
        post_id = request.POST.get('post_id')
        content = request.POST.get('content', None)
        user = request.POST.get('user_id')
        if (Users.objects.filter(id=user).first().username == "test"):
            comment = Comment.objects.create(
                content=content,
                post_id=Posts.objects.filter(id=post_id).first(),
                user_id=Users.objects.filter(id=user).first(),
                deleted=1
            )
        else:
            comment = Comment.objects.create(
                content=content,
                post_id=Posts.objects.filter(id=post_id).first(),
                user_id=Users.objects.filter(id=user).first(),
                deleted=0
            )
        u = Users.objects.filter(id=user).first()
        count = Comment.objects.filter(post_id=post_id, deleted=0).all()
        post = Posts.objects.filter(id=post_id).first()
        post.comment_count = count.count()
        post.save()
        comment.save()

        ######### 푸시알림
        ##########본인글에 댓글 달렸을때
        push_title = '게시판'
        push_body = post.title + ' 글에 댓글이 달렸습니다! \n' + Users.objects.filter(id=user).first().username + " : " + content
        token_list = list(
            Users.objects.filter(token__isnull=False, id=post.user_id.id).exclude(id=comment.user_id.id).values_list(
                'token'))[:99]
        tokenPost = [x[0] for x in token_list]
        if tokenPost and comment.deleted == 0:
            PushSend.send_new_comment(push_title, push_body, tokenPost, post_id)

        ##########본인이 작성한 댓글의 글에 댓글 달렸을때
        push_title = '게시판'
        push_body = post.title + ' 글에 새로운 댓글이 달렸습니다! \n' + Users.objects.filter(id=user).first().username + " : " + content
        token_list = list(Comment.objects.filter(post_id=post.id).exclude(user_id=post.user_id).exclude(
            user_id=comment.user_id).exclude(deleted=1).values_list('user_id').distinct())[:99]
        userid = [x[0] for x in token_list]
        token = []
        tokenComment = []

        for i in userid:
            if (Users.objects.get(id=i).token is not None):
                token.append(Users.objects.get(id=i).token)
        for i in token:
            if i not in tokenComment and (i is not None):
                tokenComment.append(i)

        if tokenComment and comment.deleted == 0:
            PushSend.send_new_comment(push_title, push_body, tokenComment, post_id)

        # logger = logging.getLogger('test')
        # logger.error('a : '+str(userid))
        user = dict(
            id=u.id,
            username=u.username,
        )
        com = dict(
            id=comment.id,
            content=comment.content,
            updated_date=comment.updated_date,
            user=user,
        )
        data = dict(
            comment=com,
            code='000',
        )
        return Response(data=data)

    if request.method == "PATCH":       # PATCH : 댓글 수정 (미구현)
        return HttpResponse("comment patch")

    if request.method == "DELETE":
        id = request.GET.get('id')
        user_id = request.GET.get('user_id')
        comment = Comment.objects.filter(id=id).first()
        user = Users.objects.filter(id=user_id).first()
        post = Posts.objects.filter(id=comment.post_id.id).first()
        if (user_id == comment.user_id.id or user.username == "suhun"):
            comment.deleted = 1
            comment.save()
            count = Comment.objects.filter(post_id=comment.post_id.id, deleted=0).all()
            post.comment_count = count.count()
            post.save()
            data = dict(
                # msg='댓글 삭제 완료',
                code='000'
            )
        else:
            data = dict(
                # msg='작가 불일치',
                code='001'
            )
        return Response(data=data)

###################################
# 작성자와 삭제, 수정하는 자 일치 확인 #
# /post/checkauthor              #
##################################
@csrf_exempt
@api_view(('GET', 'POST', 'PATCH', 'DELETE'))
def checkAuthor(request):  # /checkauthor/
    post_id = request.POST.get('post_id')
    user_id = request.POST.get('user_id')
    post = Posts.objects.filter(id=post_id).first()
    user = Users.objects.filter(id=user_id).first()
    if (user_id == post.user_id.id or user.username == "suhun"):
        data = dict(
            msg='작가 일치',
            code='000'
        )
    else:
        data = dict(
            msg='작가 불일치',
            code='001'
        )
    return Response(data=data)
