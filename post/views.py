from django.shortcuts import render,HttpResponse,get_object_or_404
from django.http import HttpResponseRedirect
from django.views.generic import ListView,DetailView,CreateView
from django.views.generic import UpdateView,DeleteView
from .models import Post
from django.urls import reverse_lazy,reverse
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from .forms import CommentForm

def post_index(request):
    post_list = Post.objects.all()
    query = request.GET.get("q")
    if query:
        post_list = post_list.filter(
            Q(title__icontains=query)|
            Q(content__icontains=query)|
            Q(author__first_name__icontains=query)|
            Q(author__last_name__icontains=query)|
            Q(author__username__icontains=query)
            ).distinct()

    paginator = Paginator(post_list,3)

    page = request.GET.get('sayfa')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    return render(request,"index.html",{"posts":posts})


def post_detail(request,slug):
    post = get_object_or_404(Post, slug=slug)

    form = CommentForm(request.POST or None)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.save()

    context = dict()
    likes_connected = get_object_or_404(Post, slug=slug)
    liked = False

    if likes_connected.likes.filter(id=request.user.id).exists():
        liked = True
    total_likes = likes_connected.total_likes()
    context["total_likes"] = total_likes
    context["is_liked"]=liked
    context["form"]=form
    context["post"]=post

    return render(request,"detail.html",context)

def post_like(request,slug):
    post = get_object_or_404(Post, slug=slug)
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)

    else:
        post.likes.add(request.user)
       
    return HttpResponseRedirect(reverse('detail',args=[slug]))

class PostCreateView(CreateView):
    model = Post
    template_name = "edit/create.html"
    fields = ["title","content","image"]

    def form_valid(self,form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(UpdateView):
    model = Post
    template_name = "edit/update.html"
    fields = ["title","content","image"]

    def dispatch(self, request, *args, **kwargs):
        obj=self.get_object()
        if obj.author != self.request.user:
            raise PermissionDenied
        return super().dispatch(request,*args,**kwargs)

class PostDeleteView(DeleteView):
    model = Post
    template_name = 'edit/delete.html'
    success_url = reverse_lazy('index')

    def  dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.author != self.request.user:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)
