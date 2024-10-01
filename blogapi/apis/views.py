from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Post,Author,Comment
import json 
from django.db.models import F

# Create your views here.
@csrf_exempt
def blogApi(request,key=None):
    if request.method=="GET":
        if key is not None:
        
            post = Post.objects.get(id=key)
            
            comments=list(Comment.objects.filter(post=post).values('id','commenter','content'))
            print(comments)
            responseData={
                'title': post.title,
                'content': post.content,
                
                'author': post.author.name,
                'created_at': post.created_at,
                "comments":comments
            }
            
            return JsonResponse({
                
                "success":True,
                "data":responseData
            })
            
        else:           
            posts = list(Post.objects.all().select_related('author').values('id', 'title','author__name'))
            
            
            return JsonResponse(posts, safe=False)
    elif request.method=="POST":
         try:
            data = json.loads(request.body)
            title = data['title']
            content = data['content']
            author_name = data['author']
            print(request.body)
            
            author,_= Author.objects.get_or_create(name=author_name)
            post = Post.objects.create(title=title, content=content, author=author)
            print(post)
            
            return JsonResponse({
                'id': post.id,
                'title': post.title,
                'content': post.content,
                'author': author.name,
                'created_at': post.created_at
            }, status=201)

         except (KeyError, json.JSONDecodeError):
            return JsonResponse({'error': 'Invalid data'}, status=400)
    elif request.method=="PUT":
        try:
            data = json.loads(request.body)
            title = data.get('title')
            content = data.get('content')
            author_name = data.get('author')

            post = Post.objects.get(id=key)
            if title:
                post.title = title
            if content:
                post.content = content
            if author_name:
                author, _ = Author.objects.get_or_create(name=author_name)
                post.author = author

            post.save()

            return JsonResponse({
                'id': post.id,
                'title': post.title,
                'content': post.content,
                'author': post.author.name,
                'created_at': post.created_at
            }, status=200)

        except Post.DoesNotExist:
            return JsonResponse({'error': 'id is not macthing'}, status=404)
        except (KeyError, json.JSONDecodeError):
            return JsonResponse({'error': 'Invalid data'}, status=400)
    elif request.method=="DELETE":
        try:
            post = Post.objects.get(id=key)
            post.delete()
            return JsonResponse({'message': 'Post deleted successfully'}, status=204)
        except Post.DoesNotExist:
            return JsonResponse({'error': 'id not found'}, status=404)
        

@csrf_exempt
def comments(request,key,comment_id=None):
        print(comment_id)
        if request.method=='GET':
            try:
                comments=list(Comment.objects.filter(post_id=key).values('id','commenter','content'))
                if not comments:
                    return JsonResponse({"message":"no comments yet"},safe=False)
                else:
                    return JsonResponse(comments,
                                    safe=False)
            except Comment.DoesNotExist:
                return JsonResponse({'error': 'id is not found'}, status=404)
        if request.method=="POST":
            try:
                data = json.loads(request.body)
                commenter = data['commenter']
                content = data['content']

                post = Post.objects.get(id=key)
                comment = Comment.objects.create(post=post, commenter=commenter, content=content)

                return JsonResponse({
                    'id': comment.id,
                    'author': comment.commenter,
                    'content': comment.content,
                    'created_at': comment.created_at
                }, status=201)

            except Post.DoesNotExist:
                return JsonResponse({'error': 'Post not found'}, status=404)
            except (KeyError, json.JSONDecodeError):
                return JsonResponse({'error': 'Invalid data'}, status=400)
        if(request.method=="DELETE"):
            try:
                comment = Comment.objects.get(id=comment_id, post_id=key)
                comment.delete()
                return JsonResponse({'message': 'Comment deleted successfully'}, status=204)

            except Comment.DoesNotExist:
                return JsonResponse({'error': 'Comment not found'}, status=404)
        if request.method=="PUT":
            try:
                data = json.loads(request.body)
                commenter = data.get('commenter')
                content = data.get('content')
                comment = Comment.objects.get(id=comment_id, post_id=key)
                if commenter:
                    comment.commenter=commenter
                if content:
                    comment.content=content
                comment.save()
                return JsonResponse({'message': 'Comment edited successfully'}, status=204)

                
                
            except Comment.DoesNotExist:
                return JsonResponse({'error': 'id is not found'}, status=404)


        