from __future__ import absolute_import  # Allow explicit relative imports
from django.shortcuts import render, HttpResponse, render_to_response, RequestContext


# Testing - Just a blank page
def datavis(request):

    return render(request,
                  "temp.html",
                  )
