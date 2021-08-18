from django.db import connection
from reportlab.lib.units import inch

class TextUtility:

	def __init__(self, canvas):
		self.canvas = canvas

	def align_right(self, text):
		max_inches = 7.3
		text_len = self.canvas.stringWidth(text)
		x_pos = max_inches * inch - text_len
		return x_pos

def get_trayectorias_por_persona(personas_id):
	# Equivalente to the filter, but with better performance since only executes one query
	# i.trayectoria = i.candidato.trayectorialaboral_set.filter(visible_en_status=True, status=True).select_related('compania', 'datosgenerales')

	with connection.cursor() as cursor:
		query = '''
			SELECT
				pt.persona_id,
				pt.puesto_final,
				pt.periodo_alta,
				pt.periodo_baja,
				pt.motivo_salida,
				pt.observaciones_generales,
				cc.nombre,
				po1.nombre,
				po1.puesto,
				po2.nombre,
				po2.puesto,
				pd.motivo_salida
			FROM
				persona_trayectorialaboral pt
			INNER JOIN compania_compania cc
				ON cc.id = pt.compania_id
			LEFT JOIN persona_opinion po1
				ON po1.trayectoriaLaboral_id=pt.id
				AND po1.categoria=2
			LEFT JOIN persona_opinion po2
				ON po2.trayectoriaLaboral_id=pt.id
				AND po2.categoria=1
			LEFT JOIN persona_datosgenerales pd
				ON pd.trayectoriaLaboral_id = pt.id
			WHERE
				pt.persona_id in %s
				AND pt.status = true
				AND pt.visible_en_status = true
		'''
		cursor.execute(query, [tuple(personas_id)])
		trayectorias = cursor.fetchall()
		response = {}
		for t in trayectorias:
			if not t[0] in response:
				response[t[0]] = []
	
			response[t[0]].append({
				'puesto_final': t[1],
				'periodo_alta': t[2],
				'periodo_baja': t[3],
				'motivo_salida': t[4],
				'observaciones_generales': t[5],
				'compania': t[6],
				'opinion_rh' : {
					'nombre': t[7],
					'puesto': t[8]
				},
				'opinion_jefe': {
					'nombre': t[9],
					'puesto': t[10]
				},
				'datosgenerales': {
					'motivo_salida': t[11]
				}
			})

		return response
