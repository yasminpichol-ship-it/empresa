from flask import jsonify, render_template, request

from banco import conectar_banco


def registrar_rotas_funcionario(app):
    @app.route("/funcionario")
    def pagina_funcionario():
        return render_template("funcionario.html")

    @app.route("/api/funcionario", methods=["GET"])
    def listar_funcionario():
        try:
            conexao = conectar_banco()
            cursor = conexao.cursor(dictionary=True)
            sql = """
                SELECT f.id, f.nome, f.cargo, f.salario, f.id_empresa,
                       e.nome AS empresa_nome
                FROM funcionario f
                INNER JOIN empresa e ON f.id_empresa = e.id
                ORDER BY f.id DESC
            """
            cursor.execute(sql)
            funcionarios = cursor.fetchall()
            cursor.close()
            conexao.close()
            return jsonify(funcionarios), 200
        except Exception as erro:
            print("Erro ao listar funcionários:", erro)
            return jsonify({"erro": "Erro ao buscar funcionários"}), 500

    @app.route("/api/funcionario/<int:id_funcionario>", methods=["GET"])
    def obter_funcionario(id_funcionario):
        try:
            conexao = conectar_banco()
            cursor = conexao.cursor(dictionary=True)
            sql = """
                SELECT id, nome, cargo, salario, id_empresa
                FROM funcionario
                WHERE id = %s
            """
            cursor.execute(sql, (id_funcionario,))
            funcionario = cursor.fetchone()
            cursor.close()
            conexao.close()

            if not funcionario:
                return jsonify({"erro": "Funcionário não encontrado"}), 404

            return jsonify(funcionario), 200
        except Exception as erro:
            print("Erro ao obter funcionário:", erro)
            return jsonify({"erro": "Erro interno no servidor"}), 500

    @app.route("/api/funcionario", methods=["POST"])
    def criar_funcionario():
        dados = request.get_json(silent=True)
        if not isinstance(dados, dict):
            return jsonify({"erro": "Envie os dados do funcionário em JSON."}), 400

        nome = dados.get("nome")
        cargo = dados.get("cargo")
        salario = dados.get("salario")
        id_empresa = dados.get("id_empresa")

        if (
            not isinstance(nome, str)
            or not nome.strip()
            or not isinstance(cargo, str)
            or not cargo.strip()
            or salario is None
            or id_empresa is None
        ):
            return jsonify({"erro": "Todos os campos obrigatórios devem ser preenchidos!"}), 400

        try:
            conexao = conectar_banco()
            cursor = conexao.cursor()
            sql = """
                INSERT INTO funcionario (nome, cargo, salario, id_empresa)
                VALUES (%s, %s, %s, %s)
            """
            cursor.execute(sql, (nome.strip(), cargo.strip(), salario, id_empresa))
            conexao.commit()
            novo_id = cursor.lastrowid
            cursor.close()
            conexao.close()

            return jsonify({
                "mensagem": "Funcionário cadastrado com sucesso!",
                "id": novo_id,
            }), 201
        except Exception as erro:
            print("Erro ao cadastrar funcionário:", erro)
            return jsonify({"erro": "Erro ao cadastrar funcionário"}), 500

    @app.route("/api/funcionario/<int:id_funcionario>", methods=["PUT"])
    def atualizar_funcionario(id_funcionario):
        dados = request.get_json(silent=True)
        if not isinstance(dados, dict):
            return jsonify({"erro": "Envie os dados do funcionário em JSON."}), 400

        nome = dados.get("nome")
        cargo = dados.get("cargo")
        salario = dados.get("salario")
        id_empresa = dados.get("id_empresa")

        if (
            not isinstance(nome, str)
            or not nome.strip()
            or not isinstance(cargo, str)
            or not cargo.strip()
            or salario is None
            or id_empresa is None
        ):
            return jsonify({"erro": "Todos os campos obrigatórios devem ser preenchidos!"}), 400

        try:
            conexao = conectar_banco()
            cursor = conexao.cursor()
            sql = """
                UPDATE funcionario
                SET nome = %s, cargo = %s, salario = %s, id_empresa = %s
                WHERE id = %s
            """
            cursor.execute(
                sql,
                (nome.strip(), cargo.strip(), salario, id_empresa, id_funcionario),
            )
            conexao.commit()
            linhas_afetadas = cursor.rowcount
            cursor.close()
            conexao.close()

            if linhas_afetadas == 0:
                return jsonify({"erro": "Funcionário não encontrado"}), 404

            return jsonify({"mensagem": "Funcionário atualizado com sucesso!"}), 200
        except Exception as erro:
            print("Erro ao atualizar funcionário:", erro)
            return jsonify({"erro": "Erro ao atualizar funcionário"}), 500

    @app.route("/api/funcionario/<int:id_funcionario>", methods=["DELETE"])
    def deletar_funcionario(id_funcionario):
        try:
            conexao = conectar_banco()
            cursor = conexao.cursor()
            cursor.execute(
                "DELETE FROM funcionario WHERE id = %s",
                (id_funcionario,),
            )
            conexao.commit()
            linhas_afetadas = cursor.rowcount
            cursor.close()
            conexao.close()

            if linhas_afetadas == 0:
                return jsonify({"erro": "Funcionário não encontrado"}), 404

            return jsonify({"mensagem": "Funcionário excluído com sucesso!"}), 200
        except Exception as erro:
            print("Erro ao excluir funcionário:", erro)
            return jsonify({"erro": "Erro interno ao excluir funcionário"}), 500
