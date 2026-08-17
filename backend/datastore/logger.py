from database import SessionLocal, AttackLog


def save_attack(
    attack_type,
    payload,
    defense_logs,
    detection_score,
    defense_triggered,
    latency,
    username="Admin",
    role="Tester"
):
    """
    Save an attack result into the attack_logs table.
    """

    db = SessionLocal()

    try:
        attack = AttackLog(
            attack_type=attack_type,
            payload=payload,
            defense_logs=defense_logs,
            detection_score=detection_score,
            defense_triggered=defense_triggered,
            latency=str(latency),
            username=username,
            role=role
        )

        db.add(attack)
        db.commit()
        db.refresh(attack)

        return attack

    except Exception as e:
        db.rollback()
        print("Logger Error:", e)
        return None

    finally:
        db.close()