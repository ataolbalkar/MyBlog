from django.db import models
from django.utils import timezone  # Imported to create time variables.
from django.core.urlresolvers import reverse


# Create your models here.

class Post(models.Model):
    author = models.ForeignKey('auth.User')  # Foreign key connection between 'author' and 'User'
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)  # Saves the time post created as default.
    published_date = models.DateTimeField(blank=True, null=True)

    def publish(self):
        """
        Saves the current time when clicked the 'Publish' button.
        """
        self.published_date = timezone.now()
        self.save()

    def approve_comments(self):
        """
        Filters the comments according to their approved status.
        """
        return self.comments.filter(approved_comments=True)

    def get_absolute_url(self):
        """
        Specifies the url to go after completed the process.
        In this case, the url would be the display of the post.
        """
        return reverse('post_detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey('blog.Post', related_name='comments')  # Foreign key connection between 'comment' and 'Post'.
    author = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=False)

    def approve(self):
        """
        Using to approve a comment.
        """
        self.approved_comment = True
        self.save()

    def get_absolute_url(self):
        """
        Specifies the url to go after completed the process.
        Comments needs to be aproved to show, so it directs the user to 'post_list'.
        """
        return reverse('post_list')

    def __str__(self):
        return self.text
