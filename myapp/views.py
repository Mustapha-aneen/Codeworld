from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect,JsonResponse
from django.urls import reverse
import random
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
# Create your views csrf_exemf
from .models import Post,Comment

def slug_concat(title):
  s = title
  c = ""
  l = len(s.split(" "))
  for i in range(l):
    c += (s.split(" ")[i]+"-")
  rem = ""
  for i,v in enumerate(c):
    if i != len(c)-1:
      rem += v
    else:
      break
  return rem

def home_page(request):
  objects = Post.objects.all();
  paginator = Paginator(objects,3)
  page = request.GET.get("page")
  try:
    posts = paginator.page(page)
  except PageNotAnInteger:
    posts = paginator.page(1)
  except EmptyPage:
    posts = paginator.page(paginator.num_pages)
  context = {
    "posts":posts,
    'paginator':paginator,
  }
  return render(request, "home_page.html",context)
def search_posts(request):
  if(request.method == "GET"):
    search_query = request.GET.get("query")
    posts = []
    title_query = Post.objects.filter(title__contains=search_query)
    description_query = Post.objects.filter(description__contains=search_query)
    for q in title_query:
      if search_query != "":
        if q not in posts:
          posts.append(q)
    for q in description_query:
      if search_query != "":
        if q not in posts:
          posts.append(q)
  context = {
    "posts":posts,
    "query":search_query,
    "result":len(posts),
  }
  return render (request,"search_post.html",context)
def create_post_page(request):
  if(request.method == "POST"):
    title = request.POST.get('title')
    description = request.POST.get("description")
    image = request.FILES.get('image')
    post = Post(title=title,description=description,image=image)
    check = Post.objects.filter(title=title).exists()
    if check:
      ran = str(random.randint(0,1000))
      title = f"{title} {ran}"
    c = slug_concat(title)
    if Post.objects.filter(slug=c.lower()).exists():
      c = c.lower()+str(random.randint(0,1000))
    post.slug = c.lower()
    post.save()
  context = {
    
  }
  return render (request,"create_post.html",context)
def post_comment(request,year,month,day,post):
  posts = get_object_or_404(Post,
            publish__year = year,
            publish__month = month,
            publish__day = day,
            slug = post    
            )
  comments = posts.posts.filter(active=True)
  current_name = None
  if request.POST.get("action") == "post_comment":
    if request.method == "POST":
      name = request.POST.get("name")
      body = request.POST["body"]
      Comment.objects.create(
          post=posts,
          name = name,
          body = body,
        )
      return HttpResponseRedirect(reverse("myapp:post_comment",args=[posts.publish.year,posts.publish.month,posts.publish.day,posts.slug]))
  context = {
    "post":posts,
    "comments":comments,
    "current_name":current_name,
  }
  return render (request ,"post_comment.html",context)
def delete_post(request,month,post):
  posts = get_object_or_404(Post,
                      publish__month=month,
                      slug=post,
                  )
  if(request.method == "DELETE"):
    posts.delete()
    return HttpResponseRedirect(reverse("myapp:home_page"))
  context = {
    "post":posts
  }
  return render(request, "delete_post.html",context)
def edit_post(request,day,url):
  post = get_object_or_404(Post,publish__day=day,slug=url)
  if request.method == "POST":
    title = request.POST.get("title")
    description = request.POST.get("description")
    image = request.FILES.get("image")
    
    mpost = Post.objects.get(title=post.title,slug=post.slug)
    mpost.title = title
    mpost.description = description
    mpost.image = image
    if Post.objects.filter(slug=slug_concat(title).lower()).exists():
      ran = random.randint(0,1000)
      title = f"{slug_concat(title).lower()} {ran} edited"
    mpost.slug = slug_concat(title).lower()
   
    mpost.save()
    
  context = {
    "post":post,
  }
  return render(request,"edit_post.html",context)
def about(request):
  
  return render(request,"about.html")