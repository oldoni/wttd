from django.contrib import messages
from django.core import mail
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.template.loader import render_to_string

from eventex.subscriptions.forms import SubscriptionForm


def subscribe(request):
    if request.method == 'GET':
        context = {'form': SubscriptionForm()}
        return render(request, 'subscriptions/subscription_form.html', context)
    elif request.method == 'POST':
        form = SubscriptionForm(request.POST)
        if form.is_valid():
            body = render_to_string('subscriptions/subscription_email.txt', form.cleaned_data)
            mail.send_mail('Confirmação de Inscrição', body,
                           'contato@eventx.com.br',  ['contato@eventx.com.br', form.cleaned_data['email']])

            messages.success(request, 'Inscrição realizada com Sucesso')

            return HttpResponseRedirect('/inscricao/')

        else:
            return render(request, 'subscriptions/subscription_form.html', {'form': form})
