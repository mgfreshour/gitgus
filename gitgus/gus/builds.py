class Builds:
    def get_build(self, build_name):
        return self._gus().query_single_build(name=build_name)

    def create_build(self, **kwargs):
        return self._gus().create_build(**kwargs)
