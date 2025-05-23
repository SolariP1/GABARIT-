import customtkinter as ctk
from conecta import conectar_ao_banco
from auth.auth_login import *
from frames.utilidades import *

class Cadastro(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master

        self.titulo = ctk.CTkLabel(self, text="Cadastro", font=ctk.CTkFont(size=20, weight="bold"))
        self.titulo.pack(pady=20)

        self.nomeLabel = ctk.CTkLabel(self, text="Nome")
        self.nomeLabel.pack()

        self.nome = ctk.CTkEntry(self, width=250)
        self.nome.pack(pady=5)

        self.usuarioLabel = ctk.CTkLabel(self, text="Usuario")
        self.usuarioLabel.pack()

        self.usuario = ctk.CTkEntry(self, width=250)
        self.usuario.pack(pady=10)

        self.cpfLabel = ctk.CTkLabel(self, text="Cpf")
        self.cpfLabel.pack()

        self.cpf = ctk.CTkEntry(self, width=250)
        self.cpf.pack(pady=5)

        self.emailLabel = ctk.CTkLabel(self, text="E-mail")
        self.emailLabel.pack()

        self.email = ctk.CTkEntry(self, width=250)
        self.email.pack(pady=5)
        
        self.senhaLabel = ctk.CTkLabel(self, text="Senha")
        self.senhaLabel.pack()

        self.senha = ctk.CTkEntry(self, width=250, show="*")
        self.senha.pack(pady=5)

        self.confirmaSenhaLabel = ctk.CTkLabel(self, text="Confirma senha")
        self.confirmaSenhaLabel.pack()

        self.confirmaSenha = ctk.CTkEntry(self, width=250, show="*")
        self.confirmaSenha.pack(pady=5)

        self.botaoCadastrar = ctk.CTkButton(self, text="Cadastrar", command=self.cadastrar)
        self.botaoCadastrar.pack(pady=10)

        self.botaoVoltar = ctk.CTkButton(self, text="Voltar", command=self.retorno)
        self.botaoVoltar.pack(pady=10)

        self.mensagem = ctk.CTkLabel(self, text="")
        self.mensagem.pack()

        self.db, _ = conectar_ao_banco()

    def cadastrar(self):
        cursor = self.db.cursor()
        nome = self.nome.get()
        usuario = self.usuario.get()
        email = self.email.get()
        cpf = self.cpf.get()
        senha = self.senha.get()
        confirmaSenha = self.confirmaSenha.get()

        # Usando '?' em vez de '%s'
        cursor.execute("SELECT PROF_USU FROM PROFESSOR WHERE PROF_USU = ?", (usuario,))
        resultados = cursor.fetchall()
        usuario_existe = bool(resultados)

        if usuario_existe:
            self.mensagem.configure(text="Usuário já existe")
        elif senha == confirmaSenha and len(senha) >= 8 and " " not in senha:
            try:
                # Usando '?' também para a inserção
                sql = "INSERT INTO PROFESSOR (PROF_NOME, PROF_USU, PROF_EMAIL, PROF_CPF, PROF_SENHA) VALUES (?, ?, ?, ?, ?)"
                val = (nome, usuario, email, cpf, senha)
                cursor.execute(sql, val)
                self.db.commit()
                self.mensagem.configure(text="Usuário cadastrado com sucesso.")
                self.master.switch_frame(Login)
            except Exception as e:
                self.mensagem.configure(text=f"Erro ao cadastrar usuário: {e}")
        else:
            self.mensagem.configure(text="Senha inválida ou não coincide")

    def retorno(self):
        self.master.switch_frame(Login)
