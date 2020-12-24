from ..services.esdr import EsdrService

class EsdrController:
    service = EsdrService()

    def Get_Something(self):
        return self.service.Get_Something()

    def Other_Function(self, feed_id):
        return self.service.Other_Function(feed_id)