-- Archivos de ejemplo. Ajusta el DDL a tus modelos reales si usas Flask-Migrate/Alembic.
-- Puedes dejar este archivo vacío si ya manejas migraciones con Alembic.

-- CREATE TABLE IF NOT EXISTS usuarios (...);
-- CREATE TABLE IF NOT EXISTS compras  (...);
-- etc.

-- Ejemplo mínimo de tabla productos (solo demo, cámbiala según tus modelos)
CREATE TABLE IF NOT EXISTS demo_productos (
  id SERIAL PRIMARY KEY,
  nombre TEXT NOT NULL,
  precio NUMERIC(10,2) NOT NULL DEFAULT 0,
  stock INTEGER NOT NULL DEFAULT 0,
  imagen_url TEXT
);

INSERT INTO demo_productos (nombre, precio, stock, imagen_url)
VALUES
('Blusa Lila Básica', 45000, 10, 'https://example.com/img/blusa-lila.jpg'),
('Vestido Gala Azul', 180000, 5, 'https://example.com/img/gala-azul.jpg')
ON CONFLICT DO NOTHING;
