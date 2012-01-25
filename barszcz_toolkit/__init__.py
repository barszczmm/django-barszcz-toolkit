from django.utils.translation import ugettext as _
from django.contrib import messages
from django.contrib.auth.signals import user_logged_out
from django.contrib.comments.signals import comment_was_posted


def comment_notification(sender, comment, request, **kwargs):
    messages.success(request, _('Comment was posted.'), fail_silently=True)

comment_was_posted.connect(comment_notification)


def logout_notification(sender, request, user, **kwargs):
    messages.success(request, _('You have been signed out.'), fail_silently=True)

user_logged_out.connect(logout_notification)
