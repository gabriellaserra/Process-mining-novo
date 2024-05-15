import tkinter as tk

def mostrar_selecionado():
    # Obter o índice do item selecionado
    indice_selecionado = listbox.curselection()
    # Se algum item estiver selecionado
    if indice_selecionado:
        # Obter o valor do item selecionado
        valor_selecionado = listbox.get(indice_selecionado)
        # Exibir o valor selecionado
        label_valor_selecionado.config(text=f"Item selecionado: {valor_selecionado}")
    else:
        label_valor_selecionado.config(text="Nenhum item selecionado")

# Criar a janela principal
root = tk.Tk()
root.title("Exemplo Listbox")

# Criar um Listbox
listbox = tk.Listbox(root)
listbox.pack()

# Adicionar alguns itens ao Listbox
itens = ["Item 1", "Item 2", "Item 3", "Item 4"]
for item in itens:
    listbox.insert(tk.END, item)

# Criar uma label para exibir o item selecionado
label_valor_selecionado = tk.Label(root, text="Nenhum item selecionado")
label_valor_selecionado.pack()

# Botão para mostrar o item selecionado
botao_mostrar = tk.Button(root, text="Mostrar selecionado", command=mostrar_selecionado)
botao_mostrar.pack()

# Executar o loop principal
root.mainloop()