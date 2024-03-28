# def keysort(t, fun):
#     u = [(x, fun(x)) for x in t]  # decorate
#     u.sort(key=lambda xy: xy[1])  # sort
#     v = [xy[0] for xy in u]  # undecorate
#     return v

def keysort(t, fun):
    u = [{"x": x, "y": fun(x)} for x in t]  # decorate
    u.sort(key=lambda a: a["y"])  # sort
    # print(u[0]['x'].cells)
    v = [xy["x"] for xy in u]  # undecorate
    return v
