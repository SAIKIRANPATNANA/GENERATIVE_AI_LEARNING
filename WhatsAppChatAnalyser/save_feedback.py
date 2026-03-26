from mayyaDatabase import mongo_crud

def send_feedback(feedback):
    uri = "mongodb+srv://saikiranpatnana:mayya143@saikiran.bdu0jbl.mongodb.net/?retryWrites=true&w=majority"
    mongo_op = mongo_crud.mongo_operation(uri,'RadhaLovesRaju')
    database = mongo_op.create_database()
    collection = mongo_op.create_collection('feedback')
    mongo_op.insert_record(feedback,'feedback')
    print(mongo_op.read_record('feedback'))
    return True