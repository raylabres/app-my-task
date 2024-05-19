import customtkinter as ctk
from PIL import Image, ImageTk
import back

arquivo_fundo = "C:/Desenvolvimento/Projetos/lista-tarefas/imagens/fundo.png"

def mostrar_tela_menu():
    tela_menu.place(x=0, y=0)
    fonte = ctk.CTkFont(family="Arial", size=20)

    def logar():
        global label_criada_resultado
        global label_resultado

        usuario = user_entry.get()
        senha = user_pass.get()
        resultado_logar = back.login(usuario=usuario, senha=senha)

        if resultado_logar[0] == 0 and not label_criada_resultado:
                label_resultado = ctk.CTkLabel(master=tela_menu, text=resultado_logar[1], font=fonte)
                label_resultado.place(x=x_centro - 70, y=y_centro + 250)
                label_criada_resultado = True

        elif resultado_logar[0] == 1 and label_criada_resultado:
                label_resultado.destroy()
                label_criada_resultado = False
                mostrar_tela_principal(resultado_logar)
        
        elif resultado_logar[0] == 1 and not label_criada_resultado:
            mostrar_tela_principal(resultado_logar)
    
    borda_frame = ctk.CTkFrame(master=tela_menu, border_color="#000000", border_width=2) 
    label = ctk.CTkLabel(master=borda_frame, text='Entrar no Lista de Tarefas', font=fonte) 
    label.pack(pady=12,padx=10) 

    user_entry= ctk.CTkEntry(master=borda_frame, placeholder_text="Usuário", font=fonte, width=300) 
    user_entry.pack(pady=12,padx=10)


    user_pass= ctk.CTkEntry(master=borda_frame, placeholder_text="Senha", show="*", font=fonte, width=300) 
    user_pass.pack(pady=12,padx=10) 


    button = ctk.CTkButton(master=borda_frame, text='Entrar', font=fonte, width=300, height=30, fg_color="#C952EB", hover_color='#000000', command=logar) 
    button.pack(pady=12,padx=10)

    # Borda frame
    x_centro = (largura_janela - borda_frame.winfo_reqwidth()) // 2
    y_centro = (altura_janela - borda_frame.winfo_reqheight()) // 2
    borda_frame.place(x=x_centro, y=y_centro)

def mostrar_tela_principal(resultado):
    tela_menu.place_forget()
    tela_principal.place(x=0, y=0)
    fonte = ctk.CTkFont(family="Arial", size=20)

    def atualizar_visualizar():
        # Limpa o frame atual
        for widget in tab_1_frame.winfo_children():
            widget.destroy()
        
        lista_tarefas = back.visualizar(resultado)
        
        for pos_linha, linha in enumerate(lista_tarefas):
            frame_tarefa = ctk.CTkFrame(master=tab_1_frame, fg_color="#242424")
            frame_tarefa.pack(fill='x', expand=True, padx=20, pady=20)
            for pos_campo, campo in enumerate(linha):
                if pos_campo == 0:
                    label_status = ctk.CTkLabel(master=frame_tarefa, text=f"{campo}º Tarefa")
                    label_status.pack(padx=10, pady=10)
                elif pos_campo == 1:
                    label_status = ctk.CTkLabel(master=frame_tarefa, text=f"ID: {campo}")
                    label_status.pack(padx=10, pady=10) 
                elif pos_campo == 2:
                    label_status = ctk.CTkLabel(master=frame_tarefa, text=f"Nome: {campo}")
                    label_status.pack(padx=10, pady=10) 
                elif pos_campo == 3:
                    label_status = ctk.CTkLabel(master=frame_tarefa, text=f"Descrição: {campo}")
                    label_status.pack(padx=10, pady=10) 
                elif pos_campo == 4:
                    label_status = ctk.CTkLabel(master=frame_tarefa, text=f"Data Inicío: {campo}")
                    label_status.pack(padx=10, pady=10) 
                elif pos_campo == 5:
                    label_status = ctk.CTkLabel(master=frame_tarefa, text=f"Data Fim: {campo}")
                    label_status.pack(padx=10, pady=10) 
                elif pos_campo == 6:
                    label_status = ctk.CTkLabel(master=frame_tarefa, text=f"Status: {campo}")
                    label_status.pack(padx=10, pady=10)

    def criar_tarefa():
        global label_criada_nova_tarefa
        global label_resultado_nova_tarefa

        nome = nome_entry.get()
        descricao = descricao_entry.get()
        data_inicio = data_inicio_entry.get()
        data_fim = data_fim_entry.get()
        status = status_entry.get()

        resultado_nova_tarefa = back.nova_tarefa(resultado, nome, descricao, data_inicio, data_fim, status)
        
        if resultado_nova_tarefa[0] == 0 and not label_criada_nova_tarefa:
            label_resultado_nova_tarefa = ctk.CTkLabel(master=borda_tab_2_frame, text=resultado_nova_tarefa[1], font=fonte)
            label_resultado_nova_tarefa.pack(padx=20, pady=20)
            label_criada_nova_tarefa = True

        elif resultado_nova_tarefa[0] == 1 and not label_criada_nova_tarefa:
            label_resultado_nova_tarefa = ctk.CTkLabel(master=borda_tab_2_frame, text=resultado_nova_tarefa[1], font=fonte)
            label_resultado_nova_tarefa.pack(padx=20, pady=20)
            label_criada_nova_tarefa = True
            atualizar_visualizar()    

        elif resultado_nova_tarefa[0] == 0 and label_criada_nova_tarefa:
            label_resultado_nova_tarefa.destroy()
            label_resultado_nova_tarefa = ctk.CTkLabel(master=borda_tab_2_frame, text=resultado_nova_tarefa[1], font=fonte)
            label_resultado_nova_tarefa.pack(padx=20, pady=20)
            atualizar_visualizar()

        elif resultado_nova_tarefa[0] == 1 and label_criada_nova_tarefa:
            label_resultado_nova_tarefa.destroy()
            label_resultado_nova_tarefa = ctk.CTkLabel(master=borda_tab_2_frame, text=resultado_nova_tarefa[1], font=fonte)
            label_resultado_nova_tarefa.pack(padx=20, pady=20)
            atualizar_visualizar()

    def alterar_tarefa():
        global label_criada_alterar_tarefa
        global label_resultado_alterar_terefa

        id_alterar = id_entry_alterar.get()
        nome_alterar = nome_entry_alterar.get()
        descricao_alterar = descricao_entry_alterar.get()
        data_inicio_alterar = data_inicio_entry_alterar.get()
        data_fim_alterar = data_fim_entry_alterar.get()
        status_alterar = status_entry_alterar.get()

        resultado_alterar_tarefa = back.alterar(resultado, id_alterar, nome_alterar, descricao_alterar, data_inicio_alterar, data_fim_alterar, status_alterar)

        if resultado_alterar_tarefa[0] == 0 and not label_criada_alterar_tarefa:
            label_resultado_alterar_terefa = ctk.CTkLabel(master=borda_tab_3_frame, text=resultado_alterar_tarefa[1], font=fonte)
            label_resultado_alterar_terefa.pack(padx=20, pady=20)
            label_criada_alterar_tarefa = True

        elif resultado_alterar_tarefa[0] == 1 and not label_criada_alterar_tarefa:
            label_resultado_alterar_terefa = ctk.CTkLabel(master=borda_tab_3_frame, text=resultado_alterar_tarefa[1], font=fonte)
            label_resultado_alterar_terefa.pack(padx=20, pady=20)
            label_criada_alterar_tarefa = True
            atualizar_visualizar()    

        elif resultado_alterar_tarefa[0] == 0 and label_criada_alterar_tarefa:
            label_resultado_alterar_terefa.destroy()
            label_resultado_alterar_terefa = ctk.CTkLabel(master=borda_tab_3_frame, text=resultado_alterar_tarefa[1], font=fonte)
            label_resultado_alterar_terefa.pack(padx=20, pady=20)
            atualizar_visualizar()

        elif resultado_alterar_tarefa[0] == 1 and label_criada_alterar_tarefa:
            label_resultado_alterar_terefa.destroy()
            label_resultado_alterar_terefa = ctk.CTkLabel(master=borda_tab_3_frame, text=resultado_alterar_tarefa[1], font=fonte)
            label_resultado_alterar_terefa.pack(padx=20, pady=20)
            atualizar_visualizar()

    def deletar_tarefa():
        global label_criada_deletar_tarefa
        global label_resultado_deletar_terefa

        id_deletar = id_entry_deletar.get()

        resultado_deletar_tarefa = back.deletar(resultado, id_deletar)

        if resultado_deletar_tarefa[0] == 0 and not label_criada_deletar_tarefa:
            label_resultado_deletar_terefa = ctk.CTkLabel(master=borda_tab_4_frame, text=resultado_deletar_tarefa[1], font=fonte)
            label_resultado_deletar_terefa.pack(padx=20, pady=20)
            label_criada_deletar_tarefa = True

        elif resultado_deletar_tarefa[0] == 1 and not label_criada_deletar_tarefa:
            label_resultado_deletar_terefa = ctk.CTkLabel(master=borda_tab_4_frame, text=resultado_deletar_tarefa[1], font=fonte)
            label_resultado_deletar_terefa.pack(padx=20, pady=20)
            label_criada_deletar_tarefa = True
            atualizar_visualizar()    

        elif resultado_deletar_tarefa[0] == 0 and label_criada_deletar_tarefa:
            label_resultado_deletar_terefa.destroy()
            label_resultado_deletar_terefa = ctk.CTkLabel(master=borda_tab_4_frame, text=resultado_deletar_tarefa[1], font=fonte)
            label_resultado_deletar_terefa.pack(padx=20, pady=20)
            atualizar_visualizar()

        elif resultado_deletar_tarefa[0] == 1 and label_criada_deletar_tarefa:
            label_resultado_deletar_terefa.destroy()
            label_resultado_deletar_terefa = ctk.CTkLabel(master=borda_tab_4_frame, text=resultado_deletar_tarefa[1], font=fonte)
            label_resultado_deletar_terefa.pack(padx=20, pady=20)
            atualizar_visualizar()


    tabview = ctk.CTkTabview(master=tela_principal, width=largura_janela - 25, height=altura_janela - 80, fg_color="#303030", border_color="#000000", border_width=2)
    tabview.pack(padx=12, pady=10)

    tabview.add("Visualizar")
    tabview.add("Criar")
    tabview.add("Alterar")
    tabview.add("Deletar")

    # Adicionar a imagem ao CTkLabel
    label_imagem_fundo = ctk.CTkLabel(tabview.tab('Visualizar'), image=imagem_ctk, text="")
    label_imagem_fundo.place(x=0, y=0, relwidth=1, relheight=1)

    # Adicionar a imagem ao CTkLabel
    label_imagem_fundo = ctk.CTkLabel(tabview.tab('Criar'), image=imagem_ctk, text="")
    label_imagem_fundo.place(x=0, y=0, relwidth=1, relheight=1)

    # Adicionar a imagem ao CTkLabel
    label_imagem_fundo = ctk.CTkLabel(tabview.tab('Alterar'), image=imagem_ctk, text="")
    label_imagem_fundo.place(x=0, y=0, relwidth=1, relheight=1)

    # Adicionar a imagem ao CTkLabel
    label_imagem_fundo = ctk.CTkLabel(tabview.tab('Deletar'), image=imagem_ctk, text="")
    label_imagem_fundo.place(x=0, y=0, relwidth=1, relheight=1)


    tab_1_frame = ctk.CTkScrollableFrame(master=tabview.tab("Visualizar"), width=tabview.winfo_reqwidth() / 2, height=tabview.winfo_reqheight() / 2, fg_color="#303035", border_color="#C952EB", border_width=2, orientation="vertical", scrollbar_button_color="#C952EB")
    tab_1_frame.pack(expand=True, padx=20, pady=20)

    atualizar_visualizar()  # Inicializa a aba "Visualizar"

    borda_tab_2_frame = ctk.CTkFrame(master=tabview.tab("Criar"), border_color="#000000", border_width=2) 
    label = ctk.CTkLabel(master=borda_tab_2_frame, text='Criar nova tarefa', font=fonte) 
    label.pack(pady=12,padx=10) 

    nome_entry = ctk.CTkEntry(master=borda_tab_2_frame, placeholder_text="Nome", font=fonte, width=300) 
    nome_entry.pack(pady=12,padx=10)

    descricao_entry = ctk.CTkEntry(master=borda_tab_2_frame, placeholder_text="Descrição", font=fonte, width=300) 
    descricao_entry.pack(pady=12,padx=10)

    data_inicio_entry = ctk.CTkEntry(master=borda_tab_2_frame, placeholder_text="Data Início", font=fonte, width=300) 
    data_inicio_entry.pack(pady=12,padx=10)

    data_fim_entry = ctk.CTkEntry(master=borda_tab_2_frame, placeholder_text="Data Fim", font=fonte, width=300) 
    data_fim_entry.pack(pady=12,padx=10)

    status_entry = ctk.CTkEntry(master=borda_tab_2_frame, placeholder_text="Status", font=fonte, width=300) 
    status_entry.pack(pady=12,padx=10)

    button = ctk.CTkButton(master=borda_tab_2_frame, text='Criar', font=fonte, width=300, height=30, fg_color="#C952EB", hover_color='#000000',  command=criar_tarefa) 
    button.pack(pady=12,padx=10)

    borda_tab_2_frame.grid(row=1, column=1, padx=20, pady=20)
    # Peso das colunas e linhas para centralizar o borda_frame
    tabview.tab("Criar").grid_columnconfigure(0, weight=1)
    tabview.tab("Criar").grid_columnconfigure(2, weight=1)
    tabview.tab("Criar").grid_rowconfigure(0, weight=1)
    tabview.tab("Criar").grid_rowconfigure(2, weight=1)


    borda_tab_3_frame = ctk.CTkFrame(master=tabview.tab("Alterar"), border_color="#000000", border_width=2)
    label = ctk.CTkLabel(master=borda_tab_3_frame, text="Alter dados tarefa", font=fonte)
    label.pack(pady=12, padx=10)

    id_entry_alterar = ctk.CTkEntry(master=borda_tab_3_frame, placeholder_text="Id", font=fonte, width=300) 
    id_entry_alterar.pack(pady=12,padx=10)

    nome_entry_alterar = ctk.CTkEntry(master=borda_tab_3_frame, placeholder_text="Nome", font=fonte, width=300) 
    nome_entry_alterar.pack(pady=12,padx=10)

    descricao_entry_alterar = ctk.CTkEntry(master=borda_tab_3_frame, placeholder_text="Descrição", font=fonte, width=300) 
    descricao_entry_alterar.pack(pady=12,padx=10)

    data_inicio_entry_alterar = ctk.CTkEntry(master=borda_tab_3_frame, placeholder_text="Data Início", font=fonte, width=300) 
    data_inicio_entry_alterar.pack(pady=12,padx=10)

    data_fim_entry_alterar = ctk.CTkEntry(master=borda_tab_3_frame, placeholder_text="Data Fim", font=fonte, width=300) 
    data_fim_entry_alterar.pack(pady=12,padx=10)

    status_entry_alterar = ctk.CTkEntry(master=borda_tab_3_frame, placeholder_text="Status", font=fonte, width=300) 
    status_entry_alterar.pack(pady=12,padx=10)

    button_alterar = ctk.CTkButton(master=borda_tab_3_frame, text='Alterar', font=fonte, width=300, height=30, fg_color="#C952EB", hover_color='#000000', command=alterar_tarefa) 
    button_alterar.pack(pady=12,padx=10)

    borda_tab_3_frame.grid(row=1, column=1, padx=20, pady=20)
     # Peso das colunas e linhas para centralizar o borda_frame
    tabview.tab("Alterar").grid_columnconfigure(0, weight=1)
    tabview.tab("Alterar").grid_columnconfigure(2, weight=1)
    tabview.tab("Alterar").grid_rowconfigure(0, weight=1)
    tabview.tab("Alterar").grid_rowconfigure(2, weight=1)

    borda_tab_4_frame = ctk.CTkFrame(master=tabview.tab("Deletar"), border_color="#000000", border_width=2)
    label = ctk.CTkLabel(master=borda_tab_4_frame, text="Deletar tarefa", font=fonte)
    label.pack(pady=12, padx=10)

    id_entry_deletar = ctk.CTkEntry(master=borda_tab_4_frame, placeholder_text="Id", font=fonte, width=300) 
    id_entry_deletar .pack(pady=12,padx=10)

    button_deletar = ctk.CTkButton(master=borda_tab_4_frame, text='Alterar', font=fonte, width=300, height=30, fg_color="#C952EB", hover_color='#000000', command=deletar_tarefa) 
    button_deletar.pack(pady=12,padx=10)

    borda_tab_4_frame.grid(row=1, column=1, padx=20, pady=20)
    # Peso das colunas e linhas para centralizar o borda_frame
    tabview.tab("Deletar").grid_columnconfigure(0, weight=1)
    tabview.tab("Deletar").grid_columnconfigure(2, weight=1)
    tabview.tab("Deletar").grid_rowconfigure(0, weight=1)
    tabview.tab("Deletar").grid_rowconfigure(2, weight=1)


# Criar a janela principal
janela = ctk.CTk()
janela.title("App - Lista de Tarefas")
largura_janela = janela.winfo_screenwidth()
altura_janela = janela.winfo_screenheight()
janela.geometry(f"{largura_janela}x{altura_janela}")

# Carregar a imagem
imagem = Image.open(arquivo_fundo)
imagem = imagem.resize((largura_janela, altura_janela))
#imagem_tk = ImageTk.PhotoImage(imagem)
imagem_ctk = ctk.CTkImage(light_image=imagem, dark_image=imagem, size=(largura_janela, altura_janela))

# Tela menu
tela_menu = ctk.CTkFrame(janela, fg_color="#303030", width=largura_janela, height=altura_janela)
label_criada_resultado = False
label_resultado = None

# Adicionar a imagem ao CTkLabel
label_imagem = ctk.CTkLabel(tela_menu, image=imagem_ctk, text="")
label_imagem.pack(pady=20)  # Adicione padding conforme necessário


# Tela principal
tela_principal = ctk.CTkFrame(janela, fg_color="#303030", width=largura_janela, height=altura_janela)
label_criada_nova_tarefa = False
label_resultado_nova_tarefa = None
label_criada_alterar_tarefa = False
label_resultado_alterar_terefa = None
label_criada_deletar_tarefa = False
label_resultado_deletar_terefa = None


# Inicialmente, mostra a tela inicial
mostrar_tela_menu()

janela.mainloop()