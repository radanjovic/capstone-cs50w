from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.template.loader import render_to_string
import json
from django.http import JsonResponse
from django.views.decorators import csrf
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator

from .models import * # All the models we created
from .forms import * # All the forms we created
from .util import * # All the helper functions we created

# Saving cats and types as global dicts for future use.
categories = {
    'Adventure':'Adventure',
    'Comedy':'Comedy',
    'Epic':'Epic',
    'Erotica':'Erotica',
    'FairyTale':'FairyTale',
    'Fantasy':'Fantasy',
    'HistoricalFiction':'HistoricalFiction',
    'Horror':'Horror',
    'Mistery':'Mistery',
    'Romance':'Romance',
    'Satire':'Satire',
    'ScienceFiction':'ScienceFiction',
    'Thriller':'Thriller'
}
types = {
    'Concept':'Concept',
    'Draft':'Draft',
    'ShortStory':'ShortStory',
}

# Since this is a members only site - many (most) of the views will
# be decorated with login_required decorator. Previosly, in settigs.py
# we have set the new default login url for this decorator, that sends
# users who are not logged-in to the default login view.

# Defaul index view
@login_required
def index(request):
    return render(request, 'astator/index.html')

# User pages
@login_required
def users(request, username):
    """Displaying pages for users, with their profile, bio and their scripts."""
    try:
        profile = User.objects.get(username=username)
        scripts = Script.objects.filter(user=profile).all().order_by("-created")
        user = request.user

        # Current user gets redirected to their myprofile page
        if profile == user:
            return HttpResponseRedirect(reverse('myprofile'))

        # Adding/removing to/from favorite authors
        if request.method == "POST":
            followers = profile.followers
            if 'add' in request.POST:
                add = Favorite.objects.create(user=user, author=profile)
                add.save()
            elif 'remove' in request.POST:
                remove = Favorite.objects.get(user=user, author=profile)
                remove.delete()
            return HttpResponseRedirect(reverse('users', args=(username,)))

        # GET - displaying user page
        else:
            followers = profile.followers.all()
            already_favorite = False
            for i in followers:
                if user == i.user:
                    already_favorite = True
            return render(request, 'astator/profile.html', {
                'profile':profile,
                'scripts':scripts,
                'already_in_favorites':already_favorite,
            })
    except User.DoesNotExist:
        raise Http404("User with requested username does not exist.")

# WriterHub - this page shows only users that are marked as authors - and they
# get marked as authors as soon as they post their first script. If they've not yet
# posted their script, they will not be visible in the hub.
@login_required
def writerhub(request):
    """Displaying all the writers with option for users to search dynamically"""
    # Code by: SHxKM from GitHub, repository: django-ajax-search
    ctx = {}
    url_parameter = request.GET.get("q")

    if url_parameter:
        writers = User.objects.filter(author=True).filter(name__icontains=url_parameter)
    else:
        writers = User.objects.filter(author=True)

    ctx["writers"] = writers
    if request.is_ajax():

        html = render_to_string(
            template_name="astator/writerhub_search.html", context={"writers": writers}
        )
        data_dict = {"html_from_view": html}
        return JsonResponse(data=data_dict, safe=False)

    return render(request, "astator/writerhub.html", context=ctx)

# Explore
@login_required
def explore(request):
    """Displaying all the scripts published on Astator, for users to browse in some way"""
    scripts = Script.objects.all().order_by('-created')
    paginator = Paginator(scripts, 10) # Showing 10 scripts at a time.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # In explore and browse we pass the cat and typ dicts for our template loops
    # to loop over and display in the little red circle by each cat and typ just
    # how many script there are in those cat and typ, at that particular moment.
    cat = dict()
    for category in categories:
        cat[category]=len(Script.objects.filter(category=category))
    
    typ = dict()
    for i in types:
        typ[i]=len(Script.objects.filter(script_type=i))

    return render(request, 'astator/explore.html', {
        'cat':cat,
        'page_obj':page_obj,
        'typ':typ,
    })

# Browsing explore
@login_required
def browse(request, query):
    """Displaying all the scripts in particular selected category or all the scripts of selected type."""

    cat = dict()
    for category in categories:
        cat[category]=len(Script.objects.filter(category=category))

    typ = dict()
    for i in types:
        typ[i]=len(Script.objects.filter(script_type=i))

    # Checking what quiry user selected against all the cats
    if query in categories:
        if Script.objects.filter(category=query):
            scripts = Script.objects.filter(category=query).order_by('-created')
            paginator = Paginator(scripts, 10)
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
            return render(request, 'astator/browse.html', {
                "page_obj":page_obj,
                'cat':cat,
                'typ':typ,
                'query':query,
                'read_later':read_later
                })
        else:
            scripts = Script.objects.all().order_by('-created')
            paginator = Paginator(scripts, 10)
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
            return render(request, 'astator/explore.html', {
                'message':'At this moment, there are no scripts in this category. Try browsing for another category or browse all the scripts here. You can also create first script for this category, by goint to My Profile and clicking on Add New Script.',
                'cat':cat,
                'typ':typ,
                'page_obj':page_obj,
            })

    # If not a cat, maybe a typ
    elif query in types:
        if Script.objects.filter(script_type=query):
            scripts = Script.objects.filter(script_type=query).order_by('-created')
            paginator = Paginator(scripts, 10)
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
            return render(request, 'astator/browse.html', {
                "page_obj":page_obj,
                'cat':cat,
                'typ':typ,
                'query':query,
                })
        else:
            scripts = Script.objects.all().order_by('-created')
            paginator = Paginator(scripts, 10)
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
            return render(request, 'astator/explore.html', {
                'message':'At this moment, there are no scripts of this type. Try browsing for another type or browse all the scripts here. You can also create first script for this type, by goint to My Profile and clicking on Add New Script.',
                'cat':cat,
                'typ':typ,
                'page_obj':page_obj,
            })
    # User must've typed something in the URL bar that isn't cat nor typ
    else:
        raise Http404("Requested query does not exist")
  
# Script view
@login_required
def script(request, script_id):
    """Displaying props of each individual script, incl its title, cover, summary, ratings, comments and suggestions."""
    try:
        script = Script.objects.get(pk=script_id)
        read_later = ReadLater.objects.filter(user=request.user)
        comments = Comment.objects.filter(script=script)
        suggestions = Suggestion.objects.filter(script=script)
        ratings = Rating.objects.filter(script=script)
        ratings_num = len(ratings)
        readers = len(Reading.objects.filter(script=script))

        already_rated = False # Will be used to check if the script is already rated by current user
        added_to_rl = False # Will be used to check if the script is alredy in the ReadLater list of current user

        if read_later:
            for i in read_later:
                if script == i.script:
                    added_to_rl = True
        if ratings:
            for rating in ratings:
                if request.user == rating.user:
                    already_rated = True

        sl_avg = 0
        ch_avg = 0
        wr_avg = 0

        # Calculating each individual rating percentage (of total rating) to pass as our
        # width perc in script.html for bars. Also summing them up to show how many ratings
        # of each 5, 4, 3, 2 and 1 there were, to display in a chart.
        # This is not the most elegant approach and requires more writing and repeating oneself,
        # but the other approachs(with dicts, for example) would also require more writing
        # in template and loops bellow, and might also be overwhelming. Also, once written, 
        # this works as expected...
        sl_ratings = []
        sl_five = 0
        sl_five_perc = 0
        sl_four = 0
        sl_four_perc = 0
        sl_three = 0
        sl_three_perc = 0
        sl_two = 0
        sl_two_perc = 0
        sl_one = 0
        sl_one_perc = 0

        ch_ratings = []
        ch_five = 0
        ch_five_perc = 0
        ch_four = 0
        ch_four_perc = 0
        ch_three = 0
        ch_three_perc = 0
        ch_two = 0
        ch_two_perc = 0
        ch_one = 0
        ch_one_perc = 0

        wr_ratings = []
        wr_five = 0
        wr_five_perc = 0
        wr_four = 0
        wr_four_perc = 0
        wr_three = 0
        wr_three_perc = 0
        wr_two = 0
        wr_two_perc = 0
        wr_one = 0
        wr_one_perc = 0

        # Populating above lists of ratings and calculating avgs
        if ratings:
            for rating in ratings:
                sl_ratings.append(rating.storyline_rating)
                ch_ratings.append(rating.characters_rating)
                wr_ratings.append(rating.writing_rating)

            sl_avg = round(average_rating(sl_ratings), 1)
            ch_avg = round(average_rating(ch_ratings), 1)
            wr_avg = round(average_rating(wr_ratings), 1)
        # Checking how many of each rating for each rating_cat there are
        # and updating our vars above
        if ratings:
            for i in sl_ratings:
                if i == 5: sl_five += 1
                elif i == 4: sl_four += 1
                elif i == 3: sl_three += 1
                elif i == 2: sl_two += 1
                elif i == 1: sl_one += 1
            
            for i in ch_ratings:
                if i == 5: ch_five += 1
                elif i == 4: ch_four += 1
                elif i == 3: ch_three += 1
                elif i == 2: ch_two += 1
                elif i == 1: ch_one += 1

            for i in wr_ratings:
                if i == 5: wr_five += 1
                elif i == 4: wr_four += 1
                elif i == 3: wr_three += 1
                elif i == 2: wr_two += 1
                elif i == 1: wr_one += 1
        # Finally, calculating the percentage to pass as width of bars
        # and updating our vars above. Both percent and average_rating
        # are functions from our util.py
        if ratings:
            sl_five_perc = percent(sl_five, ratings_num)
            sl_four_perc = percent(sl_four, ratings_num)
            sl_three_perc = percent(sl_three, ratings_num)
            sl_two_perc = percent(sl_two, ratings_num)
            sl_one_perc = percent(sl_one, ratings_num)

            ch_five_perc = percent(ch_five, ratings_num)
            ch_four_perc = percent(ch_four, ratings_num)
            ch_three_perc = percent(ch_three, ratings_num)
            ch_two_perc = percent(ch_two, ratings_num)
            ch_one_perc = percent(ch_one, ratings_num)

            wr_five_perc = percent(wr_five, ratings_num)
            wr_four_perc = percent(wr_four, ratings_num)
            wr_three_perc = percent(wr_three, ratings_num)
            wr_two_perc = percent(wr_two, ratings_num)
            wr_one_perc = percent(wr_one, ratings_num)

        # Forms for comments and suggestions
        comment_form = CommentForm()
        suggestion_form = SuggestionForm()

        # If form was submitted
        if request.method == "POST":

            if "add_to_rl" in request.POST:
                # Creating new obj to RL model
                rl = ReadLater.objects.create(user=request.user, script=script)
                rl.save()
                return HttpResponseRedirect(reverse('script', args=(script_id,)))

            elif "remove_from_rl" in request.POST:
                # Deleting selected obj from RL model
                rl = ReadLater.objects.get(user=request.user, script=script)
                rl.delete()
                return HttpResponseRedirect(reverse('script', args=(script_id,)))

            elif "post_comment" in request.POST:
                # Posting comment
                form = CommentForm(request.POST)
                if form.is_valid():
                    comment = form.save(commit=False)
                    comment.user = request.user
                    comment.script = script
                    comment.save()
                    return HttpResponseRedirect(reverse('script', args=(script_id,)))

            elif "post_suggest" in request.POST:
                # Posting suggestion
                form = SuggestionForm(request.POST)
                if form.is_valid():
                    suggestion = form.save(commit=False)
                    suggestion.user = request.user
                    suggestion.script = script
                    suggestion.save()
                    return HttpResponseRedirect(reverse('script', args=(script_id,)))

            elif "post_rating" in request.POST:
                # Posting rating
                # Since we created this form by ourselves, with only HTML
                # we must check the form ourselves
                try:
                    # First we check that user truly submitted int's (which they will if they just 
                    # click on the stars and submit. But if they play with console and change the values,
                    # this try except will catch that).
                    sl_rating = int(request.POST['post_sl'])
                    ch_rating = int(request.POST['post_ch'])
                    wr_rating = int(request.POST['post_wr'])

                    # Second, we check that rating is truly between 1 and 5. Once again, by default it 
                    # will be, but in case that user changes the value to (still) int but that is lower 
                    # than 1 or higher than 5, this if will catch it. Check_rating is function from util.py
                    if check_rating(sl_rating) and check_rating(ch_rating) and check_rating(wr_rating):
                        new_rating = Rating.objects.create(user=request.user, script=script, storyline_rating=sl_rating, characters_rating=ch_rating, writing_rating=wr_rating)
                        new_rating.save()
                        return HttpResponseRedirect(reverse('script', args=(script_id,)))
                    
                    # If rating is under 1 or over 5.
                    else:
                        return render(request, "astator/script.html", {
                    "message":"Something went wront, please try again. Make sure that your rating is a number between 1 and 5.",
                    "script":script,
                    "added_to_rl":added_to_rl,
                    "comments":comments,
                    "suggestions":suggestions,
                    "comment_form":comment_form,
                    "suggestion_form":suggestion_form,
                    "num":ratings_num,
                    "readers":readers,
                    "already_rated":already_rated,
                    "sl_avg":sl_avg,
                    "ch_avg":ch_avg,
                    "wr_avg":wr_avg,
                    "sl_five":sl_five,
                    "sl_five_perc":sl_five_perc,
                    "sl_four":sl_four,
                    "sl_four_perc":sl_four_perc,
                    "sl_three":sl_three,
                    "sl_three_perc":sl_three_perc,
                    "sl_two":sl_two,
                    "sl_two_perc":sl_two_perc,
                    "sl_one":sl_one,
                    "sl_one_perc":sl_one_perc,
                    "ch_five":ch_five,
                    "ch_five_perc":ch_five_perc,
                    "ch_four":ch_four,
                    "ch_four_perc":ch_four_perc,
                    "ch_three":ch_three,
                    "ch_three_perc":ch_three_perc,
                    "ch_two":ch_two,
                    "ch_two_perc":ch_two_perc,
                    "ch_one":ch_one,
                    "ch_one_perc":ch_one_perc,
                    "wr_five":wr_five,
                    "wr_five_perc":wr_five_perc,
                    "wr_four":wr_four,
                    "wr_four_perc":wr_four_perc,
                    "wr_three":wr_three,
                    "wr_three_perc":wr_three_perc,
                    "wr_two":wr_two,
                    "wr_two_perc":wr_two_perc,
                    "wr_one":wr_one,
                    "wr_one_perc":wr_one_perc,
                })

                # If rating is not int
                except:
                    return render(request, "astator/script.html", {
                    "message":"Something went wront, please try again. Make sure that your rating is between 1 and 5.",
                    "script":script,
                    "added_to_rl":added_to_rl,
                    "comments":comments,
                    "suggestions":suggestions,
                    "comment_form":comment_form,
                    "suggestion_form":suggestion_form,
                    "num":ratings_num,
                    "readers":readers,
                    "already_rated":already_rated,
                    "sl_avg":sl_avg,
                    "ch_avg":ch_avg,
                    "wr_avg":wr_avg,
                    "sl_five":sl_five,
                    "sl_five_perc":sl_five_perc,
                    "sl_four":sl_four,
                    "sl_four_perc":sl_four_perc,
                    "sl_three":sl_three,
                    "sl_three_perc":sl_three_perc,
                    "sl_two":sl_two,
                    "sl_two_perc":sl_two_perc,
                    "sl_one":sl_one,
                    "sl_one_perc":sl_one_perc,
                    "ch_five":ch_five,
                    "ch_five_perc":ch_five_perc,
                    "ch_four":ch_four,
                    "ch_four_perc":ch_four_perc,
                    "ch_three":ch_three,
                    "ch_three_perc":ch_three_perc,
                    "ch_two":ch_two,
                    "ch_two_perc":ch_two_perc,
                    "ch_one":ch_one,
                    "ch_one_perc":ch_one_perc,
                    "wr_five":wr_five,
                    "wr_five_perc":wr_five_perc,
                    "wr_four":wr_four,
                    "wr_four_perc":wr_four_perc,
                    "wr_three":wr_three,
                    "wr_three_perc":wr_three_perc,
                    "wr_two":wr_two,
                    "wr_two_perc":wr_two_perc,
                    "wr_one":wr_one,
                    "wr_one_perc":wr_one_perc,
                })
        # Get
        else: 
            return render(request, "astator/script.html", {
            # Once again, not the most elegant approach..
            "script":script,
            "added_to_rl":added_to_rl,
            "comments":comments,
            "suggestions":suggestions,
            "comment_form":comment_form,
            "suggestion_form":suggestion_form,
            "num":ratings_num,
            "readers":readers,
            "already_rated":already_rated,
            "sl_avg":sl_avg,
            "ch_avg":ch_avg,
            "wr_avg":wr_avg,
            "sl_five":sl_five,
            "sl_five_perc":sl_five_perc,
            "sl_four":sl_four,
            "sl_four_perc":sl_four_perc,
            "sl_three":sl_three,
            "sl_three_perc":sl_three_perc,
            "sl_two":sl_two,
            "sl_two_perc":sl_two_perc,
            "sl_one":sl_one,
            "sl_one_perc":sl_one_perc,
            "ch_five":ch_five,
            "ch_five_perc":ch_five_perc,
            "ch_four":ch_four,
            "ch_four_perc":ch_four_perc,
            "ch_three":ch_three,
            "ch_three_perc":ch_three_perc,
            "ch_two":ch_two,
            "ch_two_perc":ch_two_perc,
            "ch_one":ch_one,
            "ch_one_perc":ch_one_perc,
            "wr_five":wr_five,
            "wr_five_perc":wr_five_perc,
            "wr_four":wr_four,
            "wr_four_perc":wr_four_perc,
            "wr_three":wr_three,
            "wr_three_perc":wr_three_perc,
            "wr_two":wr_two,
            "wr_two_perc":wr_two_perc,
            "wr_one":wr_one,
            "wr_one_perc":wr_one_perc,
        })

    except Script.DoesNotExist:
        raise Http404("Requested script does not exist")

# Read Script
@login_required
def read(request, script_id):
    """Default view for reading selected script"""
    try:
        script = Script.objects.get(pk=script_id)
        content = getText(script.upload)

        user = request.user
        readings = Reading.objects.filter(user=user)

        # When user click on read, aside from displaying the read view to him, 
        # we want to check if the user is already reading the book (to avoid 
        # duplicates in our DB), and if not, to create a new Reading obj, so that
        # user can later on see all the scripts they read in their myprofile page.
        # Naturally, user can't 'read' in this sense, his own script.
        already_reading = False

        if script.user != user:
            for reading in readings:
                if reading.script == script:
                    already_reading = True
            if not already_reading:
                read = Reading(user=user, script=script)
                read.save()

        return render(request, 'astator/read.html', {
            'script':script,
            'content':content,
        })
    except Script.DoesNotExist:
        raise Http404("Requested script does not exist")

# Finishing with reading a specified script
@csrf_exempt # Since we are not submitting any important data, we can create exempt for simplicity
@login_required
def finish_reading(request, script_id):
    """Removing selected script from reading now"""
    if request.method == "POST":
        try:
            script = Script.objects.get(pk=script_id)
            user = request.user
            data = json.loads(request.body)
            # Double-checking if remove is what we want
            if data.get('action') == 'finish':
                r = Reading.objects.get(user=user, script=script)
                r.delete()
                return JsonResponse({"message":"Removed from Reading successfully."}, status=201)
        except Script.DoesNotExist:
            return JsonResponse({"error": "Script not found"}, status=404)
    else:
        return HttpResponseRedirect(reverse('index'))

# Removing from ReadLater from My Profile page
@csrf_exempt # Since we are not submitting any important data, we can create exempt for simplicity
@login_required
def read_later(request, script_id):
    """Removing selected script from read_later"""
    if request.method == "POST":
        try:
            script = Script.objects.get(pk=script_id)
            user = request.user
            data = json.loads(request.body)
            # Double-checking if remove is what we want
            if data.get('action') == 'remove':
                rl = ReadLater.objects.get(user=user, script=script)
                rl.delete()
                return JsonResponse({"message":"Removed from Read Later successfully."}, status=201)
        except Script.DoesNotExist:
            return JsonResponse({"error": "Script not found"}, status=404)
    else:
        return HttpResponseRedirect(reverse('index'))

#Deleting scripts
@login_required
def delete(request, script_id):
    try:
        script = Script.objects.get(pk=script_id)
        user = request.user
        if user != script.user: # Double checking that only owner can delete their scripts
            raise Http404("Requested page is not available.") 
        script.delete()
        scripts = Script.objects.filter(user=user)
        if len(scripts) == 0:
            user.author = False # Removing from authors if no more scripts
            user.save()
        return HttpResponseRedirect(reverse('myprofile'))
    except:
        raise Http404("Requested script does not exist")

# Adding note
@csrf_exempt # Since we are not submitting any important data, we can create exempt for simplicity
@login_required
def add_note(request, script_id):
    """Adding a new note via JS fetch"""
    if request.method == "POST":
        try:
            script = Script.objects.get(pk=script_id)
            user = request.user

            data = json.loads(request.body)
            if data.get('note') is not None:
                note = data['note']
                source = f'{script.user.name}, "{script.title}"' # Formating source
                new_note = Note.objects.create(user=user, note=note, source=source)
                new_note.save()
                return JsonResponse({"message": "Note saved successfully."}, status=201)

        except Script.DoesNotExist:
            return JsonResponse({"error": "Script not found"}, status=404)

    else:
        return HttpResponseRedirect(reverse('index'))

# Deleting note
@csrf_exempt # Since we are not submitting any important data, we can create exempt for simplicity
@login_required
def delete_note(request, note_id):
    """Deleting selected note"""
    if request.method == "POST":
        try:
            note = Note.objects.get(pk=note_id)
            data = json.loads(request.body)
            if data.get('action') == 'delete':
                note.delete()
                return JsonResponse({"message": "Note deleted successfully."}, status=201)

        except Note.DoesNotExist:
            return JsonResponse({"error": "Note not found"}, status=404)

    else:
        return HttpResponseRedirect(reverse('index'))


# Logged-in user's profile
@login_required
def myprofile(request):
    user = request.user
    # All in reverse chono order
    scripts = Script.objects.filter(user=user).order_by("-created")
    readings = Reading.objects.filter(user=user).order_by("-created")
    read_later = ReadLater.objects.filter(user=user).order_by("-created")
    favorites = Favorite.objects.filter(user=user).order_by("-created")
    notes = Note.objects.filter(user=user).order_by("-created")

    return render(request, "astator/myprofile.html", {
        "user":user, 
        "scripts":scripts,
        "readings":readings,
        "read_later":read_later,
        "favorites":favorites,
        "notes":notes,
        })

# Edit profile
@login_required
def edit_profile(request):
    """Letting users edit their profile informations."""
    if request.method == "POST":
        form = EditProfileForm(request.POST, request.FILES or None, instance=request.user)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('myprofile'))
        else:
            return render(request, 'astator/edit_profile.html', {
                'message':'Something went wrong, please try again. Make sure you follow the instructions bellow each of the fields.',
                'form':form,
            })
    # GET
    else:
        form = EditProfileForm(instance=request.user)
        return render(request, 'astator/edit_profile.html', {'form':form,})

# Change password
@login_required
def change_password(request):
    """Letting users change their passwords"""
    if request.method == "POST":
        form = ChangePasswordForm(data=request.POST, user=request.user)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user) # For not logging user out after change of pw.
            return HttpResponseRedirect(reverse('myprofile'))
        else:
            return render(request, 'astator/change_password.html', {
                'message':'Something went wrong, please try again. Make sure you type in the correct old password, and that your new password meets the specified requirements.',
                'form':form,
            })
    # GET
    else:
        form = ChangePasswordForm(user=request.user)
        return render(request, 'astator/change_password.html', {'form':form,})

# Adding new script
@login_required
def create(request):
    """Creating (adding) new script. """
    # POST
    if request.method == "POST":
        form = CreateScriptForm(request.POST, request.FILES or None)
        if form.is_valid():
            script = form.save(commit=False)
            script.user = request.user
            script.save()
            user = request.user
            user.author = True # Making sure to mark this user as an author.
            user.save()
            return HttpResponseRedirect(reverse('script', args=(script.id,)))
        else:
            return render(request, "astator/create.html", 
                {"form":form, 
                "message":"Something went wrong. Please try filling out the empty fields again. Make sure that your script is.docx text file."
            })
    # GET
    else:
        form = CreateScriptForm()
        return render(request, "astator/create.html", {"form":form})


# Terms and conditions page
def terms(request):
    return render(request, 'astator/terms.html')

# DEMO Blog pages - open to everybody - even non-users For SEO purposes, each 
# blog page would be new html file. Since this is just a demo, real blog pages 
# won't be built, but instead 3 demo pages will be shown as a demo.
# For the future, one might imagine a full fledged separate blog app, in which 
# superusers (admins) would have a button to create new blog, and just enter 
# markdown content (for example), which would then be stored in a separate db, 
# cashed and served to users, similarly to what we did in wiki.. or something similar.
def blog(request):
    """Displaying demo main blog page..."""
    return render(request, 'blog/main.html')

# Also, for SEO one would incorporate blog page title in URL, but this is just
# for show..
def blog_posts(request, post_id):
    """Displaying separate demo blog pages"""
    if post_id == 1:
        return render(request, 'blog/utilizingastator.html')
    elif post_id == 2:
        return render(request, 'blog/selfvstrad.html')
    elif post_id == 3:
        return render(request, 'blog/habbits.html')
    else:
        raise Http404("Requested page does not exist")

def login_view(request):
    # We want to make sure that only NOT logged-in users can visit this form,
    # else logged-in users will be redirected to index.
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('index'))

    # POST
    if request.method == "POST":

        # Authenticate user
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # If there is a user with that username and password
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        # If not
        else:
            return render(request, "astator/login.html", {
                "message": "Invalid username and/or password."
            })
    # GET
    else:
        return render(request, "astator/login.html")

def logout_view(request):
    # Loggin user out - index will auto redirect to login again
    logout(request)
    return HttpResponseRedirect(reverse("index"))

def register(request):
    """Registering new users"""
    # We want to make sure that only NOT logged-in users can visit this form,
    # else logged-in users will be redirected to index.
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('index'))

    # POST
    if request.method == "POST":
        # In addition to our form we must make sure to get the files too, if photo is uploaded
        # Since photo is optional, or None is needed for those cases.
        form = RegisterForm(request.POST, request.FILES or None)
        if form.is_valid():
            user = form.save()
            login(request, user) # Log in right away
            return HttpResponseRedirect(reverse('index'))
        else:
            return render(request, "astator/register.html", 
            {"form":form, 
            "message":"Something went wrong. Please try filling out the empty fields again. Make sure that your passwords match and that they satisfy the requirements listed bellow."
            })
    # GET
    else:
        form = RegisterForm()
        return render(request, "astator/register.html", {"form":form})
