from pickle import FALSE, TRUE
from django.shortcuts import redirect, render, resolve_url
from django.http import HttpResponse
from django.contrib.sites.shortcuts import get_current_site
import json
import requests
from .models import ValidML
from datetime import datetime  
from datetime import timedelta
from django.utils import timezone
import pytz


def integration(request):
    url = ''
    payload = {'a': 'b', 'c': 'd'}
    result = requests.post(url, params=payload)
    print(result.url)
    print(result)
    return HttpResponse(result)


def ValidateMercado(request):
        local_tz = pytz.timezone('America/Sao_Paulo')
        date=TRUE
        NewCode=FALSE
        if len(ValidML.objects.filter(company=request.user.company))>0:
            NewCode=ValidML.objects.filter(company=request.user.company)[0]
            date = datetime.now().replace(tzinfo=pytz.utc).astimezone(local_tz)>NewCode.expires_in.replace(tzinfo=pytz.utc).astimezone(local_tz)
        if date:
            if request.GET.get('code') is None:
                return redirect('https://auth.mercadolivre.com.br/authorization?response_type=code&client_id=845563285221624&redirect_uri=http://localhost:8000/integration/validate/')
            else:
                if len(ValidML.objects.filter(company=request.user.company))>0:
                    code = request.GET.get('code')
                    NewCode.code = code
                    client_id='845563285221624'
                    NewCode.client_id = client_id
                    NewCode.client_secret = 'FPlhRLB73eFJepOPqCs44JHBUFwHhezV'
                    client_secret = 'FPlhRLB73eFJepOPqCs44JHBUFwHhezV'
                    url = 'https://api.mercadolibre.com/oauth/token'
                    payload = {'accept': 'application/json', 'content-type': 'application/x-www-form-urlencoded', 'grant_type': 'authorization_code',
                                'client_id': client_id, 'client_secret': client_secret, 'code': code, 'redirect_uri': 'http://localhost:8000/integration/validate/'}
                    result = requests.post(url, params=payload)
                    data = result.json()
                    if 'error' in data:
                        return redirect('https://auth.mercadolivre.com.br/authorization?response_type=code&client_id=845563285221624&redirect_uri=http://localhost:8000/integration/validate/')
                    else:
                        NewCode.access_token = data['access_token']
                        NewCode.expires_in = datetime.now() + timedelta(seconds=data['expires_in'])
                        NewCode.save()
                else:
                    code = request.GET.get('code')
                    client_id='845563285221624'
                    client_secret = 'FPlhRLB73eFJepOPqCs44JHBUFwHhezV'
                    url = 'https://api.mercadolibre.com/oauth/token'
                    payload = {'accept': 'application/json', 'content-type': 'application/x-www-form-urlencoded', 'grant_type': 'authorization_code',
                                'client_id': client_id, 'client_secret': client_secret, 'code': code, 'redirect_uri': 'http://localhost:8000/integration/validate/'}
                    result = requests.post(url, params=payload)
                    data = result.json()
                    if 'error' in data:
                        return redirect('https://auth.mercadolivre.com.br/authorization?response_type=code&client_id=845563285221624&redirect_uri=http://localhost:8000/integration/validate/')
                    else:
                        NewCode = ValidML(company=request.user.company,code=code,client_id=client_id,client_secret=client_secret,access_token=data['access_token'],expires_in=datetime.now() + timedelta(seconds=data['expires_in']))
                        NewCode.save()
            return redirect('http://localhost:8000/products/')
                    
                    # payload = {'Authorization': 'Bearer ' + result.json()['access_token']}
                    # user = requests.get('https://api.mercadolibre.com/users/me')
                    # stock_value = requests.post(
                    #      ' https://api.mercadolibre.com/users/'+user.json()['id']+'/items/', params=payload)
                    
                    # return redirect("home")
        else:
#             user = requests.get('https://api.mercadolibre.com/sites/MLB/search?nickname=RIOSVITOR22')
#             #stock_value = requests.get('https://api.mercadolibre.com/users/'+str(user.json()['seller']['id'])+'/items/search?status=active', params=payload)
#             # return redirect("home")          
#             # 
#             body = {
# 	"variations": [{
# 		"id": 174893652050,
# 		"available_quantity": 10
# 	}]
# } 
          
            # put = requests.put('https://api.mercadolibre.com/items/MLB2732437899',data=json.dumps(body), headers={'Authorization': 'Bearer {}'.format(NewCode.access_token),'Accept': 'application/json', 'Content-Type': 'application/json'})
            return redirect('http://localhost:8000/products/')