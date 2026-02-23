from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse
from django.utils import timezone
from datetime import timedelta

from .forms import SignUpForm, LoginForm, VerifyEmailForm
from .models import EmailVerification, GameScore


# ── helpers ──────────────────────────────────────────────────────────────────

def _is_staff(user):
    return user.is_active and user.is_staff


# ── public views ─────────────────────────────────────────────────────────────

def home(request):
    return render(request, 'accounts/home.html')


def signup_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()  # saves with is_active=False

            # Create verification record
            verification = EmailVerification.objects.create(user=user)

            # Store user id + code in session so verify view can display it
            request.session['pending_verification_user_id'] = user.pk
            request.session['pending_code'] = verification.code
            return redirect('verify_email')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = SignUpForm()

    return render(request, 'accounts/signup.html', {'form': form})


def verify_email_view(request):
    user_id = request.session.get('pending_verification_user_id')
    if not user_id:
        messages.warning(request, 'No pending verification. Please sign up first.')
        return redirect('signup')

    user = get_object_or_404(User, pk=user_id)

    if request.method == 'POST':
        form = VerifyEmailForm(request.POST)
        if form.is_valid():
            entered = form.cleaned_data['code'].strip()
            try:
                verification = EmailVerification.objects.get(user=user)
            except EmailVerification.DoesNotExist:
                messages.error(request, 'Verification record not found. Please sign up again.')
                return redirect('signup')

            if verification.code == entered:
                # Activate the account
                user.is_active = True
                user.save()
                verification.is_verified = True
                verification.save()

                # Clean up session and log the user in
                del request.session['pending_verification_user_id']
                login(request, user)
                messages.success(request, f'Welcome to AuthApp, {user.username}! 🎉')
                return redirect('dashboard')
            else:
                messages.error(request, 'Incorrect code. Please try again.')
    else:
        form = VerifyEmailForm()

    return render(request, 'accounts/verify_email.html', {
        'form':  form,
        'email': user.email,
        'code':  request.session.get('pending_code'),  # shown on page; cleared on success
    })


def resend_code_view(request):
    """Regenerate and resend the verification code."""
    user_id = request.session.get('pending_verification_user_id')
    if not user_id:
        return redirect('signup')

    user = get_object_or_404(User, pk=user_id)
    try:
        verification = EmailVerification.objects.get(user=user)
        verification.regenerate_code()
        # Store new code in session so verify page can display it
        request.session['pending_code'] = verification.code
    except EmailVerification.DoesNotExist:
        messages.error(request, 'No verification record found.')

    return redirect('verify_email')


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            # Check if user exists but is unverified
            try:
                pending_user = User.objects.get(username=username)
                if not pending_user.is_active:
                    request.session['pending_verification_user_id'] = pending_user.pk
                    messages.warning(
                        request,
                        'Your email is not verified yet. Please enter the code sent to your email.'
                    )
                    return redirect('verify_email')
            except User.DoesNotExist:
                pass

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {user.username}!')
                next_url = request.GET.get('next', 'dashboard')
                return redirect(next_url)
            else:
                messages.error(request, 'Invalid username or password. Please try again.')
    else:
        form = LoginForm()

    return render(request, 'accounts/login.html', {'form': form})


@login_required
def dashboard(request):
    return render(request, 'accounts/dashboard.html', {'user': request.user})


def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out successfully.')
    return redirect('home')


# ── admin panel ──────────────────────────────────────────────────────────────

def _is_superuser(user):
    return user.is_active and user.is_superuser


@user_passes_test(_is_staff, login_url='/login/')
def admin_panel_view(request):
    total_users    = User.objects.count()
    verified_count = EmailVerification.objects.filter(is_verified=True).count()
    unverified_with_record = EmailVerification.objects.filter(is_verified=False).count()
    staff_count    = User.objects.filter(is_staff=True).count()
    superuser_count = User.objects.filter(is_superuser=True).count()
    week_ago       = timezone.now() - timedelta(days=7)
    new_this_week  = User.objects.filter(date_joined__gte=week_ago).count()
    search_query   = request.GET.get('q', '').strip()
    all_users      = User.objects.order_by('-date_joined')
    if search_query:
        all_users = (all_users.filter(username__icontains=search_query)
                     | User.objects.filter(email__icontains=search_query)).order_by('-date_joined')

    context = {
        'total_users':      total_users,
        'verified_count':   verified_count,
        'unverified_count': unverified_with_record,
        'staff_count':      staff_count,
        'superuser_count':  superuser_count,
        'new_this_week':    new_this_week,
        'all_users':        all_users,
        'is_super_admin':   request.user.is_superuser,
        'search_query':     search_query,
    }
    return render(request, 'accounts/admin_panel.html', context)


@user_passes_test(_is_superuser, login_url='/login/')
def promote_user_view(request, user_id):
    """Super Admin promotes a regular user to Staff Admin."""
    if request.method == 'POST':
        target = get_object_or_404(User, pk=user_id)
        if target.is_superuser:
            messages.warning(request, f'{target.username} is already a Super Admin.')
        elif target.is_staff:
            messages.info(request, f'{target.username} is already a Staff Admin.')
        else:
            target.is_staff = True
            target.save()
            messages.success(request, f'✅ {target.username} has been promoted to Staff Admin.')
    return redirect('admin_panel')


@user_passes_test(_is_superuser, login_url='/login/')
def demote_user_view(request, user_id):
    """Super Admin demotes a Staff Admin to regular user."""
    if request.method == 'POST':
        target = get_object_or_404(User, pk=user_id)
        if target.is_superuser:
            messages.error(request, 'Cannot demote a Super Admin.')
        elif target.pk == request.user.pk:
            messages.error(request, 'You cannot demote yourself.')
        elif not target.is_staff:
            messages.info(request, f'{target.username} is already a regular user.')
        else:
            target.is_staff = False
            target.save()
            messages.success(request, f'✅ {target.username} has been demoted to regular user.')
    return redirect('admin_panel')


@user_passes_test(_is_superuser, login_url='/login/')
def delete_user_view(request, user_id):
    """Super Admin deletes a user account."""
    if request.method == 'POST':
        target = get_object_or_404(User, pk=user_id)
        if target.pk == request.user.pk:
            messages.error(request, 'You cannot delete your own account.')
        elif target.is_superuser:
            messages.error(request, 'Cannot delete another Super Admin.')
        else:
            username = target.username
            target.delete()
            messages.success(request, f'\u2705 User "{username}" has been deleted.')
    return redirect('admin_panel')


@user_passes_test(_is_superuser, login_url='/login/')
def disable_user_view(request, user_id):
    """Super Admin disables a user (sets is_active=False, blocks login)."""
    if request.method == 'POST':
        target = get_object_or_404(User, pk=user_id)
        if target.pk == request.user.pk:
            messages.error(request, 'You cannot disable your own account.')
        elif target.is_superuser:
            messages.error(request, 'Cannot disable a Super Admin.')
        else:
            target.is_active = False
            target.save()
            messages.success(request, f'\u26d4 {target.username} has been disabled.')
    return redirect('admin_panel')


@user_passes_test(_is_superuser, login_url='/login/')
def enable_user_view(request, user_id):
    """Super Admin re-enables a disabled user."""
    if request.method == 'POST':
        target = get_object_or_404(User, pk=user_id)
        target.is_active = True
        target.save()
        messages.success(request, f'\u2705 {target.username} has been re-enabled.')
    return redirect('admin_panel')


# ── game ──────────────────────────────────────────────────────────────────────

import json

@login_required
def game_view(request):
    """Render the mini game page."""
    try:
        user_best = GameScore.objects.filter(user=request.user).order_by('-score').first()
    except Exception as e:
        print(f'[game_view] DB error: {e}')
        user_best = None
    return render(request, 'accounts/game.html', {'user_best': user_best})


@login_required
def submit_score_view(request):
    """Receive a JSON POST with the player's score and save it."""
    if request.method != 'POST':
        return JsonResponse({'error': 'POST required'}, status=405)
    try:
        data  = json.loads(request.body)
        score = int(data.get('score', 0))
        if score < 0:
            return JsonResponse({'error': 'Invalid score'}, status=400)
        GameScore.objects.create(user=request.user, score=score)
        user_best = GameScore.objects.filter(user=request.user).order_by('-score').first()
        return JsonResponse({'ok': True, 'best': user_best.score if user_best else score})
    except (ValueError, KeyError, json.JSONDecodeError):
        return JsonResponse({'error': 'Bad data'}, status=400)
    except Exception as e:
        print(f'[submit_score] DB error: {e}')
        return JsonResponse({'error': 'Score could not be saved'}, status=500)


def leaderboard_view(request):
    """Show top 20 scores across all users."""
    try:
        top_scores = GameScore.objects.select_related('user').order_by('-score')[:20]
        user_best  = None
        if request.user.is_authenticated:
            user_best = GameScore.objects.filter(user=request.user).order_by('-score').first()
    except Exception as e:
        print(f'[leaderboard] DB error: {e}')
        top_scores = []
        user_best  = None
    return render(request, 'accounts/leaderboard.html', {
        'top_scores': top_scores,
        'user_best':  user_best,
    })

