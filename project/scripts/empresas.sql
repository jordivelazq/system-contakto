SELECT
  compania.id,
  REPLACE(REPLACE(REPLACE(compania.nombre, ',', ' '), '"', ''), '  ', ' ') AS Nombre
FROM compania_compania compania
WHERE compania.status=1
ORDER BY compania.nombre
;
