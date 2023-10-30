from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import F, Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormMixin

from .forms import CommentForm
from .models import Post, Category, Comment


class PostList(ListView):
    """List view for blog posts."""

    model = Post
    paginate_by = 5
    extra_context = {'title': 'Блог'}
    allow_empty = False


class PostsByCategory(PostList):
    """List view for blog posts filtered by category."""

    def get_queryset(self):
        return Post.objects.filter(category__slug=self.kwargs['slug'])

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = Category.objects.get(slug=self.kwargs['slug'])
        return context


class Search(PostList):
    """List view for blog posts filtered by search query."""

    allow_empty = True

    def get_queryset(self):
        q = self.request.GET.get('q')
        return Post.objects.filter(Q(title__icontains=q) | Q(content__icontains=q))

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Результати пошуку'
        context['q'] = self.request.GET.get('q')
        return context


class SinglePost(FormMixin, DetailView):
    """Detail view for a single blog post."""

    model = Post
    form_class = CommentForm

    def get_context_data(self, *, object_list=None, **kwargs):
        """Get the context data for the single blog post.

        This method is extended to update a post's view count and
        pass post comments to the context
        """
        context = super().get_context_data()
        context['title'] = Post.objects.get(slug=self.kwargs['slug'])

        self.object.views = F('views') + 1
        self.object.save()
        self.object.refresh_from_db()

        _list = Comment.objects.filter(post__slug=self.kwargs.get('slug'), parent__isnull=True)
        paginator = Paginator(_list, 10)
        page = self.request.GET.get('page')
        context['comments'] = paginator.get_page(page)

        return context

    def post(self, request, *args, **kwargs):
        """Handle the HTTP POST request to add a comment to the blog post.
        Redirect to the current blog post with the comment anchor.
        """
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
        """Get the URL to redirect to after successfully submitting a comment."""
        return reverse_lazy('blog:post', kwargs={'slug': self.kwargs['slug']})


@login_required
def like_comment(request):
    """View for liking/unliking a comment."""
    comment = get_object_or_404(Comment, id=request.POST['comment_id'])
    if comment.users_like.filter(pk=request.user.pk).exists():
        comment.users_like.remove(request.user)
        action_result = 'removed'
    else:
        comment.users_like.add(request.user)
        action_result = 'added'
    like_total = comment.users_like.count()
    return JsonResponse({'like_total': like_total, 'action_result': action_result})
