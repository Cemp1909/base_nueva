-- ===== TIPOS Y EXTENSIONES OPCIONALES =====
-- CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- =====================================================
-- CATEGORÍAS DE PRODUCTOS (cada una con stock >= 0)
-- =====================================================
CREATE TABLE IF NOT EXISTS blusas (
    id SERIAL PRIMARY KEY,
    talla VARCHAR(10),
    color VARCHAR(50),
    tipo  VARCHAR(20),
    imagen VARCHAR(255),
    stock INTEGER NOT NULL DEFAULT 0,
    CONSTRAINT ck_blusas_stock_nonneg CHECK (stock >= 0)
);

CREATE INDEX IF NOT EXISTS idx_blusas_color ON blusas(color);
CREATE INDEX IF NOT EXISTS idx_blusas_talla ON blusas(talla);

CREATE TABLE IF NOT EXISTS blusones (
    id SERIAL PRIMARY KEY,
    talla VARCHAR(10),
    color VARCHAR(50),
    tipo  VARCHAR(20),
    imagen VARCHAR(255),
    stock INTEGER NOT NULL DEFAULT 0,
    CONSTRAINT ck_blusones_stock_nonneg CHECK (stock >= 0)
);

CREATE TABLE IF NOT EXISTS vestidos (
    id SERIAL PRIMARY KEY,
    talla VARCHAR(10),
    color VARCHAR(50),
    tipo  VARCHAR(20),
    imagen VARCHAR(255),
    stock INTEGER NOT NULL DEFAULT 0,
    CONSTRAINT ck_vestidos_stock_nonneg CHECK (stock >= 0)
);

CREATE TABLE IF NOT EXISTS enterizos (
    id SERIAL PRIMARY KEY,
    talla VARCHAR(10),
    color VARCHAR(50),
    tipo  VARCHAR(20),
    imagen VARCHAR(255),
    stock INTEGER NOT NULL DEFAULT 0,
    CONSTRAINT ck_enterizos_stock_nonneg CHECK (stock >= 0)
);

CREATE TABLE IF NOT EXISTS jeans (
    id SERIAL PRIMARY KEY,
    talla VARCHAR(10),
    color VARCHAR(50),
    tipo  VARCHAR(20),
    imagen VARCHAR(255),
    stock INTEGER NOT NULL DEFAULT 0,
    CONSTRAINT ck_jeans_stock_nonneg CHECK (stock >= 0)
);

CREATE TABLE IF NOT EXISTS vestidosgala (
    id SERIAL PRIMARY KEY,
    talla VARCHAR(10),
    color VARCHAR(50),
    tipo  VARCHAR(20),
    imagen VARCHAR(255),
    stock INTEGER NOT NULL DEFAULT 0,
    CONSTRAINT ck_vestidosgala_stock_nonneg CHECK (stock >= 0)
);

-- =====================================================
-- COMPRAS (pedidos simples)
-- =====================================================
CREATE TABLE IF NOT EXISTS compras (
    id SERIAL PRIMARY KEY,
    nombre_cliente VARCHAR(100) NOT NULL,
    direccion VARCHAR(200) NOT NULL,
    telefono VARCHAR(20) NOT NULL,
    producto VARCHAR(100) NOT NULL,
    cantidad INTEGER NOT NULL,
    total NUMERIC(12,2) NOT NULL,
    fecha TIMESTAMP DEFAULT NOW(),
    CONSTRAINT ck_compras_cantidad_pos CHECK (cantidad > 0)
);

-- =====================================================
-- USUARIOS
-- =====================================================
CREATE TABLE IF NOT EXISTS usuarios (
    id SERIAL PRIMARY KEY,
    nombre_usuario VARCHAR(50) UNIQUE NOT NULL,
    contrasena_hash VARCHAR(255) NOT NULL,
    nombre_completo VARCHAR(100),
    email VARCHAR(120) UNIQUE NOT NULL,
    telefono VARCHAR(20),
    direccion VARCHAR(200),
    fecha_registro TIMESTAMP DEFAULT NOW(),
    rol VARCHAR(20) DEFAULT 'cliente'   -- 'admin' | 'cliente' | 'vendedor'
);

CREATE INDEX IF NOT EXISTS idx_usuarios_rol ON usuarios(rol);

-- =====================================================
-- TRANSACCIONES
-- =====================================================
CREATE TABLE IF NOT EXISTS transactions (
    id SERIAL PRIMARY KEY,
    tx_id VARCHAR(64) UNIQUE,
    amount NUMERIC(12,2) NOT NULL,
    currency VARCHAR(8) DEFAULT 'USD',
    status VARCHAR(20) DEFAULT 'pending',   -- pending | success | failed
    method VARCHAR(20) DEFAULT 'card_fake',
    card_last4 VARCHAR(4),
    card_brand VARCHAR(20),
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_transactions_status ON transactions(status);
CREATE INDEX IF NOT EXISTS idx_transactions_created_at ON transactions(created_at);
