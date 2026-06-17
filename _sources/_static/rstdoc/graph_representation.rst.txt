- GraphRepresentation: ``Dict[int, Dict[int, Dict[str, Any]]]``: A dictionary where the keys 
  are vertex identifiers and the values are dictionaries mapping neighboring vertex 
  identifiers to edge attributes (e.g., ``weight``). This is the internal representation 
  used by the :class:`pygraphs.Graph` class.