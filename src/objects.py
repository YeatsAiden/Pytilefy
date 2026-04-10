class Object:
    def __init__(self, singleton: bool = False, custom_id: str = None) -> None:
        self.objects: Objects = objects
        self._id: str = self.__class__.__name__ if custom_id == None else custom_id
        self._singleton: bool = singleton
        self.objects.register_object(self)

    def update(self, *args, **kwargs):
        pass

    def delete(self, *args, **kwargs):
        self.objects.delete_object(self)


class Objects:
    def __init__(self) -> None:
        self.objects = {"singletons": {}, "groups": {}}

    def register_object(self, obj: Object) -> None:
        if obj._singleton:
            self.objects["singletons"][obj._id] = obj
        elif obj not in self.objects["groups"]:
            self.objects["groups"][obj._id] = [obj]
        else:
            self.objects["groups"][obj._id].append(obj)

    def delete_object(self, obj: Object) -> None:
        if obj._singleton and obj._id in self.objects["singletons"]:
            self.objects["singletons"].pop(obj._id)
        elif obj._id in self.objects["groups"]:
            self.objects["groups"][obj._id].remove(obj)

    # Only for singletons (Usually managers)
    def __getitem__(self, key):
        return self.objects["singletons"][key]

    def get_group(self, group: str):
        if group in self.objects["groups"][group]:
            return self.objects["groups"][group]
        return []


objects = Objects()
