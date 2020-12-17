SELECT
  compania.id,
  REPLACE(compania.nombre, ',', ' ') as nombre,
  (select count(*) from investigacion_investigacion where compania_id=compania.id) as investigaciones
FROM compania_compania compania
LEFT JOIN compania_contacto contacto
  ON compania.id = contacto.compania_id
LEFT JOIN compania_sucursales sucursal
  ON compania.id = sucursal.compania_id
LEFT JOIN persona_trayectorialaboral trayectoria
  ON compania.id = trayectoria.compania_id
WHERE compania.telefono='' 
  AND compania.telefono_alt='' 
  AND compania.es_cliente = 0 
  AND contacto.id IS NULL
  AND sucursal.id IS NULL
  AND trayectoria.id IS NULL
ORDER BY compania.nombre
;
