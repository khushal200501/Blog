from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse
from django.urls import reverse
from apps.models import Post, BlogComment
from django.contrib import messages
from apps.templatetags import get_dict
from django.contrib.auth.decorators import login_required
from django.template.defaultfilters import slugify

def bloghome(request):
    userPosts = Post.objects.all() 
    if request.user.is_authenticated:
        allPosts = userPosts
    else:
        allPosts = userPosts[:4]

    context = {
        'posts_count': len(allPosts),
        'userPosts': allPosts
    }
    return render(request, "apps/bloghome.html", context)
    #return HttpResponse('bloghome')

def search(request):
    query=request.GET['query']
    if len(query)>50:
        allPosts= Post.objects.none()
    else:
        allPostsTitle=Post.objects.filter(title__icontains=query)
        allPostsContent=Post.objects.filter(content__icontains=query)
        allPosts = allPostsTitle.order_by().union(allPostsContent.order_by()).order_by('-timestamp')
    if allPosts.count() == 0:
        messages.warning(request, "No search results found.")
    params= {'allPosts':allPosts, 'query':query}
    return render(request,'apps/search.html', params)

def blogpost(request, slug):    
    post = get_object_or_404(Post, slug=slug)
    session_key = f'viewed_post_{post.sno}' 

    # Check if the post has been viewed in the current session
    if not request.session.get(session_key):
        # If not viewed then increment the count and save
        post.views = post.views + 1
        post.save()        
        # post viewed in the session
        request.session[session_key] = True

    # Working of Like/Unlike button
    if request.method == 'POST':
        user = request.user        

        if post.likes.filter(pk=user.pk).exists():
            post.likes.remove(user) # Unlike
        else:
            post.likes.add(user)    # Like
        anchor = f'#post-{post.slug}'
        return redirect(reverse('BlogPost', kwargs={'slug': post.slug}) + anchor)
    
    comments=BlogComment.objects.filter(post=post ,parent=None).order_by('-timestamp')
    replies=BlogComment.objects.filter(post=post).exclude(parent=None).order_by('-timestamp')
    replyDict= {}
    for reply in replies:
        if reply.parent.sno not in replyDict.keys():
            replyDict[reply.parent.sno] = [reply]
        else:
            replyDict[reply.parent.sno].append(reply)
    context={'post':post, 'comments':comments, 'user':request.user, 'replyDict':replyDict}
    return render(request,"apps/blogpost.html", context)
    #return HttpResponse(f'blogpost{slug}')

@login_required(login_url='/home/login/')
def addpost(request):    
    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content") 
        user = request.user
        newslug = slugify(title)

        if len(title) >20 and len(content)>100:
            Post.objects.create(
            title=title,
            content=content,
            user=user, 
            slug=newslug, 
            )               
            messages.success(request, "Your blog has been successfully created.")
            return redirect('/apps/') 
        else:
            messages.warning(request, "Try to post a descriptive Title or Content.")                 
            return redirect("/apps/")
    return render(request, "apps/addpost.html")

def postcomment(request):
    if request.method =="POST":
        comment=request.POST.get("comment")
        user=request.user
        postsno=request.POST.get("postsno")
        post=Post.objects.get(sno=postsno)
        parentsno=request.POST.get("parentsno")
        if parentsno =="":
            if len(comment) >5:
                comment=BlogComment(comment=comment, user=user, post=post)
                comment.save()
                messages.success(request, "Your comment has been posted.")
            else:
                messages.warning(request, "Try to enter a longer comment.")
        else:
            if len(comment) >5:
                parent=BlogComment.objects.get(sno=parentsno)
                comment=BlogComment(comment=comment, user=user, post=post, parent=parent)
                comment.save()
                messages.success(request, "Your reply has been posted.")
            else:
                messages.warning(request, "Try to enter a longer reply.")        
    return redirect(f"/apps/{post.slug}")

