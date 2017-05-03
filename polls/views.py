# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from .models import Question
from django.http import HttpResponse, Http404
from django.template import loader

# some django shortcuts ================================
from django.shortcuts import render, get_object_or_404
# render also returns an HttpResponse object
# get_object_or_404() = a shortcut for fetch + error handling (also has for list / object)


# INDEX controller #
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


# DETAIL controller #
def detail(request, question_id):
    # Python's version of ${variable} => %s + % + value
    # response = "You're looking at the question %s."
    # return HttpResponse(response % question_id)

    # a Try / Catch for Errors
    # try:
    #     question = Question.objects.get(pk=question_id)
    # except Question.DoesNotExist:
    #     raise Http404('Question does not exist')

    # Using the error fetch shortcut
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})



def results(request, question_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)


def vote(request, question_id):
    response = "You're voting on question %s."
    return HttpResponse(response % question_id)
