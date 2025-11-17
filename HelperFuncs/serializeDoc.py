from bson.dbref import DBRef

def serialize_doc(doc):
    if not isinstance(doc, dict):
        return doc

    serialized = {}
    for k, v in doc.items():
        if isinstance(v, DBRef):
            serialized[k] = {"collection": v.collection, "id": v.id}
        elif isinstance(v, list):
            serialized[k] = [
                {"collection": x.collection, "id": x.id} if isinstance(x, DBRef)
                else serialize_doc(x) if isinstance(x, dict)
                else x
                for x in v
            ]
        elif isinstance(v, dict):
            serialized[k] = serialize_doc(v)
        else:
            serialized[k] = v
    return serialized