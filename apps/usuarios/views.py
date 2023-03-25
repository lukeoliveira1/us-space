from django.shortcuts import render, redirect

from apps.usuarios.forms import LoginForms, CadastroForms

from django.contrib.auth.models import User

from django.contrib import auth

from django.contrib import messages

def login(request):
    form = LoginForms()

    if request.method == 'POST':
        form = LoginForms(request.POST)

        if form.is_valid():
            # pegando valores do form
            nome = form['nome_login'].value()
            senha = form['senha'].value()

        # método que autentica um usuário, pode retornar True ou None
        usuario = auth.authenticate(
            request,
            username=nome,
            password=senha
        )
        if usuario is not None:
            auth.login(request, usuario) # faz login
            messages.success(request, f'{nome} logado com sucesso!')
            return redirect('index')
        else:
            messages.error(request, 'Erro ao efetuar login')
            return redirect('login')

    return render(request, 'usuarios/login.html', {'form': form})

def cadastro(request):
    form = CadastroForms()

    if request.method == 'POST':
        #recebendo os dados passados em um novo form
        form = CadastroForms(request.POST)

        # validando formulário
        if form.is_valid():
            nome=form['nome_cadastro'].value() #mesmo nome utilizado no form.py
            email=form['email'].value()
            senha=form['senha_1'].value() #puxando info do form

            # verificando se o usuário já existe
            if User.objects.filter(username=nome).exists():
                messages.error(request, 'Usuário já existente')
                return redirect('cadastro') # redireciona pra página de cadastro

            # criando usuário
            usuario = User.objects.create_user(
                username=nome,
                email=email,
                password=senha
            )
            usuario.save() # salvando

            messages.success(request, 'Cadastro efetuado com sucesso!')
            return redirect('login')

    return render(request, 'usuarios/cadastro.html', {'form': form})

def logout(request):
    # fazendo logout
    auth.logout(request)
    messages.success(request, 'Logout efetuado com sucesso!')
    return redirect('login')