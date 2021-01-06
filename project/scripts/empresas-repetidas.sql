SELECT
  REPLACE(cc.nombre, '.', '') as nombre,
  cc.id,
  (select count(*) from investigacion_investigacion where compania_id=cc.id) as investigaciones 
FROM compania_compania cc 
WHERE id IN (
  [RESULT FROM SELECT - BELOW -]
)
ORDER BY investigaciones, nombre;



SELECT 
  GROUP_CONCAT(IDS)
FROM
    (
      SELECT
        cc2.nombre,
        count(*) as total,
        GROUP_CONCAT(cc2.id) as IDS  
      FROM compania_compania cc2
      GROUP BY cc2.nombre
      HAVING total > 1
      ORDER BY cc2.nombre
    ) t1
