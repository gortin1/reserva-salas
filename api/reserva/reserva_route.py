from flask import Blueprint, request, jsonify
import requests
from api.reserva.reserva_model import ReservaNaoEncontrada, reserva_por_id, listar_reservas, adicionar_reserva, atualizar_reserva, excluir_reserva

reservas_blueprint = Blueprint("reservas", __name__)

def validar_turma(turma_id):
    response = requests.get(f"http://api-gestao-escolar:5000/api/turmas/{turma_id}")
    return response.status_code == 200

@reservas_blueprint.route('/reservas', methods = ['POST'])
def create_reserva():
    try:
        dados = request.json
        turma_id = dados.get("turma_id")

        if not validar_turma(turma_id):
            return jsonify({'erro': 'Turma não encontrada'}), 404

        response, status_code = adicionar_reserva(dados)
        return jsonify(response), status_code
    
    except Exception as e:
        return jsonify({'erro': 'Erro interno no servidor.', 'detalhes': str(e)}), 500

@reservas_blueprint.route('/reservas', methods = ['GET'])
def get_reservas():
    return jsonify(listar_reservas()), 200

@reservas_blueprint.route('/reservas/<int:id>', methods = ['GET'])
def get_reserva(id):
    try:
        reserva = reserva_por_id(id)
        return jsonify(reserva), 200
    except ReservaNaoEncontrada:
        return jsonify({'erro': 'Reserva não encontrada.'}), 404
    
@reservas_blueprint.route('/reservas/<int:id>', methods = ['PUT'])
def update_reserva(id):
    dados = request.json
    turma_id = dados.get("turma_id")

    if not validar_turma(turma_id):
        return jsonify({'erro': 'Turma não encontrada'}), 404
    
    try: 
        atualizar_reserva(id, dados)
        reserva_atualizada = reserva_por_id(id)
        return jsonify({
            'message': 'Reserva atualizada com sucesso.',
            'reserva': reserva_atualizada
        }), 200
    except ReservaNaoEncontrada:
        return jsonify({'erro': 'Reserva não encontrada.'}), 404
    
@reservas_blueprint.route('/reservas/<int:id>', methods=['DELETE'])
def delete_reserva(id):
    try:
        excluir_reserva(id)
        return jsonify({'message': 'Reserva excluída com sucesso.'}), 200
    except ReservaNaoEncontrada:
        return jsonify({'erro': 'Reserva não encontrada.'}), 404
