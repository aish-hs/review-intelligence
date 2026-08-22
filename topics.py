# ==================================================
# TOPIC / ASPECT DETECTION
# ==================================================

def detect_aspects(review):

    aspects = {
        "Product Quality": [
            "quality",
            "product",
            "material",
            "performance",
            "durable"
        ],

        "Delivery": [
            "delivery",
            "shipping",
            "arrived",
            "late",
            "delay"
        ],

        "Packaging": [
            "packaging",
            "package",
            "box",
            "packed"
        ],

        "Price": [
            "price",
            "expensive",
            "cheap",
            "cost",
            "value"
        ],

        "Customer Service": [
            "service",
            "support",
            "staff",
            "customer care"
        ]
    }

    detected = []

    review_lower = review.lower()

    for aspect, keywords in aspects.items():

        for keyword in keywords:

            if keyword in review_lower:

                detected.append(aspect)

                break

    return detected