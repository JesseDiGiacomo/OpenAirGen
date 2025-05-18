[app]

# (string) Título do aplicativo
title = OpenAir Generator

# (string) Nome do pacote (deve ser único)
package.name = org.kivy.openairgenerator

# (string) Domínio reverso do pacote
package.domain = org.kivy.

# (string) Diretório de origem do projeto
source.dir = .

# (list) Lista de requisitos (bibliotecas) do Python
reqs = kivy, kivymd, requests, beautifulsoup4, plyer

# (int) Versão da API do Android para compilar
android.api = 27

# (int) Versão mínima da API do Android suportada
android.minapi = 21

# (list) Permissões do Android
android.permissions = WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE, INTERNET

# (str) Orientação do aplicativo (portrait, landscape, all)
orientation = portrait

# (bool) Se deve copiar o logcat para o dispositivo
logcat_filters = *:V

# (int) Nível de logcat (V, D, I, W, E, F, S)
log_level = 2

# (list) Arquivos a serem incluídos no pacote
#source.include_exts = py,png,jpg,kv,atlas

# (list) Diretórios a serem excluídos do pacote
#source.exclude_dirs = tests, bin, venv

# (list) Extensões de arquivos a serem excluídas do pacote
#source.exclude_exts = spec

# (bool) Se deve usar o modo depuração
# (para obter logs mais detalhados e permitir a depuração remota)
debug = True

# (string) Versão do aplicativo
version = 1.0.0

# (str) Regex para extrair a versão (se não usar 'version')
#version.regex = __version__ = '(.*)'

# (str) Arquivo para procurar a regex da versão
#version.filename = %(source.dir)s/__init__.py

#
# opções específicas do android
#

# (str) Arquivo .so a ser incluído no APK
#android.so_libs =

# (list) Arquivos de recursos do Android a serem incluídos
#android.res_files =

# (list) Arquivos de ativos do Android a serem incluídos
#android.assets =

# (str) Caminho para um ícone personalizado
#android.icon =

# (str) Caminho para uma tela de apresentação personalizada
#android.presplash =

# (str) Caminho para o arquivo services.jar
#android.services =

# (bool) Se deve incluir o suporte a WebGL
#android.use_webgl = False

# (bool) Se deve usar o modo de tela cheia
#android.fullscreen = 0

# (str) Modo de entrada (ou 'window'). O padrão é 'auto'
#android.input_mode = auto

# (str) Cor de fundo da janela (formato #RRGGBB)
#android.window_bgcolor = #ffffff

# (int) Modo de exibição da janela
#android.window_display = 0

# (list) Opções de metadados do Android
# (chave=valor)
#android.meta_data =

# (list) Opções de serviços do Android
# (chave=valor)
#android.services_meta_data =

# (list) Opções de permissões do Android
#android.permissions =

# (list) Opções de recursos do Android
#android.uses_sdk =
#android.uses_permission =
#android.uses_feature =

# (str) Modo de instalação (internal, external)
#android.install_location = auto

# (bool) Se deve compilar para armeabi-v7a
android.archs = armeabi-v7a, arm64-v8a

# (int) Nível de otimização (-O0, -O1, -O2, -O3)
android.optimization_level = 0

#
# Opções de assinatura (release)
#

# (bool) Se deve assinar o APK
# (requer keystore)
#android.release = True

# (str) Caminho para o keystore
#android.keystore = %(source.dir)s/debug.keystore

# (str) Alias da chave
#android.keyalias = androiddebugkey

# (str) Senha do keystore
#android.keystore.pass = android

# (str) Senha da chave
#android.key.pass = android