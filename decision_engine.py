# ==================================================
# BUSINESS DECISION ENGINE
# ==================================================


def _priority_rank(priority):
    return {
        "CRITICAL": 4,
        "HIGH": 3,
        "MEDIUM": 2,
        "LOW": 1
    }.get(str(priority).upper(), 0)


PROBLEM_ACTIONS = {
    "Delivery": {
        "action": "Audit the delivery pipeline, identify the bottleneck, and improve dispatch/tracking communication.",
        "impact": "Reducing delivery failures can improve customer satisfaction and reduce repeat complaints."
    },
    "Product Quality": {
        "action": "Investigate defective-product patterns, strengthen quality checks, and review supplier or manufacturing controls.",
        "impact": "Fewer quality failures can reduce returns, complaints, and customer churn."
    },
    "Customer Service": {
        "action": "Review support response times, escalation handling, and communication quality for the affected customers.",
        "impact": "Faster and clearer support can improve trust and reduce unresolved complaints."
    },
    "Price": {
        "action": "Review pricing and perceived value against customer expectations and competing alternatives.",
        "impact": "Better value alignment can improve purchase confidence and retention."
    },
    "Packaging": {
        "action": "Audit packaging materials and handling procedures to prevent damage during fulfillment and delivery.",
        "impact": "Better packaging can reduce damaged deliveries, replacements, and negative reviews."
    }
}


def _action_for_problem(problem, existing_action=None):
    """
    Always return an action dictionary.

    This function previously returned a string when existing_action
    was supplied. That caused:

        AttributeError: 'str' object has no attribute 'get'

    because the caller expected a dictionary.
    """

    # If an existing action is already a dictionary
    if isinstance(existing_action, dict):
        return {
            "action": existing_action.get("action", ""),
            "impact": existing_action.get("impact", "")
        }

    # If an existing action is a string
    if isinstance(existing_action, str) and existing_action.strip():
        default_impact = PROBLEM_ACTIONS.get(
            problem,
            {}
        ).get(
            "impact",
            "Resolving the highest-impact issue should improve customer experience and reduce repeat complaints."
        )

        return {
            "action": existing_action,
            "impact": default_impact
        }

    # Use predefined action
    return PROBLEM_ACTIONS.get(
        problem,
        {
            "action": "Investigate the issue, identify the operational bottleneck, and monitor the next review cycle.",
            "impact": "Resolving the highest-impact issue should improve customer experience and reduce repeat complaints."
        }
    )


def _safe_dict(value):
    """
    Convert invalid/non-dictionary values into an empty dictionary.
    """
    return value if isinstance(value, dict) else {}


def _safe_list(value):
    """
    Convert invalid/non-list values into an empty list.
    """
    return value if isinstance(value, list) else []


def generate_business_decision(
    problem_counts,
    problem_severity,
    root_cause_intelligence,
    trend_intelligence,
    action_plan,
    total_reviews,
    negative_percent
):
    """
    Convert customer intelligence into a single business decision chain:

    Problem
        ↓
    Root Cause
        ↓
    Priority
        ↓
    Recommended Action
        ↓
    Expected Impact
    """

    # --------------------------------------------------
    # SAFE INPUT NORMALIZATION
    # --------------------------------------------------

    problem_counts = _safe_dict(problem_counts)
    problem_severity = _safe_dict(problem_severity)
    root_cause_intelligence = _safe_dict(root_cause_intelligence)
    trend_intelligence = _safe_dict(trend_intelligence)
    action_plan = _safe_list(action_plan)

    # --------------------------------------------------
    # ROOT CAUSE DATA
    # --------------------------------------------------

    root_results = _safe_list(
        root_cause_intelligence.get(
            "root_cause_analysis",
            []
        )
    )

    highest_root = root_cause_intelligence.get(
        "highest_priority_root_cause"
    )

    if not isinstance(highest_root, dict):
        highest_root = None

    highest_severity = None

    # --------------------------------------------------
    # FIND HIGHEST SEVERITY PROBLEM
    # --------------------------------------------------

    if problem_severity:

        valid_severity = {}

        for problem, data in problem_severity.items():

            if isinstance(data, dict):
                valid_severity[problem] = data

        if valid_severity:

            highest_problem = max(
                valid_severity,
                key=lambda p: float(
                    valid_severity[p].get(
                        "severity_score",
                        0
                    ) or 0
                )
            )

            highest_severity = {
                "problem": highest_problem,
                **valid_severity[highest_problem]
            }

    # --------------------------------------------------
    # DETERMINE MAIN BUSINESS PROBLEM
    # --------------------------------------------------

    problem = (
        highest_severity or {}
    ).get("problem")

    if not problem and highest_root:

        problem = highest_root.get(
            "problem"
        )

    if not problem and problem_counts:

        problem = max(
            problem_counts,
            key=lambda p: (
                problem_counts.get(p, 0)
                if isinstance(problem_counts.get(p), (int, float))
                else 0
            )
        )

    # --------------------------------------------------
    # NO PROBLEM DETECTED
    # --------------------------------------------------

    if not problem:

        return {
            "status": "MONITOR",
            "problem": "No major customer problem detected",
            "root_cause": "No root cause required",
            "priority": "LOW",
            "severity_score": 0,
            "negative_reviews": 0,
            "recommended_action": "Continue monitoring customer feedback.",
            "expected_impact": "Maintain current customer experience and detect emerging issues early.",
            "evidence": 0,
            "related_occurrences": 0,
            "trend": "NO DATA",
            "decision_confidence": 100,
            "reason": "The current review set contains no detected problem requiring intervention.",
            "decision_chain": [
                "No major problem",
                "No root cause required",
                "LOW",
                "Continue monitoring",
                "Maintain customer experience"
            ]
        }

    # --------------------------------------------------
    # PROBLEM SEVERITY
    # --------------------------------------------------

    severity = problem_severity.get(
        problem,
        {}
    )

    if not isinstance(severity, dict):
        severity = {}

    priority = severity.get(
        "priority",
        "LOW"
    )

    severity_score = float(
        severity.get(
            "severity_score",
            0
        ) or 0
    )

    negative_reviews_raw = severity.get(
        "negative_reviews",
        problem_counts.get(
            problem,
            0
        )
    )

    try:
        negative_reviews = int(
            negative_reviews_raw or 0
        )
    except (ValueError, TypeError):
        negative_reviews = 0

    # --------------------------------------------------
    # FIND ROOT CAUSE
    # --------------------------------------------------

    root_item = None

    for item in root_results:

        if not isinstance(item, dict):
            continue

        if item.get("problem") == problem:

            root_item = item
            break

    if (
        root_item is None
        and highest_root
        and highest_root.get("problem") == problem
    ):
        root_item = highest_root

    root_cause = (
        "Insufficient evidence to identify a specific root cause"
    )

    evidence = 0

    if root_item:

        causes = _safe_list(
            root_item.get(
                "root_causes",
                []
            )
        )

        if causes:

            valid_causes = [
                item
                for item in causes
                if isinstance(item, dict)
            ]

            if valid_causes:

                strongest = max(
                    valid_causes,
                    key=lambda item: int(
                        item.get(
                            "evidence_count",
                            0
                        ) or 0
                    )
                )

                root_cause = strongest.get(
                    "cause",
                    root_cause
                )

                try:
                    evidence = int(
                        strongest.get(
                            "evidence_count",
                            0
                        ) or 0
                    )
                except (ValueError, TypeError):
                    evidence = 0

    # --------------------------------------------------
    # FALLBACK ROOT CAUSE
    # --------------------------------------------------

    elif highest_root:

        root_data = highest_root.get(
            "root_cause"
        )

        if isinstance(root_data, dict):

            root_cause = root_data.get(
                "cause",
                root_cause
            )

            try:
                evidence = int(
                    root_data.get(
                        "evidence_count",
                        0
                    ) or 0
                )
            except (ValueError, TypeError):
                evidence = 0

    # --------------------------------------------------
    # FIND EXISTING ACTION
    # --------------------------------------------------

    existing_action = None

    for item in action_plan:

        if not isinstance(item, dict):
            continue

        if item.get("problem") == problem:

            existing_action = {
                "action": item.get(
                    "action",
                    ""
                ),
                "impact": item.get(
                    "impact",
                    ""
                )
            }

            break

    # --------------------------------------------------
    # GET RECOMMENDED ACTION
    # --------------------------------------------------

    action_data = _action_for_problem(
        problem,
        existing_action
    )

    # Safety check:
    # action_data MUST be a dictionary.
    if not isinstance(action_data, dict):

        action_data = {
            "action": str(action_data),
            "impact": "Resolving the identified issue should improve customer experience."
        }

    action = action_data.get(
        "action",
        "Investigate the issue and monitor customer feedback."
    )

    impact = action_data.get(
        "impact",
        "Resolving the identified issue should improve customer experience."
    )

    # --------------------------------------------------
    # TREND INTELLIGENCE
    # --------------------------------------------------

    trend = trend_intelligence.get(
        "sentiment_trend",
        {}
    )

    if not isinstance(trend, dict):
        trend = {}

    trend_name = trend.get(
        "trend",
        "NO DATA"
    )

    # --------------------------------------------------
    # TOPIC / PROBLEM RELATIONSHIPS
    # --------------------------------------------------

    relationships = _safe_list(
        trend_intelligence.get(
            "topic_problem_relationships",
            []
        )
    )

    related_counts = []

    for item in relationships:

        if not isinstance(item, dict):
            continue

        if item.get("problem") != problem:
            continue

        count = item.get(
            "count",
            0
        )

        try:
            count = int(
                count or 0
            )
        except (ValueError, TypeError):
            count = 0

        related_counts.append(
            count
        )

    related_count = max(
        related_counts or [0]
    )

    # --------------------------------------------------
    # DECISION CONFIDENCE
    # --------------------------------------------------

    confidence = 45

    if severity_score >= 75:
        confidence += 20

    elif severity_score >= 50:
        confidence += 15

    elif severity_score >= 25:
        confidence += 8

    if evidence > 0:

        confidence += min(
            20,
            evidence * 5
        )

    if related_count > 0:

        confidence += min(
            10,
            related_count * 2
        )

    confidence = min(
        100,
        confidence
    )

    # --------------------------------------------------
    # BUSINESS DECISION STATUS
    # --------------------------------------------------

    if trend_name == "WORSENING":

        status = (
            "ACT NOW"
            if _priority_rank(priority) >= 3
            else "WATCH CLOSELY"
        )

        reason = (
            "The issue is supported by detected problem evidence "
            "and sentiment is worsening."
        )

    elif priority == "CRITICAL":

        status = "ACT NOW"

        reason = (
            "The issue has critical severity and should be "
            "addressed immediately."
        )

    elif priority == "HIGH":

        status = "ACT SOON"

        reason = (
            "The issue has high customer impact and should be "
            "addressed in the next improvement cycle."
        )

    elif priority == "MEDIUM":

        status = "PLAN"

        reason = (
            "The issue is meaningful but does not currently "
            "require emergency intervention."
        )

    else:

        status = "MONITOR"

        reason = (
            "The issue is currently low priority; continue "
            "monitoring for recurrence."
        )

    # --------------------------------------------------
    # FINAL BUSINESS DECISION
    # --------------------------------------------------

    return {
        "status": status,
        "problem": problem,
        "root_cause": root_cause,
        "priority": priority,
        "severity_score": round(
            severity_score,
            1
        ),
        "negative_reviews": negative_reviews,
        "recommended_action": action,
        "expected_impact": impact,
        "evidence": evidence,
        "related_occurrences": int(
            related_count
        ),
        "trend": trend_name,
        "decision_confidence": int(
            confidence
        ),
        "reason": reason,
        "decision_chain": [
            problem,
            root_cause,
            priority,
            action,
            impact
        ]
    }