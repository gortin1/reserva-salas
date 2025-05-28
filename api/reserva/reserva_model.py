from database import db
from datetime import datetime

class Reserva(db.Model):
    __tablename__ = 'reservas'

    id = db.Column(db.Integer, primary_key=True)
    turma_id = db.Column(db.Integer, nullable=False)
    sala = db.Column(db.String(50), nullable=False)
    data = db.Column(db.Date, nullable=False)
    hora_inicio = db.Column(db.Time, nullable=False)
    hora_fim = db.Column(db.Time, nullable=False)

    def __init__(
            self, 
            turma_id,  
            sala,
            data,
            hora_inicio,
            hora_fim

            ):

            self.turma_id = turma_id
            self.sala = sala
            self.data = data
            self.hora_inicio = hora_inicio
            self.hora_fim = hora_fim

    def to_dict(self):
            return {
                "id" : self.id,
                "turma_id" : self.turma_id,
                "sala" : self.sala,
                "data" : self.data.isoformat(),
                "hora_inicio" : self.hora_inicio.strftime("%H:%M"),
                "hora_fim" : self.hora_fim.strftime("%H:%M")
                
            }   

class ReservaNaoEncontrada(Exception):
    pass

def listar_reservas():
    reservas = Reserva.query.all()
    return [reserva.to_dict() for reserva in reservas]

def reserva_por_id(id):
    reserva = Reserva.query.get(id)

    if not reserva:
        raise ReservaNaoEncontrada(f"Reserva não encontrada.")
    return reserva.to_dict()

def adicionar_reserva(novos_dados):
    try:
        turma_id = novos_dados['turma_id']
        sala = novos_dados['sala']
        data_str = novos_dados['data']
        hora_inicio_str = novos_dados['hora_inicio']
        hora_fim_str = novos_dados['hora_fim']
    
        data = datetime.strptime(data_str, "%Y-%m-%d").date()
        hora_inicio = datetime.strptime(hora_inicio_str, "%H:%M").time()
        hora_fim = datetime.strptime(hora_fim_str, "%H:%M").time()

        nova_reserva = Reserva(
            turma_id = turma_id,
            sala = sala,
            data = data,
            hora_inicio = hora_inicio,
            hora_fim = hora_fim
        )

        db.session.add(nova_reserva)
        db.session.commit()
        return {'message': 'Reserva adicionada com sucesso.'}, 201
    
    except KeyError as e:
        return {'erro': 'Campo obrigatório ausente.', 'detalhes': str(e)}, 400
    except ValueError as e:
        return {'erro': 'Formato de data ou hora inválido.', 'detalhes': str(e)}, 400
    except Exception as e:
        return {'erro': 'Erro interno no servidor.', 'detalhes': str(e)}, 500

def atualizar_reserva(id, novos_dados):
    try:
        reserva = Reserva.query.get(id)
        if not reserva:
            raise ReservaNaoEncontrada(f"Reserva não encontrada.")
        
        turma_id = novos_dados['turma_id']
        sala = novos_dados['sala']
        data_str = novos_dados['data']
        hora_inicio_str = novos_dados['hora_inicio']
        hora_fim_str = novos_dados['hora_fim']

        data = datetime.strptime(data_str, "%Y-%m-%d").date()
        hora_inicio = datetime.strptime(hora_inicio_str, "%H:%M").time()
        hora_fim = datetime.strptime(hora_fim_str, "%H:%M").time()
        
        reserva.turma_id = turma_id
        reserva.sala = sala
        reserva.data = data
        reserva.hora_inicio = hora_inicio
        reserva.hora_fim = hora_fim
        
        db.session.commit()
        return {'message': 'Reserva atualizada com sucesso.'}, 200
    
    except KeyError as e:
        return {'erro': 'Campo obrigatório ausente.', 'detalhes': str(e)}, 400
    except ValueError as e:
        return {'erro': 'Formato de data ou hora inválido.', 'detalhes': str(e)}, 400
    except Exception as e:
        return {'erro': 'Erro interno no servidor.', 'detalhes': str(e)}, 500
        
def excluir_reserva(id):
    reserva = Reserva.query.get(id)
    if not reserva:
        raise ReservaNaoEncontrada(f"Reserva não encontrada.")

    db.session.delete(reserva)
    db.session.commit()
    return {'message': 'Reserva excluída com sucesso.'}, 200