from fastapi import APIRouter
from sqlalchemy import func

from database import SessionLocal, AttackLog


router = APIRouter()


# ============================================================
# ANALYTICS SUMMARY
# ============================================================

@router.get("/analytics")
def get_analytics():

    db = SessionLocal()

    try:

        # ----------------------------------------------------
        # TOTAL ATTACKS
        # ----------------------------------------------------

        total_attacks = (
            db.query(AttackLog).count()
        )

        # ----------------------------------------------------
        # BLOCKED ATTACKS
        # ----------------------------------------------------

        blocked_attacks = (
            db.query(AttackLog)
            .filter(
                AttackLog.defense_triggered == True
            )
            .count()
        )

        # ----------------------------------------------------
        # ALLOWED ATTACKS
        # ----------------------------------------------------

        allowed_attacks = (
            db.query(AttackLog)
            .filter(
                AttackLog.defense_triggered == False
            )
            .count()
        )

        # ----------------------------------------------------
        # AVERAGE RISK SCORE
        # ----------------------------------------------------

        average_score = (
            db.query(
                func.avg(
                    AttackLog.detection_score
                )
            )
            .scalar()
        )

        if average_score is None:
            average_score = 0

        # ----------------------------------------------------
        # DEFENSE EFFECTIVENESS
        # ----------------------------------------------------
        #
        # This represents the percentage of attacks blocked.
        #
        # It is called "defense_accuracy" in the dashboard,
        # but technically it is a block rate because we do not
        # currently have ground-truth labels.
        # ----------------------------------------------------

        if total_attacks > 0:

            defense_accuracy = (
                blocked_attacks /
                total_attacks
            ) * 100

        else:

            defense_accuracy = 0

        # ----------------------------------------------------
        # ATTACK TYPE DISTRIBUTION
        # ----------------------------------------------------

        attack_types = (
            db.query(
                AttackLog.attack_type,
                func.count(AttackLog.id)
            )
            .group_by(
                AttackLog.attack_type
            )
            .all()
        )

        attack_type_data = []

        for attack_type, count in attack_types:

            attack_type_data.append({
                "attack_type": attack_type,
                "count": count
            })

        # ----------------------------------------------------
        # LATENCY
        # ----------------------------------------------------
        #
        # database.py stores latency as String.
        # Therefore, calculate the values safely in Python.
        # ----------------------------------------------------

        all_logs = (
            db.query(AttackLog).all()
        )

        latency_values = []

        for log in all_logs:

            if log.latency is None:
                continue

            try:

                value = float(log.latency)

                latency_values.append(value)

            except (ValueError, TypeError):

                continue

        # ----------------------------------------------------
        # AVERAGE AND MAXIMUM LATENCY
        # ----------------------------------------------------

        if latency_values:

            average_latency = (
                sum(latency_values)
                / len(latency_values)
            )

            maximum_latency = max(
                latency_values
            )

        else:

            average_latency = 0
            maximum_latency = 0

        # ----------------------------------------------------
        # FINAL RESPONSE
        # ----------------------------------------------------

        return {

            "success": True,

            "total_attacks": total_attacks,

            "blocked_attacks": blocked_attacks,

            "allowed_attacks": allowed_attacks,

            "defense_accuracy": round(
                defense_accuracy,
                2
            ),

            "average_risk_score": round(
                float(average_score),
                2
            ),

            "average_latency": round(
                average_latency,
                4
            ),

            "maximum_latency": round(
                maximum_latency,
                4
            ),

            "attack_types": attack_type_data

        }

    # ========================================================
    # ERROR HANDLING
    # ========================================================

    except Exception as e:

        return {

            "success": False,

            "total_attacks": 0,

            "blocked_attacks": 0,

            "allowed_attacks": 0,

            "defense_accuracy": 0,

            "average_risk_score": 0,

            "average_latency": 0,

            "maximum_latency": 0,

            "attack_types": [],

            "error": str(e)

        }

    # ========================================================
    # CLOSE DATABASE
    # ========================================================

    finally:

        db.close()