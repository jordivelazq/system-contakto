SELECT
  compania.id,
  REPLACE(REPLACE(compania.nombre, ',', ' '), '"', '') as nombre,
  (select count(*) as count_i from investigacion_investigacion investigacion where investigacion.compania_id=compania.id) as candidatos,
  (select count(*) as count_t from persona_trayectorialaboral trayectoria where trayectoria.compania_id=compania.id) as trayectorias
FROM compania_compania compania
WHERE compania.es_cliente = 0 
HAVING trayectorias < 4
 AND candidatos < 4
ORDER BY trayectorias, candidatos, nombre
;
