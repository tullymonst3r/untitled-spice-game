init -11 python in missionslib: 
    missions = []
    currentMission = None
    lastMissionEnded = False

    class Mission(object):
        easy = False
        hard = False
        hell = False
        def __init__(self, name: str, description: str, *args, **kwargs):
            self.name = name
            self.description = description
            self.x = kwargs.get('x', 0)
            self.y = kwargs.get('y', 0)
        def __str__(self):
            return self.name

    missions.append(Mission('Travel to Lyngarth', 'Garlic sets out on a journey to the kingdom of Lyngarth.', x=-1350, y =-2150))
    missions.append(Mission('Exploring the kingdom', 'Garlic takes a trip around the kingdom of Lyngarth.', x=-1150, y =-1350))
    missions.append(Mission('Guardian Vow', 'Garlic\'s first day in the High Guardian Academy.', x=-500, y =-1450))
