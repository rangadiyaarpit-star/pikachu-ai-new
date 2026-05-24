from django.http import JsonResponse
from django.shortcuts import render

from assistant.pikachu import process_command


def home(request):

    return render(request, "index.html")


def handle_command(request):

    command = request.GET.get("command")

    if command:

        response = process_command(command)


        # IF RESPONSE EMPTY

        if response is None:

            response = "✅ Command Executed"


        return JsonResponse({

            "response": response

        })


    return JsonResponse({

        "response": "No command received"

    })