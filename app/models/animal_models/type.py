from Backend_Python.app.models.animal_models.animal_model import AnimalModel


class Type(AnimalModel):
    """cat, dog ..."""
    name: str = ''
