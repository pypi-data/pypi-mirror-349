import django.urls
import django.utils
import django.utils.timezone
import django.views
import django.views.generic
from .models import Question, Choice
import django.shortcuts
import django.http
import django.db.models


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics  # For simpler common views
from .serializers import QuestionSerializer, ChoiceSerializer


class IndexView(django.views.generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.filter(
            pub_date__lte=django.utils.timezone.now()
        ).order_by('-pub_date')[:5]


class DetailView(django.views.generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

    def get_queryset(self):
        """excludes any questions that aren't published yet."""
        return Question.objects.filter(pub_date__lte=django.utils.timezone.now())


class ResultsView(django.views.generic.DetailView):
    model = Question
    template_name = 'polls/results.html'


def vote(request, question_id):
    question: Question = django.shortcuts.get_object_or_404(Question, pk=question_id)
    try:
        selected_choice: Choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return django.shortcuts.render(
            request=request,
            template_name='polls/detail.html',
            context={
                'question': question,
                'error_message': "You didn't select a choice.",
            },
        )
    else:
        selected_choice.votes = django.db.models.F('votes') + 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after sucessfully dealing with POST data.
        # This prevents data from being posted twice if a use hits the Back button.
        return django.http.HttpResponseRedirect(
            django.urls.reverse('polls:results', args=(question_id,))
        )


class QuestionListAPIView(generics.ListCreateAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer


class QuestionDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer


class ChoiceListCreateAPIView(generics.ListCreateAPIView):
    queryset = Choice.objects.all()
    serializer_class = ChoiceSerializer


class ChoiceDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Choice.objects.all()
    serializer_class = ChoiceSerializer
