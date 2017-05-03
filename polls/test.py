""" Unit tests for Polls app """


#  Good Testing Practics ======================================
#  ============================================================
# a separate TestClass for each model or view
# a separate test method for each set of conditions you want to test
# test method names that describe their function

import datetime
from django.utils import timezone
from django.test import TestCase
from django.urls import reverse

from .models import Question

class QuestionMethodTests(TestCase):
    """ Testing the 'was_published_recently' method on Question class """
    def test_was_published_recently_with_future_question(self):
        """ should return false for questions whose pub_date is in the future """
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        """ should return false for questions whose pub_date is older than 1 day """
        time = timezone.now() - datetime.timedelta(days=30)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        """ should return True for questions whose pub_date is within the last day """
        time = timezone.now() - datetime.timedelta(hours=1)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)




# Helper function to create new Question instances
def create_question(question_text, days):
    """ function that creates a question with the given text"""
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)

class QuestionViewTests(TestCase):
    def test_index_view_with_no_question(self):
        """ if no question exists => appropriate message should be displayed """
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_index_view_with_past_question(self):
        """ qs with a pub_date in the past should be displayed """
        create_question(question_text='What time is it?', days=-30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: What time is it?>']
        )

    def test_index_view_with_future_question(self):
        """ q's in the future should not be displayed """
        create_question('What is for lunch?', days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_index_view_with_future_and_past_question(self):
        """ q's in past should show, q's in future should not """
        create_question(question_text='Past question?', days=-30)
        create_question(question_text='Future question?', days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question?>']
        )

    def test_index_view_with_two_past_questions(self):
        """ both past q's should show up """
        create_question(question_text='First past question', days=-25)
        create_question(question_text='Second past question', days=-35)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: First past question>', '<Question: Second past question>']
        )



class QuestionIndexDetailTests(TestCase):
    def test_detail_view_with_future_question(self):
        """ detail view for future question should return 404 not found """
        future_question = create_question(question_text='Future question', days=28)
        url = reverse('polls:detail', args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_detail_view_with_past_question(self):
        """ detail view with past question should return with display text """
        past_question = create_question(question_text='Past question', days=-28)
        url = reverse('polls:detail', args=(past_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, past_question.question_text)


class QuestionResultsTests(TestCase):
    def test_results_view_with_future_question(self):
        """ results view for future question should return 404 not found """
        future_question = create_question(question_text='Future question', days=28)
        url = reverse('polls:results', args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_results_view_with_past_question(self):
        """ results view for past question should display text """
        past_question = create_question(question_text='Past question', days=-28)
        url = reverse('polls:results', args=(past_question.id,))
        response=self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, past_question.question_text)