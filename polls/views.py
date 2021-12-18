from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from polls.models import Question, Choice
from django.urls import reverse
from django.views import generic

# generic View
class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        return Question.objects.order_by('-pub_date')[:5]

class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

class AllResultsView(generic.ListView):
    template_name = 'polls/all_result.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        return Question.objects.order_by('-pub_date')[:5]

# 함수형 설문앱
# def index(request):
#     latest_question_list = Question.objects.order_by('-pub_date')[:5]
#     # output = ', '.join([q.question_text for q in latest_question_list])
#     # return HttpResponse(output)
#     context = {'latest_question_list': latest_question_list}
#     return  render(request,  'polls/index.html', context)

# def detail(request, question_id):
#     # return HttpResponse("You're looking at question %s" %question_id)
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, 'polls/detail.html', {'question':question})
#
# def results(request, question_id):
#     # reponse = HttpResponse("You're looking at the results of question %s" %question_id)
#     # return reponse
#     question = get_object_or_404(Question, pk=question_id)
#     return  render(request, 'polls/results.html', {'question':question})

def vote(request, question_id):
    # return  HttpResponse("You're voting on question %s" %question_id)
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except(KeyError, Choice.DoesNotExist):
        return render(request,'polls/detail.html', {'question':question, 'error_message':"You did't select a choice",})
    else:
        selected_choice.votes += 1
        selected_choice.save()

        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))