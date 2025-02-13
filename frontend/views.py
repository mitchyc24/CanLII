import requests

from django.shortcuts import render
from django.conf import settings

def home(request):
    results = []

    # Fetch jurisdictions (always fetch, regardless of request method)
    jurisdiction_url = f'https://api.canlii.org/v1/caseBrowse/en/?api_key={settings.CANLII_API_KEY}'
    jurisdiction_response = requests.get(jurisdiction_url)
    jurisdictions = jurisdiction_response.json().get('caseDatabases',)

    # Fetch databases (always fetch, regardless of request method)
    database_url = f'https://api.canlii.org/v1/legislationBrowse/en/?api_key={settings.CANLII_API_KEY}'
    database_response = requests.get(database_url)
    databases = database_response.json().get('legislationDatabases',)

    if request.method == 'POST':
        keyword = request.POST.get('keyword')
        jurisdiction = request.POST.get('jurisdiction')
        database = request.POST.get('database')

        if keyword:
            # Search across all jurisdictions and databases if none are selected
            if not jurisdiction and not database:
                # Combine case law and legislation databases
                all_databases = jurisdictions + databases
                for db in all_databases:
                    url = f'https://api.canlii.org/v1/caseBrowse/en/{db["databaseId"]}/?api_key={settings.CANLII_API_KEY}&fullText={keyword}'
                    response = requests.get(url)
                    if response.status_code == 200:
                        # Combine results (assuming 'cases' is the key for results in the response)
                        results = results + response.json().get('cases',)

            else:
                # Search specific jurisdiction or database
                if jurisdiction:
                    url = f'https://api.canlii.org/v1/caseBrowse/en/{jurisdiction}/?api_key={settings.CANLII_API_KEY}&fullText={keyword}'
                    response = requests.get(url)
                    if response.status_code == 200:
                        results = response.json().get('cases',)

                if database:
                    url = f'https://api.canlii.org/v1/legislationBrowse/en/{database}/?api_key={settings.CANLII_API_KEY}&fullText={keyword}'
                    response = requests.get(url)
                    if response.status_code == 200:
                        results = response.json().get('legislations',)

    return render(request, 'home.html', {
        'results': results,
        'jurisdictions': jurisdictions,
        'databases': databases,
    })