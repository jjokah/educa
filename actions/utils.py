import datetime
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from .models import Action


def create_action(user, verb, target=None):
    """Create a new action for a user"""

    # Check for any similar action made in the last minute
    now = timezone.now()
    last_minute = now - datetime.timedelta(seconds=60)
    similar_actions = Action.objects.filter(
        user_id=user.id,
        verb=verb,
        created__gte=last_minute
    )
    # If a target is provided, further filter similar actions by target
    if target:
        target_ct = ContentType.objects.get_for_model(target)
        similar_actions = similar_actions.filter(
            target_ct=target_ct,
            target_id=target.id
        )
    # If no similar actions found, create a new action
    if not similar_actions:
        action = Action(user=user, verb=verb, target=target)
        action.save()
        return True
    # Similar action exists, so don't create a new one
    return False
