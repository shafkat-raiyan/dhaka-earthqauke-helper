
STAGES = ("All", "Before Earthquake", "During Earthquake", "After Earthquake")


DEFAULT_DATA = [
    {"id": "G01", "title": "Secure Heavy Furniture", "stage": "Before Earthquake", "content": "Anchor top-heavy furniture and bookcases to wall studs."},
    {"id": "G02", "title": "Prepare Emergency Kit", "stage": "Before Earthquake", "content": "Pack food, water, flashlight, and first-aid supplies."},
    {"id": "G03", "title": "Identify Safe Spots", "stage": "Before Earthquake", "content": "Locate sturdy tables or interior walls away from glass."},
    {"id": "G04", "title": "Drop, Cover, Hold On", "stage": "During Earthquake", "content": "DROP to hands and knees, COVER head under table, HOLD ON."},
    {"id": "G05", "title": "Stay Indoors in High-Rises", "stage": "During Earthquake", "content": "Do not run outside or use elevators during shaking."},
    {"id": "G06", "title": "Move to Open Space", "stage": "During Earthquake", "content": "If outdoors, move away from buildings and electric wires."},
    {"id": "G07", "title": "Check for Injuries", "stage": "After Earthquake", "content": "Provide basic first aid. Do not move seriously injured people."},
    {"id": "G08", "title": "Inspect Gas Lines", "stage": "After Earthquake", "content": "If you smell gas, open windows and turn off main valve."},
    {"id": "G09", "title": "Head to Assembly Grounds", "stage": "After Earthquake", "content": "Evacuate using stairs to designated open fields or parks."},
    {"id": "G10", "title": "Expect Aftershocks", "stage": "After Earthquake", "content": "Be prepared for secondary tremors after the main quake."}
]


class Guideline:
    def __init__(self, g_id, title, stage, content):
        self.g_id = str(g_id).strip()
        self.title = str(title).strip()
        self.stage = str(stage).strip()
        self.content = str(content).strip()

    def to_dict(self):
       
        return {
            "id": self.g_id,
            "title": self.title,
            "stage": self.stage,
            "content": self.content
        }