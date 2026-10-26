# empresa_flask

Aplicação Flask para login e gerenciamento de empresas e funcionários.

## Executar no Visual Studio Code

1. Abra a pasta do projeto no VS Code.
2. Crie e ative um ambiente virtual no terminal:

   ```powershell
   python -m venv .venv
   .venv\Scripts\Activate.ps1
   ```

3. Instale as dependências:

   ```powershell
   python -m pip install -r requirements.txt
   ```

4. Configure o MySQL conforme os valores em `banco.py` e crie as tabelas `usuario`, `empresa` e `funcionario` usadas pela aplicação. A tabela `funcionario` deve ter `id`, `nome`, `cargo`, `salario` e `id_empresa`, com `id_empresa` relacionado a `empresa.id`.
5. Pressione **F5** e escolha **Executar site Flask**. Quando o servidor iniciar, o VS Code abrirá o site no navegador padrão (normalmente em `http://127.0.0.1:5000`). Se não abrir automaticamente, copie o endereço exibido no terminal para o navegador.

O login e as operações de empresas e funcionários dependem de um servidor MySQL ativo e das tabelas configuradas. A API de funcionários está disponível em `/api/funcionario`; a interface visual de gerenciamento ainda está em desenvolvimento.
