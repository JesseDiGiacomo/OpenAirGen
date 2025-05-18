from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen
from kivy.clock import Clock
from datetime import datetime
import os
import shutil
import subprocess
from kivy.utils import platform
import traceback
import threading  # Importe o módulo threading

if platform != "android":
    from tkinter import filedialog
else:
    from android.permissions import request_permissions, Permission
    from plyer import filechooser

KV = """
Screen:
    MDBoxLayout:
        orientation: "vertical"
        padding: dp(20)
        spacing: dp(10)

        MDLabel:
            text: "OpenAir Generator"
            halign: "center"
            font_style: "H5"

        MDTextButton:
            text: "Selecionar destino do arquivo"
            pos_hint: {"center_x": 0.5}
            on_release: app.escolher_destino()
            theme_text_color: "Custom"
            text_color: app.theme_cls.primary_light

        MDRaisedButton:
            id: gerar_btn
            text: "Gerar OpenAir"
            pos_hint: {"center_x": 0.5}
            on_release: app.gerar_openair()
            disabled: True

        MDLabel:
            id: status_label
            text: "Status: aguardando..."
            halign: "center"
            theme_text_color: "Secondary"

        ScrollView:
            MDLabel:
                halign: "center"
                id: log_area
                text: ""
                padding: 10, 10
                size_hint_y: None
                height: self.texture_size[1]
                text_size: self.width, None
"""

class MainScreen(Screen):
    pass

class OpenAirApp(MDApp):
    destino_custom = ""

    def build(self):
        self.title = "OpenAir Generator"
        if platform == "android":
            request_permissions([Permission.WRITE_EXTERNAL_STORAGE, Permission.READ_EXTERNAL_STORAGE])
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "BlueGray"
        return Builder.load_string(KV)

    def gerar_openair(self):
        try:
            self.root.ids.status_label.text = "[1/3] Executando run_all.py..."
            self.root.ids.log_area.text = ""
            Clock.schedule_once(self._executar_script, 0.5)
        except Exception as e:
            self.log_erro(e)

    def _executar_script(self, dt):
        threading.Thread(target=self._processar_e_salvar).start()

    def _processar_e_salvar(self):
        try:
            Clock.schedule_once(lambda dt: self.atualizar_status("[2/3] Processando dados..."), 0)
            resultado = subprocess.run(["python", "run_all.py"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            log = resultado.stdout + "\n" + resultado.stderr
            Clock.schedule_once(lambda dt: self.atualizar_log(log), 0)

            hoje = datetime.utcnow()
            nome_arquivo = f"espaco_aereo_{hoje.strftime('%Y-%m-%d')}.txt"

            if self.destino_custom:
                caminho_completo = os.path.join(self.destino_custom, nome_arquivo)
                zonas = self.get_zonas()  # Obter as zonas processadas
                if zonas:
                    from openair_writer import gerar_openair_a_partir_de_zonas
                    gerar_openair_a_partir_de_zonas(zonas, caminho_completo)
                    Clock.schedule_once(lambda dt: self.atualizar_log(f"\n[OK] Arquivo salvo em: {caminho_completo}\n"), 0)
                else:
                    Clock.schedule_once(lambda dt: self.atualizar_log("\n[ERRO] Nenhuma zona extraída.\n"), 0)
            else:
                Clock.schedule_once(lambda dt: self.atualizar_log("\n[ERRO] Destino não selecionado.\n"), 0)

            Clock.schedule_once(lambda dt: self.atualizar_status("[3/3] Concluído!"), 0)

        except Exception as e:
            self.log_erro(e)
            Clock.schedule_once(lambda dt: self.atualizar_status("Erro ao executar."), 0)

    def escolher_destino(self):
        if platform == "android":
            filechooser.choose_dir(on_selection=self._set_destino)
        else:
            pasta = filedialog.askdirectory()
            self._set_destino([pasta] if pasta else [])

    def _set_destino(self, selecao):
        if selecao:
            self.destino_custom = selecao[0]
            self.root.ids.log_area.text += f"\nDestino escolhido: {self.destino_custom}\n"
            self.root.ids.gerar_btn.disabled = False

    def log_erro(self, e):
        with open("error_log.txt", "w") as log:
            log.write("Erro:\n")
            log.write(str(e) + "\n\n")
            log.write(traceback.format_exc())

    def atualizar_status(self, texto):
        self.root.ids.status_label.text = texto

    def atualizar_log(self, texto):
        self.root.ids.log_area.text = texto

    def get_zonas(self):
        from aixm_parser import processar_xmls
        return processar_xmls()

if __name__ == '__main__':
    try:
        OpenAirApp().run()
    except Exception as e:
        with open("error_log.txt", "w") as f:
            f.write(traceback.format_exc())