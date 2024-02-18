def keysort(t, fun):
    u = [(x, fun(x)) for x in t]  # decorate
    u.sort(key=lambda xy: xy[1])  # sort
    v = [xy[0] for xy in u]  # undecorate
    return v

def o(t, n=None, u=None):
        if isinstance(t, (int, float)):
            return str(round(t, n))
        if not isinstance(t, dict) and not isinstance(t, list):
            return str(t)

        u = []
        for k, v in t.items() if isinstance(t, dict) else enumerate(t):
            if str(k)[0] != "_":
                if len(t) > 0:
                    u.append(o(v, n))
                else:
                    u.append(f"${o(k, n)}: ${o(v, n)}")

        return "{" + ", ".join(u) + "}"
