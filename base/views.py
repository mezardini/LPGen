from mistralai.models.chat_completion import ChatMessage
from mistralai.client import MistralClient
from django.shortcuts import render
import environ
env = environ.Env()
environ.Env.read_env()

# Create your views here.


def generate(request):

    if request.method == 'POST':
        details = request.POST['details']
        target_audience = request.POST['audience']

        api_key = env('MistralAPIKEY')
        model = "mistral-tiny"

        client = MistralClient(api_key=api_key)

        CTC = 'CTA-Button-Copy'

        result = {}

        headline_message = [
            ChatMessage(
                role="user",
                content=f"Generate a headline for a business named that {details} and is targeted at {target_audience}, not more than 7 words"
            )
        ]

        subheadline_message = [
            ChatMessage(
                role="user",
                content=f"Generate a subheadline for the landing page of a business that {details} and is targeted at {target_audience}, not more than 15 words. No emoji!!!"
            )
        ]

        cta_message = [
            ChatMessage(
                role="user",
                content=f"Generate a CTA button copy for the landing page of a business that {details} and is targeted at {target_audience}. 4 words maximum, An example is 'Start your free trial'. No emoji!!!"
            )
        ]

        features_message = [
            ChatMessage(
                role="user",
                content=f"Generate a features section for the landing page of a business that {details} and is targeted at {target_audience}, start with a tagline for the section, a subheadline and then 3 features with 3 lines of explanation. No emoji!!!"
            )
        ]

        benefits_message = [
            ChatMessage(
                role="user",
                content=f"Generate a benefits section for the landing page of a business that {details} and is targeted at {target_audience}, start with a tagline for the section, a subheadline and then 3 benefit with 2 lines of explanation. No emoji!!!"
            )
        ]

        # offer_message = [
        #     ChatMessage(
        #         role="user",
        #         content=f"Generate a superb offer breakdown pitch for the landing page of a business that {details} and is targeted at {target_audience}. No emoji!!!"
        #     )
        # ]

        # urgency_message = [
        #     ChatMessage(
        #         role="user",
        #         content=f"Generate a message that creates urgency to visitors for the landing page of a business that {details} and is targeted at {target_audience}. No emoji!!!"
        #     )
        # ]

        faqs_message = [
            ChatMessage(
                role="user",
                content=f"Generate a FAQs section for the landing page of a business that {details} and is targeted at {target_audience}, 3 questions and answers. No emoji!!"
            )
        ]

        sections = {
            'headline': headline_message,
            'subheadline': subheadline_message,
            'cta': cta_message,
            'features': features_message,
            'benefits': benefits_message,
            # 'offer': offer_message,
            # 'urgency': urgency_message,
            'faqs': faqs_message,

        }

        result = {}

        for key, message in sections.items():
            chat_response = client.chat(
                model=model,
                messages=message,
            )

            result[key] = chat_response.choices[0].message.content

        context = result  # directly use the result dictionary as the context

        return render(request, 'action.html', context)

    return render(request, 'action.html')


def index(request):

    return render(request, 'home.html')