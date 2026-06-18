from flask import Flask, jsonify

from conectar.funcaoConectar import conectar


app = Flask(__name__)

#ROTAS PARA Serie_A
##ROTA GET
##############################################
@app.route("/Serie_A", methods=["GET"])
def listar_SerieA():
    conn = conectar()
    #conn.execute("PRAGMA foreign_keys = ON") #ativa as chaves estrangeiras das tabelas (pois, não é ativado por padrão)
    cursor = conn.cursor()
    cursor.execute("SELECT idSerie_A, NomeClube, PontosClube, PossicaoClube, JogosClube, SaldoGols, VitoriasClube, EmpateClube, DerrotaClube, GolsProClube, GolsContraClube  FROM Serie_A")
    dados = [
        {"idSerie_A": row[0], "NomeClube": row[1], "PontosClube": row[2], "PossicaoClube": row[3], "JogosClube": row[4], "SaldoGols": row[5], "VitoriasClube": row[6], "EmpateClube": row[7], "DerrotaClube": row[8], "GolsProClube": row[9], "GolsContraClube": row[10]  }
        for row in cursor.fetchall()
    ]
    conn.close()
    return jsonify(dados)

##ROTA INSERT
#############################################

from flask import request, jsonify, abort
@app.route("/Serie_A", methods=["POST"])
def criar_SerieA():
    dados = request.get_json(silent=True)
    if not dados:
        abort(400, description="JSON inválido ou ausente")
        

    # Validação de campos obrigatórios
    campos_obrigatorios = {"NomeClube", "PontosClube", "PossicaoClube", "JogosClube", "SaldoGols", "VitoriasClube", "EmpateClube", "DerrotaClube", "GolsProClube", "GolsContraClube"}
    if not campos_obrigatorios.issubset(dados.keys()):
        abort(400, description=f"Campos obrigatórios: {', '.join(campos_obrigatorios)}")

    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO Serie_A (NomeClube, PontosClube, PossicaoClube, JogosClube, SaldoGols, VitoriasClube, EmpateClube, DerrotaClube, GolsProClube, GolsContraClube) "
        "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
        (dados["NomeClube"], dados["PontosClube"], dados["PossicaoClube"], dados["JogosClube"], dados["SaldoGols"], dados["VitoriasClube"], dados["EmpateClube"], dados["DerrotaClube"], dados["GolsProClube"], dados["GolsContraClube"])
    )
    conn.commit()
    novo_id = cursor.lastrowid
    conn.close()

    # 201 Created + Location do recurso recém‑criado
    resposta = jsonify({"idSerie_A": novo_id, **dados})
    resposta.status_code = 201
    resposta.headers["Location"] = f"/Serie_A/{novo_id}"
    return resposta

##ROTA UPDATE
#############################################
@app.route("/Serie_A/<int:idSerie_A>", methods=["PUT", "PATCH"])
def atualizar_SerieA(idSerie_A):
    dados = request.get_json(silent=True)
    if not dados:
        abort(400, description="JSON inválido ou ausente")

    # Para PUT, garanta que todos os campos estejam presentes
    if request.method == "PUT":
        campos_esperados = {"NomeClube", "PontosClube", "PossicaoClube", "JogosClube", "SaldoGols", "VitoriasClube", "EmpateClube", "DerrotaClube", "GolsProClube", "GolsContraClube"}
        if not campos_esperados.issubset(dados.keys()):
            abort(400, description=f"PUT requer todos os campos: {', '.join(campos_esperados)}")

    # Monta dinamicamente o SQL somente com os campos enviados
    campos_validos = {"NomeClube", "PontosClube", "PossicaoClube", "JogosClube", "SaldoGols", "VitoriasClube", "EmpateClube", "DerrotaClube", "GolsProClube", "GolsContraClube"}
    set_clauses = []
    valores = []
    for campo in campos_validos & dados.keys():
        set_clauses.append(f"{campo} = ?")
        valores.append(dados[campo])

    if not set_clauses:
        abort(400, description="Nenhum campo válido para atualizar")

    valores.append(idSerie_A)  # último parâmetro é o WHERE

    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        f"UPDATE Serie_A SET {', '.join(set_clauses)} WHERE idSerie_A = ?",
        tuple(valores)
    )
    conn.commit()

    if cursor.rowcount == 0:
        conn.close()
        abort(404, description="Clube não encontrado")

    conn.close()
    # 204 = No Content, mas você pode devolver 200 com o JSON atualizado se preferir
    return ("", 204)


##ROTA DELETE
#############################################
from flask import jsonify, abort

@app.route("/Serie_A/<int:idSerie_A>", methods=["DELETE"])
def deletar_SerieA(idSerie_A):
    conn = conectar()
    cursor = conn.cursor()

    # tenta apagar o registro informado
    cursor.execute("DELETE FROM Serie_A WHERE idSerie_A = ?", (idSerie_A,))
    conn.commit()

    # cursor.rowcount informa quantas linhas foram afetadas
    if cursor.rowcount == 0:
        conn.close()
        # nenhum registro com esse ID → devolve 404
        abort(404, description="Clube não encontrado")

    conn.close()
    # 204 = No Content (padrão para deleções bem‑sucedidas)
    return ("", 204)




#ROTAS PARA Serie_B
##ROTA GET
##############################################
@app.route("/Serie_B", methods=["GET"])
def listar_SerieB():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT idSerie_B, NomeClube, PontosClube, PossicaoClube, JogosClube, SaldoGols, VitoriasClube, EmpateClube, DerrotaClube, GolsProClube, GolsContraClube FROM Serie_B")

    dados = [
        {
            "idSerie_B": row[0],
            "NomeClube": row[1],
            "PontosClube": row[2],
            "PossicaoClube": row[3],
            "JogosClube": row[4],
            "SaldoGols": row[5],
            "VitoriasClube": row[6],
            "EmpateClube": row[7],
            "DerrotaClube": row[8],
            "GolsProClube": row[9],
            "GolsContraClube": row[10]
        }
        for row in cursor.fetchall()
    ]

    conn.close()
    return jsonify(dados)

##ROTA INSERT
##############################################
@app.route("/Serie_B", methods=["POST"])
def criar_SerieB():
    dados = request.get_json(silent=True)

    if not dados:
        abort(400, description="JSON inválido ou ausente")

    campos_obrigatorios = {
        "NomeClube",
        "PontosClube",
        "PossicaoClube",
        "JogosClube",
        "SaldoGols",
        "VitoriasClube",
        "EmpateClube",
        "DerrotaClube",
        "GolsProClube",
        "GolsContraClube"
    }

    if not campos_obrigatorios.issubset(dados.keys()):
        abort(400, description=f"Campos obrigatórios: {', '.join(campos_obrigatorios)}")

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO Serie_B (NomeClube, PontosClube, PossicaoClube, JogosClube, SaldoGols, VitoriasClube, EmpateClube, DerrotaClube, GolsProClube, GolsContraClube) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
        (
            dados["NomeClube"],
            dados["PontosClube"],
            dados["PossicaoClube"],
            dados["JogosClube"],
            dados["SaldoGols"],
            dados["VitoriasClube"],
            dados["EmpateClube"],
            dados["DerrotaClube"],
            dados["GolsProClube"],
            dados["GolsContraClube"]
        )
    )

    conn.commit()
    novo_id = cursor.lastrowid
    conn.close()

    resposta = jsonify({"idSerie_B": novo_id, **dados})
    resposta.status_code = 201
    resposta.headers["Location"] = f"/Serie_B/{novo_id}"

    return resposta

##ROTA UPDATE
##############################################
@app.route("/Serie_B/<int:idSerie_B>", methods=["PUT", "PATCH"])
def atualizar_SerieB(idSerie_B):
    dados = request.get_json(silent=True)

    if not dados:
        abort(400, description="JSON inválido ou ausente")

    if request.method == "PUT":
        campos_esperados = {
            "NomeClube",
            "PontosClube",
            "PossicaoClube",
            "JogosClube",
            "SaldoGols",
            "VitoriasClube",
            "EmpateClube",
            "DerrotaClube",
            "GolsProClube",
            "GolsContraClube"
        }

        if not campos_esperados.issubset(dados.keys()):
            abort(400, description=f"PUT requer todos os campos: {', '.join(campos_esperados)}")

    campos_validos = {
        "NomeClube",
        "PontosClube",
        "PossicaoClube",
        "JogosClube",
        "SaldoGols",
        "VitoriasClube",
        "EmpateClube",
        "DerrotaClube",
        "GolsProClube",
        "GolsContraClube"
    }

    set_clauses = []
    valores = []

    for campo in campos_validos & dados.keys():
        set_clauses.append(f"{campo} = ?")
        valores.append(dados[campo])

    if not set_clauses:
        abort(400, description="Nenhum campo válido para atualizar")

    valores.append(idSerie_B)

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute(
        f"UPDATE Serie_B SET {', '.join(set_clauses)} WHERE idSerie_B = ?",
        tuple(valores)
    )

    conn.commit()

    if cursor.rowcount == 0:
        conn.close()
        abort(404, description="Clube não encontrado")

    conn.close()

    return ("", 204)

##ROTA DELETE
##############################################
@app.route("/Serie_B/<int:idSerie_B>", methods=["DELETE"])
def deletar_SerieB(idSerie_B):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM Serie_B WHERE idSerie_B = ?",
        (idSerie_B,)
    )

    conn.commit()

    if cursor.rowcount == 0:
        conn.close()
        abort(404, description="Clube não encontrado")

    conn.close()

    return ("", 204)





#ROTAS PARA Serie_C
##ROTA GET
##############################################
@app.route("/Serie_C", methods=["GET"])
def listar_SerieC():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT idSerie_C, NomeClube, PontosClube, PossicaoClube, JogosClube, SaldoGols, VitoriasClube, EmpateClube, DerrotaClube, GolsProClube, GolsContraClube FROM Serie_C")

    dados = [
        {
            "idSerie_C": row[0],
            "NomeClube": row[1],
            "PontosClube": row[2],
            "PossicaoClube": row[3],
            "JogosClube": row[4],
            "SaldoGols": row[5],
            "VitoriasClube": row[6],
            "EmpateClube": row[7],
            "DerrotaClube": row[8],
            "GolsProClube": row[9],
            "GolsContraClube": row[10]
        }
        for row in cursor.fetchall()
    ]

    conn.close()
    return jsonify(dados)

##ROTA INSERT
##############################################
@app.route("/Serie_C", methods=["POST"])
def criar_SerieC():
    dados = request.get_json(silent=True)

    if not dados:
        abort(400, description="JSON inválido ou ausente")

    campos_obrigatorios = {
        "NomeClube",
        "PontosClube",
        "PossicaoClube",
        "JogosClube",
        "SaldoGols",
        "VitoriasClube",
        "EmpateClube",
        "DerrotaClube",
        "GolsProClube",
        "GolsContraClube"
    }

    if not campos_obrigatorios.issubset(dados.keys()):
        abort(400, description=f"Campos obrigatórios: {', '.join(campos_obrigatorios)}")

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO Serie_C (NomeClube, PontosClube, PossicaoClube, JogosClube, SaldoGols, VitoriasClube, EmpateClube, DerrotaClube, GolsProClube, GolsContraClube) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
        (
            dados["NomeClube"],
            dados["PontosClube"],
            dados["PossicaoClube"],
            dados["JogosClube"],
            dados["SaldoGols"],
            dados["VitoriasClube"],
            dados["EmpateClube"],
            dados["DerrotaClube"],
            dados["GolsProClube"],
            dados["GolsContraClube"]
        )
    )

    conn.commit()
    novo_id = cursor.lastrowid
    conn.close()

    resposta = jsonify({"idSerie_C": novo_id, **dados})
    resposta.status_code = 201
    resposta.headers["Location"] = f"/Serie_C/{novo_id}"

    return resposta

##ROTA UPDATE
##############################################
@app.route("/Serie_C/<int:idSerie_C>", methods=["PUT", "PATCH"])
def atualizar_SerieC(idSerie_C):
    dados = request.get_json(silent=True)

    if not dados:
        abort(400, description="JSON inválido ou ausente")

    if request.method == "PUT":
        campos_esperados = {
            "NomeClube",
            "PontosClube",
            "PossicaoClube",
            "JogosClube",
            "SaldoGols",
            "VitoriasClube",
            "EmpateClube",
            "DerrotaClube",
            "GolsProClube",
            "GolsContraClube"
        }

        if not campos_esperados.issubset(dados.keys()):
            abort(400, description=f"PUT requer todos os campos: {', '.join(campos_esperados)}")

    campos_validos = {
        "NomeClube",
        "PontosClube",
        "PossicaoClube",
        "JogosClube",
        "SaldoGols",
        "VitoriasClube",
        "EmpateClube",
        "DerrotaClube",
        "GolsProClube",
        "GolsContraClube"
    }

    set_clauses = []
    valores = []

    for campo in campos_validos & dados.keys():
        set_clauses.append(f"{campo} = ?")
        valores.append(dados[campo])

    if not set_clauses:
        abort(400, description="Nenhum campo válido para atualizar")

    valores.append(idSerie_C)

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute(
        f"UPDATE Serie_C SET {', '.join(set_clauses)} WHERE idSerie_C = ?",
        tuple(valores)
    )

    conn.commit()

    if cursor.rowcount == 0:
        conn.close()
        abort(404, description="Clube não encontrado")

    conn.close()

    return ("", 204)

##ROTA DELETE
##############################################
@app.route("/Serie_C/<int:idSerie_C>", methods=["DELETE"])
def deletar_SerieC(idSerie_C):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM Serie_C WHERE idSerie_C = ?",
        (idSerie_C,)
    )

    conn.commit()

    if cursor.rowcount == 0:
        conn.close()
        abort(404, description="Clube não encontrado")

    conn.close()

    return ("", 204)







    #ROTAS PARA Serie_D
##ROTA GET
##############################################
@app.route("/Serie_D", methods=["GET"])
def listar_SerieD():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT idSerie_D, NomeClube, PontosClube, PossicaoClube, JogosClube, SaldoGols, VitoriasClube, EmpateClube, DerrotaClube, GolsProClube, GolsContraClube FROM Serie_D")

    dados = [
        {
            "idSerie_D": row[0],
            "NomeClube": row[1],
            "PontosClube": row[2],
            "PossicaoClube": row[3],
            "JogosClube": row[4],
            "SaldoGols": row[5],
            "VitoriasClube": row[6],
            "EmpateClube": row[7],
            "DerrotaClube": row[8],
            "GolsProClube": row[9],
            "GolsContraClube": row[10]
        }
        for row in cursor.fetchall()
    ]

    conn.close()
    return jsonify(dados)

##ROTA INSERT
##############################################
@app.route("/Serie_D", methods=["POST"])
def criar_SerieD():
    dados = request.get_json(silent=True)

    if not dados:
        abort(400, description="JSON inválido ou ausente")

    campos_obrigatorios = {
        "NomeClube",
        "PontosClube",
        "PossicaoClube",
        "JogosClube",
        "SaldoGols",
        "VitoriasClube",
        "EmpateClube",
        "DerrotaClube",
        "GolsProClube",
        "GolsContraClube"
    }

    if not campos_obrigatorios.issubset(dados.keys()):
        abort(400, description=f"Campos obrigatórios: {', '.join(campos_obrigatorios)}")

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO Serie_D (NomeClube, PontosClube, PossicaoClube, JogosClube, SaldoGols, VitoriasClube, EmpateClube, DerrotaClube, GolsProClube, GolsContraClube) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
        (
            dados["NomeClube"],
            dados["PontosClube"],
            dados["PossicaoClube"],
            dados["JogosClube"],
            dados["SaldoGols"],
            dados["VitoriasClube"],
            dados["EmpateClube"],
            dados["DerrotaClube"],
            dados["GolsProClube"],
            dados["GolsContraClube"]
        )
    )

    conn.commit()
    novo_id = cursor.lastrowid
    conn.close()

    resposta = jsonify({"idSerie_D": novo_id, **dados})
    resposta.status_code = 201
    resposta.headers["Location"] = f"/Serie_D/{novo_id}"

    return resposta

##ROTA UPDATE
##############################################
@app.route("/Serie_D/<int:idSerie_D>", methods=["PUT", "PATCH"])
def atualizar_SerieD(idSerie_D):
    dados = request.get_json(silent=True)

    if not dados:
        abort(400, description="JSON inválido ou ausente")

    if request.method == "PUT":
        campos_esperados = {
            "NomeClube",
            "PontosClube",
            "PossicaoClube",
            "JogosClube",
            "SaldoGols",
            "VitoriasClube",
            "EmpateClube",
            "DerrotaClube",
            "GolsProClube",
            "GolsContraClube"
        }

        if not campos_esperados.issubset(dados.keys()):
            abort(400, description=f"PUT requer todos os campos: {', '.join(campos_esperados)}")

    campos_validos = {
        "NomeClube",
        "PontosClube",
        "PossicaoClube",
        "JogosClube",
        "SaldoGols",
        "VitoriasClube",
        "EmpateClube",
        "DerrotaClube",
        "GolsProClube",
        "GolsContraClube"
    }

    set_clauses = []
    valores = []

    for campo in campos_validos & dados.keys():
        set_clauses.append(f"{campo} = ?")
        valores.append(dados[campo])

    if not set_clauses:
        abort(400, description="Nenhum campo válido para atualizar")

    valores.append(idSerie_D)

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute(
        f"UPDATE Serie_D SET {', '.join(set_clauses)} WHERE idSerie_D = ?",
        tuple(valores)
    )

    conn.commit()

    if cursor.rowcount == 0:
        conn.close()
        abort(404, description="Clube não encontrado")

    conn.close()

    return ("", 204)

##ROTA DELETE
##############################################
@app.route("/Serie_D/<int:idSerie_D>", methods=["DELETE"])
def deletar_SerieD(idSerie_D):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM Serie_D WHERE idSerie_D = ?",
        (idSerie_D,)
    )

    conn.commit()

    if cursor.rowcount == 0:
        conn.close()
        abort(404, description="Clube não encontrado")

    conn.close()

    return ("", 204)



if __name__ == "__main__":
    app.run(debug=True)