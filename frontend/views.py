import requests
from django.shortcuts import render
from django.conf import settings


def home(request):
    results = None  # Initialize results to None
    if request.method == 'POST':
        keyword = request.POST.get('keyword')
        jurisdiction = request.POST.get('jurisdiction')
        database = request.POST.get('database')

        # Construct API URL (example for case law)
        if jurisdiction:
            url = f'https://api.canlii.org/v1/caseBrowse/en/{jurisdiction}/?api_key={settings.CANLII_API_KEY}'
            if keyword:
                url += f'&fullText={keyword}'
            response = requests.get(url)
            results = response.json()
            #... handle other databases and filters

    return render(request, 'home.html', {'results': results})