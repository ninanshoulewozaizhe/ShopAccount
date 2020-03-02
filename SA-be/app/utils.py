
def form2Dict(form, key_dict):
    result = {}
    for key in key_dict.keys():
        result[key] = form.get(key, key_dict[key])
    return result
