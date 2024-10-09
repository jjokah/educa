from django.contrib import messages
from django.contrib.auth import authenticate, get_user_model, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_POST

from actions.models import Action
from actions.utils import create_action

from .forms import (
    LoginForm, UserRegistrationForm,
    UserEditForm, ProfileEditForm
)
from .models import Contact, Profile


def user_login(request):
    """
    Handle user login.
    """
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            # Attempt to authenticate the user
            user = authenticate(
                request,
                username=cd['username'],
                password=cd['password']
            )
            if user is not None:
                if user.is_active:
                    # Log in the authenticated user
                    login(request, user)
                    return HttpResponse('Authenticated successfully')
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')
    else:
        # For GET requests, create an empty form
        form = LoginForm()
    # Render the login form template
    return render(request, 'account/login.html', {'form': form})


@login_required
def dashboard(request):
    """
    Display the user dashboard.
    """
    # Display all actions by default
    actions = Action.objects.exclude(user=request.user)
    following_ids = request.user.following.values_list(
        'id', flat=True
    )
    if following_ids:
        # If user is following others, retrieve only their actions
        actions = actions.filter(user_id__in=following_ids)
    actions = actions.select_related(
        'user', 'user__profile'
    ).prefetch_related('target')[:10]
    return render(
        request,
        'account/dashboard.html',
        {'section': 'dashboard', 'actions': actions}
    )


def register(request):
    """
    Handle user registration.
    """
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
            # Set the chosen password
            new_user.set_password(
                user_form.cleaned_data['password']
            )
            # Save the User object
            new_user.save()
            # # Create the user profile
            # Profile.objects.create(user=new_user)
            # create_action(new_user, 'has created an account')
            return render(
                request,
                'account/register_done.html',
                {'new_user': new_user}
            )
    else:
        user_form = UserRegistrationForm()
    return render(
        request,
        'account/register.html',
        {'user_form': user_form}
    )


@login_required
def edit(request):
    """
    Handle user profile editing.
    """
    if request.method == 'POST':
        # Create form instances with submitted data
        user_form = UserEditForm(
            instance=request.user,
            data=request.POST
        )
        profile_form = ProfileEditForm(
            instance=request.user.profile,
            data=request.POST,
            files=request.FILES # Include uploaded files
        )
        # Validate both forms
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(
                request,
                'Profile updated successfully'
            )
        else:
            messages.error(request, 'Error updating your profile')
    else:
        # For GET requests, initialize forms with current user data
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)

    # Render the edit form template with form instances
    return render(
        request,
        'account/edit.html',
        {
            'user_form': user_form,
            'profile_form': profile_form
        }
    )


User = get_user_model() # retrieve the User model dynamically


@login_required
def user_list(request):
    """
    Get all active users.
    """
    users = User.objects.filter(is_active=True)
    return render(
        request,
        'account/user/list.html',
        {'section': 'people', 'users': users}
    )


@login_required
def user_detail(request, username):
    """
    Retrieve an active user with the given username.
    """
    user = get_object_or_404(User, username=username, is_active=True)
    return render(
        request,
        'account/user/detail.html',
        {'section': 'people', 'user': user}
    )


@require_POST
@login_required
def user_follow(request):
    """
    Handle user follow/unfollow actions.
    """
    user_id = request.POST.get('id')
    action = request.POST.get('action')

    if user_id and action:
        # Attempt to get the user to follow/unfollow
        try:
            user = User.objects.get(id=user_id)
            if action == 'follow':
                # Create a new Contact object (follow the user)
                Contact.objects.get_or_create(
                    user_from=request.user,
                    user_to=user
                )
                create_action(request.user, 'is following', user)
            else:
                # Delete the Contact object (unfollow the user)
                Contact.objects.filter(
                    user_from=request.user,
                    user_to=user
                ).delete()
            return JsonResponse({'status': 'ok'})
        # Return error if the user to follow/unfollow doesn't exist
        except User.DoesNotExist:
            return JsonResponse({'status': 'error: user does not exit'})
    # Return error if either user_id or action is missing
    return JsonResponse({'status': 'error'})