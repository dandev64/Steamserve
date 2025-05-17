from django.shortcuts import render, redirect, get_object_or_404
from .models import Game
from .utils import checkQueryDuplicate, createCommonSet, getSuggestedApps, mergeSort
from django.http import JsonResponse
from django.contrib import messages

# Create your views here.
def home(request):
    # total count of model instances in the database
    total = "{:,}".format(Game.objects.count())
    return render(request, 'home.html', {'total': total})

def results(request):
    if (request.method=="POST"):
        # get the fields from the home form
        # key information: app_id & sort by attribute
        first = request.POST.get("app1")
        second = request.POST.get("app2")
        third = request.POST.get("app3")
        sortattr = request.POST.get("sortattr")
        sortby = request.POST.get("sortby")

        try:
            # all it actually expects is the app_id, so we strip the inputs down to just that, then convert to int
            first = int(first.partition(":")[0])
            second = int(second.partition(":")[0])
            third = int(third.partition(":")[0])

            # getting the model instances by app_id, then creating a list out of then for display
            app1 = get_object_or_404(Game, app_id=first)
            app2 = get_object_or_404(Game, app_id=second)
            app3 = get_object_or_404(Game, app_id=third)
            applist = [app1, app2, app3]

        except:
            # basic error handling in case user input is invalid
            messages.error(request, "Invalid input. Please use the search buttons and do not tamper with the autofill.")
            return redirect('home')
        
        # simple function to check whether there are any duplicates in the query
        hasDupes = checkQueryDuplicate(applist)

        # if there are, redirect back w/ error message
        if hasDupes == True:
            messages.error(request, "Invalid input. Please do not include duplicates in your query.")
            return redirect('home')

        # adding spaces after commas for display in the page
        for app in applist:
            app.developers = app.developers.replace(",", ", ")
            app.publishers = app.publishers.replace(",", ", ")
            app.genres = app.genres.replace(",", ", ")

        # create sets out of the genres of each model instance
        genreset1 = set(app1.genres.split(", ")) if app1.genres else set()
        genreset2 = set(app2.genres.split(", ")) if app2.genres else set()
        genreset3 = set(app3.genres.split(", ")) if app3.genres else set()

        # call function in utils.py to create a set of common genres + display string
        commonset, showgenres, fallback = createCommonSet(genreset1, genreset2, genreset3)

        # call function in utils.py to use mergesort algorithm for sorting all the apps:
        allapps = Game.objects.all()
        sortedapps = mergeSort(allapps, sortattr)

        # if descending selected, reverse the sorted list
        if sortby == "descending":
            sortedapps.reverse()

        # call function in utils.py to iterate through the sorted list
        appsuggestions = getSuggestedApps(commonset, sortedapps, applist)
        querytotal = len(appsuggestions)

        return render(request, 'results.html',
                      {'applist': applist,
                       'sortattr': sortattr,
                       'sortby': sortby,
                       'showgenres': showgenres,
                       'appsuggestions': appsuggestions,
                       'querytotal': querytotal,
                       'fallback': fallback})
    else:
        return redirect('home')

def search(request):
    # get query and convert it to lowercase for searching
    query = request.GET.get('query', '').lower()

    # list of matching results
    results = []

    # get all apps from the database
    applist = Game.objects.all()

    # perform linear search to find apps matching query:
    for app in applist:
        if query in app.name.lower():
            # for each matching result, display these attributes:
            results.append({
                'app_id': app.app_id,
                'name': app.name,
                'release_date': app.release_date
            })
            
        # limit results to only 20
        if len(results) == 20:
            break

    return JsonResponse({'results': results})

def about(request):
    return render(request, 'about.html')