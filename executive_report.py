# ==================================================
# EXECUTIVE AI DECISION REPORT
# ==================================================


def _safe(value, default="Not available"):
    """Return a clean display value."""
    if value is None:
        return default

    if isinstance(value, str):
        value = value.strip()

        if not value:
            return default

        return value

    return value


def generate_executive_report(decision):
    """
    Convert the Business Decision Engine output
    into a manager-friendly executive report.
    """

    if not isinstance(decision, dict):
        return {
            "headline": "No business decision available",
            "summary": "There is not enough information to generate an executive report.",
            "problem": "Not available",
            "root_cause": "Not available",
            "priority": "LOW",
            "action": "Continue monitoring customer feedback.",
            "impact": "Maintain current customer experience.",
            "confidence": 0,
            "status": "MONITOR"
        }

    problem = _safe(
        decision.get("problem"),
        "No major customer problem detected"
    )

    root_cause = _safe(
        decision.get("root_cause"),
        "No specific root cause identified"
    )

    priority = str(
        _safe(
            decision.get("priority"),
            "LOW"
        )
    ).upper()

    action = _safe(
        decision.get("recommended_action"),
        "Continue monitoring customer feedback."
    )

    impact = _safe(
        decision.get("expected_impact"),
        "Maintain current customer experience."
    )

    status = str(
        _safe(
            decision.get("status"),
            "MONITOR"
        )
    ).upper()

    trend = str(
        _safe(
            decision.get("trend"),
            "NO DATA"
        )
    ).upper()

    try:
        confidence = int(
            decision.get(
                "decision_confidence",
                0
            ) or 0
        )
    except (ValueError, TypeError):
        confidence = 0

    try:
        negative_reviews = int(
            decision.get(
                "negative_reviews",
                0
            ) or 0
        )
    except (ValueError, TypeError):
        negative_reviews = 0

    try:
        severity_score = float(
            decision.get(
                "severity_score",
                0
            ) or 0
        )
    except (ValueError, TypeError):
        severity_score = 0

    try:
        related_occurrences = int(
            decision.get(
                "related_occurrences",
                0
            ) or 0
        )
    except (ValueError, TypeError):
        related_occurrences = 0

    # --------------------------------------------------
    # EXECUTIVE HEADLINE
    # --------------------------------------------------

    if status == "ACT NOW":

        headline = (
            f"Immediate attention required for {problem}."
        )

    elif status == "ACT SOON":

        headline = (
            f"{problem} should be addressed in the next improvement cycle."
        )

    elif status == "PLAN":

        headline = (
            f"{problem} requires planned improvement."
        )

    elif status == "WATCH CLOSELY":

        headline = (
            f"{problem} is showing warning signals and should be closely monitored."
        )

    else:

        headline = (
            f"{problem} is currently under monitoring."
        )

    # --------------------------------------------------
    # EXECUTIVE SUMMARY
    # --------------------------------------------------

    summary_parts = [
        f"The highest-priority customer issue is {problem}.",
        f"The identified root cause is {root_cause}.",
        f"The issue has a {priority} priority level."
    ]

    if negative_reviews > 0:

        summary_parts.append(
            f"{negative_reviews} negative review(s) are associated with this issue."
        )

    if trend != "NO DATA":

        summary_parts.append(
            f"Current sentiment trend: {trend}."
        )

    summary = " ".join(summary_parts)

    # --------------------------------------------------
    # RECOMMENDATION
    # --------------------------------------------------

    recommendation = (
        f"Business should {action.lower()}"
    )

    # --------------------------------------------------
    # CONFIDENCE INTERPRETATION
    # --------------------------------------------------

    if confidence >= 80:

        confidence_label = "HIGH"

    elif confidence >= 60:

        confidence_label = "MEDIUM"

    elif confidence >= 40:

        confidence_label = "MODERATE"

    else:

        confidence_label = "LOW"

    # --------------------------------------------------
    # RETURN REPORT
    # --------------------------------------------------

    return {
        "headline": headline,
        "summary": summary,
        "problem": problem,
        "root_cause": root_cause,
        "priority": priority,
        "status": status,
        "action": action,
        "recommendation": recommendation,
        "impact": impact,
        "trend": trend,
        "severity_score": round(
            severity_score,
            1
        ),
        "negative_reviews": negative_reviews,
        "related_occurrences": related_occurrences,
        "confidence": confidence,
        "confidence_label": confidence_label
    }