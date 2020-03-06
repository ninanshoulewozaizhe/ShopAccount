import json

def form2Dict(form, key_dict):
    result = {}
    for key in key_dict.keys():
        result[key] = form.get(key, key_dict[key])
    return result

def getSalesCountfromSalesStr(sales):
    result = 0
    sales = json.loads(json.dumps(sales))
    for value in sales.value():
        result += value
    return result