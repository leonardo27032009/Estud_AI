from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import google.generativeai as genai
import os

app = Flask(__name__)
CORS(app)

# Configure sua chave de API do Gemini
GOOGLE_API_KEY = "AIzaSyBZd8MDuFNpqxOfcFXJOh4TnE3RF0tppYA"
print(os.environ)
genai.configure(api_key=GOOGLE_API_KEY)

# Selecione o modelo Gemini que você deseja usar
model = genai.GenerativeModel("gemini-2.0-flash")

gemini_disponivel = True if GOOGLE_API_KEY else False
if not gemini_disponivel:
    print("Erro: A variável de ambiente GOOGLE_API_KEY não está configurada.")
else:
    print("Chave de API do Gemini configurada com sucesso.")


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/gerar_questao', methods=['POST'])
def gerar_questao_endpoint():
    data = request.get_json()
    materia = data.get('materia')
    unidade = data.get('unidade')
    dificuldade = data.get('dificuldade')
    
    if not all([materia, unidade, dificuldade]):
        return jsonify({'erro': 'Parâmetros incompletos'}), 400

    if gemini_disponivel:
        prompt = (
            f"Gere uma pergunta de múltipla escolha sobre {materia}, especificamente sobre o tema '{unidade}', com um nível de dificuldade {dificuldade}. "
            f"A pergunta deve ter quatro opções (A, B, C, D) e indicar a resposta correta. "
            f"Formate a resposta da seguinte maneira:\n\n"
            f"Pergunta: [texto da pergunta]\n"

            f"A) [opção A]\n"

            f"B) [opção B]\n"

            f"C) [opção C]\n"

            f"D) [opção D]\n"

            f"Resposta correta: [Letra da opção correta] Explicação:"
        )

        try:
            response = model.generate_content(prompt)
            texto_gerado = response.text.strip()
            print(f"Questão gerada pelo Gemini:\n{texto_gerado}")
            return jsonify({'questao': texto_gerado})

        except Exception as e:
            erro = f"Erro ao gerar a questão com o Gemini: {e}"
            print(f"Detalhes do erro do Gemini: {e}")
            return jsonify({'erro': 'Ocorreu um erro ao gerar a questão com o Gemini.'}), 500
    else:
        return jsonify({'erro': e}), 503


if __name__ == "__main__":
    app.run(debug=True)