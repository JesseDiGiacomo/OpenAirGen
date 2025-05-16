from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.theming import ThemeManager
from kivy.uix.screenmanager import Screen
from kivy.clock import Clock
from datetime import datetime
import os
import shutil
import subprocess
from kivy.utils import platform
import traceback

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
        try:
            self.root.ids.status_label.text = "[2/3] Processando dados..."
            resultado = subprocess.run(["python", "run_all.py"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            log = resultado.stdout + "\n" + resultado.stderr
            self.root.ids.log_area.text = log

            hoje = datetime.utcnow()
            nome = f"espaco_aereo_{hoje.strftime('%Y-%m-%d')}.txt"
            origem = os.path.join("data", f"{hoje.year}", f"{str(hoje.month).zfill(2)}", nome)

            if self.destino_custom and os.path.exists(origem):
                destino = os.path.join(self.destino_custom, nome)
                os.makedirs(os.path.dirname(destino), exist_ok=True)
                shutil.copyfile(origem, destino)
                self.root.ids.log_area.text += f"\n[OK] Arquivo salvo em: {destino}\n"

            self.root.ids.status_label.text = "[3/3] Concluído!"

        except Exception as e:
            self.log_erro(e)
            self.root.ids.status_label.text = "Erro ao executar."

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

if __name__ == '__main__':
    try:
        OpenAirApp().run()
    except Exception as e:
        with open("error_log.txt", "w") as f:
            f.write(traceback.format_exc())