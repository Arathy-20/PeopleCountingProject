def classify_density(count):

    if count < 50:
        return (
            "Light Crowd",
            "cs-badge-light",
            "🟢"
        )

    if count < 200:
        return (
            "Moderate Crowd",
            "cs-badge-moderate",
            "🟡"
        )

    return (
        "Heavy Crowd",
        "cs-badge-heavy",
        "🔴"
    )