import random

# function to check for duplicates in the list of queried apps
def checkQueryDuplicate(applist):
    return len(applist) != len(set(applist))

# function to create set of common genres
def createCommonSet(genreset1, genreset2, genreset3):
    # initialize set of common genres + display string
    commonset = set()
    showgenres = ""

    # fallback boolean to display indicator if true
    fallback = False

    # if no genres are found in any of the sets *at all* for some reason, this acts as a fallback:
    if not genreset1 and not genreset2 and not genreset3:
        # this pick is entirely arbitrary, but as long as there's something there it's okay
        commonset.add("Indie")
        fallback = True
    else:
        # set operations to create a common set out of the genres listed
        # union of intersections of genre set pairs
        commonset = (genreset1 & genreset2) | (genreset1 & genreset3) | (genreset2 & genreset3)

        # if no matching elements are found, just grab a random element from any of the sets
        if not commonset:
            # create a list out of the union of all genre sets
            fallbacklist = list(genreset1 | genreset2 | genreset3)
            commonset.add(random.choice(fallbacklist))
            fallback = True

    # string to display in the page itself
    showgenres = ", ".join(commonset)

    return commonset, showgenres, fallback

# function to conduct linear search on apps based on common genres
def getSuggestedApps(commonset, sortedapps, applist):
    # list for matching apps
    appmatches = []

    # exclude app_ids of games already listed in user query
    excluded = {app.app_id for app in applist}

    # main loop for adding apps to the list:
    for app in sortedapps:
        # if app_id is found in exclusion list, pass over it
        if app.app_id in excluded:
            continue

        # create sets out of the genre string attributes
        tempgenres = set(app.genres.split(",")) if app.genres else set()
        
        # if set of common genres is a subset of this app's genres, add to the list
        if commonset <= tempgenres:
            appmatches.append(app)
        
        # if it reaches 10 results, break the loop prematurely
        if len(appmatches) == 10:
            break

    # add spaces for display purposes
    for app in appmatches:
        app.genres = app.genres.replace(",", ", ")
        app.developers = app.developers.replace(",", ", ")
        app.publishers = app.publishers.replace(",", ", ")

    # return matching apps
    return appmatches

# functions to perform mergesort
def mergeSort(a, attr):
    if len(a) == 1:
        return a

    splitOne = a[:len(a)//2]
    splitTwo = a[len(a)//2:]

    splitOne = mergeSort(splitOne, attr)
    splitTwo = mergeSort(splitTwo, attr)

    return merge(splitOne, splitTwo, attr)

def merge(a, b, attr):
    c = []

    while len(a) > 0 and len(b) > 0:
        # using getattr() to retrieve the value of the chosen attribute to sort by for comparison
        # otherwise, nothing else changed with the code
        if getattr(a[0], attr) > getattr(b[0], attr):
            c.append(b[0])
            b.pop(0)

        else:
            c.append(a[0])
            a.pop(0)

    while len(a) > 0:
        c.append(a[0])
        a.pop(0)

    while len(b) > 0:
        c.append(b[0])
        b.pop(0)

    return c