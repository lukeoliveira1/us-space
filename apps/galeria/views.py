from django.shortcuts import render, get_object_or_404, redirect

from apps.galeria.models import Fotografia
from apps.galeria.forms import FotografiaForms

from django.contrib import messages

def index(request):
    # se o usuário não estiver autenticado
    if not request.user.is_authenticated:
        messages.error(request, 'Usuário não logado')
        return redirect('login')

    fotografias = Fotografia.objects.order_by("data_fotografia").filter(publicada=True)
    return render(request, 'galeria/index.html', {"cards": fotografias})

def imagem(request, foto_id):
    fotografia = get_object_or_404(Fotografia, pk=foto_id)
    return render(request, 'galeria/imagem.html', {"fotografia": fotografia})

def buscar(request):
    # se o usuário não estiver autenticado
    if not request.user.is_authenticated:
        messages.error(request, 'Usuário não logado')
        return redirect('login')

    fotografias = Fotografia.objects.order_by("data_fotografia").filter(publicada=True)

    if "buscar" in request.GET:
    # conferindo se existe "buscar" na url
        
        # pegando o nome "buscar", referência ao name "buscar" no form do _menu.html
        nome_a_buscar = request.GET['buscar']
        
        if nome_a_buscar:
        # buscando com "autocomplete", se tiver algo parecido já aceita
            fotografias = fotografias.filter(nome__icontains=nome_a_buscar)

    return render(request, "galeria/index.html", {"cards": fotografias})

def nova_imagem(request):
    # só pode cadastrar uma nova imagem se estiver logado
    if not request.user.is_authenticated:
        messages.error(request, 'Usuário não logado')
        return redirect('login')

    form = FotografiaForms # pegando o form

    # se o form for preenchido, pegar as informações
    if request.method == 'POST':

        # criando um novo form e jogando as informações do outro pra esse
        # POST pega strings, FILES pega imagens/arquivos
        form = FotografiaForms(request.POST, request.FILES) 

        if form.is_valid():
            form.save() # salvando no banco, logo salva a imagem
            messages.success(request, 'Nova fotografia cadastrada!')
            return redirect('index')

    return render(request, 'galeria/nova_imagem.html', {'form': form})

def editar_imagem(request, foto_id):
    # pegando objeto fotografia com base no id
    fotografia = Fotografia.objects.get(id=foto_id)

    # instance, pra colocar no form as informações que já tem dentro do objeto 
    form = FotografiaForms(instance=fotografia)

    if request.method == 'POST':

        # criar um novo form com as novas informações
        # instance, o que não for alterado, fica como já tinha no objeto fotografia
        form = FotografiaForms(request.POST, request.FILES, instance=fotografia)

        if form.is_valid():
            form.save() # salvando no banco
            messages.success(request, 'Fotografia editada com sucesso!')
            return redirect('index')

    return render(request, 'galeria/editar_imagem.html', {'form': form, 'foto_id': foto_id})

def deletar_imagem(request, foto_id):
    # pegando objeto fotografia com base no id
    fotografia = Fotografia.objects.get(id=foto_id)

    fotografia.delete() # deletando
    messages.success(request, 'Deleção feita com sucesso!')
    return redirect('index')

def filtro(request, categoria):
    # filtrando os objetos pela True em publicada + categoria 
    fotografias = Fotografia.objects.order_by("data_fotografia").filter(publicada=True, categoria=categoria)

    return render(request, 'galeria/index.html', {"cards": fotografias})