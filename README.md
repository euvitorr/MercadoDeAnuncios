# MercadoDeAnuncios

Esse é um projeto privado de um gerenciador de anuncios para o Mercado Livre

Para executar o projeto é preciso ter o python v3.7 com pip instalado, com as seguintes bibliotecas:
pip install django
pip install virtualenv
pip install python-decouple
pip install dj-database-url
pip install django-storages
pip install django-storages
pip install django-widget_tweaks
pip install django-modeladmin-reorder
pip install django-embed_video
pip install django_extensions
pip install django-allauth
pip install django-debug_toolbar
pip install boto3
pip install pillow

Conta com informações que permitem acessar via api os dados do mercado livre com base em alterações cadastradas no bando SQLite, podendo ser cadastradas por um superusuário no admin do Django.

acesse a pasta do virtualenv e ative-a

o seguinte comando vai ajudar:
source venv/bin/activate

Após acesse a pasta interna do projeto, nela execute o comando para aplicar as migrations e gerar o banco de dados automaticamente:
python manage.py makemigrations (gera um arquivo com base nas models que é responsável por criar as tabelas e modificações de forma versionada)
python manage.py migrate (aplica no SQLite)

Após é necessário que você crie um Super Usuário, para acessar a página administrativa do Django
python manate.py createsuperuser

Por fim é só executar o projeto e realizar o login com o cadastro informado, também é possível realizar o cadastro de um usuário sem privilégios, para isso utilize o seguinte comando:
python manage.py runserver

Ele vai indicar o link para acesso, abra ele no navegador e terá acesso ao site para realizar os devidos cadastros, por meio de login e cadastro.

