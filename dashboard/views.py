from django.shortcuts import render,HttpResponse,redirect,get_object_or_404
from .models import EventReminder
from django.contrib import messages
from django.contrib.auth import authenticate, login , logout
from django.contrib.auth.models import User
from .models import EventReminder
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required


def edit_wish(request, wish_id):
    wish = get_object_or_404(EventReminder, id=wish_id, user=request.user)

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'delete':  # If the action is delete, remove the wish
            wish.delete()
            messages.success(request, "Wish deleted successfully!")
            return redirect('wishboard')

        # Otherwise, it's an update request
        wish.sender_name = request.POST.get('sender_name')
        wish.recipient_name = request.POST.get('recipient_name')
        wish.sender_email = request.POST.get('sender_email')
        wish.recipient_email = request.POST.get('recipient_email')
        wish.location = request.POST.get('location')
        wish.date = request.POST.get('date')
        wish.occasion = request.POST.get('occasion')
        wish.custom_message = request.POST.get('message')

        wish.save()
        messages.success(request, "Wish updated successfully!")
        return redirect('wishboard')

    return render(request, 'edit_wish.html', {'wish': wish})


@require_POST
def delete_wish(request, wish_id):
    wish = get_object_or_404(EventReminder, id=wish_id, user=request.user)
    wish.delete()
    messages.success(request, "Wish deleted successfully!")
    return redirect('wishboard')



def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('username')
        password = request.POST.get('password')

        if 'signup' in request.POST:
            # Signup flow
            if User.objects.filter(username=email).exists():
                messages.error(request, 'User already exists. Please log in.')
            else:
                user = User.objects.create_user(username=email, email=email, password=password)
                login(request, user)  # Automatically log in after signup
                messages.success(request, 'Account created and logged in successfully!')
                return redirect('homepage')

        else:
            # Login flow
            try:
                user_obj = User.objects.get(username=email)
                user = authenticate(request, username=email, password=password)
                if user:
                    login(request, user)
                    messages.success(request, 'Logged in successfully!')
                    return redirect('homepage')
                else:
                    messages.error(request, 'Invalid password.')
            except User.DoesNotExist:
                messages.error(request, 'User does not exist. Please sign up.')

    return render(request, 'authentication.html')

def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect('homepage')

def birthday_view(request):
    if  request.user.is_authenticated:
        return render(request,'birthday.html')
    else:
        messages.error(request, 'Please log in to continue.')
        return render(request,'homepage.html')

def anniversary_view(request):
    if  request.user.is_authenticated:
        return render(request,'anniversary.html')
    else:
        messages.error(request, 'Please log in to continue.')
        return render(request,'homepage.html')

def homepage(request):
    return render(request,'homepage.html')

def wishboard(request):
    # Fetch all wishes for the logged-in user
    user_wishes = EventReminder.objects.filter(user=request.user).order_by('-date')
    
    if request.method == 'POST':
        # Get the ID of the wish to delete
        wish_id = request.POST.get('wish_id')
        
        if wish_id:
            try:
                # Find the wish by ID and delete it
                wish = EventReminder.objects.get(id=wish_id, user=request.user)
                wish.delete()  # Delete the wish from the database
                
                # Add a success message
                messages.success(request, "Wish deleted successfully!")
                
                return redirect('wishboard')  # Redirect to the same page to refresh
            except EventReminder.DoesNotExist:
                pass  # Handle the case if the wish does not exist (optional)
    
    return render(request, 'wishboard.html', {'wishes': user_wishes})

def save_event_reminder(request):
    if request.method == 'POST':
        sender_name = request.POST.get('sender_name')
        recipient_name = request.POST.get('recipient_name')
        sender_email = request.POST.get('sender_email')
        recipient_email = request.POST.get('recipient_email')
        location = request.POST.get('location')
        date = request.POST.get('date')
        occasion = request.POST.get('occasion')
        custom_message = request.POST.get('custom_message', '')

        # Save data with relation to the logged-in user
        EventReminder.objects.create(
            user=request.user,
            sender_name=sender_name,
            recipient_name=recipient_name,
            sender_email=sender_email,
            recipient_email=recipient_email,
            location=location,
            date=date,
            occasion=occasion,
            custom_message=custom_message
        )
    return redirect('/homepage')

def birthday_templates(request):
    return render(request, 'birthday_templates.html')

def anniversary_templates(request):
    return render(request, 'anniversary_templates.html')

@login_required
def personal_details(request):
    user = request.user

    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')

        if first_name and last_name:
            user.first_name = first_name
            user.last_name = last_name
            user.save()
            messages.success(request, "✅ Your details have been saved!")

        return redirect('personal_details')

    context = {
        'first_name': user.first_name,
        'last_name': user.last_name,
    }
    return render(request, 'personal_details.html', context)