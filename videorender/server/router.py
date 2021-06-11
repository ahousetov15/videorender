from rest_framework import routers


class MainRouter(routers.DefaultRouter):

    def extend(self, router) -> None:
        self.registry.extend(router.registry)
