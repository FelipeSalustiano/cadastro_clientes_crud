import datetime
import pandas as pd
import json
import os
import customtkinter as ctk
from tkinter import messagebox, ttk

# --- Configurações e Variáveis Globais ---
ARQUIVO_USUARIOS = 'usuarios.json'
ARQUIVO_LOCAIS = 'locais.json'

usuarios = {}
locais = {}

ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD = 'admin'

current_user_data = None # Para guardar o username do usuário logado

# --- Funções de Carregamento e Salvamento de Dados ---
def carregar_dados():
    """Carrega os dados dos arquivos JSON."""
    global usuarios, locais
    if os.path.exists(ARQUIVO_USUARIOS):
        try:
            with open(ARQUIVO_USUARIOS, 'r', encoding='utf-8') as f:
                usuarios = json.load(f)
        except json.JSONDecodeError:
            messagebox.showerror("Erro de Leitura", "Erro ao ler o arquivo de usuários. O arquivo pode estar corrompido.")
            usuarios = {}
    if os.path.exists(ARQUIVO_LOCAIS):
        try:
            with open(ARQUIVO_LOCAIS, 'r', encoding='utf-8') as f:
                locais = json.load(f)
        except json.JSONDecodeError:
            messagebox.showerror("Erro de Leitura", "Erro ao ler o arquivo de locais. O arquivo pode estar corrompido.")
            locais = {}

def salvar_dados():
    """Salva os dados nos arquivos JSON."""
    with open(ARQUIVO_USUARIOS, 'w', encoding='utf-8') as f:
        json.dump(usuarios, f, indent=4, ensure_ascii=False)
    with open(ARQUIVO_LOCAIS, 'w', encoding='utf-8') as f:
        json.dump(locais, f, indent=4, ensure_ascii=False)

# --- Lógica de Negócios ---
def verificar_aptidao_usuario(idade, renda):
    """Verifica se um usuário é apto com base na idade e renda."""
    try:
        return int(idade) >= 18 and float(renda) <= 2000
    except ValueError:
        return False # Caso a idade ou renda não sejam números válidos

def calcular_capacidade_producao(andares, area):
    """Calcula a capacidade de produção de um local."""
    try:
        return int(andares) * float(area) * 2
    except ValueError:
        return 0 # Caso andares ou área não sejam números válidos

# --- Classes da Interface Gráfica ---

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Sistema de Fazendas Verticais")
        self.geometry("800x600")
        ctk.set_appearance_mode("System")  # Modes: "System" (default), "Dark", "Light"
        ctk.set_default_color_theme("blue")  # Themes: "blue", "green", "dark-blue"

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        carregar_dados() # Carrega os dados ao iniciar a aplicação

        self.create_widgets()
        self.show_login_frame()

    def create_widgets(self):
        # --- Frame de Login ---
        self.login_frame = ctk.CTkFrame(self)
        self.login_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        self.login_frame.grid_rowconfigure((0,1,2,3,4,5), weight=1)
        self.login_frame.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(self.login_frame, text="Bem-vindo!", font=("Roboto", 24)).grid(row=0, column=0, pady=20)
        ctk.CTkLabel(self.login_frame, text="Login", font=("Roboto", 18)).grid(row=1, column=0, pady=10)

        self.login_username_entry = ctk.CTkEntry(self.login_frame, placeholder_text="Usuário", width=200)
        self.login_username_entry.grid(row=2, column=0, pady=5)
        self.login_password_entry = ctk.CTkEntry(self.login_frame, placeholder_text="Senha", show="*", width=200)
        self.login_password_entry.grid(row=3, column=0, pady=5)

        ctk.CTkButton(self.login_frame, text="Entrar", command=self.attempt_login).grid(row=4, column=0, pady=10)
        ctk.CTkButton(self.login_frame, text="Não tem conta? Registre-se", command=self.show_register_frame, fg_color="gray").grid(row=5, column=0, pady=5)

        # --- Frame de Registro ---
        self.register_frame = ctk.CTkFrame(self)
        self.register_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        self.register_frame.grid_rowconfigure((0,1,2,3,4), weight=1)
        self.register_frame.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(self.register_frame, text="Registro de Usuário Comum", font=("Roboto", 18)).grid(row=0, column=0, pady=20)

        self.reg_username_entry = ctk.CTkEntry(self.register_frame, placeholder_text="Escolha um nome de usuário", width=250)
        self.reg_username_entry.grid(row=1, column=0, pady=5)
        self.reg_password_entry = ctk.CTkEntry(self.register_frame, placeholder_text="Escolha uma senha", show="*", width=250)
        self.reg_password_entry.grid(row=2, column=0, pady=5)
        self.reg_confirm_password_entry = ctk.CTkEntry(self.register_frame, placeholder_text="Confirme a senha", show="*", width=250)
        self.reg_confirm_password_entry.grid(row=3, column=0, pady=5)

        ctk.CTkButton(self.register_frame, text="Registrar", command=self.register_user).grid(row=4, column=0, pady=10)
        ctk.CTkButton(self.register_frame, text="Voltar ao Login", command=self.show_login_frame, fg_color="gray").grid(row=5, column=0, pady=5)

        # --- Frame do Menu do Administrador ---
        self.admin_menu_frame = ctk.CTkFrame(self)
        self.admin_menu_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        self.admin_menu_frame.grid_rowconfigure((0,1,2,3,4,5,6), weight=1)
        self.admin_menu_frame.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(self.admin_menu_frame, text="Menu do Administrador", font=("Roboto", 24)).grid(row=0, column=0, pady=20)
        ctk.CTkButton(self.admin_menu_frame, text="Gerenciar Usuários", command=self.show_manage_users_admin_frame).grid(row=1, column=0, pady=10, ipadx=20, ipady=10)
        ctk.CTkButton(self.admin_menu_frame, text="Gerenciar Locais", command=self.show_manage_locais_frame).grid(row=2, column=0, pady=10, ipadx=20, ipady=10)
        ctk.CTkButton(self.admin_menu_frame, text="Sair", command=self.logout, fg_color="red").grid(row=3, column=0, pady=20)

        # --- Frame de Gerenciamento de Usuários (Admin) ---
        self.manage_users_admin_frame = ctk.CTkFrame(self)
        self.manage_users_admin_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        self.manage_users_admin_frame.grid_rowconfigure((0,1,2,3,4,5,6,7), weight=1)
        self.manage_users_admin_frame.grid_columnconfigure(0, weight=1)
        self.manage_users_admin_frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(self.manage_users_admin_frame, text="Gerenciar Usuários (Admin)", font=("Roboto", 20)).grid(row=0, column=0, columnspan=2, pady=10)

        # Formulário para adicionar/atualizar
        form_frame = ctk.CTkFrame(self.manage_users_admin_frame)
        form_frame.grid(row=1, column=0, rowspan=6, sticky="nsew", padx=10, pady=10)
        form_frame.grid_columnconfigure(0, weight=1)
        form_frame.grid_columnconfigure(1, weight=2)

        ctk.CTkLabel(form_frame, text="Usuário (login):").grid(row=0, column=0, sticky="w", padx=5, pady=2)
        self.admin_user_username_entry = ctk.CTkEntry(form_frame)
        self.admin_user_username_entry.grid(row=0, column=1, sticky="ew", padx=5, pady=2)

        ctk.CTkLabel(form_frame, text="Senha:").grid(row=1, column=0, sticky="w", padx=5, pady=2)
        self.admin_user_password_entry = ctk.CTkEntry(form_frame)
        self.admin_user_password_entry.grid(row=1, column=1, sticky="ew", padx=5, pady=2)

        ctk.CTkLabel(form_frame, text="Nome Completo:").grid(row=2, column=0, sticky="w", padx=5, pady=2)
        self.admin_user_name_entry = ctk.CTkEntry(form_frame)
        self.admin_user_name_entry.grid(row=2, column=1, sticky="ew", padx=5, pady=2)

        ctk.CTkLabel(form_frame, text="Idade:").grid(row=3, column=0, sticky="w", padx=5, pady=2)
        self.admin_user_idade_entry = ctk.CTkEntry(form_frame)
        self.admin_user_idade_entry.grid(row=3, column=1, sticky="ew", padx=5, pady=2)

        ctk.CTkLabel(form_frame, text="Endereço:").grid(row=4, column=0, sticky="w", padx=5, pady=2)
        self.admin_user_endereco_entry = ctk.CTkEntry(form_frame)
        self.admin_user_endereco_entry.grid(row=4, column=1, sticky="ew", padx=5, pady=2)

        ctk.CTkLabel(form_frame, text="Pessoas na Casa:").grid(row=5, column=0, sticky="w", padx=5, pady=2)
        self.admin_user_pessoas_casa_entry = ctk.CTkEntry(form_frame)
        self.admin_user_pessoas_casa_entry.grid(row=5, column=1, sticky="ew", padx=5, pady=2)

        ctk.CTkLabel(form_frame, text="Renda Familiar:").grid(row=6, column=0, sticky="w", padx=5, pady=2)
        self.admin_user_renda_entry = ctk.CTkEntry(form_frame)
        self.admin_user_renda_entry.grid(row=6, column=1, sticky="ew", padx=5, pady=2)

        ctk.CTkLabel(form_frame, text="Profissão:").grid(row=7, column=0, sticky="w", padx=5, pady=2)
        self.admin_user_profissao_entry = ctk.CTkEntry(form_frame)
        self.admin_user_profissao_entry.grid(row=7, column=1, sticky="ew", padx=5, pady=2)

        button_frame = ctk.CTkFrame(form_frame)
        button_frame.grid(row=8, column=0, columnspan=2, pady=10)
        ctk.CTkButton(button_frame, text="Adicionar", command=self.add_user_admin_gui).pack(side="left", padx=5)
        ctk.CTkButton(button_frame, text="Atualizar", command=self.update_user_admin_gui).pack(side="left", padx=5)
        ctk.CTkButton(button_frame, text="Limpar Campos", command=self.clear_user_form).pack(side="left", padx=5)

        # Tabela de Usuários
        self.user_tree = ttk.Treeview(self.manage_users_admin_frame, columns=("Usuario", "Nome", "Idade", "Endereco", "Apto"), show="headings")
        self.user_tree.grid(row=1, column=1, rowspan=5, sticky="nsew", padx=10, pady=10)
        self.user_tree.bind("<<TreeviewSelect>>", self.load_selected_user_to_form)

        for col in self.user_tree["columns"]:
            self.user_tree.heading(col, text=col)
            self.user_tree.column(col, width=80, anchor="center")

        # Configurar scrollbar
        vsb = ttk.Scrollbar(self.manage_users_admin_frame, orient="vertical", command=self.user_tree.yview)
        vsb.grid(row=1, column=2, rowspan=5, sticky="ns", padx=0, pady=10)
        self.user_tree.configure(yscrollcommand=vsb.set)

        button_row_frame = ctk.CTkFrame(self.manage_users_admin_frame)
        button_row_frame.grid(row=6, column=1, pady=10)
        ctk.CTkButton(button_row_frame, text="Remover Selecionado", command=self.remove_user_admin_gui, fg_color="red").pack(side="left", padx=5)
        ctk.CTkButton(self.manage_users_admin_frame, text="Voltar", command=self.show_admin_menu_frame).grid(row=7, column=0, columnspan=2, pady=10)

        # --- Frame de Gerenciamento de Locais (Admin) ---
        self.manage_locais_frame = ctk.CTkFrame(self)
        self.manage_locais_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        self.manage_locais_frame.grid_rowconfigure((0,1,2,3,4,5,6), weight=1)
        self.manage_locais_frame.grid_columnconfigure(0, weight=1)
        self.manage_locais_frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(self.manage_locais_frame, text="Gerenciar Locais (Admin)", font=("Roboto", 20)).grid(row=0, column=0, columnspan=2, pady=10)

        # Formulário para adicionar/atualizar locais
        local_form_frame = ctk.CTkFrame(self.manage_locais_frame)
        local_form_frame.grid(row=1, column=0, rowspan=5, sticky="nsew", padx=10, pady=10)
        local_form_frame.grid_columnconfigure(0, weight=1)
        local_form_frame.grid_columnconfigure(1, weight=2)

        ctk.CTkLabel(local_form_frame, text="Nome do Local:").grid(row=0, column=0, sticky="w", padx=5, pady=2)
        self.local_nome_entry = ctk.CTkEntry(local_form_frame)
        self.local_nome_entry.grid(row=0, column=1, sticky="ew", padx=5, pady=2)

        ctk.CTkLabel(local_form_frame, text="Endereço:").grid(row=1, column=0, sticky="w", padx=5, pady=2)
        self.local_endereco_entry = ctk.CTkEntry(local_form_frame)
        self.local_endereco_entry.grid(row=1, column=1, sticky="ew", padx=5, pady=2)

        ctk.CTkLabel(local_form_frame, text="Responsável:").grid(row=2, column=0, sticky="w", padx=5, pady=2)
        self.local_responsavel_entry = ctk.CTkEntry(local_form_frame)
        self.local_responsavel_entry.grid(row=2, column=1, sticky="ew", padx=5, pady=2)

        ctk.CTkLabel(local_form_frame, text="Contato:").grid(row=3, column=0, sticky="w", padx=5, pady=2)
        self.local_contato_entry = ctk.CTkEntry(local_form_frame)
        self.local_contato_entry.grid(row=3, column=1, sticky="ew", padx=5, pady=2)

        ctk.CTkLabel(local_form_frame, text="Andares:").grid(row=4, column=0, sticky="w", padx=5, pady=2)
        self.local_andares_entry = ctk.CTkEntry(local_form_frame)
        self.local_andares_entry.grid(row=4, column=1, sticky="ew", padx=5, pady=2)

        ctk.CTkLabel(local_form_frame, text="Área (m²):").grid(row=5, column=0, sticky="w", padx=5, pady=2)
        self.local_area_entry = ctk.CTkEntry(local_form_frame)
        self.local_area_entry.grid(row=5, column=1, sticky="ew", padx=5, pady=2)

        local_button_frame = ctk.CTkFrame(local_form_frame)
        local_button_frame.grid(row=6, column=0, columnspan=2, pady=10)
        ctk.CTkButton(local_button_frame, text="Adicionar Local", command=self.add_local_gui).pack(side="left", padx=5)
        ctk.CTkButton(local_button_frame, text="Atualizar Local", command=self.update_local_gui).pack(side="left", padx=5)
        ctk.CTkButton(local_button_frame, text="Limpar Campos", command=self.clear_local_form).pack(side="left", padx=5)

        # Tabela de Locais
        self.local_tree = ttk.Treeview(self.manage_locais_frame, columns=("Nome do Local", "Endereço", "Responsável", "Capacidade", "Apto"), show="headings")
        self.local_tree.grid(row=1, column=1, rowspan=4, sticky="nsew", padx=10, pady=10)
        self.local_tree.bind("<<TreeviewSelect>>", self.load_selected_local_to_form)

        for col in self.local_tree["columns"]:
            self.local_tree.heading(col, text=col)
            self.local_tree.column(col, width=80, anchor="center")
        
        # Configurar scrollbar para locais
        vsb_local = ttk.Scrollbar(self.manage_locais_frame, orient="vertical", command=self.local_tree.yview)
        vsb_local.grid(row=1, column=2, rowspan=4, sticky="ns", padx=0, pady=10)
        self.local_tree.configure(yscrollcommand=vsb_local.set)

        local_action_button_frame = ctk.CTkFrame(self.manage_locais_frame)
        local_action_button_frame.grid(row=5, column=1, pady=10)
        ctk.CTkButton(local_action_button_frame, text="Remover Selecionado", command=self.remove_local_gui, fg_color="red").pack(side="left", padx=5)

        ctk.CTkButton(self.manage_locais_frame, text="Voltar", command=self.show_admin_menu_frame).grid(row=6, column=0, columnspan=2, pady=10)

        # --- Frame do Menu do Usuário Comum ---
        self.user_menu_frame = ctk.CTkFrame(self)
        self.user_menu_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        self.user_menu_frame.grid_rowconfigure((0,1,2,3,4,5,6), weight=1)
        self.user_menu_frame.grid_columnconfigure(0, weight=1)
        self.user_menu_frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(self.user_menu_frame, text="Meus Dados", font=("Roboto", 24)).grid(row=0, column=0, columnspan=2, pady=20)

        # Formulário de dados do usuário comum
        user_data_form_frame = ctk.CTkFrame(self.user_menu_frame)
        user_data_form_frame.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=10, pady=10)
        user_data_form_frame.grid_columnconfigure(0, weight=1)
        user_data_form_frame.grid_columnconfigure(1, weight=2)

        ctk.CTkLabel(user_data_form_frame, text="Nome Completo:").grid(row=0, column=0, sticky="w", padx=5, pady=2)
        self.user_common_name_entry = ctk.CTkEntry(user_data_form_frame)
        self.user_common_name_entry.grid(row=0, column=1, sticky="ew", padx=5, pady=2)

        ctk.CTkLabel(user_data_form_frame, text="Idade:").grid(row=1, column=0, sticky="w", padx=5, pady=2)
        self.user_common_idade_entry = ctk.CTkEntry(user_data_form_frame)
        self.user_common_idade_entry.grid(row=1, column=1, sticky="ew", padx=5, pady=2)

        ctk.CTkLabel(user_data_form_frame, text="Endereço:").grid(row=2, column=0, sticky="w", padx=5, pady=2)
        self.user_common_endereco_entry = ctk.CTkEntry(user_data_form_frame)
        self.user_common_endereco_entry.grid(row=2, column=1, sticky="ew", padx=5, pady=2)

        ctk.CTkLabel(user_data_form_frame, text="Pessoas na Casa:").grid(row=3, column=0, sticky="w", padx=5, pady=2)
        self.user_common_pessoas_casa_entry = ctk.CTkEntry(user_data_form_frame)
        self.user_common_pessoas_casa_entry.grid(row=3, column=1, sticky="ew", padx=5, pady=2)

        ctk.CTkLabel(user_data_form_frame, text="Renda Familiar:").grid(row=4, column=0, sticky="w", padx=5, pady=2)
        self.user_common_renda_entry = ctk.CTkEntry(user_data_form_frame)
        self.user_common_renda_entry.grid(row=4, column=1, sticky="ew", padx=5, pady=2)

        ctk.CTkLabel(user_data_form_frame, text="Profissão:").grid(row=5, column=0, sticky="w", padx=5, pady=2)
        self.user_common_profissao_entry = ctk.CTkEntry(user_data_form_frame)
        self.user_common_profissao_entry.grid(row=5, column=1, sticky="ew", padx=5, pady=2)

        ctk.CTkButton(self.user_menu_frame, text="Salvar Meus Dados", command=self.save_user_common_data).grid(row=2, column=0, pady=10)
        ctk.CTkButton(self.user_menu_frame, text="Voltar ao Login", command=self.logout, fg_color="red").grid(row=3, column=0, pady=10)

    # --- Funções de Navegação entre Frames ---
    def show_frame(self, frame):
        self.login_frame.grid_forget()
        self.register_frame.grid_forget()
        self.admin_menu_frame.grid_forget()
        self.manage_users_admin_frame.grid_forget()
        self.manage_locais_frame.grid_forget()
        self.user_menu_frame.grid_forget()
        frame.grid(row=0, column=0, sticky="nsew")

    def show_login_frame(self):
        self.login_username_entry.delete(0, ctk.END)
        self.login_password_entry.delete(0, ctk.END)
        self.show_frame(self.login_frame)

    def show_register_frame(self):
        self.reg_username_entry.delete(0, ctk.END)
        self.reg_password_entry.delete(0, ctk.END)
        self.reg_confirm_password_entry.delete(0, ctk.END)
        self.show_frame(self.register_frame)

    def show_admin_menu_frame(self):
        self.show_frame(self.admin_menu_frame)

    def show_manage_users_admin_frame(self):
        self.show_frame(self.manage_users_admin_frame)
        self.populate_user_tree() # Atualiza a lista de usuários
        self.clear_user_form() # Limpa o formulário

    def show_manage_locais_frame(self):
        self.show_frame(self.manage_locais_frame)
        self.populate_local_tree() # Atualiza a lista de locais
        self.clear_local_form() # Limpa o formulário

    def show_user_menu_frame(self, username):
        global current_user_data
        current_user_data = username
        self.show_frame(self.user_menu_frame)
        self.load_user_common_data(username)

    # --- Funções de Autenticação ---
    def attempt_login(self):
        username = self.login_username_entry.get()
        password = self.login_password_entry.get()

        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            messagebox.showinfo("Login", "Login de Administrador efetuado com sucesso!")
            self.show_admin_menu_frame()
        elif username in usuarios and usuarios[username].get('senha') == password:
            messagebox.showinfo("Login", f"Bem-vindo, {username}!")
            self.show_user_menu_frame(username)
        else:
            messagebox.showerror("Login Inválido", "Usuário ou senha incorretos.")

    def register_user(self):
        username = self.reg_username_entry.get()
        password = self.reg_password_entry.get()
        confirm_password = self.reg_confirm_password_entry.get()

        if not username or not password or not confirm_password:
            messagebox.showerror("Erro de Registro", "Todos os campos são obrigatórios.")
            return

        if username in usuarios or username == ADMIN_USERNAME:
            messagebox.showerror("Erro de Registro", "Nome de usuário já existe ou é reservado. Tente outro.")
            return

        if password != confirm_password:
            messagebox.showerror("Erro de Registro", "As senhas não coincidem.")
            return

        usuarios[username] = {
            "senha": password, # Em um sistema real, a senha seria hashada
            "registrado": False # Marcador para indicar que os dados completos ainda precisam ser preenchidos
        }
        salvar_dados()
        messagebox.showinfo("Registro", "Usuário registrado com sucesso! Faça login para preencher seus dados.")
        self.show_login_frame()

    def logout(self):
        global current_user_data
        current_user_data = None
        messagebox.showinfo("Sair", "Você foi desconectado.")
        self.show_login_frame()

    # --- Funções de Gerenciamento de Usuários (Admin) ---
    def populate_user_tree(self):
        for i in self.user_tree.get_children():
            self.user_tree.delete(i)

        for username, data in usuarios.items():
            if username != ADMIN_USERNAME: # Não exibe o admin na lista de usuários gerenciáveis
                user_name = data.get('nome', 'N/A')
                user_idade = data.get('idade', 'N/A')
                user_endereco = data.get('endereco', 'N/A')
                user_apto = "Sim" if data.get('apto') else "Não" if data.get('apto') is not None else "N/A"
                self.user_tree.insert("", "end", iid=username, values=(username, user_name, user_idade, user_endereco, user_apto))

    def load_selected_user_to_form(self, event):
        selected_item = self.user_tree.focus() # Get the iid directly
        if not selected_item:
            return

        username = selected_item # selected_item is already the iid
        user_data = usuarios.get(username)

        if user_data:
            self.clear_user_form()
            self.admin_user_username_entry.insert(0, username)
            self.admin_user_username_entry.configure(state="disabled") # Não permite alterar o username
            self.admin_user_password_entry.insert(0, user_data.get('senha', ''))
            self.admin_user_name_entry.insert(0, user_data.get('nome', ''))
            self.admin_user_idade_entry.insert(0, str(user_data.get('idade', '')))
            self.admin_user_endereco_entry.insert(0, user_data.get('endereco', ''))
            self.admin_user_pessoas_casa_entry.insert(0, str(user_data.get('pessoas_casa', '')))
            self.admin_user_renda_entry.insert(0, str(user_data.get('renda', '')))
            self.admin_user_profissao_entry.insert(0, user_data.get('profissao', ''))

    def clear_user_form(self):
        self.admin_user_username_entry.configure(state="normal")
        self.admin_user_username_entry.delete(0, ctk.END)
        self.admin_user_password_entry.delete(0, ctk.END)
        self.admin_user_name_entry.delete(0, ctk.END)
        self.admin_user_idade_entry.delete(0, ctk.END)
        self.admin_user_endereco_entry.delete(0, ctk.END)
        self.admin_user_pessoas_casa_entry.delete(0, ctk.END)
        self.admin_user_renda_entry.delete(0, ctk.END)
        self.admin_user_profissao_entry.delete(0, ctk.END)

    def add_user_admin_gui(self):
        username = self.admin_user_username_entry.get()
        senha = self.admin_user_password_entry.get()
        nome = self.admin_user_name_entry.get()
        idade = self.admin_user_idade_entry.get()
        endereco = self.admin_user_endereco_entry.get()
        pessoas_casa = self.admin_user_pessoas_casa_entry.get()
        renda = self.admin_user_renda_entry.get()
        profissao = self.admin_user_profissao_entry.get()

        if not all([username, senha, nome, idade, endereco, pessoas_casa, renda, profissao]):
            messagebox.showerror("Erro", "Todos os campos devem ser preenchidos.")
            return
        if username in usuarios or username == ADMIN_USERNAME:
            messagebox.showerror("Erro", "Nome de usuário já existe ou é reservado.")
            return
        try:
            idade_int = int(idade)
            pessoas_casa_int = int(pessoas_casa)
            renda_float = float(renda)
        except ValueError:
            messagebox.showerror("Erro", "Idade, Pessoas na Casa e Renda devem ser números.")
            return

        apto = verificar_aptidao_usuario(idade_int, renda_float)
        local_designado = endereco if apto else "N/A"
        prazo_comparecimento = (datetime.date.today() + datetime.timedelta(days=15)).isoformat() if apto else "N/A"

        usuarios[username] = {
            "senha": senha,
            "nome": nome,
            "idade": idade_int,
            "endereco": endereco,
            "pessoas_casa": pessoas_casa_int,
            "renda": renda_float,
            "profissao": profissao,
            "apto": apto,
            "local_designado": local_designado,
            "prazo_comparecimento": prazo_comparecimento,
            "registrado": True
        }
        salvar_dados()
        messagebox.showinfo("Sucesso", "Usuário adicionado!")
        self.clear_user_form()
        self.populate_user_tree()

    def update_user_admin_gui(self):
        username = self.admin_user_username_entry.get()
        if not username or username not in usuarios or username == ADMIN_USERNAME:
            messagebox.showerror("Erro", "Selecione um usuário para atualizar ou o usuário não existe.")
            return

        # Coleta os valores dos campos. Se estiverem vazios, mantém os valores existentes
        user_data = usuarios[username]
        
        user_data['senha'] = self.admin_user_password_entry.get() or user_data.get('senha', '')
        user_data['nome'] = self.admin_user_name_entry.get() or user_data.get('nome', '')
        
        try:
            idade_str = self.admin_user_idade_entry.get()
            user_data['idade'] = int(idade_str) if idade_str else user_data.get('idade', 0)

            user_data['endereco'] = self.admin_user_endereco_entry.get() or user_data.get('endereco', '')
            
            pessoas_casa_str = self.admin_user_pessoas_casa_entry.get()
            user_data['pessoas_casa'] = int(pessoas_casa_str) if pessoas_casa_str else user_data.get('pessoas_casa', 0)
            
            renda_str = self.admin_user_renda_entry.get()
            user_data['renda'] = float(renda_str) if renda_str else user_data.get('renda', 0.0)
            
            user_data['profissao'] = self.admin_user_profissao_entry.get() or user_data.get('profissao', '')

        except ValueError:
            messagebox.showerror("Erro", "Idade, Pessoas na Casa e Renda devem ser números.")
            return

        # Recalcular aptidão e prazos
        user_data['apto'] = verificar_aptidao_usuario(user_data['idade'], user_data['renda'])
        user_data['local_designado'] = user_data['endereco'] if user_data['apto'] else "N/A"
        user_data['prazo_comparecimento'] = (datetime.date.today() + datetime.timedelta(days=30)).isoformat() if user_data['apto'] else "N/A"
        user_data['registrado'] = True

        salvar_dados()
        messagebox.showinfo("Sucesso", "Usuário atualizado!")
        self.clear_user_form()
        self.populate_user_tree()

    def remove_user_admin_gui(self):
        selected_item = self.user_tree.focus() # Get the iid directly
        if not selected_item:
            messagebox.showerror("Erro", "Selecione um usuário para remover.")
            return

        username = selected_item # selected_item is already the iid
        if username == ADMIN_USERNAME:
            messagebox.showerror("Erro", "Não é possível remover o administrador.")
            return

        if messagebox.askyesno("Confirmar Remoção", f"Tem certeza que deseja remover o usuário {username}?"):
            if usuarios.pop(username, None):
                salvar_dados()
                messagebox.showinfo("Sucesso", "Usuário removido!")
                self.populate_user_tree()
                self.clear_user_form()
            else:
                messagebox.showerror("Erro", "Usuário não encontrado.")

    # --- Funções de Gerenciamento de Locais (Admin) ---
    def populate_local_tree(self):
        for i in self.local_tree.get_children():
            self.local_tree.delete(i)

        for nome_local, data in locais.items():
            capacidade = data.get('capacidade_producao', 'N/A')
            apto = data.get('apto', 'N/A')
            self.local_tree.insert("", "end", iid=nome_local, values=(nome_local, data.get('endereco', ''), data.get('responsavel', ''), capacidade, apto))

    def load_selected_local_to_form(self, event):
        selected_item = self.local_tree.focus()
        if not selected_item:
            return

        nome_local = self.local_tree.item(selected_item, "iid")
        local_data = locais.get(nome_local)

        if local_data:
            self.clear_local_form()
            self.local_nome_entry.insert(0, nome_local)
            self.local_nome_entry.configure(state="disabled") # Não permite alterar o nome do local
            self.local_endereco_entry.insert(0, local_data.get('endereco', ''))
            self.local_responsavel_entry.insert(0, local_data.get('responsavel', ''))
            self.local_contato_entry.insert(0, local_data.get('contato', ''))
            self.local_andares_entry.insert(0, str(local_data.get('andares', '')))
            self.local_area_entry.insert(0, str(local_data.get('area', '')))

    def clear_local_form(self):
        self.local_nome_entry.configure(state="normal")
        self.local_nome_entry.delete(0, ctk.END)
        self.local_endereco_entry.delete(0, ctk.END)
        self.local_responsavel_entry.delete(0, ctk.END)
        self.local_contato_entry.delete(0, ctk.END)
        self.local_andares_entry.delete(0, ctk.END)
        self.local_area_entry.delete(0, ctk.END)

    def add_local_gui(self):
        nome_local = self.local_nome_entry.get()
        endereco = self.local_endereco_entry.get()
        responsavel = self.local_responsavel_entry.get()
        contato = self.local_contato_entry.get()
        andares = self.local_andares_entry.get()
        area = self.local_area_entry.get()

        if not all([nome_local, endereco, responsavel, contato, andares, area]):
            messagebox.showerror("Erro", "Todos os campos devem ser preenchidos.")
            return
        if nome_local in locais:
            messagebox.showerror("Erro", "Nome de local já existe.")
            return
        try:
            andares_int = int(andares)
            area_float = float(area)
        except ValueError:
            messagebox.showerror("Erro", "Andares e Área devem ser números.")
            return

        capacidade = calcular_capacidade_producao(andares_int, area_float)
        apto = "Sim" if capacidade >= 1000 else "Não"

        locais[nome_local] = {
            "nome_local": nome_local,
            "endereco": endereco,
            "responsavel": responsavel,
            "contato": contato,
            "andares": andares_int,
            "area": area_float,
            "capacidade_producao": capacidade,
            "apto": apto,
            "mensagem": "O responsável será contatado para mais informações."
        }
        salvar_dados()
        messagebox.showinfo("Sucesso", "Local adicionado!")
        self.clear_local_form()
        self.populate_local_tree()

    def update_local_gui(self):
        nome_local = self.local_nome_entry.get()
        if not nome_local or nome_local not in locais:
            messagebox.showerror("Erro", "Selecione um local para atualizar ou o local não existe.")
            return

        local_data = locais[nome_local]

        local_data['endereco'] = self.local_endereco_entry.get() or local_data.get('endereco', '')
        local_data['responsavel'] = self.local_responsavel_entry.get() or local_data.get('responsavel', '')
        local_data['contato'] = self.local_contato_entry.get() or local_data.get('contato', '')
        
        try:
            andares_str = self.local_andares_entry.get()
            local_data['andares'] = int(andares_str) if andares_str else local_data.get('andares', 0)

            area_str = self.local_area_entry.get()
            local_data['area'] = float(area_str) if area_str else local_data.get('area', 0.0)
        except ValueError:
            messagebox.showerror("Erro", "Andares e Área devem ser números.")
            return

        capacidade = calcular_capacidade_producao(local_data['andares'], local_data['area'])
        local_data['capacidade_producao'] = capacidade
        local_data['apto'] = "Sim" if capacidade >= 1000 else "Não"

        salvar_dados()
        messagebox.showinfo("Sucesso", "Local atualizado!")
        self.clear_local_form()
        self.populate_local_tree()

    def remove_local_gui(self):
        selected_item = self.local_tree.focus()
        if not selected_item:
            messagebox.showerror("Erro", "Selecione um local para remover.")
            return

        nome_local = self.local_tree.item(selected_item, "iid")
        if messagebox.askyesno("Confirmar Remoção", f"Tem certeza que deseja remover o local {nome_local}?"):
            if locais.pop(nome_local, None):
                salvar_dados()
                messagebox.showinfo("Sucesso", "Local removido!")
                self.populate_local_tree()
                self.clear_local_form()
            else:
                messagebox.showerror("Erro", "Local não encontrado.")

    # --- Funções do Usuário Comum ---
    def load_user_common_data(self, username):
        user_data = usuarios.get(username)
        if user_data and user_data.get('registrado'):
            self.user_common_name_entry.delete(0, ctk.END)
            self.user_common_name_entry.insert(0, user_data.get('nome', ''))
            
            self.user_common_idade_entry.delete(0, ctk.END)
            self.user_common_idade_entry.insert(0, str(user_data.get('idade', '')))
            
            self.user_common_endereco_entry.delete(0, ctk.END)
            self.user_common_endereco_entry.insert(0, user_data.get('endereco', ''))
            
            self.user_common_pessoas_casa_entry.delete(0, ctk.END)
            self.user_common_pessoas_casa_entry.insert(0, str(user_data.get('pessoas_casa', '')))
            
            self.user_common_renda_entry.delete(0, ctk.END)
            self.user_common_renda_entry.insert(0, str(user_data.get('renda', '')))
            
            self.user_common_profissao_entry.delete(0, ctk.END)
            self.user_common_profissao_entry.insert(0, user_data.get('profissao', ''))

        else:
            # If the user has no complete data, clear the fields and show the message
            self.user_common_name_entry.delete(0, ctk.END)
            self.user_common_idade_entry.delete(0, ctk.END)
            self.user_common_endereco_entry.delete(0, ctk.END)
            self.user_common_pessoas_casa_entry.delete(0, ctk.END)
            self.user_common_renda_entry.delete(0, ctk.END)
            self.user_common_profissao_entry.delete(0, ctk.END)
            if user_data and not user_data.get('registrado'):
                messagebox.showinfo("Preencher Dados", "Por favor, preencha seus dados completos.")

    def save_user_common_data(self):
        username = current_user_data
        if not username:
            messagebox.showerror("Erro", "Nenhum usuário logado.")
            return

        nome = self.user_common_name_entry.get()
        idade = self.user_common_idade_entry.get()
        endereco = self.user_common_endereco_entry.get()
        pessoas_casa = self.user_common_pessoas_casa_entry.get()
        renda = self.user_common_renda_entry.get()
        profissao = self.user_common_profissao_entry.get()

        if not all([nome, idade, endereco, pessoas_casa, renda, profissao]):
            messagebox.showerror("Erro", "Todos os campos devem ser preenchidos.")
            return

        try:
            idade_int = int(idade)
            pessoas_casa_int = int(pessoas_casa)
            renda_float = float(renda)
        except ValueError:
            messagebox.showerror("Erro", "Idade, Pessoas na Casa e Renda devem ser números.")
            return

        apto = verificar_aptidao_usuario(idade_int, renda_float)
        local_designado = endereco if apto else "N/A"
        prazo_comparecimento = (datetime.date.today() + datetime.timedelta(days=30)).isoformat() if apto else "N/A"

        usuarios[username].update({
            "nome": nome,
            "idade": idade_int,
            "endereco": endereco,
            "pessoas_casa": pessoas_casa_int,
            "renda": renda_float,
            "profissao": profissao,
            "apto": apto,
            "local_designado": local_designado,
            "prazo_comparecimento": prazo_comparecimento,
            "registrado": True
        })
        salvar_dados()
        messagebox.showinfo("Sucesso", "Seus dados foram salvos!")

# --- Execução da Aplicação ---
if __name__ == "__main__":
    app = App()
    app.mainloop()