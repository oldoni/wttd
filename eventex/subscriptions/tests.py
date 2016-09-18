from django.test import TestCase
from django.core import mail
from eventex.subscriptions.forms import SubscriptionForm


class SubscribeTest(TestCase):

    def setUp(self):
        self.resp = self.client.get('/inscricao/')

    def test_get(self):
        """"get /inscricao/ must have code status 200"""
        self.assertEqual(200,  self.resp.status_code)

    def test_template(self):
        """Must use subscriptions/subscription_form.html"""
        self.assertTemplateUsed(self.resp, 'subscriptions/subscription_form.html')

    def test_html(self):
        """"Html must have input tag"""
        self.assertContains(self.resp, '<form')
        self.assertContains(self.resp, '<input', 6)
        self.assertContains(self.resp, 'type="text"', 3)
        self.assertContains(self.resp, 'type="email"')
        self.assertContains(self.resp, 'type="submit"')

    def test_csrf(self):
        """HTML must contain csrf"""
        self.assertContains(self.resp, 'csrfmiddlewaretoken')

    def test_has_form(self):
        """"Context must have subscription form """
        form = self.resp.context['form']
        self.assertIsInstance(form, SubscriptionForm)

    def test_form_must_have_4_fields(self):
        form = self.resp.context['form']

        self.assertSequenceEqual(['name', 'cpf', 'email', 'phone'], list(form.fields))



class SubscribeTestPost(TestCase):

    def setUp(self):
        self.data = dict(name='marcelo', cpf='11111111111',
                         email='marcelo@oldevel.com', phone='11 2222 3333')
        self.resp = self.client.post('/inscricao/', self.data)

    def test_post(self):
        """valid post should redirect to /inscricao/"""
        self.assertEqual(302, self.resp.status_code)

    def test_send_subscribe_email(self):
        """"send email to confirm the subscription"""
        self.assertEqual(1, len(mail.outbox))

    def test_subscription_mail_data(self):
        email = mail.outbox[0]
        expect = 'Confirmação de Inscrição'
        self.assertEqual(expect, email.subject)
        expect = 'contato@eventx.com.br'
        self.assertEqual(expect, email.from_email)
        expect = ['contato@eventx.com.br', 'marcelo@oldevel.com']
        self.assertEqual(expect, email.to)

    def test_subscription_mail_body(self):
        email = mail.outbox[0]
        self.assertIn('marcelo', email.body)
        self.assertIn('CPF', email.body)
        self.assertIn('Telefone', email.body)


class SubscriptionInvalidPost(TestCase):

    def setUp(self):
        self.resp = self.client.post('/inscricao/', {})

    def test_post(self):
        """invalid post """
        self.assertEqual(200, self.resp.status_code)

    def test_template(self):
        self.assertTemplateUsed(self.resp, 'subscriptions/subscription_form.html')

    def test_has_form(self):
        form = self.resp.context['form']
        self.assertIsInstance(form, SubscriptionForm)

    def test_form_has_erros(self):
        form = self.resp.context['form']
        self.assertTrue(form.errors)


class SubscriptionSuccessMessage(TestCase):
    def test_success_message(self):
        data = dict(name='marcelo', cpf='11111111111',
                    email='marcelo@oldevel.com', phone='11 2222 3333')
        resp = self.client.post('/inscricao/', data, follow=True)

        self.assertContains(resp, 'Inscrição realizada com Sucesso')

