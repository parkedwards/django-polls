# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from .models import Question
from django.http import HttpResponse, Http404
from django.template import loader

from django.shortcuts import render  # render also returns an HttpResponse object

# Create your views here.


# INDEX CONTROLLER #
def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    # template = loader.get_template('polls/index.html')
    # context = {
    #     'latest_question_list': latest_question_list
    # }
    # return HttpResponse(template.render(context, request))

    # data to pass in render
    context = {'latest_question_list': latest_question_list}
    return render(request, 'polls/index.html', context)
    # This is a condensed version of the commented code above


# DETAIL CONTROLLER #
def detail(request, question_id):
    # response = "You're looking at the question %s."
    # return HttpResponse(response % question_id)
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise Http404('Question does not exist')
    return render(request, 'polls/detail.html', {'question': question})
    # Adding some error handling



def results(request, question_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)


def vote(request, question_id):
    response = "You're voting on question %s."
    return HttpResponse(response % question_id)
