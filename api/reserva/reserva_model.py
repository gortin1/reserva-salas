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
    nova_reserva = Reserva(
        turma_id = novos_dados['turma_id'],
        sala = novos_dados['sala'],
        data=datetime.strptime(novos_dados['data'], "%Y-%m-%d").date(),
        hora_inicio=datetime.strptime(novos_dados['hora_inicio'], "%H:%M").time(),
        hora_fim=datetime.strptime(novos_dados['hora_fim'], "%H:%M").time()
    )

    db.session.add(nova_reserva)
    db.session.commit()
    return {'message': 'Reserva adicionada com sucesso.'}, 201

def atualizar_reserva(id, novos_dados):
    reserva = Reserva.query.get(id)
    if not reserva:
        raise ReservaNaoEncontrada(f"Reserva não encontrada.")
    
    reserva.turma_id = novos_dados['turma_id']
    reserva.sala = novos_dados['sala']
    reserva.data = datetime.strptime(novos_dados['data'], "%Y-%m-%d").date()
    reserva.hora_inicio = datetime.strptime(novos_dados['hora_inicio'], "%H:%M").time()
    reserva.hora_fim = datetime.strptime(novos_dados['hora_fim'], "%H:%M").time()
    
    db.session.commit()
    return {'message': 'Reserva atualizada com sucesso.'}, 200
    
def excluir_reserva(id):
    reserva = Reserva.query.get(id)
    if not reserva:
        raise ReservaNaoEncontrada(f"Reserva não encontrada.")

    db.session.delete(reserva)
    db.session.commit()
    return {'message': 'Reserva excluída com sucesso.'}, 200