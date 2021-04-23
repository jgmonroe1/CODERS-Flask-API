import json
import decimal
#this class was taken from stackoverflow:
#https://stackoverflow.com/questions/65309377/typeerror-object-of-type-decimal-is-not-json-serializable
class Encoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, decimal.Decimal): return float(obj)