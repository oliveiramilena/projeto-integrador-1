# Projeto Integrador I Univesp - 2026
## Plataforma de Simulados do Vestibular UNIVESP

### Instruções:

Clonar o repositório
> git clone https://github.com/oliveiramilena/projeto-integrador-1.git

Criar e entrar no ambiente virtual 
> python3 -m venv venv
> source venv/bin/activate

Instalar as dependências do projeto
> pip install -r requirements.txt

Criar um arquivo .env com as variáveis de ambiente, seguindo o .env.example
> cp .env.example .env

Iniciar a aplicação
> flask run --debug --host=0.0.0.0

#### Obs.: O argumento --host=0.0.0.0 permite que a aplicação seja acessivel por outros dispositivos da rede, útil para o acesso em celulares.