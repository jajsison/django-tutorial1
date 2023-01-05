from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import TemplateView
from django.utils import timezone

from .models import Choice, Question


class IndexView(TemplateView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        return Question.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:5]

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)

        context['latest_question_list'] = self.get_queryset()
        return context


class DetailView(TemplateView):
    model = Question
    template_name = 'polls/detail.html'

   # def get_queryset(self):
    #    """
    #   Excludes any questions that aren't published yet.
    #  """
    # import pdb
    # pdb.set_trace()
    # return Question.objects.get(pub_date__lte=timezone.now())

    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        # import pdb
        # pdb.set_trace()
        context['question'] = Question.objects.get(id=self.kwargs['pk'])

        return context


class ResultsView(TemplateView):
    model = Question
    template_name = 'polls/results.html'


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
