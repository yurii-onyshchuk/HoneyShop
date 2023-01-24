from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView
from django.db.models import F
from django.views.generic.edit import FormMixin

from .models import Post, Category, Comment
from .forms import CommentForm


class PostList(ListView):
    model = Post
    paginate_by = 5
    extra_context = {'title': 'Блог'}
    allow_empty = False


class PostsByCategory(PostList):

    def get_queryset(self):
        return Post.objects.filter(category__slug=self.kwargs['slug'])

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = Category.objects.get(slug=self.kwargs['slug'])
        return context


class Search(PostList):
    allow_empty = True

    def get_queryset(self):
        return Post.objects.filter(title__icontains=self.request.GET.get('s'))

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Результати пошуку'
        context['q'] = self.request.GET.get('q')
        return context

class SinglePost(FormMixin, DetailView):
    model = Post
    form_class = CommentForm

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        self.object.views = F('views') + 1
        self.object.save()
        self.object.refresh_from_db()
        _list = Comment.objects.filter(post__slug=self.kwargs.get('slug'), parent__isnull=True)
        paginator = Paginator(_list, 10)
        page = self.request.GET.get('page')
        context['comments'] = paginator.get_page(page)
        context['title'] = Post.objects.get(slug=self.kwargs['slug'])
        return context

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        post = self.get_object()
        if form.is_valid():
            if request.POST.get('parent', None):
                form.instance.parent_id = int(request.POST.get('parent'))
            form.instance.post = post
            form.instance.user = self.request.user
            form.save()
        return redirect(post.get_absolute_url() + '#comments')

    def get_success_url(self):
        return reverse_lazy('blog:post', kwargs={'slug': self.kwargs['slug']})



@login_required
def like_comment(request):
    comment = get_object_or_404(Comment, id=request.POST['comment_id'])
    if comment.users_like.filter(username=request.user.username).exists():
        comment.users_like.remove(request.user)
        action_result = 'removed'
    else:
        comment.users_like.add(request.user)
        action_result = 'added'
    like_total = comment.users_like.count()
    return JsonResponse({'like_total': like_total, 'action_result': action_result})
