import json

def form2Dict(form, key_dict):
    result = {}
    for key in key_dict.keys():
        result[key] = form.get(key, key_dict[key])
    return result

def getSalesCountfromSalesStr(sales):
    result = 0
    sales = json.loads(sales)
    for value in sales.values():
        result += value
    return result
