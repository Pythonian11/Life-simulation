import time
import random
import threading

#Goober1 stats
Goober1MaxHealth = 120
Goober1Health = 100
Goober1X = 0
Goober1Y = 0
Goober1Speed = 1.3
Goober1Sight = 0.8
Goober1Hunger = 10
Goober1Thirst = 10
Goober1dead = False
Goober1Action = "Idle"
#Goober2 stats
Goober2MaxHealth = 120
Goober2Health = 120
Goober2X = 50
Goober2Y = -23
Goober2Speed = 0.7
Goober2Sight = 1.3
Goober2Hunger = 15
Goober2Thirst = 7
Goober2dead = False
Goober2Action = "Idle"
#bush1 stats
Bush1X = 32
Bush1Y = -12
Bush1Fruitnom = 1
Bush1state = "Full"
#bush2 stats
Bush2X = -3
Bush2Y = 45
Bush2Fruitnom = 1
Bush2state = "Full"
#pond1 stats
Pond1X = 43
Pond1Y = 0
#pond2 stats
Pond2X = 12
Pond2Y = 14
#pond3 stats
Pond3X = -36
Pond3Y = -49
#Hill stats
HillX = 36
HillY = -12

DroughtActive = False
PredatorActive = False
FloodActive = False
ActiveEvent = "None"
PredatorX = 0
PredatorY = 0
GooberChildren = []


def Disastercycle():
    global Bush1state, Bush1Fruitnom, Bush2Fruitnom, Bush2state
    global Goober1Health, Goober2Health, Goober1Thirst, Goober2Thirst
    global Goober1X, Goober1Y, Goober2X, Goober2Y
    global DroughtActive, PredatorActive, FloodActive, ActiveEvent, PredatorX, PredatorY

    while True:
        time.sleep(120)
        Disaster = random.choice(["Starvation", "Drought", "Predator", "Flood"])
        ActiveEvent = Disaster

        if Disaster == "Starvation":
            print("Disaster: Starvation!")
            for _ in range(200):
                Bush1state = "Empty"
                Bush1Fruitnom = 0
                Bush2state = "Empty"
                Bush2Fruitnom = 0
                time.sleep(0.1)

        elif Disaster == "Drought":
            print("Disaster: Drought!")
            DroughtActive = True
            for _ in range(30):
                Goober1Thirst = max(0, Goober1Thirst - 2)
                Goober2Thirst = max(0, Goober2Thirst - 2)
                if Goober1Thirst <= 0:
                    Goober1Health -= 2
                if Goober2Thirst <= 0:
                    Goober2Health -= 2
                time.sleep(1)
            DroughtActive = False

        elif Disaster == "Predator":
            print("Disaster: Predator attack!")
            PredatorActive = True
            PredatorX = (Goober1X + Goober2X) / 2
            PredatorY = (Goober1Y + Goober2Y) / 2
            for _ in range(25):
                if Goober1Health > 0:
                    dist1 = distance(PredatorX, PredatorY, Goober1X, Goober1Y)
                    if dist1 <= 5:
                        Goober1Health -= 5
                if Goober2Health > 0:
                    dist2 = distance(PredatorX, PredatorY, Goober2X, Goober2Y)
                    if dist2 <= 5:
                        Goober2Health -= 5

                if Goober1Health > 0 and Goober2Health > 0:
                    PredatorX += (Goober1X + Goober2X) / 2 - PredatorX
                    PredatorY += (Goober1Y + Goober2Y) / 2 - PredatorY
                    PredatorX *= 0.85
                    PredatorY *= 0.85
                time.sleep(1)
            PredatorActive = False

        elif Disaster == "Flood":
            print("Disaster: Flood!")
            FloodActive = True
            for _ in range(30):
                if distance(Goober1X, Goober1Y, HillX, HillY) > 8:
                    Goober1Health -= 3
                if distance(Goober2X, Goober2Y, HillX, HillY) > 8:
                    Goober2Health -= 3
                time.sleep(1)
            FloodActive = False

        ActiveEvent = "None"


def Harming_healing():
    global Goober1Thirst, Goober1Hunger, Goober2Thirst, Goober2Hunger, Goober1Health, Goober2Health
    while True:
        if Goober1Hunger <= 0:
            Goober1Health -= 5
        if Goober1Thirst <= 0:
            Goober1Health -= 5
        if Goober2Hunger <= 0:
            Goober2Health -= 5
        if Goober2Thirst <= 0:
            Goober2Health -= 5

        if Goober2Thirst > 4 and Goober2Hunger > 4:
            Goober2Health = min(Goober2MaxHealth, Goober2Health + 1)
        if Goober1Thirst > 4 and Goober1Hunger > 4:
            Goober1Health = min(Goober1MaxHealth, Goober1Health + 1)

        Goober1Health = max(0, Goober1Health)
        Goober2Health = max(0, Goober2Health)

        time.sleep(0.5)
        


def Deathdetect():
    global Goober1dead, Goober2dead, Goober2Health, Goober1Health
    while True:
        if Goober1Health <= 0 and not Goober1dead:
            print("Goober 1 Died!")
            Goober1dead = True
        if Goober2Health <= 0 and not Goober2dead:
            print("Goober 2 Died!")
            Goober2dead = True
        if Goober1dead and Goober2dead:
            break
        time.sleep(0.5)


def Thirstdrain():
    global Goober1Thirst, Goober2Thirst
    while True:
        Goober1Thirst -= 1
        Goober2Thirst -= 1
        time.sleep(10)


def Hungerdrain():
    global Goober1Hunger, Goober2Hunger
    while True:
        Goober1Hunger -= 1
        Goober2Hunger -= 1
        time.sleep(8)


def Eat(bushnom, goober="Goober1"):
    global Bush1state, Bush1Fruitnom, Bush2state, Bush2Fruitnom
    global Goober1Hunger, Goober2Hunger

    if bushnom == "1":
        if Bush1Fruitnom <= 0:
            return False
        Bush1state = "Empty"
        Bush1Fruitnom = 0
    elif bushnom == "2":
        if Bush2Fruitnom <= 0:
            return False
        Bush2state = "Empty"
        Bush2Fruitnom = 0
    else:
        return False

    if goober == "Goober1":
        Goober1Hunger = min(10, Goober1Hunger + 5)
    elif goober == "Goober2":
        Goober2Hunger = min(15, Goober2Hunger + 5)

    return True


def Drink(pondnom, goober="Goober1"):
    global Goober1Thirst, Goober2Thirst

    if pondnom not in ("1", "2", "3"):
        return False

    if goober == "Goober1":
        Goober1Thirst = min(10, Goober1Thirst + 5)
    elif goober == "Goober2":
        Goober2Thirst = min(10, Goober2Thirst + 5)

    return True


def Bushregen():
    global Bush1state, Bush1Fruitnom, Bush2state, Bush2Fruitnom
    while True:
        if Bush1state != "Full":
            Bush1Fruitnom += 1
            Bush1state = "Full"
        if Bush2state != "Full":
            Bush2Fruitnom += 1
            Bush2state = "Full"
        time.sleep(30)


def distance(x1, y1, x2, y2):
    return ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5


def FindNearestBush(gooberX, gooberY, sightRange):
    candidates = []
    bushes = [
        ("1", Bush1X, Bush1Y, Bush1Fruitnom),
        ("2", Bush2X, Bush2Y, Bush2Fruitnom),
    ]
    for bushName, bushX, bushY, fruitCount in bushes:
        if fruitCount > 0:
            dist = distance(gooberX, gooberY, bushX, bushY)
            if dist <= sightRange:
                candidates.append((dist, bushName, bushX, bushY))
    if not candidates:
        return None
    return min(candidates, key=lambda item: item[0])


def FindNearestPond(gooberX, gooberY, sightRange):
    ponds = [
        ("1", Pond1X, Pond1Y),
        ("2", Pond2X, Pond2Y),
        ("3", Pond3X, Pond3Y),
    ]
    candidates = []
    for pondName, pondX, pondY in ponds:
        dist = distance(gooberX, gooberY, pondX, pondY)
        if dist <= sightRange:
            candidates.append((dist, pondName, pondX, pondY))
    if not candidates:
        return None
    return min(candidates, key=lambda item: item[0])


def GetMoveSpeed(baseSpeed, hunger, thirst):
    if hunger <= 2 or thirst <= 2:
        return baseSpeed * 2
    return baseSpeed


def MoveToward(currentX, currentY, targetX, targetY, stepSize):
    if targetX > currentX:
        currentX = min(targetX, currentX + stepSize)
    elif targetX < currentX:
        currentX = max(targetX, currentX - stepSize)

    if targetY > currentY:
        currentY = min(targetY, currentY + stepSize)
    elif targetY < currentY:
        currentY = max(targetY, currentY - stepSize)

    return currentX, currentY


def AttemptReproduction():
    global Goober1dead, Goober2dead, Goober1Health, Goober2Health
    global Goober1Speed, Goober1Sight, Goober2Speed, Goober2Sight
    global Goober1MaxHealth, Goober2MaxHealth, Goober1X, Goober1Y, Goober2X, Goober2Y
    global GooberChildren, ActiveEvent

    if Goober1dead or Goober2dead:
        return False
    if ActiveEvent != "None":
        return False
    if distance(Goober1X, Goober1Y, Goober2X, Goober2Y) > 5:
        return False
    if Goober1Health < 50 or Goober2Health < 50:
        return False
    if random.random() > 0.08:
        return False

    childName = f"Goober {len(GooberChildren) + 3}"
    childSpeed = round((Goober1Speed + Goober2Speed) / 2, 2)
    childSight = round((Goober1Sight + Goober2Sight) / 2, 2)
    childMaxHealth = int(round((Goober1MaxHealth + Goober2MaxHealth) / 2))
    childX = (Goober1X + Goober2X) / 2
    childY = (Goober1Y + Goober2Y) / 2

    GooberChildren.append({
        "Name": childName,
        "Speed": childSpeed,
        "Sight": childSight,
        "MaxHealth": childMaxHealth,
        "Health": childMaxHealth,
        "Hunger": 8,
        "Thirst": 8,
        "X": childX,
        "Y": childY,
    })
    print(f"New offspring {childName} was born from the parents! Traits averaged naturally.")
    return True


def Goober1AI():
    global Goober1dead, Goober1X, Goober1Y, Goober1Hunger, Goober1Thirst, Goober1Action
    global PredatorX, PredatorY, ActiveEvent
    patrolPoints = [(0, 0), (4, 0), (0, 4), (-4, 0), (0, -4), (2, 2), (15, 8), (-10, -6), (12, -12), (-8, 10)]
    patrolIndex = 0

    while not Goober1dead:
        sightRange = max(10 * Goober1Sight, 80)
        bushTarget = FindNearestBush(Goober1X, Goober1Y, sightRange)
        pondTarget = FindNearestPond(Goober1X, Goober1Y, sightRange)
        moveSpeed = GetMoveSpeed(Goober1Speed, Goober1Hunger, Goober1Thirst)

        if PredatorActive:
            fleeTargetX = Goober1X + (Goober1X - PredatorX)
            fleeTargetY = Goober1Y + (Goober1Y - PredatorY)
            Goober1Action = "Running from predator"
            Goober1X, Goober1Y = MoveToward(Goober1X, Goober1Y, fleeTargetX, fleeTargetY, moveSpeed * 1.5)

        elif FloodActive:
            if distance(Goober1X, Goober1Y, HillX, HillY) > 8:
                Goober1Action = "Heading to the hill"
                Goober1X, Goober1Y = MoveToward(Goober1X, Goober1Y, HillX, HillY, moveSpeed * 1.5)
            else:
                Goober1Action = "On safe ground"

        elif DroughtActive:
            if pondTarget is not None:
                _, pondName, pondX, pondY = pondTarget
                if distance(Goober1X, Goober1Y, pondX, pondY) <= 2:
                    Goober1Action = f"Drinking at pond {pondName}"
                    Drink(pondName, "Goober1")
                else:
                    Goober1Action = f"Seeking water at pond {pondName}"
                    Goober1X, Goober1Y = MoveToward(Goober1X, Goober1Y, pondX, pondY, moveSpeed * 1.3)
            else:
                Goober1Action = "Searching for water"

        elif Goober1Hunger <= 6 and bushTarget is not None:
            _, bushName, bushX, bushY = bushTarget
            if distance(Goober1X, Goober1Y, bushX, bushY) <= 2:
                Goober1Action = f"Eating at bush {bushName}"
                Eat(bushName, "Goober1")
            else:
                Goober1Action = f"Heading to bush {bushName}"
                Goober1X, Goober1Y = MoveToward(Goober1X, Goober1Y, bushX, bushY, moveSpeed)

        elif Goober1Thirst <= 6 and pondTarget is not None:
            _, pondName, pondX, pondY = pondTarget
            if distance(Goober1X, Goober1Y, pondX, pondY) <= 2:
                Goober1Action = f"Drinking at pond {pondName}"
                Drink(pondName, "Goober1")
            else:
                Goober1Action = f"Heading to pond {pondName}"
                Goober1X, Goober1Y = MoveToward(Goober1X, Goober1Y, pondX, pondY, moveSpeed)

        elif bushTarget is not None and Goober1Hunger <= 8:
            _, bushName, bushX, bushY = bushTarget
            Goober1Action = f"Checking bush {bushName}"
            Goober1X, Goober1Y = MoveToward(Goober1X, Goober1Y, bushX, bushY, moveSpeed * 0.5)

        elif pondTarget is not None and Goober1Thirst <= 8:
            _, pondName, pondX, pondY = pondTarget
            Goober1Action = f"Checking pond {pondName}"
            Goober1X, Goober1Y = MoveToward(Goober1X, Goober1Y, pondX, pondY, moveSpeed * 0.5)

        else:
            Goober1Action = "Patrolling"
            patrolX, patrolY = patrolPoints[patrolIndex % len(patrolPoints)]
            if abs(Goober1X - patrolX) < 0.2 and abs(Goober1Y - patrolY) < 0.2:
                patrolIndex += 1
            Goober1X, Goober1Y = MoveToward(Goober1X, Goober1Y, patrolX, patrolY, moveSpeed * 0.6)

        if not Goober1dead and not Goober2dead and ActiveEvent == "None":
            if distance(Goober1X, Goober1Y, Goober2X, Goober2Y) <= 3:
                if Goober1Health > 50 and Goober2Health > 50:
                    AttemptReproduction()

        time.sleep(1)


def Goober2AI():
    global Goober2dead, Goober2X, Goober2Y, Goober2Hunger, Goober2Thirst, Goober2Action
    global PredatorX, PredatorY
    patrolPoints = [(0, 0), (-4, 0), (0, -4), (4, 0), (0, 4), (-2, -2), (-15, 12), (10, -10), (-12, -12), (8, 15)]
    patrolIndex = 0

    while not Goober2dead:
        sightRange = max(10 * Goober2Sight, 80)
        bushTarget = FindNearestBush(Goober2X, Goober2Y, sightRange)
        pondTarget = FindNearestPond(Goober2X, Goober2Y, sightRange)
        moveSpeed = GetMoveSpeed(Goober2Speed, Goober2Hunger, Goober2Thirst)

        if PredatorActive:
            fleeTargetX = Goober2X + (Goober2X - PredatorX)
            fleeTargetY = Goober2Y + (Goober2Y - PredatorY)
            Goober2Action = "Running from predator"
            Goober2X, Goober2Y = MoveToward(Goober2X, Goober2Y, fleeTargetX, fleeTargetY, moveSpeed * 1.5)

        elif FloodActive:
            if distance(Goober2X, Goober2Y, HillX, HillY) > 8:
                Goober2Action = "Heading to the hill"
                Goober2X, Goober2Y = MoveToward(Goober2X, Goober2Y, HillX, HillY, moveSpeed * 1.5)
            else:
                Goober2Action = "On safe ground"

        elif DroughtActive:
            if pondTarget is not None:
                _, pondName, pondX, pondY = pondTarget
                if distance(Goober2X, Goober2Y, pondX, pondY) <= 2:
                    Goober2Action = f"Drinking at pond {pondName}"
                    Drink(pondName, "Goober2")
                else:
                    Goober2Action = f"Seeking water at pond {pondName}"
                    Goober2X, Goober2Y = MoveToward(Goober2X, Goober2Y, pondX, pondY, moveSpeed * 1.3)
            else:
                Goober2Action = "Searching for water"

        elif Goober2Hunger <= 6 and bushTarget is not None:
            _, bushName, bushX, bushY = bushTarget
            if distance(Goober2X, Goober2Y, bushX, bushY) <= 2:
                Goober2Action = f"Eating at bush {bushName}"
                Eat(bushName, "Goober2")
            else:
                Goober2Action = f"Heading to bush {bushName}"
                Goober2X, Goober2Y = MoveToward(Goober2X, Goober2Y, bushX, bushY, moveSpeed)

        elif Goober2Thirst <= 6 and pondTarget is not None:
            _, pondName, pondX, pondY = pondTarget
            if distance(Goober2X, Goober2Y, pondX, pondY) <= 2:
                Goober2Action = f"Drinking at pond {pondName}"
                Drink(pondName, "Goober2")
            else:
                Goober2Action = f"Heading to pond {pondName}"
                Goober2X, Goober2Y = MoveToward(Goober2X, Goober2Y, pondX, pondY, moveSpeed)

        elif bushTarget is not None and Goober2Hunger <= 8:
            _, bushName, bushX, bushY = bushTarget
            Goober2Action = f"Checking bush {bushName}"
            Goober2X, Goober2Y = MoveToward(Goober2X, Goober2Y, bushX, bushY, moveSpeed * 0.5)

        elif pondTarget is not None and Goober2Thirst <= 8:
            _, pondName, pondX, pondY = pondTarget
            Goober2Action = f"Checking pond {pondName}"
            Goober2X, Goober2Y = MoveToward(Goober2X, Goober2Y, pondX, pondY, moveSpeed * 0.5)

        else:
            Goober2Action = "Patrolling"
            patrolX, patrolY = patrolPoints[patrolIndex % len(patrolPoints)]
            if abs(Goober2X - patrolX) < 0.2 and abs(Goober2Y - patrolY) < 0.2:
                patrolIndex += 1
            Goober2X, Goober2Y = MoveToward(Goober2X, Goober2Y, patrolX, patrolY, moveSpeed * 0.6)

        time.sleep(1)


def ShowGameStats():
    while True:
        print("\n" + "=" * 110)
        print(f"{'LIFE SIM STATS':^110}")
        print("=" * 110)
        print(f"{'Name':<10} {'Health':>8} {'Hunger':>8} {'Thirst':>8} {'X':>8} {'Y':>8} {'Status':<22}")
        print("-" * 110)
        print(f"{'Goober 1':<10} {Goober1Health:>8} {Goober1Hunger:>8} {Goober1Thirst:>8} {Goober1X:>8.1f} {Goober1Y:>8.1f} {Goober1Action:<22}")
        print(f"{'Goober 2':<10} {Goober2Health:>8} {Goober2Hunger:>8} {Goober2Thirst:>8} {Goober2X:>8.1f} {Goober2Y:>8.1f} {Goober2Action:<22}")
        print("-" * 110)
        print(f"{'Resource':<10} {'X':>8} {'Y':>8} {'Fruit':>8} {'State':<10}")
        print("-" * 110)
        print(f"{'Bush 1':<10} {Bush1X:>8} {Bush1Y:>8} {Bush1Fruitnom:>8} {Bush1state:<10}")
        print(f"{'Bush 2':<10} {Bush2X:>8} {Bush2Y:>8} {Bush2Fruitnom:>8} {Bush2state:<10}")
        print(f"{'Pond 1':<10} {Pond1X:>8} {Pond1Y:>8} {'-':>8} {'Water':<10}")
        print(f"{'Pond 2':<10} {Pond2X:>8} {Pond2Y:>8} {'-':>8} {'Water':<10}")
        print(f"{'Pond 3':<10} {Pond3X:>8} {Pond3Y:>8} {'-':>8} {'Water':<10}")
        print(f"{'Event':<10} {'Current':>8} {'Offspring':>10}")
        print(f"{'Status':<10} {ActiveEvent:>8} {len(GooberChildren):>10}")
        print("=" * 110)
        time.sleep(3)


Goober1thread = threading.Thread(target=Goober1AI)
Goober2thread = threading.Thread(target=Goober2AI)
Bushregenthread = threading.Thread(target=Bushregen)
Thirstthread = threading.Thread(target=Thirstdrain)
Hungerthread = threading.Thread(target=Hungerdrain)
Health_harmthread = threading.Thread(target=Harming_healing)
StatsThread = threading.Thread(target=ShowGameStats)
Deathcheckthread = threading.Thread(target=Deathdetect)
Disasterthread = threading.Thread(target=Disastercycle)


print("Welcome to life sim!")
choice = input("Any thoughts?")
if choice == "Admin":
    print() #placeholder
else:
    print() #not placeholder
Goober1thread.start()
Goober2thread.start()
Bushregenthread.start()
Thirstthread.start()
Hungerthread.start()
Health_harmthread.start()
StatsThread.start()
Deathcheckthread.start()
Disasterthread.start()