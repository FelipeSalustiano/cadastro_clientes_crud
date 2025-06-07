# 🧑‍💻 Sistema de Gerenciamento de Usuários e Locais

Este é um sistema simples de gerenciamento de usuários desenvolvido em **Python**, com interface gráfica utilizando **Tkinter** e persistência de dados com **SQLite**. O projeto permite o cadastro, listagem, atualização e remoção de usuários, além de verificação de aptidão com base em idade e renda. O projeto foi dividido em duas partes. O arquivo "crud_main" é o código principal, enquanto o "crud_layout" possui o mesmo script do main, porém com o layout e banco de dados implementados. 

## 🚀 Funcionalidades

- Cadastro de usuários com nome, idade, endereço, número de pessoas na casa, renda e profissão.
- Verificação de aptidão com base em:
  - Idade ≥ 18 anos
  - Renda ≤ R$ 2.000
- Atribuição de local e prazo de comparecimento automático para usuários aptos.
- Atualização dos dados dos usuários.
- Remoção de usuários cadastrados.
- Listagem de todos os usuários em formato de tabela.
- Interface gráfica (Tkinter) e banco de dados (SQLite).

## 🛠️ Tecnologias Utilizadas

- Python 3.x
- Tkinter (interface gráfica)
- SQLite (banco de dados)
- Pandas (para exibição de dados em tabela no terminal)


