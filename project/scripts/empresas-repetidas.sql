SELECT
  REPLACE(cc.nombre, '.', '') as nombre,
  cc.id,
  (select count(*) from investigacion_investigacion where compania_id=cc.id) as investigaciones,
  (select count(*) from persona_trayectorialaboral trayectoria where trayectoria.compania_id=cc.id) as trayectoria,
  (select count(*) from compania_contacto contacto where contacto.compania_id=cc.id) as contacto,
  (select count(*) from compania_sucursales sucursales where sucursales.compania_id=cc.id) as sucursales
FROM compania_compania cc 
WHERE id IN (
  [RESULT FROM SELECT - BELOW -]
)
ORDER BY nombre;



SELECT 
  GROUP_CONCAT(IDS)
FROM
    (
      SELECT
        cc2.nombre,
        count(*) as total,
        GROUP_CONCAT(cc2.id) as IDS
      FROM compania_compania cc2
      WHERE es_cliente = 0
      GROUP BY cc2.nombre
      HAVING total > 1
      ORDER BY cc2.nombre
    ) t1
