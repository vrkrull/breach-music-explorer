def vgm_score(title, query):

    t = title.lower()
    q = query.lower()

    score = 0

    if q in t:
        score += 50

    # OST priority
    if "ost" in t or "soundtrack" in t:
        score += 40

    # composer hints
    composers = ["mitsuda", "uematsu", "kondo"]
    if any(c in t for c in composers):
        score += 30

    # penalize noise
    bad = ["remix", "cover", "live", "arrangement"]
    if any(b in t for b in bad):
        score -= 80

    return score