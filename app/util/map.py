def to_pydantic(obj):
    return obj.model_validate(obj)
