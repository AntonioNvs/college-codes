import json
import pandas as pd

class LoadEvent:
    raw_path = f"drive/MyDrive/pff/event/premier-league/2022-2023"

    def __init__(self, match_id) -> None:
        self.match_id = match_id
        self.filepath = f"{self.raw_path}/{match_id}.json"

    def run(self):
        with open(self.filepath, "r") as file:
            data = json.loads(json.loads(file.read()))
        
        events = data["gameEvents"]

        info = []

        for idx, event in enumerate(events):
            game_event_id = event["id"]

            if len(event["possessionEvents"]) > 0:
                sample = event["possessionEvents"][0]

                possession_event_id = sample["id"]

                if sample["passingEvent"] is not None:
                    pressure_player = event["pressurePlayer"]["id"] if event["pressurePlayer"] is not None else None
                    defender_player = sample["passingEvent"]["defenderPlayer"]["id"] if sample["passingEvent"]["defenderPlayer"] is not None else None
                    passer_player = sample["passingEvent"]["passerPlayer"]["id"] if sample["passingEvent"]["passerPlayer"] is not None else None
                    passer_foot_player = sample["passingEvent"]["passerPlayer"]["preferredFoot"] if sample["passingEvent"]["passerPlayer"] is not None else None
                    target_player = sample["passingEvent"]["targetPlayer"]["id"] if sample["passingEvent"]["passerPlayer"] is not None else None

                    info.append({
                        "game_event_id": int(game_event_id),
                        "possession_event_id": int(possession_event_id),
                        "possession_event_type": sample["possessionEventType"],
                        "incompletion_reason_type": sample["passingEvent"]["incompletionReasonType"],
                        "pass_body_type": sample["passingEvent"]["passBodyType"],
                        "pass_high_point_type": sample["passingEvent"]["passHighPointType"],
                        "pass_outcome_type": sample["passingEvent"]["passOutcomeType"],
                        "pass_type": sample["passingEvent"]["passType"],
                        "pressure_type": event["pressureType"],
                        "team_of_passer": event["team"]["id"] if event["team"] is not None else None,
                        "pressurePlayer": pressure_player,
                        "defender_player": defender_player,
                        "passer_player": passer_player,
                        "passer_foot_player": passer_foot_player,
                        "target_player": target_player,
                        "sub_type_event": event["subType"],
                        "next_game_event_id": events[idx+1]["id"]
                    })

        return pd.DataFrame(info)


d = LoadEvent(4450).run()