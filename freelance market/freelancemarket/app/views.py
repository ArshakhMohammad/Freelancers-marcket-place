from multiprocessing import context
from urllib import request

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password

from .models import Freelancer, Client, Job, Application
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout


# =========================
# LANDING PAGE
# =========================

def landing(request):
    freelancers = Freelancer.objects.all()
    return render(request, "landing.html", {"freelancers": freelancers})


# =========================
# FREELANCER REGISTER
# =========================

def freelancer_reg(request):

    if request.method == "POST":

        full_name = request.POST.get("full_name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        skills = request.POST.get("skills")
        title = request.POST.get("title")
        bio = request.POST.get("bio")
        rate = request.POST.get("rate")

        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        profile_image = request.FILES.get("profile_image")

        # PASSWORD CHECK
        if password != confirm_password:
            messages.error(request, "Passwords do not match")
            return redirect("freelancer_reg")

        # EMAIL CHECK
        if Freelancer.objects.filter(email=email).exists():
            messages.error(request, "Email already exists")
            return redirect("freelancer_reg")

        # CREATE FREELANCER
        freelancer = Freelancer.objects.create(
            full_name=full_name,
            email=email,
            phone=phone,
            skills=skills,
            title=title,
            bio=bio,
            rate=rate,
            profile_image=profile_image,
            password=make_password(password)
        )

        freelancer.save()

        messages.success(request, "Registration Successful")

        return redirect("freelancer_login")

    return render(request, "freelancerreg.html")


# =========================
# FREELANCER LOGIN
# =========================

def freelancer_login(request):

    if request.method == "POST":

        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            freelancer = Freelancer.objects.get(email=email)

            # CHECK BLOCKED STATUS
            if freelancer.is_blocked:
                messages.error(
                    request,
                    "Your account has been blocked by admin."
                )
                return redirect("freelancer_login")

            # CHECK PASSWORD
            if check_password(password, freelancer.password):

                request.session["freelancer_id"] = freelancer.id
                request.session["freelancer_name"] = freelancer.full_name

                messages.success(request, "Login Successful")

                return redirect("freelancer_dashboard")

            else:
                messages.error(request, "Invalid Password")

        except Freelancer.DoesNotExist:
            messages.error(request, "Email does not exist")

    return render(request, "freelancerlogin.html")

# =========================
# FREELANCER DASHBOARD
# =========================

def freelancer_dashboard(request):

    freelancer_id = request.session.get("freelancer_id")

    if not freelancer_id:
        return redirect("freelancer_login")

    freelancer = Freelancer.objects.get(id=freelancer_id)

    applications = Application.objects.filter(
        freelancer=freelancer
    ).select_related(
        "job",
        "job__client"
    )

    total_applications = applications.count()

    pending_proposals = applications.filter(
        status="pending"
    ).count()

    accepted_jobs = applications.filter(
        status="accepted"
    ).count()

    context = {
    "freelancer": freelancer,
    "applications": applications,
    "total_projects": applications.count(),
    "pending_proposals": applications.filter(status="pending").count(),
    "completed_jobs": applications.filter(status="accepted").count(),
    }

    return render(
        request,
        "freelancerdashboard.html",
        context
    )
# =========================
# FREELANCER LOGOUT
# =========================

def freelancer_logout(request):

    request.session.flush()

    return redirect("freelancer_login")


# =========================
# FREELANCER PROFILE VIEW
# =========================

def freelancer_profile(request, freelancer_id):

    freelancer = get_object_or_404(
        Freelancer,
        id=freelancer_id
    )

    context = {
        "freelancer": freelancer
    }

    return render(
        request,
        "profile.html",
        context
    )


# =========================
# UPDATE PROFILE
# =========================

# def profile(request, freelancer_id):

#     freelancer = get_object_or_404(
#         Freelancer,
#         id=freelancer_id
#     )

#     if request.method == "POST":

#         freelancer.full_name = request.POST.get("full_name")
#         freelancer.email = request.POST.get("email")
#         freelancer.phone = request.POST.get("phone")
#         freelancer.skills = request.POST.get("skills")

#         # THESE FIELDS MUST EXIST IN MODEL
#         freelancer.title = request.POST.get("title")
#         freelancer.bio = request.POST.get("bio")

#         # PROFILE IMAGE
#         if request.FILES.get("profile_image"):
#             freelancer.profile_image = request.FILES.get("profile_image")

#         freelancer.save()

#         messages.success(
#             request,
#             "Profile Updated Successfully"
#         )

#         return redirect(
#             "profile",
#             freelancer_id=freelancer.id
#         )

#     context = {
#         "freelancer": freelancer
#     }

#     return render(
#         request,
#         "profile.html",
#         context
#     )


# =========================
# CLIENT REGISTER
# =========================

from django.shortcuts import render, redirect
from .models import Client


def client_reg(request):

    if request.method == "POST":

        email = request.POST.get("email")

        if Client.objects.filter(email=email).exists():
            messages.error(request, "Email already registered")
            return redirect("client_reg")

        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if password != confirm_password:
            messages.error(request, "Passwords do not match")
            return redirect("client_reg")

        Client.objects.create(
            full_name=request.POST.get("full_name"),
            phone=request.POST.get("phone"),
            email=email,
            password=make_password(password),
            location=request.POST.get("location"),
            client_type=request.POST.get("client_type"),
            services=request.POST.get("services"),
            contact_method=request.POST.get("contact_method")
        )

        messages.success(request, "Registration successful")
        return redirect("client_login")

    return render(request, "clientreg.html")

# =========================
# CLIENT LOGIN
# =========================

def client_login(request):

    if request.method == "POST":

        email = request.POST.get("email")
        password = request.POST.get("password")

        try:

            client = Client.objects.get(email=email)

            # CHECK IF BLOCKED
            if client.is_blocked:
                messages.error(
                    request,
                    "Your account has been blocked by admin."
                )
                return redirect("client_login")

            # CHECK PASSWORD
            if check_password(
                password,
                client.password
            ):

                request.session["client_id"] = client.id
                request.session["client_name"] = client.full_name

                messages.success(
                    request,
                    "Login Successful"
                )

                return redirect("client_dashboard")

            else:

                messages.error(
                    request,
                    "Invalid Password"
                )

        except Client.DoesNotExist:

            messages.error(
                request,
                "Email does not exist"
            )

    return render(
        request,
        "clientlogin.html"
    )

# =========================
# CLIENT DASHBOARD
# =========================

def client_dashboard(request):
    client_id = request.session.get("client_id")

    if not client_id:
        return redirect("client_login")

    client = Client.objects.get(id=client_id)

    if request.method == "POST":
        action = request.POST.get("action")

        if action == "update_profile":
            client.full_name = request.POST.get("full_name")
            client.email = request.POST.get("email")
            client.phone = request.POST.get("phone")
            client.location = request.POST.get("location")
            client.save()
            return redirect("client_dashboard")

        elif action == "post_job":
            Job.objects.create(
                client=client,
                title=request.POST.get("title"),
                description=request.POST.get("description"),
                budget=request.POST.get("budget"),
                location=request.POST.get("job_location"),
                category=request.POST.get("category", "General")
            )
            return redirect("client_dashboard")

    search_query = request.GET.get("search", "")

    if search_query:
        freelancers = Freelancer.objects.filter(skills__icontains=search_query)
    else:
        freelancers = Freelancer.objects.all()

    jobs = Job.objects.filter(client=client).order_by("-created_at")

    applications = Application.objects.filter(
        job__client=client
    ).select_related(
        "job",
        "freelancer"
    ).order_by("-created_at")

    context = {
        "client": client,
        "jobs": jobs,
        "applications": applications,
        "application_count": applications.count(),
        "freelancers": freelancers,
        "top_freelancers": Freelancer.objects.all()[:6],
        "search_query": search_query,
    }

    return render(request, "clientdashboard.html", context)

# =========================
# CLIENT LOGOUT
# =========================

def client_logout(request):

    request.session.flush()

    return redirect("client_login")


# =========================
# POST JOB
# =========================

def post_job(request):

    client_id = request.session.get("client_id")

    if not client_id:

        return redirect("client_login")

    client = Client.objects.get(id=client_id)

    if request.method == "POST":

        title = request.POST.get("title")
        description = request.POST.get("description")
        budget = request.POST.get("budget")
        location = request.POST.get("location")
        category = request.POST.get("category")

        Job.objects.create(

            client=client,
            title=title,
            description=description,
            budget=budget,
            location=location,
            category=category

        )

        messages.success(
            request,
            "Job Posted Successfully"
        )

        return redirect("client_dashboard")

    return render(
        request,
        "postjob.html"
    )

def job_list(request):

    jobs = Job.objects.all().order_by("-created_at")

    freelancer_id = request.session.get("freelancer_id")

    applied_jobs = []

    if freelancer_id:
        applications = Application.objects.filter(
            freelancer_id=freelancer_id
        )

        applied_jobs = applications.values_list("job_id", flat=True)

        for job in jobs:
            my_app = applications.filter(job=job).first()
            accepted_app = Application.objects.filter(
                job=job,
                status="accepted"
            ).first()

            job.application_status = my_app.status if my_app else None
            job.is_taken = True if accepted_app else False
            job.taken_by_me = True if my_app and my_app.status == "accepted" else False

    else:
        for job in jobs:
            accepted_app = Application.objects.filter(
                job=job,
                status="accepted"
            ).first()

            job.application_status = None
            job.is_taken = True if accepted_app else False
            job.taken_by_me = False

    return render(request, "joblist.html", {
        "jobs": jobs,
        "applied_jobs": applied_jobs,
    })
# profile freelancer


def profile(request,freelancer_id):

    freelancer = get_object_or_404(Freelancer, id=freelancer_id)

    if request.method == "POST":

        freelancer.full_name = request.POST.get("full_name")
        freelancer.title = request.POST.get("profession")
        freelancer.email = request.POST.get("email")
        freelancer.phone = request.POST.get("phone")
        freelancer.location = request.POST.get("location")
        freelancer.bio = request.POST.get("about")
        freelancer.skills = request.POST.get("skills")

        if request.FILES.get("profile_image"):
            freelancer.profile_image = request.FILES.get("profile_image")

        freelancer.save()

        return redirect("profile", freelancer_id=freelancer.id)

    return render(
        request,
        "profile.html",
        {"freelancer": freelancer}
    )

def apply_job(request, job_id):

    freelancer_id = request.session.get("freelancer_id")

    if not freelancer_id:
        return redirect("freelancer_login")

    freelancer = Freelancer.objects.get(id=freelancer_id)
    job = Job.objects.get(id=job_id)
    cover_letter = request.POST.get("cover_letter")

    # prevent duplicate apply
    exists = Application.objects.filter(
        job=job,
        freelancer=freelancer
    ).exists()

    if not exists:
        Application.objects.create(
            job=job,
            freelancer=freelancer,
            cover_letter=cover_letter
        )

    return redirect("job_list")

def job_applications(request, job_id):

    applications = Application.objects.filter(
        job_id=job_id
    )

    return render(
        request,
        "applications.html",
        {"applications":applications}
    )

def accept_application(request, app_id):

    application = get_object_or_404(
        Application,
        id=app_id
    )

    already_accepted = Application.objects.filter(
        job=application.job,
        status="accepted"
    ).exists()

    if already_accepted:
        messages.error(
            request,
            "A freelancer has already been selected for this job."
        )
        return redirect("client_dashboard")

    application.status = "accepted"
    application.save()

    Application.objects.filter(
        job=application.job
    ).exclude(
        id=application.id
    ).update(
        status="rejected"
    )

    return redirect("client_dashboard")


def reject_application(request, app_id):

    application = Application.objects.get(
        id=app_id
    )

    application.status = "rejected"
    application.save()

    return redirect("client_dashboard")

def apply_job(request, job_id):

    freelancer_id = request.session.get("freelancer_id")

    if not freelancer_id:
        return redirect("freelancer_login")

    freelancer = Freelancer.objects.get(id=freelancer_id)

    job = get_object_or_404(Job, id=job_id)

    # Prevent duplicate applications
    if Application.objects.filter(
        job=job,
        freelancer=freelancer
    ).exists():

        messages.warning(request,"You already applied for this job.")

        return redirect("job_list")

    if request.method == "POST":

        cover_letter = request.POST.get(
            "cover_letter"
        )

        Application.objects.create(
            job=job,
            freelancer=freelancer,
            cover_letter=cover_letter
        )

        messages.success(request,"Application submitted successfully.")

        return redirect("job_list")

    return render(request,"apply__job.html",{"job": job})

def my_applications(request):

    freelancer_id = request.session.get("freelancer_id")

    if not freelancer_id:
        return redirect("freelancer_login")

    applications = Application.objects.filter(
        freelancer_id=freelancer_id
    ).select_related(
        "job",
        "job__client"
    ).order_by("-created_at")

    context = {
        "applications": applications,
        "pending_count": applications.filter(status="pending").count(),
        "accepted_count": applications.filter(status="accepted").count(),
        "rejected_count": applications.filter(status="rejected").count(),
        "completed_count": applications.filter(job__completed=True).count(),
        "work_pending_count": applications.filter(
            status="accepted",
            job__completed=False,
            job__completion_requested=False
        ).count(),
        "approval_pending_count": applications.filter(
            status="accepted",
            job__completion_requested=True,
            job__completed=False
        ).count(),
    }

    return render(request, "my_applications.html", context)
def cancel_application(request, job_id):


    freelancer_id = request.session.get("freelancer_id")

    if not freelancer_id:
        return redirect("freelancer_login")

    Application.objects.filter(
        freelancer_id=freelancer_id,
        job_id=job_id
    ).delete()

    return redirect("job_list")

def mark_completed(request, job_id):

    freelancer_id = request.session.get("freelancer_id")

    if not freelancer_id:
        return redirect("freelancer_login")

    application = get_object_or_404(
        Application,
        job_id=job_id,
        freelancer_id=freelancer_id,
        status="accepted"
    )

    job = application.job
    job.completion_requested = True
    job.save()

    return redirect("my_applications")

def approve_completion(request, job_id):

    job = get_object_or_404(Job, id=job_id)

    job.completed = True
    job.completion_requested = False
    job.save()

    return redirect("client_dashboard")

def reject_completion(request, job_id):

    job = Job.objects.get(id=job_id)

    job.completion_requested = False

    job.save()

    return redirect("client_dashboard")


# -------------------------------
           # ADMIN PANEL
# --------------------------------




def admin_login(request):

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None and user.is_staff:
            login(request, user)
            return redirect("admin_panel")
        else:
            messages.error(request, "Invalid admin login")

    return render(request, "admin_login.html")


@login_required
def admin_panel(request):

    search_client = request.GET.get("search_client", "")
    search_freelancer = request.GET.get("search_freelancer", "")

    clients = Client.objects.all().order_by("-id")
    freelancers = Freelancer.objects.all().order_by("-id")

    if search_client:
        clients = clients.filter(full_name__icontains=search_client) | clients.filter(email__icontains=search_client)

    if search_freelancer:
        freelancers = freelancers.filter(full_name__icontains=search_freelancer) | freelancers.filter(email__icontains=search_freelancer)

    context = {
        "clients": clients,
        "freelancers": freelancers,
        "search_client": search_client,
        "search_freelancer": search_freelancer,
        "client_count": Client.objects.count(),
        "freelancer_count": Freelancer.objects.count(),
    }

    return render(request, "admindashboard.html", context)


@login_required
def block_client(request, client_id):
    client = get_object_or_404(Client, id=client_id)
    client.is_blocked = True
    client.save()
    return redirect("admin_panel")


@login_required
def unblock_client(request, client_id):
    client = get_object_or_404(Client, id=client_id)
    client.is_blocked = False
    client.save()
    return redirect("admin_panel")


@login_required
def block_freelancer(request, freelancer_id):
    freelancer = get_object_or_404(Freelancer, id=freelancer_id)
    freelancer.is_blocked = True
    freelancer.save()
    return redirect("admin_panel")


@login_required
def unblock_freelancer(request, freelancer_id):
    freelancer = get_object_or_404(Freelancer, id=freelancer_id)
    freelancer.is_blocked = False
    freelancer.save()
    return redirect("admin_panel")


@login_required
def warn_client(request, client_id):

    client = get_object_or_404(Client, id=client_id)

    if request.method == "POST":
        client.warning_message = request.POST.get("warning_message")
        client.save()

    return redirect("admin_panel")


@login_required
def warn_freelancer(request, freelancer_id):

    freelancer = get_object_or_404(Freelancer, id=freelancer_id)

    if request.method == "POST":
        freelancer.warning_message = request.POST.get("warning_message")
        freelancer.save()

    return redirect("admin_panel")


def admin_logout(request):
    request.session.flush()
    return redirect('landing')