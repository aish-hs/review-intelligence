# ==================================================
# CUSTOMER ACTION CENTER
# ==================================================


# ==================================================
# GENERATE ACTION PLAN
# ==================================================

def generate_action_plan(
    negative_percent,
    topic_counts,
    problem_counts
):

    actions = []

    # ==================================================
    # NO PROBLEMS
    # ==================================================

    if not problem_counts:

        actions.append({
            "priority": "LOW",
            "problem": "No major problem detected",
            "action": (
                "Continue monitoring customer feedback "
                "and maintain the current service quality."
            ),
            "impact": (
                "Maintaining positive customer experience "
                "can support customer retention."
            )
        })

        return actions


    # ==================================================
    # PRIORITY ORDER
    # ==================================================

    sorted_problems = sorted(
        problem_counts.items(),
        key=lambda item: item[1],
        reverse=True
    )


    # ==================================================
    # CREATE ACTIONS
    # ==================================================

    for problem, count in sorted_problems:

        percentage = (
            count /
            max(1, sum(problem_counts.values()))
        ) * 100


        # ----------------------------------------------
        # PRIORITY
        # ----------------------------------------------

        if negative_percent >= 40 and count >= 2:

            priority = "CRITICAL"

        elif negative_percent >= 20:

            priority = "HIGH"

        else:

            priority = "MEDIUM"


        # ----------------------------------------------
        # DELIVERY
        # ----------------------------------------------

        if problem == "Delivery":

            action = (
                "Review delivery partners, shipping delays, "
                "fulfillment time and shipment tracking."
            )

            impact = (
                "Faster and more reliable delivery can "
                "improve customer satisfaction and reduce "
                "negative reviews."
            )


        # ----------------------------------------------
        # PRODUCT QUALITY
        # ----------------------------------------------

        elif problem == "Product Quality":

            action = (
                "Investigate product defects, quality-control "
                "procedures and product reliability."
            )

            impact = (
                "Improving product quality can reduce "
                "returns, complaints and negative feedback."
            )


        # ----------------------------------------------
        # PACKAGING
        # ----------------------------------------------

        elif problem == "Packaging":

            action = (
                "Improve packaging materials and protection "
                "during transportation."
            )

            impact = (
                "Better packaging can reduce product damage "
                "and improve customer satisfaction."
            )


        # ----------------------------------------------
        # PRICE
        # ----------------------------------------------

        elif problem == "Price":

            action = (
                "Review pricing strategy and improve the "
                "perceived value offered to customers."
            )

            impact = (
                "Better value perception can improve "
                "customer satisfaction and purchase confidence."
            )


        # ----------------------------------------------
        # CUSTOMER SERVICE
        # ----------------------------------------------

        elif problem == "Customer Service":

            action = (
                "Improve customer support response time, "
                "communication and issue resolution."
            )

            impact = (
                "Better support can improve customer trust "
                "and reduce dissatisfaction."
            )


        # ----------------------------------------------
        # UNKNOWN PROBLEM
        # ----------------------------------------------

        else:

            action = (
                "Investigate this issue and monitor future "
                "customer feedback."
            )

            impact = (
                "Resolving recurring customer problems can "
                "improve overall customer experience."
            )


        # ----------------------------------------------
        # STORE ACTION
        # ----------------------------------------------

        actions.append({

            "priority": priority,

            "problem": problem,

            "count": count,

            "percentage": round(
                percentage,
                1
            ),

            "action": action,

            "impact": impact

        })


    return actions


# ==================================================
# GET HIGHEST PRIORITY ACTION
# ==================================================

def get_highest_priority_action(
    actions
):

    if not actions:

        return None


    priority_order = {

        "CRITICAL": 3,

        "HIGH": 2,

        "MEDIUM": 1,

        "LOW": 0

    }


    highest_action = max(

        actions,

        key=lambda action:
        priority_order.get(
            action["priority"],
            0
        )

    )


    return highest_action