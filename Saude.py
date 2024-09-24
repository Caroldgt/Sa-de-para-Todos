import sqlite3

# Conexão ao banco de dados SQLite
conn = sqlite3.connect('saude_para_todos.db')
c = conn.cursor()

# Criação das tabelas
c.execute('''CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                idade INTEGER NOT NULL CHECK(idade > 0),
                genero TEXT NOT NULL,
                telefone TEXT NOT NULL,
                endereco TEXT NOT NULL)''')

c.execute('''CREATE TABLE IF NOT EXISTS consultas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario_nome TEXT NOT NULL,
                data TEXT NOT NULL,
                urgencia TEXT NOT NULL)''')

conn.commit()

def cadastrar_usuario():
    while True:
        nome = input("Digite o nome do usuário: ").strip()
        if not nome:
            print("O nome não pode estar vazio. Tente novamente.")
            continue
        
        idade = input("Digite a idade do usuário: ")
        if not idade.isdigit() or int(idade) <= 0:
            print("Idade deve ser um número positivo. Tente novamente.")
            continue
        idade = int(idade)

        genero = input("Digite o gênero do usuário (Masculino/Feminino/Outro): ").strip().capitalize()
        if genero not in ["Masculino", "Feminino", "Outro"]:
            print("Gênero deve ser Masculino, Feminino ou Outro. Tente novamente.")
            continue
        
        telefone = input("Digite o telefone do usuário: ").strip()
        if not telefone:
            print("O telefone não pode estar vazio. Tente novamente.")
            continue
        
        endereco = input("Digite o endereço do usuário: ").strip()
        if not endereco:
            print("O endereço não pode estar vazio. Tente novamente.")
            continue
        
        # Inserindo os dados no banco de dados
        c.execute("INSERT INTO usuarios (nome, idade, genero, telefone, endereco) VALUES (?, ?, ?, ?, ?)",
                  (nome, idade, genero, telefone, endereco))
        conn.commit()
        print("Usuário cadastrado com sucesso!")
        break

def cadastrar_consulta():
    while True:
        usuario_nome = input("Digite o nome do usuário para a consulta: ").strip()
        if not usuario_nome:
            print("O nome não pode estar vazio. Tente novamente.")
            continue
        
        # Verifica se o usuário existe
        c.execute("SELECT * FROM usuarios WHERE nome=?", (usuario_nome,))
        usuario = c.fetchone()
        if not usuario:
            print("Usuário não encontrado. Tente novamente.")
            continue

        data = input("Digite a data da consulta (YYYY-MM-DD): ").strip()
        if not data:
            print("A data não pode estar vazia. Tente novamente.")
            continue

        urgencia = input("Digite o nível de urgência (Baixa, Média, Alta): ").strip().capitalize()
        if urgencia not in ["Baixa", "Média", "Alta"]:
            print("Urgência deve ser Baixa, Média ou Alta. Tente novamente.")
            continue
        
        # Inserindo os dados no banco de dados
        c.execute("INSERT INTO consultas (usuario_nome, data, urgencia) VALUES (?, ?, ?)",
                  (usuario_nome, data, urgencia))
        conn.commit()
        print("Consulta cadastrada com sucesso!")
        break

def listar_pacientes():
    c.execute("SELECT * FROM usuarios")
    usuarios = c.fetchall()
    print("--- Lista de Pacientes ---")
    for usuario in usuarios:
        print(f"Nome: {usuario[1]}, Idade: {usuario[2]}, Gênero: {usuario[3]}, Telefone: {usuario[4]}, Endereço: {usuario[5]}")

def main():
    while True:
        print("--- Sistema de Saúde para Todos ---")
        print("1. Cadastrar Usuário")
        print("2. Cadastrar Consulta")
        print("3. Listar Pacientes")
        print("4. Sair")
        opcao = input("Escolha uma opção: ")

        if opcao == '1':
            cadastrar_usuario()
        elif opcao == '2':
            cadastrar_consulta()
        elif opcao == '3':
            listar_pacientes()
        elif opcao == '4':
            print("Saindo do sistema...")
            break
        else:
            print("Opção inválida. Tente novamente.")

# Chama a função principal
if __name__ == "__main__":
    main()

# Fechando a conexão com o banco de dados
conn.close()
