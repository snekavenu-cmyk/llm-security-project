from fastapi import APIRouter
from database import SessionLocal, AttackLog


router = APIRouter()


# ============================================================
# GET ALL ATTACK LOGS
# ============================================================

@router.get("/logs")
def get_logs():

    db = SessionLocal()

    try:

        logs = (
            db.query(AttackLog)
            .order_by(AttackLog.created_at.desc())
            .all()
        )

        results = []

        for log in logs:

            results.append({
                "id": log.id,
                "attack_type": log.attack_type,
                "payload": log.payload,
                "defense_logs": log.defense_logs,
                "detection_score": log.detection_score,
                "defense_triggered": log.defense_triggered,
                "latency": log.latency,
                "username": log.username,
                "role": log.role,
                "created_at": (
                    log.created_at.isoformat()
                    if log.created_at
                    else None
                )
            })

        return {
            "success": True,
            "count": len(results),
            "logs": results
        }

    except Exception as e:

        return {
            "success": False,
            "count": 0,
            "logs": [],
            "error": str(e)
        }

    finally:

        db.close()