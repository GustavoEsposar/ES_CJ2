from pymongo import MongoClient

DATABASE_URL = "mongodb+srv://profe_palito:12vzhBfp03An7Q1W@cluster0.7pzrn.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

client = MongoClient(DATABASE_URL)

db = client.get_database("cj2ES")

carrinho_oficial = { 'itens': [ 
        { '_id': '1', 'nome' : 'camiseta', 'preco': 50.0, 'quantidade': 2 },
        { '_id': '2', 'nome' : 'calca', 'preco': 100.0, 'quantidade': 1 }
    ],
     'total': 0 }

def get_collection(collection_name):
    global carrinho_oficial

    return carrinho_oficial

def atualizar_quantidade(item_id, quantidade):
    global carrinho_oficial

    for item in carrinho_oficial['itens']:
        if int(item['_id']) == int(item_id):
            item['quantidade'] = quantidade
            break

def get_comprador_id(email):
    """Função para buscar o ID do comprador com base no email."""
    compradores_collection = db["compradores"]
    comprador = compradores_collection.find_one({"email": email})
    return comprador["_id"] if comprador else None
 
def add_endereco_to_comprador(comprador_id, endereco):
    """Função para adicionar um novo endereço ao comprador específico."""
    compradores_collection = db["compradores"]
    result = compradores_collection.update_one(
        {"_id": comprador_id},
        {"$push": {"enderecos": endereco.to_dict()}}
    )
    return result.modified_count > 0  # Retorna True se um documento foi modificado
