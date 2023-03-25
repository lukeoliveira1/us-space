from django import forms

class LoginForms(forms.Form):
    nome_login=forms.CharField(
        label='Nome de Login', 
        required=True, 
        max_length=100,
        widget=forms.TextInput(
            attrs={
                #para estilização
                'class': 'form-control',
                #tipo de estilização do input
                'placeholder': 'Ex.: user',
            }
        )
    )
    senha=forms.CharField(
        label='Senha', 
        required=True, 
        max_length=70,
        # widget - para deixar input do formato password
        # widget = forms.PasswordInput()
        widget=forms.PasswordInput(
            attrs={
                #para estilização
                'class': 'form-control',
                'placeholder': 'Digite a sua senha',
            }
        ),
    )

class CadastroForms(forms.Form):
    nome_cadastro=forms.CharField(
        label='Nome de Cadastro', 
        required=True, 
        max_length=100,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Ex.: user',
            }
        )
    )
    email=forms.EmailField(
        label='Email',
        required=True,
        max_length=100,
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Ex.: user@email.com',
            }
        )
    )
    senha_1=forms.CharField(
        label='Senha', 
        required=True, 
        max_length=70,
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Digite a sua senha',
            }
        ),
    )
    senha_2=forms.CharField(
        label='Confirme a sua senha', 
        required=True, 
        max_length=70,
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Digite a sua senha novamente',
            }
        ),
    )

    # validação nome sem espaço
    def clean_nome_cadastro(self):
        nome = self.cleaned_data.get('nome_cadastro') # pegando o nome cadastrado

        if nome:
            nome = nome.strip() # retirando os espaços do nome
            if ' ' in nome:
                # validação do próprio form
                raise forms.ValidationError('Espaços não são permitidos nesse campo')
            else:
                return nome

    # validação senhas iguais
    def clean_senha_2(self):
        senha_1 = self.cleaned_data.get('senha_1') # pegando o senha 1
        senha_2 = self.cleaned_data.get('senha_2') # pegando o senha 2

        if senha_1 and senha_2: # validando que ambas existem
            if senha_1 != senha_2:
                # validação do próprio form
                raise forms.ValidationError('Senhas não são iguais')
            else:
                return senha_2