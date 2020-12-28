-- DELETE FROM compania_compania WHERE id IN (
--   SELECT id FROM (
    SELECT
      compania.id as id,
      (select count(*) as count_t from persona_trayectorialaboral trayectoria where trayectoria.compania_id=compania.id) as trayectoria,
      (select count(*) as count_i from investigacion_investigacion investigacion where investigacion.compania_id=compania.id) as investigacion,
      (select count(*) as count_t from compania_contacto contacto where contacto.compania_id=compania.id) as contacto,
      (select count(*) as count_i from compania_sucursales sucursales where sucursales.compania_id=compania.id) as sucursales
    FROM compania_compania compania
    WHERE compania.es_cliente = 0
    HAVING
      (select count(*) as count_t from persona_trayectorialaboral trayectoria where trayectoria.compania_id=compania.id) < 4
      AND (select count(*) as count_i from investigacion_investigacion investigacion where investigacion.compania_id=compania.id) < 4
      AND (select count(*) as count_t from compania_contacto contacto where contacto.compania_id=compania.id) < 4
      AND (select count(*) as count_i from compania_sucursales sucursales where sucursales.compania_id=compania.id) < 4
    ORDER BY trayectoria DESC, investigacion DESC, contacto DESC, sucursales DESC, compania.id
--   ) AS companies_to_delete ORDER BY id
-- );
