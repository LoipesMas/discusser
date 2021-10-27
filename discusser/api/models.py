from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    """
    Model representing a single post
    """
    date = models.DateTimeField(auto_now_add=True)
    content = models.TextField()

    # Using SET_NULL so the post could stay when user deletes their account
    # Could instead use a "DELETED" user that would "adopt" those posts
    author = models.ForeignKey(User, models.SET_NULL, null=True)

    def get_author(self):
        """
        Returns the author's username or empty string if no author
        """
        return self.author.username if self.author else ""

    def get_likes(self):
        """
        Return the count of likes on this post
        """
        return len(Like.objects.filter(post_id__exact=self.id))


class Like(models.Model):
    """
    Model representing a like on a post
    """
    user = models.ForeignKey(User, models.CASCADE)
    post = models.ForeignKey(Post, models.CASCADE)
