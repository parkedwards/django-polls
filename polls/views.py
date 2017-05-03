# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from .models import Question, Choice
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse

# some django shortcuts ================================
from django.shortcuts import render, get_object_or_404
# render also returns an HttpResponse object
# get_object_or_404() = a shortcut for fetch + error handling (also has for list / object)


# ========== Think of these as Express Middleware Functions ============
# ========== ie (req, res) => { } =================

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



# RESULTS controller #
def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})



#  VOTE controller - post request #
#  request.POST is the post request object; contains k/v pairs with sent data
def vote(request, question_id):
    # question_id gets passed in through routing, extracted via regex
    question = get_object_or_404(Question, pk=question_id)
    try:
        # Remember that the 'choice' value in the post request is the ID
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/details.html', {
            'question': question,
            'error_message': 'You did not select a choice'
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # HttpResponseRedirect takes one arg -> the redirect URL
        # Should generally return a Redirect after a POST request
        # so you don't duplicate requests
        # reverse() method points towards the route you want to redirect to
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
