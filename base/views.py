from django.http import Http404, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from .models import *
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from .forms import StudentForm, WebsiteFeedbackForm, ConsultantForm, EditProfile, TestForm, ScaledFeedbackForm
from django.contrib.auth.decorators import login_required
from datetime import timedelta, datetime, date
from django.db.models import Q


# Create your views here.
# **************************************************** LOGIN-SIGNUP ********************************************
def login_page(request):
    page = 'login'

    # to restrict the user from visiting login page url if he is logged in
    if request.user.is_authenticated:
        if request.user.is_student():
            return redirect('home')
        if request.user.is_consultant():
            return redirect('consultantDashboard', pk=request.user.id)

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = MentalUser.objects.filter(email=email).first()
        except:
            messages.error(request, 'User does not exist')

        if user is not None and not user.is_active:
            messages.error(request, 'Your account is still pending approval.')
        else:
            user = authenticate(request, email=email, password=password)

            if user is not None:
                if user.is_student():
                    # Log in the student and redirect to the student homepage
                    login(request, user)
                    return redirect('home')
                elif user.is_consultant():
                    # Log in the consultant and redirect to the consultant dashboard if approved
                    login(request, user)
                    return redirect('consultantDashboard', pk=request.user.id)
            else:
                # Display error message if authentication fails
                messages.error(request, 'Invalid email or password')

    context = {'page': page}
    return render(request, 'base/login_signup.html', context)


@login_required(login_url='/login')
def logout_user(request):
    logout(request)
    return redirect('login')


def student_signup(request):
    page = 'studentSignup'
    form = StudentForm()

    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.instance.password = make_password(form.cleaned_data['password'])
            form.save()
            messages.success(request, 'Account created successfully')  # not rendered in login page, style it
            return redirect('login')

    context = {'page': page,
               'form': form, }
    return render(request, 'base/login_signup.html', context)


def consultant_signup(request):
    page = 'consultantSignup'
    form = ConsultantForm()

    if request.method == 'POST':
        form = ConsultantForm(request.POST, request.FILES)
        if form.is_valid():
            form.instance.password = make_password(form.cleaned_data['password'])
            form.save(commit=False)
            form.save()
            messages.success(request, 'Your account has been created and is pending approval.')
            return redirect('login')
        else:
            messages.error(request, 'error occurred')

    context = {'page': page,
               'form': form, }
    return render(request, 'base/login_signup.html', context)


# **************************************************** STUDENT ********************************************
@login_required(login_url='/login')
def home(request):
    disorders = DisordersContent.objects.all()
    consultants = Consultant.objects.all()

    feedback_form = WebsiteFeedbackForm()

    if request.method == 'POST':
        feedback_form = WebsiteFeedbackForm(request.POST, student=request.user.student)
        if feedback_form.is_valid():
            feedback_form.save()
            return redirect('home')
            # handle successful form submission

    students_feedback = WebsiteFeedback.objects.all()

    context = {'feedback_form': feedback_form,
               'students_feedback': students_feedback,
               'disorders': disorders,
               'consultants': consultants, }
    return render(request, 'base/home.html', context)


@login_required(login_url='/login')
def disorder_detail(request, pk):
    disorder = get_object_or_404(DisordersContent, pk=pk)
    disorders = DisordersContent.objects.all()
    context = {'disorder': disorder,
               'disorders': disorders, }
    return render(request, 'base/disorders/disordersContent.html', context)


@login_required(login_url='/login')
def daily_routines(request):
    disorders = DisordersContent.objects.all()
    context = {'footer_margin': '1150px',
               'disorders': disorders, }
    return render(request, 'base/dailyRoutines.html', context)


@login_required(login_url='/login')
def ourTeam(request):
    disorders = DisordersContent.objects.all()
    consultants = Consultant.objects.all()
    context = {'disorders': disorders,
               'consultants': consultants, }
    return render(request, 'base/ourTeam.html', context)


@login_required(login_url='/login')
def FAQ(request):
    disorders = DisordersContent.objects.all()
    context = {'disorders': disorders, }
    return render(request, 'base/FAQ.html', context)


@login_required(login_url='/login')
def suitable_consultants(request, symptom):
    consultants = Consultant.objects.filter(major__contains=symptom)
    sessions = Session.objects.all()

    context = {'consultants': consultants,
               'sessions': sessions,
               'symptom': symptom, }
    return render(request, 'base/bookAppointment/suitableConsultants.html', context)


@login_required(login_url='/login')
def available_times(request, pk, symptom):
    consultant = Consultant.objects.get(id=pk)
    sessions = Session.objects.filter(consultant=consultant)

    today = datetime.now().date()  # date
    dates = [today + timedelta(days=i) for i in range(7)]

    session_start_time = datetime.combine(today, consultant.startTime)
    session_end_time = datetime.combine(today, consultant.endTime)

    start_times = []
    while session_start_time + timedelta(minutes=20) <= session_end_time:
        start_times.append(session_start_time.strftime('%H:%M'))
        session_start_time += timedelta(minutes=20 + 30)

    end_times = [(datetime.combine(date.today(), datetime.strptime(start_time, '%H:%M').time()) + timedelta(
        minutes=20)).strftime('%H:%M') for start_time in start_times]

    session_times = []
    for start_time, end_time in zip(start_times, end_times):
        session_times.append(f"{start_time} - {end_time}")

    # create a dictionary to hold the session data for each date and time
    session_data = {}
    for session in sessions:
        # add the current session date as a key and set its value to empty
        # then add current session time corresponding to the current session date, with the session object as its value
        session_data.setdefault(session.sessionDate, {})[session.sessionTime.strftime('%H:%M')] = session

    # iterate over the session times and dates to render the available or booked button
    table_rows = []
    for session_time in session_times:
        row = []
        for theDate in dates:
            # Create a datetime object combining the current date (theDate) and the session time
            session_datetime = datetime.combine(theDate, datetime.strptime(session_time[:5], '%H:%M').time())

            # Check if the session time has passed the current time
            if session_datetime < datetime.now():
                row.append('<button class="passed" type="button">Passed</button>')
            else:
                # Query the sessions to check if a session exists for the current session time and date
                session = sessions.filter(sessionDate=theDate, sessionTime=session_datetime).first()
                if session:
                    row.append('<button class="booked" type="button">Booked</button>')
                else:
                    row.append('<button class="available" type="button">Available</button>')
        table_rows.append((session_time, row))

    context = {'consultant': consultant,
               'dates': dates,
               'session_data': session_data,
               'table_rows': table_rows,
               'symptom': symptom}
    return render(request, 'base/bookAppointment/availableTimes.html', context)


@login_required(login_url='/login')
def book_appointment(request):
    today = datetime.now().date()  # date
    current_time = datetime.now().time()  # current time
    dates = [today + timedelta(days=i) for i in range(7)]

    # Check if the user has a booked session within the next 7 days
    booked_sessions = Session.objects.filter(student=request.user, sessionDate__in=dates)

    if booked_sessions.exists():
        latest_session = booked_sessions.latest('sessionDate', 'sessionTime')
        if latest_session.sessionDate > today or (
                latest_session.sessionDate == today and latest_session.sessionTime > current_time):
            # User already has a booked session in the future or today in a later time
            messages.error(request,
                           f'You already have a booked session with {latest_session.consultant.username} on {latest_session.sessionDate} at {latest_session.sessionTime.strftime("%H:%M")}.')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

    if request.method == 'POST':
        session_time = request.POST.get('session_time')
        start_time = datetime.strptime(session_time.split(' - ')[0], '%H:%M').time()
        start_time_str = start_time.strftime('%H:%M')
        consultant_id = request.POST.get('consultant_id')
        student_id = request.POST.get('student_id')

        session_date_index_str = request.POST.get('session_date')
        if session_date_index_str:
            session_date_index = int(session_date_index_str)
            session_date = dates[session_date_index]
            consultant = Consultant.objects.get(id=consultant_id)
            student = Student.objects.get(id=student_id)
            session = Session(student=student, consultant=consultant, sessionTime=start_time_str,
                              sessionDate=session_date)
            session.save()

    # If the POST request did not occur or failed validation, redirect to the previous page
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


@login_required(login_url='/login')
def test_view(request, pk):
    user = Student.objects.get(id=pk)
    if request.method == 'POST':
        form = TestForm(request.POST)
        if form.is_valid():
            test = form.save(commit=False)
            test.user = user
            test.save()
            symptom_key = form.cleaned_data['symptoms']
            return redirect('consulPage', symptom=symptom_key)

        else:
            messages.error(request, 'please fill all information')
    else:
        form = TestForm()

    context = {'user': user,
               'form': form, }
    return render(request, 'base/bookAppointment/Test.html', context)


@login_required(login_url='/login')
def student_history(request, pk):
    user = Student.objects.get(id=pk)
    # retrieve sessions that have an earlier date than today's date or today's date with earlier time than current time.
    sessions = Session.objects.filter(
        Q(student=user),
        Q(sessionDate__lt=datetime.today().date()) |
        Q(sessionDate=datetime.today().date(), sessionTime__lt=datetime.now().time())
    )

    session_data = []
    for session in sessions:

        # Get the scaled feedback for the session
        scaled_feedback = ScaledFeedback.objects.filter(session=session).first()
        if scaled_feedback:
            button_color = 'green'
        else:
            button_color = 'red'

        # Add the session data to the list
        session_data.append({
            'id': session.id,
            'date': session.sessionDate,
            'time': session.sessionTime,
            'button_color': button_color,
            'consultant': session.consultant,
            'scaled_feedback': scaled_feedback.scale if scaled_feedback else None,
        })

    reversed_session_data = reversed(session_data)

    context = {'user': user,
               'session_data': reversed_session_data, }
    return render(request, 'base/studentHistory.html', context)


@login_required(login_url='/login')
def student_scaledFeedback(request):
    session_id = request.POST.get('session_id')
    session = Session.objects.get(id=session_id)

    scaled_feedback = ScaledFeedback.objects.get(session=session)

    # Get the consultant notes for the session
    notes = ""
    if scaled_feedback:
        notes = scaled_feedback.notes

    context = {'scaled_feedback': scaled_feedback.scale if scaled_feedback else None,
               'notes': notes,
               'session': session, }
    return render(request, 'base/std_scaledFeedback.html', context)


@login_required(login_url='/login')
def student_sessions(request, pk):
    user = Student.objects.get(id=pk)
    sessions = Session.objects.filter(student=user)
    current_time = datetime.now()
    session_data = []
    for session in sessions:

        # Calculate the end of the session (15 minutes after the start time)
        end_time = datetime.combine(session.sessionDate, session.sessionTime) + timedelta(minutes=20)

        if end_time < current_time:
            continue  # Skip the session if it has already passed

        # Determine whether the current time is within the session window
        if datetime.combine(session.sessionDate, session.sessionTime) <= current_time <= end_time:
            button_color = 'green'
        else:
            button_color = 'red'

        # Add the session data to the list
        session_data.append({
            'id': session.id,
            'date': session.sessionDate,
            'time': session.sessionTime,
            'button_color': button_color,
            'consultant': session.consultant,
        })

    context = {'user': user,
               'session_data': session_data, }
    return render(request, 'base/studentSessions.html', context)


@login_required(login_url='/login')
def delete_session(request):
    if request.method == 'POST':
        session_id = request.POST.get('session_id')

        # Retrieve the session object or return 404 if not found
        session = Session.objects.filter(id=session_id)
        try:
            # Delete the session
            session.delete()
            messages.success(request, 'Session deleted successfully')
        except:
            messages.error(request, 'Failed to delete the session')

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


# **************************************************** CONSULTANT ********************************************
@login_required(login_url='/login')
def consultant_dashboard(request, pk):
    user = Consultant.objects.get(id=pk)
    sessions = Session.objects.filter(consultant=user)
    current_time = datetime.now()
    session_data = []
    for session in sessions:
        # Calculate the end of the session (20 minutes after the start time)
        end_time = datetime.combine(session.sessionDate, session.sessionTime) + timedelta(minutes=20)

        # Determine whether the current time is within the session window
        if datetime.combine(session.sessionDate, session.sessionTime) <= current_time <= end_time:
            button_color = 'green'
        else:
            if datetime.combine(session.sessionDate, session.sessionTime) < datetime.now():
                button_color = 'gray'
            else:
                button_color = 'red'

        # Add the session data to the list
        session_data.append({
            'id': session.id,
            'student': session.student.username,
            'date': session.sessionDate,
            'time': session.sessionTime,
            'button_color': button_color
        })

    reversed_session_data = reversed(session_data)

    context = {'user': user,
               'session_data': reversed_session_data, }
    return render(request, 'base/consultant/consultantDashboard.html', context)


@login_required(login_url='/login')
def edit_consultant_info(request, pk):
    user = Consultant.objects.get(id=pk)
    form = EditProfile(instance=user)

    if request.method == 'POST':
        form = EditProfile(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account information was updated successfully.')
            return redirect('editConsultant', user.id)

    context = {'user': user, 'form': form}
    return render(request, 'base/consultant/editConsultantInfo.html', context)


# **************************************************** Chat Session ********************************************
@login_required(login_url='/login')
def student_chat(request, session_pk):
    session = get_object_or_404(Session, id=session_pk)
    chat_messages = session.message_set.all()  # get all messages of a certain room

    if not session.sessionEndTime:
        session.sessionEndTime = datetime.combine(session.sessionDate, session.sessionTime) + timedelta(minutes=20)
        session.save()

    if request.method == 'POST':
        Message.objects.create(
            user=request.user,
            session=session,
            body=request.POST.get('body')
        )
        return redirect('student_chat', session_pk=session.id)

    reversed_chat_messages = reversed(chat_messages)

    end_time = session.sessionEndTime

    context = {
        'session': session,
        'chat_messages': reversed_chat_messages,
        'end_time': end_time,
    }
    return render(request, 'base/chat/stdChatSession.html', context)


@login_required(login_url='/login')
def consultant_chat(request, session_pk):
    session = get_object_or_404(Session, id=session_pk)
    chat_messages = session.message_set.all()

    if not session.sessionEndTime:
        session.sessionEndTime = datetime.combine(session.sessionDate, session.sessionTime) + timedelta(minutes=20)
        session.save()

    if request.method == 'POST':
        if request.POST.get('body') is not None:
            message = Message.objects.create(
                user=request.user,
                session=session,
                body=request.POST.get('body')
            )
            return redirect('consultant_chat', session_pk=session_pk)

        if request.POST.get('session_pk'):
            session.sessionEndTime = datetime.combine(session.sessionDate, session.sessionTime) + timedelta(minutes=30)
            session.save()

    reversed_chat_messages = reversed(chat_messages)

    end_time = session.sessionEndTime

    context = {
        'session_pk': session_pk,
        'session': session,
        'chat_messages': reversed_chat_messages,
        'end_time': end_time,
    }
    return render(request, 'base/chat/consChatSession.html', context)


@login_required(login_url='/login')
def give_scaledFeedback(request, pk):
    session = Session.objects.get(id=pk)

    if request.method == 'POST':
        form = ScaledFeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.session = session
            feedback.save()

            # Optionally, you can redirect to a success page or perform additional actions
            return redirect('consultantDashboard', pk=session.consultant.id)

    else:
        form = ScaledFeedbackForm()

        context = {
            'form': form,
            'session': session,
        }
    return render(request, 'base/consultant/give_scaledFeedback.html', context)


# @login_required(login_url='/login')
# def give_scaledFeedback(request, pk):
#     session = Session.objects.get(id=pk)
#
#     if request.method == 'POST':
#         form = ScaledFeedbackForm(request.POST)
#         if form.is_valid():
#             scale = form.cleaned_data['stages']
#             notes = form.cleaned_data['notes']
#
#             # Save the form data to the model
#             feedback = ScaledFeedback(scale=scale, notes=notes, session=session)
#             feedback.save()
#
#             # Optionally, you can redirect to a success page or perform additional actions
#             return redirect('success-page')  # Replace 'success-page' with the appropriate URL or view name
#
#     else:
#         form = ScaledFeedbackForm()
#
#     return render(request, 'base/consultant/give_scaledFeedback.html', {'form': form})


@login_required(login_url='/login')
def std_enter_session(request):
    if request.method == 'POST':
        session_id = request.POST.get('session_id')

        try:
            session = Session.objects.get(id=session_id)
            return redirect('student_chat', session_pk=session.id)
        except:
            messages.error(request, 'Failed to Enter the session')

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


@login_required(login_url='/login')
def consul_enter_session(request):
    if request.method == 'POST':
        session_id = request.POST.get('session_id')

        try:
            session = Session.objects.get(id=session_id)
            return redirect('consultant_chat', session_pk=session.pk)
        except:
            messages.error(request, 'Failed to enter the session')

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
