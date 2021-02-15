from django.shortcuts import render, get_object_or_404,redirect
from blog.models import Post, Comment
from django.utils import timezone
from blog.forms import PostForm, CommentForm
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin  # When used only logged in users can access that process.
from django.views.generic import (TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView)


# Create your views here.

class AboutView(TemplateView):
    template_name = 'about.html'


class PostListView(ListView):
    """
    View of the main page. Posts will be display listed.
    """
    model = Post

    def get_queryset(self):
        """
        Filters the post according to their 'published_date' attribute and order them.
        """
        # published_date__lte = timezone.now(): published date attribute less then or equal to present time.
        # order_by('-published_date'): Order by 'published_date' but '-' means DESC.
        return Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')


class PostDetailView(DetailView):
    model = Post


class CreatePostView(LoginRequiredMixin, CreateView):
    login_url = '/login/'  # Defined to redirect the not logged in users to the 'login' page.
    redirect_field_name = 'blog/post_detail.html'  # Defined to redirect the logged in users to the process page.

    form_class = PostForm

    model = Post


class PostUpdateView(LoginRequiredMixin, UpdateView):
    login_url = '/login/'  # Defined to redirect the not logged in users to the 'login' page.
    redirect_field_name = 'blog/post_detail.html'  # Defined to redirect the logged in users to the process page.

    form_class = PostForm

    model = Post


class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('post_list')  # Redirect url after process is done.


class DraftListView(LoginRequiredMixin, ListView):
    login_url = '/login/'
    redirect_field_name = 'blog/post_draft_list.html'
    model = Post

    def get_queryset(self):
        """
        Selects the post that are not published yet.
        """
        # published_date__isnull=True: Filter to select the posts that 'published_date' attribute is null which means,
        # posts that are not published yet.
        # order_by('create_date'): Orders post by their 'created_date' attribute ASC.
        return Post.objects.filter(published_date__isnull=True).order_by('created_date')


@login_required  # Decorator to disable commenting for non-users.
def add_comment_to_post(request, pk):
    """
    Function to comment.
    :param pk: The primary key to the actual post.
    """
    post = get_object_or_404(Post, pk=pk)  # Get the post object or return 404 Error.

    if request.method == 'POST':
        form = CommentForm(request.POST)

        if form.is_valid():

            comment = form.save(commit=False)  # Save the comment according to form.
            comment.post = post  # The comment model has a foreign key as 'post'. That's 'comment.post' is this 'post'.
            comment.save()  # Save the model.
            return redirect('post_detail', pk=post.pk)  # Redirect to the 'post_detail' page.

    else:
        # If the method is not 'post', just send the form to the user.
        form = CommentForm()

    # Redirect user to the form page for the comment.
    return render(request, 'blog/comment_form.html', {'form': form})

@login_required
def comment_approve(request, pk):
    """
    Function to approve comments.
    :param pk: Primary key of the comment to approve.
    """
    comment = get_object_or_404(Comment, pk=pk)  # Get the comment object or return 404 Error.
    comment.approve()   # Run the approve method method to approve the comment.

    return redirect('post_detail', pk=comment.post.pk)  # Redirect user to the post detail page.


@login_required
def comment_remove(request, pk):
    """
    Function to delete comment.
    :param pk: Primary key of the comment to delete.
    """
    comment = get_object_or_404(Comment, pk=pk)  # Get the comment object or return 404 Error.
    # If the comment is deleted before receiving the posts 'primary key', there is no way to access 'primary key'.
    post_pk = comment.post.pk  # Saves the primary key of the post before delete the comment object.
    comment.delete()  # Delete the comment.
    return redirect('post_detail', pk=post_pk)  # Redirect user to the post detail page.

@login_required
def post_publish(request, pk):
    """
    Marks the posts as published.
    :param pk: Posts primary key.
    """
    post = get_object_or_404(Post, pk=pk)  # Get the post object or return 404 Error.
    post.publish()  # Mark the post as published.
    return redirect('post_detail', pk)  # Redirect user to the post detail page.
