import sqlite3


# open database return conn e cursor
def db():
    conn = sqlite3.connect("./db/web.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    return conn, cursor


# list store sql command create all table app
appTable = []


# table app
app = \
"""
CREATE TABLE IF NOT EXISTS app (
    id     INTEGER PRIMARY KEY,
    nome   TEXT,
    imagem BLOB
);
"""
appTable.append(app)


# table cart
cart = \
"""
CREATE TABLE IF NOT EXISTS carrinho (
    id         INTEGER PRIMARY KEY,
    id_cliente INTEGER,
    id_produto INTEGER,
    qtde       INTEGER,
    prod_selec TEXT
);
"""
appTable.append(cart)


# table category
category = \
"""
CREATE TABLE IF NOT EXISTS categoria (
    id        INTEGER PRIMARY KEY,
    descricao TEXT,
    ativo     INTEGER DEFAULT (1) 
);
"""
appTable.append(category)


# table client
client = \
"""
CREATE TABLE IF NOT EXISTS cliente (
    id            INTEGER PRIMARY KEY,
    nome          TEXT,
    vendedor_nome TEXT,
    cpf           TEXT,
    celular       TEXT,
    email         TEXT,
    senha         TEXT
);
"""
appTable.append(client)


# table purchase
purchase = \
"""
CREATE TABLE IF NOT EXISTS compra (
    id          INTEGER PRIMARY KEY,
    id_cliente  INTEGER,
    id_endereco INTEGER,
    forma_pgto  TEXT,
    data        TEXT,
    valor       REAL
);
"""
appTable.append(purchase)


# table item purchase
item_purchase = \
"""
CREATE TABLE IF NOT EXISTS compra_item (
    id_compra  INTEGER,
    id_produto INTEGER,
    qtde       INTEGER,
    preco      REAL
);
"""
appTable.append(item_purchase)


# table address
address = \
"""
CREATE TABLE IF NOT EXISTS endereco (
    id          INTEGER PRIMARY KEY,
    id_cliente  INTEGER,
    rua         TEXT,
    nro         TEXT,
    bairro      TEXT,
    cidade      TEXT,
    estado      TEXT,
    cep         TEXT,
    complemento TEXT,
    principal   INTEGER,
    ativo       INTEGER DEFAULT (1)
);
"""
appTable.append(address)


# table favorite
favorite = \
"""
CREATE TABLE IF NOT EXISTS favorito (
    id         INTEGER PRIMARY KEY,
    id_cliente INTEGER,
    id_produto INTEGER
);
"""
appTable.append(favorite)


# table product
product = \
"""
CREATE TABLE IF NOT EXISTS produto (
    id           INTEGER PRIMARY KEY,
    id_vendedor  INTEGER,
    descricao    TEXT,
    qtde         INTEGER,
    unidade      TEXT,
    preco        REAL,
    imagem       BLOB,
    observacao   TEXT,
    condicao     TEXT,
    situacao     TEXT,
    id_categoria INTEGER
);
"""
appTable.append(product)


# table description product
descriptionProduct = \
"""
CREATE TABLE IF NOT EXISTS produto_descricao (
    id_produto INTEGER,
    descricao  TEXT,
    imagem_0   BLOB,
    imagem_1   BLOB,
    imagem_2   BLOB,
    imagem_3   BLOB,
    imagem_4   BLOB
);
"""
appTable.append(descriptionProduct)


# view cart
view_cart = \
"""
CREATE VIEW IF NOT EXISTS view_carrinho AS
    SELECT cart.id,
           cart.id_cliente,
           cart.id_produto,
           pro.descricao,
           cart.qtde,
           cart.prod_selec,
           pro.qtde AS qtde_produto,
           pro.preco,
           pro.situacao,
           pro.imagem
      FROM carrinho AS cart
           LEFT JOIN
           produto AS pro ON cart.id_produto = pro.id;
"""
appTable.append(view_cart)


# view item purchase
view_item_purchase = \
"""
CREATE VIEW IF NOT EXISTS view_compra_item AS
    SELECT item.id_produto,
           item.id_compra,
           item.qtde,
           item.preco,
           com.id,
           com.data,
           com.forma_pgto,
           com.id_cliente,
           com.id_endereco,
           com.valor,
           cli.vendedor_nome,
           pro.id_vendedor,
           pro.descricao,
           pro.imagem,
           end.rua,
           end.nro,
           end.bairro,
           end.cidade
      FROM compra_item AS item
           LEFT JOIN
           compra AS com ON item.id_compra = com.id
           LEFT JOIN
           produto AS pro ON item.id_produto = pro.id
           LEFT JOIN
           cliente AS cli ON pro.id_vendedor = cli.id
           LEFT JOIN
           endereco AS end ON com.id_endereco = end.id;
"""
appTable.append(view_item_purchase)


# view favorite
view_favorite = \
"""
CREATE VIEW IF NOT EXISTS view_favorito AS
    SELECT fav.id,
           fav.id_cliente,
           fav.id_produto,
           pro.descricao,
           pro.qtde,
           pro.preco,
           pro.imagem,
           pro.situacao
      FROM favorito AS fav
           LEFT JOIN
           cliente AS cli ON fav.id_cliente = cli.id
           LEFT JOIN
           produto AS pro ON fav.id_produto = pro.id;
"""
appTable.append(view_favorite)


# view product
view_product = \
"""
CREATE VIEW IF NOT EXISTS view_produto AS
    SELECT pro.id_vendedor,
           pro.id,
           pro.descricao,
           pro.id_categoria,
           cat.descricao AS descricao_categoria,
           pro.qtde,
           pro.unidade,
           pro.preco,
           pro.imagem,
           pro.condicao,
           pro.situacao,
           pro.observacao,
           pro_desc.descricao AS produto_descricao,
           pro_desc.imagem_0,
           pro_desc.imagem_1,
           pro_desc.imagem_2,
           pro_desc.imagem_3,
           pro_desc.imagem_4
      FROM produto AS pro
           LEFT JOIN
           produto_descricao AS pro_desc ON pro.id = pro_desc.id_produto
           LEFT JOIN
           categoria AS cat ON pro.id_categoria = cat.id;
"""
appTable.append(view_product)


# create all table app
def create_all_table_app():
    conn, cursor = db()
    for table in appTable:
        cursor.execute(table)

create_all_table_app()