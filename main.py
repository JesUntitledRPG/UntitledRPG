import pygame, sys, random, os, ctypes
from pygame.locals import *
def Mbox(title, text, style):
    return ctypes.windll.user32.MessageBoxW(0, text, title, style) # this is just in case I press F1
pygame.mixer.pre_init()
pygame.init()
#i now need to have this here; hopefully I won't instantly crash
char = "Player"
enemyatk = 0
hp = 100
alreadyon = False
hpmax = 100
revives = 0
gold = 10
inv = ["HealPot", "HealPot", "HealPot", "EffectClear"]
effects = [] # stats and effects meant the same in the past(R)
enemyhp = 250
inftimer = 0  # this is the effect timer for INFECTED. the better code part crashed the game on MacOS Mojave
conftimer = 0  # inftimer but for CONFUSED
zzzztimer = 0 # conftimer but for ASLEEP
drowtimer = 0 # zzzztimer but for DROWSY
charmtimer = 0 # you get the deal. i'll explain the effects here now. this effect makes it so your attack heals the mermaid.
mermaidchooser = 0 # chooses attack
mermaidtimer = 0 # ticks down time
sadtimer = 0 # and this causes you to attack weaker and heal less.
speedtimer = 0 # starting with positive effects; this causes you to do TWO things per turn!
speedacts = 0 # i ABSOULUTELY hate having to code this thing.
atkboost = 1 # multiplies attack exponentially. if burnt, resets to 1 after a turn.
burnttimer = 0 # how to roast the Untitled RPG Guy: step 1- set this to anything but 0. step 2- you did it.
freezetimer = 0 # this causes you to not do anything for a turn... it will heal you after some time though.
regentimer = 0 # health regen :D
battleexit = 0  # affects shopkeep dialogue, prices, etc...
weap = "fists"  # currently these two things do nothing. they'll affect other things later!|
armr = "clothing"  # <--same as the last comment thingy|
shields = 0 # let's do THIS.
gameround = 0  # round is APARENTLY a python function so I can't declare that
accuracy = 100  # this is primarily for the Drowsy status effect
enemy = 0 # this is mainly so PyCharm shuts up about enemies being able to be undeclared
version = "0.5.0prealpha" # used for saves
badge = "none"
versiondiff = False
availableswitch = 0
itemactive = False
useditem = "none"
usethis = 1
infimg = False
drowimg = False
confimg = False
maag = False # stands for Mouse Action Already asiGned.
shopactive = False # used to get the itemactive stuff working on the shop system
currentweap = "Sword"
currentarmr = "Leather"
currentbadge = "BottleCap"
# these are inserted into ShopInv depending on what is on sale at the moment
shopinv = ["HealPot", "EffectClear", "Save","AlarmClock",currentbadge,"IceCog","GhostPepper","GarlicBread","Shield",currentweap,currentarmr]
# originaly shopinv = ["HealPot", "EffectClear", "MaxUp", "AlarmClock", "Armor", "Weapons", "Badge"]
stock = 6
stock2 = 6
stock3 = 1
stock4 = 1
badgereadd = False
boughtitem = "1st Floor, Mushroom Mayhem" # man ninty makes some good osts. mine'll probably suck tho
# Jes, 2022-12-04 - BOY was I wrong. didn't know Exci composed that well...
buythis = 1  # having to declare all of this before usage is painful
skip = False # skips loading
# stuff to load sfx (they are laggy)
CritSlap = pygame.mixer.Sound("sfx/critslap.wav")
Slap = pygame.mixer.Sound("sfx/slap.wav")
BadSlap = pygame.mixer.Sound("sfx/badslap.wav")
BoughtSFX = pygame.mixer.Sound("sfx/purchase1.wav")
BoughtSFX2 = pygame.mixer.Sound("sfx/purchase2.wav")
ShopEnterExit = pygame.mixer.Sound("sfx/shopenterexit.wav")
ZombieBite = pygame.mixer.Sound("sfx/zombiebite.wav")
GhostConfuse = pygame.mixer.Sound("sfx/confusion.wav")
WizardDrowsy = pygame.mixer.Sound("sfx/drowsyspell.wav")
temp7 = 0
MermaidSad = pygame.mixer.Sound("sfx/mermaidsob.wav")
MermaidCharm = pygame.mixer.Sound("sfx/mermaidcharm.wav")
CritSlash = pygame.mixer.Sound("sfx/slash1.wav")
Slash = pygame.mixer.Sound("sfx/slash2.wav")
BadSlash = pygame.mixer.Sound("sfx/slash3.wav")
SaveSound = pygame.mixer.Sound("sfx/save.wav")
# the reason this is now here is to make my life easier in case I add some new thing. also this is good practice
# borrowed from 0.4.0
# thank you, stack overflow and quora
try:
    python_file = open("save.sav", "r+")
    python_file.close()
except Exception:
    print("Temporal save created so that my code doesn't want to die inside. DON'T LOAD IT PLEASE. I still haven't woked out the quirks...")
    os.umask(0)
    with open(os.open('save.sav', os.O_CREAT | os.O_WRONLY, 0o777), 'w') as fh:
        fh.write("100,100,0,0\e0.5.0prealpha,Player,fists,clothing\eHealPot,HealPot,HealPot,EffectClear,!Ignored")
        # default save.sav file. as soon as it's generated, the game'll be rebootable.
        amogus = True
        skip = True
loadattempt = "yes"
try:
    python_file = open("config.dat", "r+")
    python_file.close()
except Exception:
    print("config.dat file not found, bois. making a predef")
    os.umask(0)
    with open(os.open('config.dat', os.O_CREAT | os.O_WRONLY, 0o777), 'w') as fh:
        fh.write("N")
try:
    if amogus == True:
        print("UI not loaded: Character not found! Name defaulting to John Egbert. Why? Because EG.")
        loadattempt = "false"
        amogus = False
except Exception:
    amogus = False
print("Loading Load UI.")
if loadattempt == "yes":
    # welcome to spaghetti land, population: me
    incremental = 0
    numbers = ""
    strings = ""
    invload = ""
    python_file = open("save.sav", "r+")
    with open("save.sav") as file:
        for line in file:
            incremental = incremental + 1
            if incremental == 1:
                splitter = line
    print(splitter)
    split = splitter.split("\e")
    print(split)
    joinnumbers = split[0]
    joinstrings = split[1]
    joininv = split[2]
    numbers = ''.join(joinnumbers)
    strings = ''.join(joinstrings)
    invload = ''.join(joininv)
    print(numbers)
    strings = strings.split(",")
    numbers = numbers.split(",")
    # conversion to inventory
    invload = invload.split(",")
    inv = invload
    # string time
    if version != strings[0]:
        print("Woah, hey there. We're gonna need to do some conversion.")
        versiondiff = True
        if strings[0] == "0.3.1prealpha" or strings[0] == "0.3prealpha":
            badge = "none"
            badgereadd = True
    char = strings[1]
    weap = strings[2]
    armr = strings[3]
    try:
        badge = strings[4]
    except Exception:
        if inv.count("BottleCap") != 0:
            badge = "BottleCap"
    if badgereadd == True:
        print("hey, thanks for swapping over to this prerelease! i recognize i wasn't that helpful swapping over save formats in the middle of development...")
        print("did ManaPot/Untitled Utilty work well? hopefully so. it'll be the Untitled Updater in the future...")
        print("anywho, you now have a badge. let's get to buisness.")
    print("your save is good to go!")
    # oh boy it's time to truly whip out the SPAGHETTI CODIFICATION
    # stackoverflow, thanks guys.
    # note from 0.5.0 PA - thanks(x2)
    numbers = [int(item) for item in numbers]
    hp = numbers[0]
    hpmax = numbers[1]
    gold = numbers[2]
    gameround = numbers[3]
    try:
        revives = numbers[4]
    except Exception:
        revives = inv.count("AlarmClock")
    inv.remove("!Ignored")
    python_file.close()
    print("Save loaded.")
    battleexit = 3
icon = pygame.image.load("assets/gameicon.png")
pygame.display.set_icon(icon)
# Colours
BACKGROUND = (30, 30, 30)
RED = (255,0,0)
SCARLETRED = (255,50,0)
GREEN = (0,255,30)
LIMEGREEN = (30,180,30)
BLUE = (30,0,255)
CYAN = (0,150,255)
GRAY1 = (60,60,60)
WHITE = (255,255,255)
BLACK = (0,0,0)
# Game Setup
FPS = 30
fpsClock = pygame.time.Clock()
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
try:
    python_file = open("config.dat", "r+")
    print("opened config")
    screensettings = python_file.read()
    if screensettings == "N":
        WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    else:
        WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT),pygame.FULLSCREEN)
except Exception:
    print("oops.")
pygame.display.set_caption('Untitled RPG Game - v0.5.0 prealpha')
def redefineenemy():
    global enemy
    global gameround
    if gameround == 0:
        enemy = "Zombie"
        print("it happened_1")
    else:
        randenemy = random.randint(1, 4)
        if gameround%5 == 0:
            enemy = "Swordsman"
            print("it happened_6")
        elif randenemy == 1:
            enemy = "Zombie"
            print("it happened_2")
        elif randenemy == 2:
            enemy = "Ghost"
            print("it happened_3")
        elif randenemy == 3:
            enemy = "Wizard"
            print("it happened_4")
        elif randenemy == 4:
            enemy = "Mermaid"
            print("it happened_5")
# Terminal Variable Declarations (T.V.D)
shoptext = ""
text = ""
text2 = ""
text3 = ""
text4 = ""
text5 = ""
text6 = ""
text7 = ""
text8 = ""
text9 = ""
text10 = ""
text11 = ""
text12 = ""
text13 = ""
text14 = ""
text15 = ""
text16 = ""
text17 = ""
text18 = ""
text19 = ""
text20 = ""
# The main function that controls the game
def main():
    looping = True
    global confimg
    global infimg
    global drowimg
    global inftimer
    global conftimer
    global speedacts
    global badge
    global hp
    global hpmax
    global revives
    global shields
    global inv
    global drowtimer
    global alreadyon
    global weap
    global freezetimer
    global speedtimer
    global armr
    global sadtimer
    global charmtimer
    global mermaidchooser
    global gameround
    global shoptext
    global enemyhp
    global availableswitch
    global temp7
    global itemactive
    global atkboost
    global useditem
    global maag
    global accuracy
    global shopactive
    global shopinv
    global stock
    global stock2
    global stock3
    global enemy
    global stock4
    global boughtitem
    global regentimer
    global buythis
    global usethis
    global burnttimer
    global effects
    global rightport
    global leftport
    global mermaidtimer
    global mermaidchooser
    global gold
    # The Global Globaldeclarators of Stability
    # The main game loop
    while looping:
        if hp > hpmax:
            hp = hpmax
        # Module loader
        def shop(type="Default"):
            pygame.mixer.stop()
            pygame.mixer.init()
            pygame.mixer.Sound.play(ShopEnterExit)
            global shopactive
            global infimg
            global confimg
            global shopinv
            random.shuffle(shopinv)
            music = random.randint(1,100)
            if music > 75:
                pygame.mixer.music.load('ost/shopjes.wav')
                print("Jes")
            elif music > 50:
                pygame.mixer.music.load('ost/shopexci1.wav')
                print("Ex1")
            elif music > 25:
                pygame.mixer.music.load('ost/shopexci2.wav')
                print("Ex2")
            else:
                pygame.mixer.music.load('ost/shopexci3.wav')
                print("Ex3")
            pygame.mixer.music.play(-1)
            if type == "Default":
                print("Entering shop...")
                # use this to load a shop
                shopactive = True
                addtext("The shopkeeper welcomes you.")
                addtext("You may buy something now.")
                inftimer = effects.count("infected")
                conftimer = effects.count("confused")
                drowtimer = effects.count("drowsy")
                burnttimer = effects.count("burnt")
                freezetimer = effects.count("freeze")
                charmtimer = effects.count("charmed")
                sadtimer = effects.count("sad")
                if inftimer != 0:
                    for i in range(inftimer):
                        effects.remove("infected")
                if conftimer != 0:
                    for i in range(conftimer):
                        effects.remove("confused")
                if drowtimer != 0:
                    for i in range(drowtimer):
                        effects.remove("drowsy")
                if burnttimer != 0:
                    for i in range(burnttimer):
                        effects.remove("burnt")
                if freezetimer != 0:
                    for i in range(freezetimer):
                        effects.remove("freeze")
                if charmtimer != 0:
                    for i in range(charmtimer):
                        effects.remove("charmed")
                if sadtimer != 0:
                    for i in range(sadtimer):
                        effects.remove("sad")
                inftimer = 0
                conftimer = 0
                drowtimer = 0
                burnttimer = 0
                sadtimer = 0
                charmtimer = 0
                buythis = 0
                boughtitem = shopinv[buythis]
                itemactive = False
            elif type == "silent":
                # used for saving and loading, not recommended for other usage
                global battleexit
                shopactive = True
                print("saved data loaded.")
                addtext("Save loaded!")
                inftimer = 0
                buythis = 0
                boughtitem = shopinv[buythis]
                itemactive = False
                battleexit = 4
        # Calculate stuff
        if enemy == 0:
            redefineenemy()
        # Get inputs
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            pressed = pygame.key.get_pressed()
            if event.type == pygame.KEYUP and event.key == K_F1:
                Mbox("Help","Click on attack to attack, defend to defend, and items to use an item. Use CANCEL to cancel an action or exit from the shop.",0)
                Mbox("Helpier Help","If you're struggling with a boss, use a GhostPepper and hit it before applying an EffectClear. This'll deal 4 times the usual damage.",0)
                Mbox("Helpiest Help","Last but not least, check the Options.Dat file. You'll see some options. If I've forgotten to include a README for the file, the first option sets your game to Fullscreen.",0)
            if event.type == pygame.KEYUP and event.key == K_a and itemactive == False and shopactive == False and amogus == False or event.type == pygame.KEYUP and event.key == K_a and itemactive == False and shopactive == False or pygame.mouse.get_pos()[0] > 0 and pygame.mouse.get_pos()[1] >= 256 and pygame.mouse.get_pos()[0] < 800 and pygame.mouse.get_pos()[1] < 386 and pygame.mouse.get_pressed()[0] == True and itemactive == False and shopactive == False and maag == False and amogus == False:
                if mermaidtimer != 0:
                    mermaidtimer -= 1
                if regentimer > 0:
                    randhealthup = random.randint(1,20)
                    # TIL variables hold place in RAM, so this should do the trick and reduce RAM usage
                    addtext("Regenerated ", randhealthup, " HP.")
                    hp += randhealthup
                    regentimer -= 1
                    if regentimer == 0:
                        effects.remove("regen")
                if speedacts == 1 and speedtimer == 0:
                    effects.remove("speed")
                if speedacts == 0 and speedtimer != 0:
                    speedtimer -= 1
                    speedacts += 2
                    addtext("You start running quicker!")
                shoptext = ""
                if speedacts == 0 or freezetimer != 0:
                    enemyatk = random.randint(1, 10)
                    if enemy == "Swordsman":
                        enemyatk *= 2
                    hp = hp - enemyatk
                    if speedtimer > 0:
                        speedtimer -= 1
                    if inftimer > 0:
                        inftimer = inftimer - 1
                        infimg = False
                    if conftimer > 0:
                        conftimer = conftimer - 1
                        confimg = False
                    if drowtimer > 0:
                        drowtimer = drowtimer - 1
                        drowimg = False
                    if burnttimer > 0:
                        burnttimer = burnttimer - 1
                    if freezetimer > 0:
                        freezetimer = freezetimer - 1
                        addtext("You're thawing out...")
                        effects.remove("freeze")
                    else:
                        atk = random.randint(10,50)
                        accchk = random.randint(1,100)
                        if accchk > accuracy:
                            atk = 0
                        if atk > 40:
                            if weap == "Sword":
                                CritSlash.play()
                            else:
                                CritSlap.play()
                        elif atk > 20:
                            if weap == "Sword":
                                Slash.play()
                            else:
                                Slap.play()
                        else:
                            if weap == "Sword":
                                BadSlash.play()
                            else:
                                BadSlap.play()
                        if conftimer != 0:
                            addtext("You misstepped while trying to attack!")
                            addtext("However, you still manage to land a hit.")
                            atk = atk / 2
                        if sadtimer > 0:
                            atk = atk / 2
                            addtext("You're still saddened...")
                            sadtimer -= 1
                        if weap == "Sword":
                            atk *= 1.5
                        atk = atk * atkboost
                        enemyhp = enemyhp - atk
                        if atk != 0 and charmtimer <= 0:
                            addtext("You attack the enemy for ", atk, " DMG.")
                        elif charmtimer > 0:
                            addtext("You can't bring yourself to attack...")
                            enemyhp += atk
                            charmtimer -= 1
                        else:
                            addtext("Missed!")
                    if conftimer == 2:
                        addtext("You misstepped while trying to attack and lost ", hp, "HP.")
                    if enemyatk == 10 and enemy == "Zombie" and shields != 0 or enemyatk == 1 and enemy == "Ghost" and shields != 0 or enemyatk == 7 and enemy == "Wizard" and shields != 0 or enemyatk == 6 and enemy == "Mermaid" and shields != 0:
                        addtext("The ", enemy, " attacks you...")
                        addtext("But you block the attack with a Shield!")
                        shields -= 1
                    elif mermaidchooser == 0:
                        mermaidchooser = random.randint(1,2)
                    elif enemyatk == 6 and enemy == "Mermaid" and mermaidtimer == 0:
                        if mermaidchooser == 1 and temp7 != 1:
                            addtext("The mermaid prepares to charm you...")
                            temp7 = 1
                            mermaidtimer = 3
                        elif mermaidchooser == 2 and temp7 != 2:
                            addtext("The mermaid whips out a sad poem...")
                            temp7 = 2
                            mermaidtimer = 3
                        else:
                            print("the mermaid was undecided.")
                    elif mermaidchooser > 0 and enemy == "Mermaid" and mermaidtimer == 0:
                        if shields == 0:
                            if mermaidchooser == 1:
                                addtext("The mermaid laughs hypnotizingly!")
                                addtext("You suddenly become CHARMED...")
                                pygame.mixer.Sound.stop(MermaidCharm)
                                pygame.mixer.Sound.play(MermaidCharm)
                                effects.append("charmed")
                                mermaidtimer = 3
                                charmtimer = 3
                                mermaidchooser = 0
                            elif mermaidchooser == 2:
                                addtext("The mermaid recites a sad poem...")
                                addtext("hypnotizingly, of course.")
                                addtext("You feel your hopes are down...")
                                pygame.mixer.Sound.stop(MermaidSad)
                                pygame.mixer.Sound.play(MermaidSad)
                                effects.append("sad")
                                mermaidtimer = 3
                                sadtimer = 3
                                mermaidchooser = 0
                            else:
                                addtext("The mermaid tries to hypnotize you.")
                                addtext("You proceed to throw a shield at them.")
                                addtext("This makes them stop.")
                                shields -= 1
                    elif enemyatk == 10 and enemy == "Zombie":
                        inftimer = 3
                        addtext("The zombie bites you in the arm!")
                        addtext("The bite poisoned you and dealt 10 DMG.")
                        effects.append("infected")
                        pygame.mixer.Sound.play(ZombieBite)
                        #infimg = True
                    elif enemyatk == 1 and enemy == "Ghost":
                        conftimer = 3
                        addtext("The ghost dazes and confuses you...")
                        addtext("Taunting you, he deals 1 DMG to you.")
                        pygame.mixer.Sound.play(GhostConfuse)
                        effects.append("confused")
                        #confimg = True
                    elif enemyatk == 7 and enemy == "Wizard":
                        drowtimer = 3
                        addtext("The wizard casts arcane magic upon you.")
                        addtext("You feel sleepy...")
                        addtext("Lost 7 HP.")
                        pygame.mixer.Sound.play(WizardDrowsy)
                        effects.append("drowsy")
                        drowimg = True
                    else:
                        addtext("The enemy attacks you for ", enemyatk, " DMG!")
                    if inftimer != 0:
                        hp = hp - 5
                        inftimer = inftimer - 1
                        addtext("The infection lurches deeper...")
                        addtext("Lost 5 HP.")
                    elif inftimer > 0:
                        addtext("You defeat the infection!")
                        addtext("Lost 5 HP in the process, though.")
                        effects.remove("infected")
                        hp = hp - 5
                    if drowtimer > 0 and drowtimer != 1:
                        addtext("You are slowly falling asleep...")
                        addtext("(but a bug is moving near you.)")
                        accuracy -= 20
                    elif drowtimer == 1:
                        addtext("You are just about to fall asleep...")
                        addtext("But the bug grosses you out.")
                        addtext("You wake up.")
                        drowtimer -= 1
                        accuracy = 100
                        try:
                            effects.remove("drowsy")
                        except Exception:
                            # Look; it's 10PM and I still am a morning person. This is a WORKAROUND.
                            # It'll be removed in 0.5.1 PA. Promise.
                            print("yeah something was rushed and went wrong")
                    if conftimer != 0:
                        randchance = random.randint(0, 100)
                        if randchance == 100 or conftimer == 1:
                            addtext("You try to regain your footing...")
                            addtext("You stabilize yourself!")
                            try:
                                effects.remove("confused")
                            except Exception:
                                # Look; it's 10PM and I still am a morning person. This is a WORKAROUND.
                                # It'll be removed in 0.5.1 PA. Promise.
                                print("yeah something was rushed and went wrong")
                            conftimer = 0
                        else:
                            addtext("You try to regain your footing...")
                            addtext("but fail miserably.")
                            conftimer -= 1
                    if burnttimer > 0:
                        hp = hp - 2
                        burnttimer = burnttimer - 1
                        addtext("You got slightly burnt...")
                        addtext("Lost 2 HP.")
                        if atkboost > 1:
                            effects.remove("atkboost")
                            atkboost = 1
                    elif burnttimer == 1:
                        addtext("You finally have enough of this.")
                        addtext("You stomp on your armor.")
                        addtext("This stopped the burning.")
                        try:
                            effects.remove("burnt")
                        except Exception:
                            # Look; it's 10PM and I still am a morning person. This is a WORKAROUND.
                            # It'll be removed in 0.5.1 PA. Promise.
                            print("yeah something was rushed and went wrong")
                        atkboost = 1
                    if charmtimer == 1:
                        addtext("You break free of the charming...")
                        try:
                            effects.remove("charmed")
                        except Exception:
                            # Look; it's 10PM and I still am a morning person. This is a WORKAROUND.
                            # It'll be removed in 0.5.1 PA. Promise.
                            print("yeah something was rushed and went wrong")
                        charmtimer -= 1
                    if sadtimer == 1:
                        addtext("You reassure yourself and focus.")
                        addtext("We'll just say you're not sad now.")
                        addtext("True depression would last WAY longer.")
                        addtext("Or so I think. I really don't know.")
                        try:
                            effects.remove("sad")
                        except Exception:
                            # Look; it's 10PM and I still am a morning person. This is a WORKAROUND.
                            # It'll be removed in 0.5.1 PA. Promise.
                            print("yeah something was rushed and went wrong")
                        sadtimer -= 1
                    if armr == "Leather":
                        editedenemyatk = enemyatk / 5
                        editedenemyatk = round(editedenemyatk)
                        hp += editedenemyatk
                    if badge == "BottleCap":
                        editedenemyatk = enemyatk / 10
                        editedenemyatk = round(editedenemyatk)
                        hp += editedenemyatk
                    addtext("HP: ", hp)
                    addtext("Enemy HP: ", enemyhp)
                    maag = 30
                else:
                    atk = random.randint(10, 50)
                    if atk > 40:
                        CritSlap.play()
                    elif atk > 20:
                        Slap.play()
                    else:
                        BadSlap.play()
                    speedacts -= 1
                    print(speedacts)
                    print(speedtimer)
                    addtext("You speedily attack the ", enemy,"!")
                    addtext("Dealt ", atk, " damage.")
                    addtext("HP: ", hp)
                    addtext("Enemy HP: ", enemyhp)
                    maag = 30
                    enemyhp -= atk
            if event.type == pygame.KEYUP and event.key == K_d and itemactive == False and shopactive == False and amogus == False or pygame.mouse.get_pos()[0] > 0 and pygame.mouse.get_pos()[1] >= 386 and pygame.mouse.get_pos()[0] < 400 and pygame.mouse.get_pos()[1] < 512 and pygame.mouse.get_pressed()[0] == True and itemactive == False and shopactive == False and maag == False and amogus == False:
                if mermaidtimer != 0:
                    mermaidtimer -= 1
                if regentimer > 0:
                    randhealthup = random.randint(1,20)
                    # TIL variables hold place in RAM, so this should do the trick and reduce RAM usage
                    addtext("Regenerated ", randhealthup, " HP.")
                    hp += randhealthup
                    regentimer -= 1
                    if regentimer == 0:
                        effects.remove("regen")
                if speedacts == 1 and speedtimer == 0:
                    effects.remove("speed")
                if speedacts == 0 and speedtimer != 0:
                    speedtimer -= 1
                    speedacts += 2
                    addtext("You start running quicker!")
                shoptext = ""
                if speedacts == 0 or freezetimer != 0:
                    enemyatk = random.randint(1, 10)
                    enemyatk = enemyatk / 2
                    addtext("You defend yourself!")
                    if enemy == "Swordsman":
                        enemyatk *= 2
                    hp = hp - enemyatk
                    if speedtimer > 0:
                        speedtimer -= 1
                    if inftimer > 0:
                        inftimer = inftimer - 1
                        infimg = False
                    if conftimer > 0:
                        conftimer = conftimer - 1
                        confimg = False
                    if drowtimer > 0:
                        drowtimer = drowtimer - 1
                        drowimg = False
                    if burnttimer > 0:
                        burnttimer = burnttimer - 1
                    if freezetimer > 0:
                        freezetimer = freezetimer - 1
                        addtext("You're thawing out...")
                        effects.remove("freeze")
                    if enemyatk == 10 and enemy == "Zombie" and shields != 0 or enemyatk == 1 and enemy == "Ghost" and shields != 0 or enemyatk == 7 and enemy == "Wizard" and shields != 0 or enemyatk == 6 and enemy == "Mermaid" and shields != 0:
                        addtext("The ", enemy, " attacks you...")
                        addtext("But you block the attack with a Shield!")
                        shields -= 1
                    elif mermaidchooser == 0:
                        mermaidchooser = random.randint(1,2)
                    elif enemyatk == 6 and enemy == "Mermaid" and mermaidtimer == 0:
                        if mermaidchooser == 1 and temp7 != 1:
                            addtext("The mermaid prepares to charm you...")
                            temp7 = 1
                            mermaidtimer = 3
                        elif mermaidchooser == 2 and temp7 != 2:
                            addtext("The mermaid whips out a sad poem...")
                            temp7 = 2
                            mermaidtimer = 3
                        else:
                            print("the mermaid was undecided.")
                    elif mermaidchooser > 0 and enemy == "Mermaid" and mermaidtimer == 0:
                        if shields == 0:
                            if mermaidchooser == 1:
                                addtext("The mermaid laughs hypnotizingly!")
                                addtext("You suddenly become CHARMED...")
                                pygame.mixer.Sound.stop(MermaidCharm)
                                pygame.mixer.Sound.play(MermaidCharm)
                                effects.append("charmed")
                                mermaidtimer = 3
                                charmtimer = 3
                                mermaidchooser = 0
                            elif mermaidchooser == 2:
                                addtext("The mermaid recites a sad poem...")
                                addtext("hypnotizingly, of course.")
                                addtext("You feel your hopes are down...")
                                pygame.mixer.Sound.stop(MermaidSad)
                                pygame.mixer.Sound.play(MermaidSad)
                                effects.append("sad")
                                mermaidtimer = 3
                                sadtimer = 3
                                mermaidchooser = 0
                            else:
                                addtext("The mermaid tries to hypnotize you.")
                                addtext("You proceed to throw a shield at them.")
                                addtext("This makes them stop.")
                                shields -= 1
                    elif enemyatk == 10 and enemy == "Zombie":
                        inftimer = 3
                        addtext("The zombie bites you in the arm!")
                        addtext("The bite poisoned you and dealt 10 DMG.")
                        effects.append("infected")
                        pygame.mixer.Sound.play(ZombieBite)
                        infimg = True
                    elif enemyatk == 1 and enemy == "Ghost":
                        conftimer = 3
                        addtext("The ghost dazes and confuses you...")
                        addtext("Taunting you, he deals 1 DMG to you.")
                        pygame.mixer.Sound.play(GhostConfuse)
                        effects.append("confused")
                        #confimg = True
                    elif enemyatk == 7 and enemy == "Wizard":
                        drowtimer = 3
                        addtext("The wizard casts arcane magic upon you.")
                        addtext("You feel sleepy...")
                        addtext("Lost 7 HP.")
                        pygame.mixer.Sound.play(WizardDrowsy)
                        effects.append("drowsy")
                        drowimg = True
                    else:
                        addtext("The enemy attacks you for ", enemyatk, " DMG!")
                    if inftimer != 0:
                        hp = hp - 5
                        inftimer = inftimer - 1
                        addtext("The infection lurches deeper...")
                        addtext("Lost 5 HP.")
                    elif inftimer > 0:
                        addtext("You defeat the infection!")
                        addtext("Lost 5 HP in the process, though.")
                        effects.remove("infected")
                        hp = hp - 5
                    if drowtimer > 0 and drowtimer != 1:
                        addtext("You are slowly falling asleep...")
                        addtext("(but a bug is moving near you.)")
                        accuracy -= 20
                    elif drowtimer == 1:
                        addtext("You are just about to fall asleep...")
                        addtext("But the bug grosses you out.")
                        addtext("You wake up.")
                        drowtimer -= 1
                        accuracy = 100
                        try:
                            effects.remove("drowsy")
                        except Exception:
                            # Look; it's 10PM and I still am a morning person. This is a WORKAROUND.
                            # It'll be removed in 0.5.1 PA. Promise.
                            print("yeah something was rushed and went wrong")
                    if conftimer != 0:
                        randchance = random.randint(0, 100)
                        if randchance == 100 or conftimer == 1:
                            addtext("You try to regain your footing...")
                            addtext("You stabilize yourself!")
                            try:
                                effects.remove("confused")
                            except Exception:
                                # Look; it's 10PM and I still am a morning person. This is a WORKAROUND.
                                # It'll be removed in 0.5.1 PA. Promise.
                                print("yeah something was rushed and went wrong")
                            conftimer = 0
                        else:
                            addtext("You try to regain your footing...")
                            addtext("but fail miserably.")
                            conftimer -= 1
                    if burnttimer > 0:
                        hp = hp - 2
                        burnttimer = burnttimer - 1
                        addtext("You got slightly burnt...")
                        addtext("Lost 2 HP.")
                        if atkboost > 1:
                            effects.remove("atkboost")
                            atkboost = 1
                    elif burnttimer == 1:
                        addtext("You finally have enough of this.")
                        addtext("You stomp on your armor.")
                        addtext("This stopped the burning.")
                        try:
                            effects.remove("burnt")
                        except Exception:
                            # Look; it's 10PM and I still am a morning person. This is a WORKAROUND.
                            # It'll be removed in 0.5.1 PA. Promise.
                            print("yeah something was rushed and went wrong")
                        atkboost = 1
                    if charmtimer == 1:
                        addtext("You break free of the charming...")
                        try:
                            effects.remove("charmed")
                        except Exception:
                            # Look; it's 10PM and I still am a morning person. This is a WORKAROUND.
                            # It'll be removed in 0.5.1 PA. Promise.
                            print("yeah something was rushed and went wrong")
                        charmtimer -= 1
                    if sadtimer == 1:
                        addtext("You reassure yourself and focus.")
                        addtext("We'll just say you're not sad now.")
                        addtext("True depression would last WAY longer.")
                        addtext("Or so I think. I really don't know.")
                        try:
                            effects.remove("sad")
                        except Exception:
                            # Look; it's 10PM and I still am a morning person. This is a WORKAROUND.
                            # It'll be removed in 0.5.1 PA. Promise.
                            print("yeah something was rushed and went wrong")
                        sadtimer -= 1
                    if armr == "Leather":
                        editedenemyatk = enemyatk / 5
                        editedenemyatk = round(editedenemyatk)
                        hp += editedenemyatk
                    if badge == "BottleCap":
                        editedenemyatk = enemyatk / 10
                        editedenemyatk = round(editedenemyatk)
                        hp += editedenemyatk
                    addtext("HP: ", hp)
                    addtext("Enemy HP: ", enemyhp)
                    maag = 30
                else:
                    speedacts -= 1
                    addtext("You block speedily! However...")
                    addtext("the enemy can't even reach you because of your speed...")
                    addtext("(REMINDER: You can't block while using SPEED!)")
                    maag = 30
            if event.type == pygame.KEYUP and event.key == K_i and itemactive == False and shopactive == False and amogus == False or pygame.mouse.get_pos()[0] > 400 and pygame.mouse.get_pos()[1] >= 386 and pygame.mouse.get_pos()[0] < 800 and pygame.mouse.get_pos()[1] < 512 and pygame.mouse.get_pressed()[0] == True and itemactive == False and shopactive == False and maag == False and amogus == False:
                if freezetimer != 0:
                    addtext("You're thawing out...")
                    effects.remove("freeze")
                    enemyatk = random.randint(1, 10)
                    hp = hp - enemyatk
                    if enemyatk == 10 and enemy == "Zombie" and shields != 0 or enemyatk == 1 and enemy == "Ghost" and shields != 0 or enemyatk == 7 and enemy == "Wizard" and shields != 0 or enemyatk == 6 and enemy == "Mermaid" and shields != 0:
                        addtext("The ", enemy, " attacks you...")
                        addtext("But you block the attack with a Shield!")
                        shields -= 1
                    elif mermaidchooser == 0:
                        mermaidchooser = random.randint(1,2)
                    elif enemyatk == 6 and enemy == "Mermaid" and mermaidtimer == 0:
                        if mermaidchooser == 1 and temp7 != 1:
                            addtext("The mermaid prepares to charm you...")
                            temp7 = 1
                            mermaidtimer = 3
                        elif mermaidchooser == 2 and temp7 != 2:
                            addtext("The mermaid whips out a sad poem...")
                            temp7 = 2
                            mermaidtimer = 3
                        else:
                            print("the mermaid was undecided.")
                    elif mermaidchooser > 0 and enemy == "Mermaid" and mermaidtimer == 0:
                        if shields == 0:
                            if mermaidchooser == 1:
                                addtext("The mermaid laughs hypnotizingly!")
                                addtext("You suddenly become CHARMED...")
                                pygame.mixer.Sound.stop(MermaidCharm)
                                pygame.mixer.Sound.play(MermaidCharm)
                                effects.append("charmed")
                                mermaidtimer = 3
                                charmtimer = 3
                                mermaidchooser = 0
                            elif mermaidchooser == 2:
                                addtext("The mermaid recites a sad poem...")
                                addtext("hypnotizingly, of course.")
                                addtext("You feel your hopes are down...")
                                pygame.mixer.Sound.stop(MermaidSad)
                                pygame.mixer.Sound.play(MermaidSad)
                                effects.append("sad")
                                mermaidtimer = 3
                                sadtimer = 3
                                mermaidchooser = 0
                            else:
                                addtext("The mermaid tries to hypnotize you.")
                                addtext("You proceed to throw a shield at them.")
                                addtext("This makes them stop.")
                                shields -= 1
                    elif enemyatk == 10 and enemy == "Zombie":
                        inftimer = 3
                        addtext("The zombie bites you in the arm!")
                        addtext("The bite poisoned you and dealt 10 DMG.")
                        effects.append("infected")
                        pygame.mixer.Sound.play(ZombieBite)
                        infimg = True
                    elif enemyatk == 1 and enemy == "Ghost":
                        conftimer = 3
                        addtext("The ghost dazes and confuses you...")
                        addtext("Taunting you, he deals 1 DMG to you.")
                        pygame.mixer.Sound.play(GhostConfuse)
                        effects.append("confused")
                        #confimg = True
                    elif enemyatk == 7 and enemy == "Wizard":
                        drowtimer = 3
                        addtext("The wizard casts arcane magic upon you.")
                        addtext("You feel sleepy...")
                        addtext("Lost 7 HP.")
                        pygame.mixer.Sound.play(WizardDrowsy)
                        effects.append("drowsy")
                        drowimg = True
                    else:
                        addtext("The enemy attacks you for ", enemyatk, " DMG!")
                    if inftimer != 0:
                        hp = hp - 5
                        inftimer = inftimer - 1
                        addtext("The infection lurches deeper...")
                        addtext("Lost 5 HP.")
                    elif inftimer > 0:
                        addtext("You defeat the infection!")
                        addtext("Lost 5 HP in the process, though.")
                        effects.remove("infected")
                        hp = hp - 5
                    if drowtimer > 0 and drowtimer != 1:
                        addtext("You are slowly falling asleep...")
                        addtext("(but a bug is moving near you.)")
                        accuracy -= 20
                    elif drowtimer == 1:
                        addtext("You are just about to fall asleep...")
                        addtext("But the bug grosses you out.")
                        addtext("You wake up.")
                        drowtimer -= 1
                        accuracy = 100
                        try:
                            effects.remove("drowsy")
                        except Exception:
                            # Look; it's 10PM and I still am a morning person. This is a WORKAROUND.
                            # It'll be removed in 0.5.1 PA. Promise.
                            print("yeah something was rushed and went wrong")
                    if conftimer != 0:
                        randchance = random.randint(0, 100)
                        if randchance == 100 or conftimer == 1:
                            addtext("You try to regain your footing...")
                            addtext("You stabilize yourself!")
                            try:
                                effects.remove("confused")
                            except Exception:
                                # Look; it's 10PM and I still am a morning person. This is a WORKAROUND.
                                # It'll be removed in 0.5.1 PA. Promise.
                                print("yeah something was rushed and went wrong")
                            conftimer = 0
                        else:
                            addtext("You try to regain your footing...")
                            addtext("but fail miserably.")
                            conftimer -= 1
                    if burnttimer > 0:
                        hp = hp - 2
                        burnttimer = burnttimer - 1
                        addtext("You got slightly burnt...")
                        addtext("Lost 2 HP.")
                        if atkboost > 1:
                            effects.remove("atkboost")
                            atkboost = 1
                    elif burnttimer == 1:
                        addtext("You finally have enough of this.")
                        addtext("You stomp on your armor.")
                        addtext("This stopped the burning.")
                        try:
                            effects.remove("burnt")
                        except Exception:
                            # Look; it's 10PM and I still am a morning person. This is a WORKAROUND.
                            # It'll be removed in 0.5.1 PA. Promise.
                            print("yeah something was rushed and went wrong")
                        atkboost = 1
                    if charmtimer == 1:
                        addtext("You break free of the charming...")
                        try:
                            effects.remove("charmed")
                        except Exception:
                            # Look; it's 10PM and I still am a morning person. This is a WORKAROUND.
                            # It'll be removed in 0.5.1 PA. Promise.
                            print("yeah something was rushed and went wrong")
                        charmtimer -= 1
                    if sadtimer == 1:
                        addtext("You reassure yourself and focus.")
                        addtext("We'll just say you're not sad now.")
                        addtext("True depression would last WAY longer.")
                        addtext("Or so I think. I really don't know.")
                        try:
                            effects.remove("sad")
                        except Exception:
                            # Look; it's 10PM and I still am a morning person. This is a WORKAROUND.
                            # It'll be removed in 0.5.1 PA. Promise.
                            print("yeah something was rushed and went wrong")
                        sadtimer -= 1
                    if armr == "Leather":
                        editedenemyatk = enemyatk / 5
                        editedenemyatk = round(editedenemyatk)
                        hp += editedenemyatk
                    if badge == "BottleCap":
                        editedenemyatk = enemyatk / 10
                        editedenemyatk = round(editedenemyatk)
                        hp += editedenemyatk
                    addtext("HP: ", hp)
                    addtext("Enemy HP: ", enemyhp)
                    maag = 30
                try:
                    global inv
                    infimg = False
                    confimg = False
                    itemactive = 9
                    usethis = 0
                    useditem = inv[usethis]
                    addtext("What item do you want to use?")
                except Exception:
                    addtext("No items found!")
                    itemactive = 0
                maag = 30
            if event.type == pygame.KEYUP and event.key == K_i and itemactive == 1 and shopactive == False and amogus == False and shopactive == False or pygame.mouse.get_pos()[0] > 0 and pygame.mouse.get_pos()[1] >= 256 and pygame.mouse.get_pos()[0] < 800 and pygame.mouse.get_pos()[1] < 386 and pygame.mouse.get_pressed()[0] == True and itemactive == 1 and shopactive == False and maag == False and amogus == False:
                addtext("Used ", useditem, ".")
                itemactive = False
                if useditem == "HealPot":
                    hp = hp + 30
                    addtext("You recovered 30 HP!")
                    inv.remove("HealPot")
                elif useditem == "Shield":
                    shields += 1
                    addtext("You shield yourself...")
                    inv.remove("Shield")
                elif useditem == "GarlicBread":
                    hp = hp + 30
                    addtext("You're now regenerating.")
                    addtext("GarlicBread is THAT good.")
                    regentimer = 3
                    inv.remove("GarlicBread")
                    effects.append("regen")
                elif useditem == "EffectClear":
                    inftimer = 0
                    conftimer = 0
                    drowtimer = 0
                    burnttimer = 0
                    charmtimer = 0
                    sadtimer = 0
                    regentimer = 0
                    speedtimer = 0
                    atkboost = 1
                    freezetimer = 0
                    accuracy = 100
                    addtext("You feel like new.")
                    effects = []
                    inv.remove("EffectClear")
                elif useditem == "AlarmClock":
                    addtext("You press some buttons. Nothing happens.")
                elif useditem == "GhostPepper":
                    addtext("You feel stronger...")
                    addtext("although you're burning.")
                    atkboost += 4
                    burnttimer = 3
                    effects.append("atkboost")
                    effects.append("burnt")
                elif useditem == "BottleCap":
                    addtext("Shiny! And cool, sure, but SHINY!")
                    shoptext = ""
                elif useditem == "IceCog":
                    addtext("You consume the IceCog...")
                    addtext("You got frozen!")
                    addtext("You feel swifter though...")
                    freezetimer = 1
                    speedtimer = 3
                    speedacts = 1
                    effects.append("freeze")
                    effects.append("speed")
                shoptext = ""
                maag = 30
            if event.type == pygame.KEYUP and event.key == K_d and itemactive == 1 and shopactive == False and amogus == False or pygame.mouse.get_pos()[0] > 400 and pygame.mouse.get_pos()[1] >= 386 and pygame.mouse.get_pos()[0] < 800 and pygame.mouse.get_pos()[1] < 512 and pygame.mouse.get_pressed()[0] == True and itemactive == 1 and shopactive == False and maag == False and amogus == False:
                if usethis == len(inv) - 1:
                    usethis = 0
                    useditem = inv[usethis]
                else:
                    usethis = usethis + 1
                    useditem = inv[usethis]
                maag = 30
            if event.type == pygame.KEYUP and event.key == K_i and itemactive == 1 and shopactive == False and amogus == False or pygame.mouse.get_pos()[0] > 0 and pygame.mouse.get_pos()[1] >= 386 and pygame.mouse.get_pos()[0] < 400 and pygame.mouse.get_pos()[1] < 512 and pygame.mouse.get_pressed()[0] == True and itemactive == 1 and shopactive == False and maag == False and amogus == False:
                if usethis == 0:
                    usethis = len(inv) - 1
                    useditem = inv[usethis]
                else:
                    usethis = usethis - 1
                    useditem = inv[usethis]
                maag = 30
            if event.type == pygame.KEYUP and event.key == K_c and itemactive == 1 and shopactive == False and amogus == False or pygame.mouse.get_pos()[0] > 0 and pygame.mouse.get_pos()[1] >= 512 and pygame.mouse.get_pos()[0] < 800 and pygame.mouse.get_pos()[1] < 640 and pygame.mouse.get_pressed()[0] == True and itemactive == 1 and shopactive == False and maag == False and amogus == False:
                addtext("Cancelled action.")
                shoptext = ""
                itemactive = False
                maag = 30
            if event.type == pygame.KEYUP and event.key == K_i and itemactive == False and shopactive == True and amogus == False or pygame.mouse.get_pos()[0] > 0 and pygame.mouse.get_pos()[1] >= 256 and pygame.mouse.get_pos()[0] < 800 and pygame.mouse.get_pos()[1] < 386 and pygame.mouse.get_pressed()[0] == True and itemactive == False and shopactive == True and maag == False and amogus == False:
                if boughtitem == "HealPot":
                    gold = gold - 10
                    if gold < 0:
                        addtext("Not enough gold!")
                        gold = gold + 10
                        maag = 30
                    else:
                        inv.append("HealPot")
                        addtext("Bought a HealPot!")
                        maag = 30
                        randchance = random.randint(1,2)
                        if randchance == 1:
                            pygame.mixer.Sound.play(BoughtSFX)
                        elif randchance == 2:
                            pygame.mixer.Sound.play(BoughtSFX2)
                if boughtitem == "GarlicBread":
                    gold = gold - 75
                    if gold < 0:
                        addtext("Not enough gold!")
                        gold = gold + 75
                        maag = 30
                    else:
                        inv.append("GarlicBread")
                        addtext("Bought some GarlicBread!")
                        # i have never tried garlic bread before. if anyone sees this archaic code before v1.0.0 FINAL RELEASE, remind me to consume some garlic bread.
                        maag = 30
                        randchance = random.randint(1,2)
                        if randchance == 1:
                            pygame.mixer.Sound.play(BoughtSFX)
                        elif randchance == 2:
                            pygame.mixer.Sound.play(BoughtSFX2)
                elif boughtitem == "EffectClear":
                    gold = gold - 10
                    if gold < 0:
                        addtext("Not enough gold!")
                        gold = gold + 10
                    else:
                        inv.append("EffectClear")
                        addtext("Bought a EffectClear!")
                        maag = 30
                        randchance = random.randint(1,2)
                        if randchance == 1:
                            pygame.mixer.Sound.play(BoughtSFX)
                        elif randchance == 2:
                            pygame.mixer.Sound.play(BoughtSFX2)
                elif boughtitem == "AlarmClock":
                    gold = gold - 300
                    if gold < 0:
                        addtext("Not enough gold!")
                        gold = gold + 300
                    else:
                        inv.append("AlarmClock")
                        addtext("Bought an AlarmClock!")
                        revives =+ 1
                        maag = 30
                        randchance = random.randint(1,2)
                        if randchance == 1:
                            pygame.mixer.Sound.play(BoughtSFX)
                        elif randchance == 2:
                            pygame.mixer.Sound.play(BoughtSFX2)
                elif boughtitem == "IceCog":
                    gold = gold - 50
                    if gold < 0:
                        addtext("Not enough gold!")
                        gold = gold + 50
                    else:
                        inv.append("IceCog")
                        addtext("Bought an IceCog!")
                        maag = 30
                        randchance = random.randint(1,2)
                        if randchance == 1:
                            pygame.mixer.Sound.play(BoughtSFX)
                        elif randchance == 2:
                            pygame.mixer.Sound.play(BoughtSFX2)
                elif boughtitem == "GhostPepper":
                    gold = gold - 50
                    if gold < 0:
                        addtext("Not enough gold!")
                        gold = gold + 50
                    else:
                        inv.append("GhostPepper")
                        addtext("Bought a GhostPepper!")
                        maag = 30
                        randchance = random.randint(1,2)
                        if randchance == 1:
                            pygame.mixer.Sound.play(BoughtSFX)
                        elif randchance == 2:
                            pygame.mixer.Sound.play(BoughtSFX2)
                elif boughtitem == "BottleCap":
                    gold = gold - 150
                    if gold < 0:
                        addtext("Not enough gold!")
                        gold = gold + 150
                    elif badge == "BottleCap":
                        gold += 150
                        addtext("You already have a BottleCap.")
                        addtext("No, you can't have two. That'd be dumb.")
                        print(badge)
                    else:
                        inv.append("BottleCap")
                        badge = "BottleCap"
                        addtext("Bought a BottleCap!")
                        addtext("You feel a bit safer now...")
                        print(badge)
                        maag = 30
                        randchance = random.randint(1,2)
                        if randchance == 1:
                            pygame.mixer.Sound.play(BoughtSFX)
                        elif randchance == 2:
                            pygame.mixer.Sound.play(BoughtSFX2)
                elif boughtitem == "Sword":
                    gold = gold - 500
                    if gold < 0:
                        addtext("Not enough gold!")
                        gold = gold + 500
                        maag = 30
                    elif weap == "Sword":
                        gold += 500
                        addtext("You already have a Sword.")
                        addtext("You can't have 2. You won't dual-wield.")
                        addtext("Buy a new weapon if you need it.")
                        print(weap)
                        maag = 30
                    else:
                        weap = "Sword"
                        addtext("Bought a Sword!")
                        addtext("You feel way stronger...")
                        print(weap)
                        maag = 30
                        randchance = random.randint(1,2)
                        if randchance == 1:
                            pygame.mixer.Sound.play(BoughtSFX)
                        elif randchance == 2:
                            pygame.mixer.Sound.play(BoughtSFX2)
                elif boughtitem == "Leather":
                    gold = gold - 500
                    if gold < 0:
                        addtext("Not enough gold!")
                        gold = gold + 500
                        maag = 30
                    elif armr == "Leather":
                        gold += 500
                        addtext("You already have Leather Armor.")
                        addtext("Buy some new armor if you need some.")
                        print(armr)
                        maag = 30
                    else:
                        armr = "Leather"
                        addtext("Bought Leather Armor!")
                        addtext("You feel a lot safer now.")
                        print(armr)
                        maag = 30
                        randchance = random.randint(1,2)
                        if randchance == 1:
                            pygame.mixer.Sound.play(BoughtSFX)
                        elif randchance == 2:
                            pygame.mixer.Sound.play(BoughtSFX2)
                elif boughtitem == "Shield":
                    gold = gold - 150
                    if gold < 0:
                        addtext("Not enough gold!")
                        gold = gold + 150
                    elif inv.count("Shield") > 0:
                        gold += 150
                        addtext("You already have a Shield.")
                        addtext("They're heavy, alright? You can't have 2.")
                        print(badge)
                    else:
                        inv.append("Shield")
                        addtext("Bought a Shield!")
                        addtext("Oh, wait. An EffectShield.")
                        addtext("We're just calling it a Shield, though.")
                        maag = 30
                        randchance = random.randint(1,2)
                        if randchance == 1:
                            pygame.mixer.Sound.play(BoughtSFX)
                        elif randchance == 2:
                            pygame.mixer.Sound.play(BoughtSFX2)
                elif boughtitem == "Save":
                    python_file = open("save.sav", "r+")
                    hp = int(hp)
                    hpmax = int(hpmax)
                    gold = int(gold)
                    gameround = int(gameround)
                    # all of this because of an error. bruh
                    strings = [version, ",", char, ",", weap, ",", armr, ",", badge]
                    variables = [hp, ",", hpmax, ",", gold, ",", gameround, ",", revives]
                    saveinv = []
                    for element in inv:
                        saveinv.append(element + ",")
                    x = "x"
                    saveinv.append(x)
                    saveinv.remove(x)
                    begintransform = ''.join(str(x) for x in variables)
                    saveinv.append("!Ignored")
                    saveline1 = ''.join(begintransform)
                    saveline2 = ''.join(strings)
                    saveline3 = ''.join(saveinv)
                    python_file.write(saveline1)
                    python_file.write("\e")
                    python_file.write(saveline2)
                    python_file.write("\e")
                    python_file.write(saveline3)
                    python_file.close()
                    # alright! saving ported. loading is going to be a whole other can of worms... ui time!
                    addtext("GAME SAVED.")
                    pygame.mixer.Sound.stop(SaveSound)
                    pygame.mixer.Sound.play(SaveSound)
            if event.type == pygame.KEYUP and event.key == K_d and itemactive == False and shopactive == True and amogus == False or pygame.mouse.get_pos()[0] > 400 and pygame.mouse.get_pos()[1] >= 386 and pygame.mouse.get_pos()[0] < 800 and pygame.mouse.get_pos()[1] < 512 and pygame.mouse.get_pressed()[0] == True and itemactive == False and shopactive == True and maag == False and amogus == False:
                if buythis == len(shopinv) - 1:
                    buythis = 0
                    boughtitem = shopinv[buythis]
                else:
                    buythis = buythis + 1
                    boughtitem = shopinv[buythis]
                maag = 30
            if event.type == pygame.KEYUP and event.key == K_a and itemactive == False and shopactive == True and amogus == False or pygame.mouse.get_pos()[0] > 0 and pygame.mouse.get_pos()[1] >= 386 and pygame.mouse.get_pos()[0] < 400 and pygame.mouse.get_pos()[1] < 512 and pygame.mouse.get_pressed()[0] == True and itemactive == False and shopactive == True and maag == False and amogus == False:
                if buythis == 0:
                    buythis = len(shopinv) - 1
                    boughtitem = shopinv[buythis]
                else:
                    buythis = buythis - 1
                    boughtitem = shopinv[buythis]
                maag = 30
            if event.type == pygame.KEYUP and event.key == K_c and itemactive == False and shopactive == True and amogus == False or pygame.mouse.get_pos()[0] > 0 and pygame.mouse.get_pos()[1] >= 512 and pygame.mouse.get_pos()[0] < 800 and pygame.mouse.get_pos()[1] < 640 and pygame.mouse.get_pressed()[0] == True and itemactive == False and shopactive == True and maag == False and amogus == False:
                shopactive = False
                addtext("You leave the shop.")
                pygame.mixer.Sound.stop(ShopEnterExit)
                pygame.mixer.Sound.play(ShopEnterExit)
                randhealthup = random.randint(20,30)
                pygame.mixer.music.fadeout(2000)
                redefineenemy()
                if enemy == "Zombie":
                    enemyhp = 250
                elif enemy == "Ghost":
                    enemyhp = 300
                elif enemy == "Wizard":
                    enemyhp = 350
                elif enemy == "Mermaid":
                    enemyhp = 450
                elif enemy == "Swordsman":
                    enemyhp = 600
                addtext("Recovered ", randhealthup, " HP.")
                hp = hp + randhealthup
                shoptext = ""
                maag = 30
        if maag != False:
            maag = maag - 3
            if maag == 0:
                maag == False
        # Processing
        if hp <= 0 and revives <= 0:
            infimg = False
            confimg = False
            enemyhp = 0.01
            addtext("You lost...")
            hp = hpmax
            shop()
            gameround = gameround + 1
            shopactive = True
        elif hp <= 0 and revives > 0:
            addtext("You fall flat into the ground...")
            pygame.time.wait(1000)
            addtext("and then the AlarmClock goes off.")
            pygame.time.wait(1000)
            addtext("You pop out of the ground!")
            addtext("You do smash the AlarmClock...")
            inv.remove("AlarmClock")
            hp = hpmax/2
            revives =- 1
        elif enemyhp <= 0:
            infimg = False
            confimg = False
            enemyhp = 0.01
            addtext("You win!")
            addgold = random.randint(10,50)
            gold = gold + addgold
            addtext("Got ",addgold," Gold.")
            gameround = gameround + 1
            shop()
            shopactive = True
        commandintbar = pygame.Rect(800,48,12,620)
        enemyhpbarfill = pygame.Rect(800,24,400,24)
        hpbarfill = pygame.Rect(800, 0, 400, 24)
        hpbarfill.width = hp * 3.90
        if enemy == "Zombie":
            enemyhpbarfill.width = enemyhp * 1.66
        elif enemy == "Ghost":
            enemyhpbarfill.width = enemyhp * 1.30
        elif enemy == "Wizard":
            enemyhpbarfill.width = enemyhp * 1.30
        elif enemy == "Mermaid":
            enemyhpbarfill.width = enemyhp * 0.86
        elif enemy == "Swordsman":
            enemyhpbarfill.width = enemyhp * 0.66
        fontObj = pygame.font.Font('fonts/RobotoMono-Regular.ttf', 19)
        # i personally have no problem incorporating this for the shop
        itemShopFontObj = pygame.font.Font('fonts/RobotoMono-Light.ttf', 12)
        shopTerm = itemShopFontObj.render(shoptext, True, WHITE, None)
        shopTermObj = shopTerm.get_rect()
        goldtext = str(gold)
        GoldTerm = itemShopFontObj.render(goldtext, True, BLACK, None)
        fpsClockCount = str(FPS)
        FPSClockView = itemShopFontObj.render(fpsClockCount, True, WHITE, None)
        FPSClockViewObj = FPSClockView.get_rect()
        # text = "" + str(enemyhp) displays text and the specified variable
        Terminal = fontObj.render(text, True, WHITE, None)
        textRectObj = Terminal.get_rect()
        Terminal2 = fontObj.render(text2, True, WHITE, None)
        textRectObj2 = Terminal2.get_rect()
        Terminal3 = fontObj.render(text3, True, WHITE, None)
        textRectObj3 = Terminal3.get_rect()
        Terminal4 = fontObj.render(text4, True, WHITE, None)
        textRectObj4 = Terminal4.get_rect()
        Terminal5 = fontObj.render(text5, True, WHITE, None)
        textRectObj5 = Terminal5.get_rect()
        Terminal6 = fontObj.render(text6, True, WHITE, None)
        textRectObj6 = Terminal6.get_rect()
        Terminal7 = fontObj.render(text7, True, WHITE, None)
        textRectObj7 = Terminal7.get_rect()
        Terminal8 = fontObj.render(text8, True, WHITE, None)
        textRectObj8 = Terminal8.get_rect()
        Terminal9 = fontObj.render(text9, True, WHITE, None)
        textRectObj9 = Terminal9.get_rect()
        Terminal10 = fontObj.render(text10, True, WHITE, None)
        textRectObj10 = Terminal10.get_rect()
        Terminal11 = fontObj.render(text11, True, WHITE, None)
        textRectObj11 = Terminal11.get_rect()
        Terminal12 = fontObj.render(text12, True, WHITE, None)
        textRectObj12 = Terminal12.get_rect()
        Terminal13 = fontObj.render(text13, True, WHITE, None)
        textRectObj13 = Terminal13.get_rect()
        Terminal14 = fontObj.render(text14, True, WHITE, None)
        textRectObj14 = Terminal14.get_rect()
        Terminal15 = fontObj.render(text15, True, WHITE, None)
        textRectObj15 = Terminal15.get_rect()
        Terminal16 = fontObj.render(text16, True, WHITE, None)
        textRectObj16 = Terminal16.get_rect()
        Terminal17 = fontObj.render(text17, True, WHITE, None)
        textRectObj17 = Terminal17.get_rect()
        Terminal18 = fontObj.render(text18, True, WHITE, None)
        textRectObj18 = Terminal18.get_rect()
        Terminal19 = fontObj.render(text19, True, WHITE, None)
        textRectObj19 = Terminal19.get_rect()
        Terminal20 = fontObj.render(text20, True, WHITE, None)
        textRectObj20 = Terminal20.get_rect()
        # Wow. This... is unefficient. I really need to learn to fix this up...
        # And now for the switch mechanism.
        # Prevents infinite declarations! Should save some FPS in the long AND short term.
        if alreadyon == False:
            alreadyon = True
            def switchcheck():
                global text
                global text1
                global text2
                global text3
                global text4
                global text5
                global text6
                global text7
                global text8
                global text9
                global text10
                global text11
                global text12
                global text13
                global text14
                global text15
                global text16
                global text17
                global text18
                global text19
                global text20
                global availableswitch
                availableswitch = 0
                if text != "":
                    availableswitch = 1
                    if text2 != "":
                        availableswitch = 2
                        if text3 != "":
                            availableswitch = 3
                            if text4 != "":
                                availableswitch = 4
                                if text5 != "":
                                    availableswitch = 5
                                    if text6 != "":
                                        availableswitch = 6
                                        if text7 != "":
                                            availableswitch = 7
                                            if text8 != "":
                                                availableswitch = 8
                                                if text9 != "":
                                                    availableswitch = availableswitch + 1
                                                    if text10 != "":
                                                        availableswitch = availableswitch + 1
                                                        if text11 != "":
                                                            availableswitch = availableswitch + 1
                                                            if text12 != "":
                                                                availableswitch = availableswitch + 1
                                                                if text13 != "":
                                                                    availableswitch = availableswitch + 1
                                                                    if text14 != "":
                                                                        availableswitch = availableswitch + 1
                                                                        if text15 != "":
                                                                            availableswitch = availableswitch + 1
                                                                            if text16 != "":
                                                                                availableswitch = availableswitch + 1
                                                                                if text17 != "":
                                                                                    availableswitch = availableswitch + 1
                                                                                    if text18 != "":
                                                                                        availableswitch = availableswitch + 1
                                                                                        if text19 != "":
                                                                                            availableswitch = availableswitch + 1
                                                                                            if text20 != "" :
                                                                                                temp = "holder"
                                                                                                temp2 = "holder2"
                                                                                                temp = text19
                                                                                                text19 = text20
                                                                                                temp2 = text18
                                                                                                text18 = temp
                                                                                                temp = text17
                                                                                                text17 = temp2
                                                                                                temp2 = text16
                                                                                                text16 = temp
                                                                                                temp = text15
                                                                                                text15 = temp2
                                                                                                temp2 = text14
                                                                                                text14 = temp
                                                                                                temp = text13
                                                                                                text13 = temp2
                                                                                                temp2 = text12
                                                                                                text12 = temp
                                                                                                temp = text11
                                                                                                text11 = temp2
                                                                                                temp2 = text10
                                                                                                text10 = temp
                                                                                                temp = text9
                                                                                                text9 = temp2
                                                                                                temp2 = text8
                                                                                                text8 = temp
                                                                                                temp = text7
                                                                                                text7 = temp2
                                                                                                temp2 = text6
                                                                                                text6 = temp
                                                                                                temp = text5
                                                                                                text5 = temp2
                                                                                                temp2 = text4
                                                                                                text4 = temp
                                                                                                temp = text3
                                                                                                text3 = temp2
                                                                                                temp2 = text2
                                                                                                text2 = temp
                                                                                                text = temp2
                                                                                                availableswitch = 19
            # please help me make this more efficient. PLEASE. I AM BEGGING YOU.
            # alright now for the text adder
            def addtext(whattoprint,var=False,extratext=False):
                switchcheck()
                global text
                global text1
                global text2
                global text3
                global text4
                global text5
                global text6
                global text7
                global text8
                global text9
                global text10
                global text11
                global text12
                global text13
                global text14
                global text15
                global text16
                global text17
                global text18
                global text19
                global text20
                if var == False and extratext == False:
                    if availableswitch == 0:
                        text = whattoprint
                    if availableswitch == 1:
                        text2 = whattoprint
                    if availableswitch == 2:
                        text3 = whattoprint
                    if availableswitch == 3:
                        text4 = whattoprint
                    if availableswitch == 4:
                        text5 = whattoprint
                    if availableswitch == 5:
                        text6 = whattoprint
                    if availableswitch == 6:
                        text7 = whattoprint
                    if availableswitch == 7:
                        text8 = whattoprint
                    if availableswitch == 8:
                        text9 = whattoprint
                    if availableswitch == 9:
                        text10 = whattoprint
                    if availableswitch == 10:
                        text11 = whattoprint
                    if availableswitch == 11:
                        text12 = whattoprint
                    if availableswitch == 12:
                        text13 = whattoprint
                    if availableswitch == 13:
                        text14 = whattoprint
                    if availableswitch == 14:
                        text15 = whattoprint
                    if availableswitch == 15:
                        text16 = whattoprint
                    if availableswitch == 16:
                        text17 = whattoprint
                    if availableswitch == 17:
                        text18 = whattoprint
                    if availableswitch == 18:
                        text19 = whattoprint
                    if availableswitch == 19:
                        text20 = whattoprint
                elif var != False and extratext == False:
                    if availableswitch == 0:
                        text = whattoprint + str(var)
                    if availableswitch == 1:
                        text2 = whattoprint + str(var)
                    if availableswitch == 2:
                        text3 = whattoprint + str(var)
                    if availableswitch == 3:
                        text4 = whattoprint + str(var)
                    if availableswitch == 4:
                        text5 = whattoprint + str(var)
                    if availableswitch == 5:
                        text6 = whattoprint + str(var)
                    if availableswitch == 6:
                        text7 = whattoprint + str(var)
                    if availableswitch == 7:
                        text8 = whattoprint + str(var)
                    if availableswitch == 8:
                        text9 = whattoprint + str(var)
                    if availableswitch == 9:
                        text10 = whattoprint + str(var)
                    if availableswitch == 10:
                        text11 = whattoprint + str(var)
                    if availableswitch == 11:
                        text12 = whattoprint + str(var)
                    if availableswitch == 12:
                        text13 = whattoprint + str(var)
                    if availableswitch == 13:
                        text14 = whattoprint + str(var)
                    if availableswitch == 14:
                        text15 = whattoprint + str(var)
                    if availableswitch == 15:
                        text16 = whattoprint + str(var)
                    if availableswitch == 16:
                        text17 = whattoprint + str(var)
                    if availableswitch == 17:
                        text18 = whattoprint + str(var)
                    if availableswitch == 18:
                        text19 = whattoprint + str(var)
                    if availableswitch == 19:
                        text20 = whattoprint + str(var)
                elif var != False and extratext != False:
                    if availableswitch == 0:
                        text = whattoprint + str(var) + extratext
                    if availableswitch == 1:
                        text2 = whattoprint + str(var) + extratext
                    if availableswitch == 2:
                        text3 = whattoprint + str(var) + extratext
                    if availableswitch == 3:
                        text4 = whattoprint + str(var) + extratext
                    if availableswitch == 4:
                        text5 = whattoprint + str(var) + extratext
                    if availableswitch == 5:
                        text6 = whattoprint + str(var) + extratext
                    if availableswitch == 6:
                        text7 = whattoprint + str(var) + extratext
                    if availableswitch == 7:
                        text8 = whattoprint + str(var) + extratext
                    if availableswitch == 8:
                        text9 = whattoprint + str(var) + extratext
                    if availableswitch == 9:
                        text10 = whattoprint + str(var) + extratext
                    if availableswitch == 10:
                        text11 = whattoprint + str(var) + extratext
                    if availableswitch == 11:
                        text12 = whattoprint + str(var) + extratext
                    if availableswitch == 12:
                        text13 = whattoprint + str(var) + extratext
                    if availableswitch == 13:
                        text14 = whattoprint + str(var) + extratext
                    if availableswitch == 14:
                        text15 = whattoprint + str(var) + extratext
                    if availableswitch == 15:
                        text16 = whattoprint + str(var) + extratext
                    if availableswitch == 16:
                        text17 = whattoprint + str(var) + extratext
                    if availableswitch == 17:
                        text18 = whattoprint + str(var) + extratext
                    if availableswitch == 18:
                        text19 = whattoprint + str(var) + extratext
                    if availableswitch == 19:
                        text20 = whattoprint + str(var) + extratext
                else:
                    print("You can't use the EXTRATEXT parameter without a variable!")
                    print("wait a second, HOW DID YOU EVEN GET THIS HANDLER?!")
                    print("If you're seeing this, Jes just broke all the laws of mathematics and coding OR python did so.")
                    print("Whatever the case, please call an ambulance for any coders nearby.")
        # Render elements of the game
        WINDOW.fill(BACKGROUND)
        if shopactive == True:
            textoverlay = pygame.image.load('assets/textoverlay.png')
            WINDOW.blit(textoverlay, (0,240))
            shoprect1 = pygame.Rect(240, 0, 40, 240)
            pygame.draw.rect(WINDOW, WHITE, shoprect1)
            shoprect2 = pygame.Rect(520, 0, 40, 240)
            pygame.draw.rect(WINDOW, WHITE, shoprect2)
            boughtitem = shopinv[buythis]
            if boughtitem == "Save":
                midport = pygame.image.load('assets/floppydisk_shop.png').convert_alpha()
                WINDOW.blit(midport, (280, 0))
                shoptext = "Save your game! [PRESS SPACE OR TAP OK. YOU CAN'T REVERSE A SAVE.]"
            elif boughtitem == "HealPot":
                midport = pygame.image.load('assets/healthpot_shop.png').convert_alpha()
                WINDOW.blit(midport, (280, 0))
                shoptext = "HealPot - 10 Gold - Heals 30 HP to the Player."
            elif boughtitem == "Sword":
                midport = pygame.image.load('assets/temp_sword.png').convert_alpha()
                WINDOW.blit(midport, (280, 0))
                shoptext = "Sword - 500 Gold - Deals more damage. WILL CHANGE HOW COMBAT WORKS LATER. YOU CAN'T GO BACK TO FISTS."
            elif boughtitem == "Leather":
                midport = pygame.image.load('assets/temp_leather.png').convert_alpha()
                WINDOW.blit(midport, (280, 0))
                shoptext = "Leather Armor - 500 Gold - Shields you from damage."
            elif boughtitem == "Shield":
                midport = pygame.image.load('assets/shield_shop.png').convert_alpha()
                WINDOW.blit(midport, (280, 0))
                shoptext = "Shield - 150 Gold - Protects from one negative status effect."
            elif boughtitem == "GarlicBread":
                midport = pygame.image.load('assets/garlicbread_shop.png').convert_alpha()
                WINDOW.blit(midport, (280, 0))
                shoptext = 'GarlicBread - 75 Gold - "homph nomph homph" - Shopkeeper, stealthily eating some GarlicBread [Gives REGEN.]'
            elif boughtitem == "EffectClear":
                midport = pygame.image.load('assets/effectclear_shop.png').convert_alpha()
                WINDOW.blit(midport, (280, 0))
                shoptext = "EffectClear - 10 Gold - Removes any and all status effects. Contains crushed GravelRock vitamin candies. Gross."
            elif boughtitem == "AlarmClock":
                midport = pygame.image.load('assets/alarmclock_shop.png').convert_alpha()
                WINDOW.blit(midport, (280, 0))
                shoptext = "AlarmClock - 300 Gold - This little THING gave me over THREE HEADACHES in one listening. It can RAISE the DEAD."
            elif boughtitem == "BottleCap":
                midport = pygame.image.load('assets/bottlecap.png').convert_alpha()
                WINDOW.blit(midport, (280, 0))
                shoptext = "BottleCap - 150 Gold - Badge - It's a generic BottleCap. This one comes from a soda, you think! [+1 DEF]"
            elif boughtitem == "IceCog":
                midport = pygame.image.load('assets/icecog_shop.png').convert_alpha()
                WINDOW.blit(midport, (280, 0))
                shoptext = "IceCog - 50 Gold - It's colder than John Freeze's heart. No refunds for freezing. [Gives you SPEED and FREEZE]"
            elif boughtitem == "GhostPepper":
                midport = pygame.image.load('assets/ghostpepper_shop.png').convert_alpha()
                WINDOW.blit(midport, (280, 0))
                shoptext = "GhostPepper - 50 Gold - Contains a ghost. No refunds. [Gives you more attack, although it'll burn you.]"
            temp3 = buythis - 1
            temp4 = buythis + 1
            if temp3 < 0:
                temp3 = len(shopinv) - 1
            if temp4 == len(shopinv):
                temp4 = 0
            temp5 = shopinv[temp3]
            temp6 = shopinv[temp4]
            if temp5 == "HealPot":
                leftport = pygame.image.load('assets/healthpot_shop.png').convert_alpha()
                WINDOW.blit(leftport, (0, 0))
            elif temp5 == "Shield":
                leftport = pygame.image.load('assets/shield_shop.png').convert_alpha()
                WINDOW.blit(leftport, (0, 0))
            elif temp5 == "GarlicBread":
                leftport = pygame.image.load('assets/garlicbread_shop.png').convert_alpha()
                WINDOW.blit(leftport, (0, 0))
            elif temp5 == "Leather":
                leftport = pygame.image.load('assets/temp_leather.png').convert_alpha()
                WINDOW.blit(leftport, (0, 0))
            elif temp5 == "Sword":
                leftport = pygame.image.load('assets/temp_sword.png').convert_alpha()
                WINDOW.blit(leftport, (0, 0))
            elif temp5 == "EffectClear":
                leftport = pygame.image.load('assets/effectclear_shop.png').convert_alpha()
                WINDOW.blit(leftport, (0, 0))
            elif temp5 == "Save":
                leftport = pygame.image.load('assets/floppydisk_shop.png').convert_alpha()
                WINDOW.blit(leftport, (0, 0))
            elif temp5 == "AlarmClock":
                leftport = pygame.image.load('assets/alarmclock_shop.png').convert_alpha()
                WINDOW.blit(leftport, (0, 0))
            elif temp5 == "BottleCap":
                leftport = pygame.image.load('assets/bottlecap.png').convert_alpha()
                WINDOW.blit(leftport, (0, 0))
            elif temp5 == "IceCog":
                leftport = pygame.image.load('assets/icecog_shop.png').convert_alpha()
                WINDOW.blit(leftport, (0, 0))
            elif temp5 == "GhostPepper":
                leftport = pygame.image.load('assets/ghostpepper_shop.png').convert_alpha()
                WINDOW.blit(leftport, (0, 0))
            if temp6 == "HealPot":
                rightport = pygame.image.load('assets/healthpot_shop.png').convert_alpha()
                WINDOW.blit(rightport, (560, 0))
            elif temp6 == "GarlicBread":
                rightport = pygame.image.load('assets/garlicbread_shop.png').convert_alpha()
                WINDOW.blit(rightport, (560, 0))
            elif temp6 == "Shield":
                rightport = pygame.image.load('assets/shield_shop.png').convert_alpha()
                WINDOW.blit(rightport, (560, 0))
            elif temp6 == "EffectClear":
                rightport = pygame.image.load('assets/effectclear_shop.png').convert_alpha()
                WINDOW.blit(rightport, (560, 0))
            elif temp6 == "Save":
                rightport = pygame.image.load('assets/floppydisk_shop.png').convert_alpha()
                WINDOW.blit(rightport, (560, 0))
            elif temp6 == "AlarmClock":
                rightport = pygame.image.load('assets/alarmclock_shop.png').convert_alpha()
                WINDOW.blit(rightport, (560, 0))
            elif temp6 == "Leather":
                rightport = pygame.image.load('assets/temp_leather.png').convert_alpha()
                WINDOW.blit(rightport, (560, 0))
            elif temp6 == "Sword":
                rightport = pygame.image.load('assets/temp_sword.png').convert_alpha()
                WINDOW.blit(rightport, (560, 0))
            elif temp6 == "BottleCap":
                rightport = pygame.image.load('assets/bottlecap.png').convert_alpha()
                WINDOW.blit(rightport, (560, 0))
            elif temp6 == "IceCog":
                rightport = pygame.image.load('assets/icecog_shop.png').convert_alpha()
                WINDOW.blit(rightport, (560, 0))
            elif temp6 == "GhostPepper":
                rightport = pygame.image.load('assets/ghostpepper_shop.png').convert_alpha()
                WINDOW.blit(rightport, (560, 0))
            okbtn = pygame.image.load('assets/techtheme_okbtn.png').convert_alpha()
            WINDOW.blit(okbtn, (0, 256))
            leftbtn = pygame.image.load('assets/techtheme_leftbtn.png').convert_alpha()
            WINDOW.blit(leftbtn, (0, 384))
            rightbtn = pygame.image.load('assets/techtheme_rightbtn.png').convert_alpha()
            WINDOW.blit(rightbtn, (400, 384))
        if itemactive == False and shopactive == False:
            atkbtn = pygame.image.load('assets/techtheme_attack.png').convert_alpha()
            WINDOW.blit(atkbtn, (0, 256))
            defbtn = pygame.image.load('assets/techtheme_defbtn.png').convert_alpha()
            WINDOW.blit(defbtn,(0,384))
            itembtn = pygame.image.load('assets/techtheme_itembtn.png').convert_alpha()
            WINDOW.blit(itembtn,(400,384))
            if inftimer != 3:
                playerport = pygame.image.load('assets/char_default.png').convert_alpha()
                WINDOW.blit(playerport, (0, 0))
                if enemy == "Zombie":
                    enemyport = pygame.image.load('assets/zombie.png').convert_alpha()
                    WINDOW.blit(enemyport, (544, 0))
                elif enemy == "Ghost":
                    enemyport = pygame.image.load('assets/ghost.png').convert_alpha()
                    WINDOW.blit(enemyport, (544, 0))
                elif enemy == "Wizard":
                    enemyport = pygame.image.load('assets/wizard.png').convert_alpha()
                    WINDOW.blit(enemyport, (544, 0))
                elif enemy == "Mermaid":
                    if mermaidchooser == 2:
                        enemyport = pygame.image.load('assets/mermaid_s.png')
                        WINDOW.blit(enemyport, (544,0))
                    else:
                        enemyport = pygame.image.load('assets/mermaid.png').convert_alpha()
                        WINDOW.blit(enemyport, (544, 0))
                elif enemy == "Swordsman":
                    enemyport = pygame.image.load('assets/swordman.png').convert_alpha()
                    WINDOW.blit(enemyport, (544, 0))
        if itemactive == True and shopactive == False:
            textoverlay = pygame.image.load('assets/textoverlay.png')
            WINDOW.blit(textoverlay, (0,240))
            shoprect1 = pygame.Rect(240, 0, 40, 240)
            pygame.draw.rect(WINDOW, WHITE, shoprect1)
            shoprect2 = pygame.Rect(520, 0, 40, 240)
            pygame.draw.rect(WINDOW, WHITE, shoprect2)
            if useditem == "HealPot":
                shoptext = "HealPot - You know well that you reuse the jars! Did you forget that HealPot jars are alive?"
            elif useditem == "EffectClear":
                shoptext = "EffectClear - Upon closer inspection, these are just gummies with crushed candy, which is weird."
            elif useditem == "Shield":
                shoptext = "Shield - You need to equip it to use it. I'd say it's obvious, but it's really not."
            elif useditem == "AlarmClock":
                shoptext = "AlarmClock - It's ticking, slowly but LOUDLY..."
            elif useditem == "BottleCap":
                shoptext = "BottleCap - Badge - You think it has an alright design. It's producing a mini-shield right now."
            elif useditem == "IceCog":
                shoptext = "IceCog - Your hands are icing up just by touching this. However, they DO feel swifter..."
            elif useditem == "GhostPepper":
                shoptext = "GhostPepper - You feel like you're going to get burnt just by licking it. And you will."
            elif useditem == "GarlicBread":
                shoptext = "GarlicBread - It's like bread, but better. Or so they say. Shopkeeper never sells normal bread."
            okbtn = pygame.image.load('assets/techtheme_okbtn.png').convert_alpha()
            WINDOW.blit(okbtn,(0,256))
            leftbtn = pygame.image.load('assets/techtheme_leftbtn.png').convert_alpha()
            WINDOW.blit(leftbtn,(0,384))
            rightbtn = pygame.image.load('assets/techtheme_rightbtn.png').convert_alpha()
            WINDOW.blit(rightbtn,(400,384))
            if useditem == "HealPot":
                midport = pygame.image.load('assets/healthpot_hand_small.png').convert_alpha()
                WINDOW.blit(midport,(280, 0))
            elif useditem == "GarlicBread":
                midport = pygame.image.load('assets/garlicbread_hand.png').convert_alpha()
                WINDOW.blit(midport,(280, 0))
            elif useditem == "Shield":
                midport = pygame.image.load('assets/shield_hand.png').convert_alpha()
                WINDOW.blit(midport,(280, 0))
            elif useditem == "EffectClear":
                midport = pygame.image.load('assets/effectclear_hand_small.png').convert_alpha()
                WINDOW.blit(midport,(280, 0))
            elif useditem == "AlarmClock":
                midport = pygame.image.load('assets/alarmclock_shop.png').convert_alpha()
                WINDOW.blit(midport,(280, 0))
            elif useditem == "BottleCap":
                midport = pygame.image.load('assets/bottlecap.png').convert_alpha()
                WINDOW.blit(midport,(280, 0))
            elif useditem == "IceCog":
                midport = pygame.image.load('assets/icecog_shop.png').convert_alpha()
                WINDOW.blit(midport,(280, 0))
            elif useditem == "GhostPepper":
                midport = pygame.image.load('assets/ghostpepper_hand.png').convert_alpha()
                WINDOW.blit(midport,(280, 0))
            else:
                midport = pygame.image.load('assets/noitem.png').convert_alpha()
                WINDOW.blit(midport,(280, 0))
            temp3 = usethis - 1
            temp4 = usethis + 1
            if temp3 < 0:
                temp3 = len(inv) - 1
            if temp4 == len(inv):
                temp4 = 0
            try:
                temp5 = inv[temp3]
                temp6 = inv[temp4]
            except Exception:
                addtext("No items found!")
            if temp5 == "HealPot":
                leftport = pygame.image.load('assets/healthpot_hand_small.png').convert_alpha()
                WINDOW.blit(leftport,(0,0))
            elif temp5 == "GarlicBread":
                leftport = pygame.image.load('assets/garlicbread_hand.png').convert_alpha()
                WINDOW.blit(leftport,(0,0))
            elif temp5 == "Shield":
                leftport = pygame.image.load('assets/shield_hand.png').convert_alpha()
                WINDOW.blit(leftport,(0,0))
            elif temp5 == "EffectClear":
                leftport = pygame.image.load('assets/effectclear_hand_small.png').convert_alpha()
                WINDOW.blit(leftport,(0,0))
            elif temp5 == "AlarmClock":
                leftport = pygame.image.load('assets/alarmclock_shop.png').convert_alpha()
                WINDOW.blit(leftport, (0, 0))
            elif temp5 == "BottleCap":
                leftport = pygame.image.load('assets/bottlecap.png').convert_alpha()
                WINDOW.blit(leftport, (0, 0))
            elif temp5 == "IceCog":
                leftport = pygame.image.load('assets/icecog_shop.png').convert_alpha()
                WINDOW.blit(leftport, (0, 0))
            elif temp5 == "GarlicBread":
                leftport = pygame.image.load('assets/garlicbread_hand.png').convert_alpha()
                WINDOW.blit(leftport, (0, 0))
            elif temp5 == "GhostPepper":
                leftport = pygame.image.load('assets/ghostpepper_hand.png').convert_alpha()
                WINDOW.blit(leftport, (0, 0))
            else:
                leftport = pygame.image.load('assets/noitem.png').convert_alpha()
                WINDOW.blit(leftport,(0,0))
            if temp6 == "HealPot":
                rightport = pygame.image.load('assets/healthpot_hand_small.png').convert_alpha()
                WINDOW.blit(rightport,(560,0))
            elif temp6 == "HealPot":
                rightport = pygame.image.load('assets/garlicbread_hand.png').convert_alpha()
                WINDOW.blit(rightport,(560,0))
            elif temp6 == "EffectClear":
                rightport = pygame.image.load('assets/effectclear_hand_small.png').convert_alpha()
                WINDOW.blit(rightport,(560,0))
            elif temp6 == "AlarmClock":
                rightport = pygame.image.load('assets/alarmclock_shop.png').convert_alpha()
                WINDOW.blit(rightport,(560,0))
            elif temp6 == "BottleCap":
                rightport = pygame.image.load('assets/bottlecap.png').convert_alpha()
                WINDOW.blit(rightport, (560, 0))
            elif temp6 == "IceCog":
                rightport = pygame.image.load('assets/icecog_shop.png').convert_alpha()
                WINDOW.blit(rightport, (560, 0))
            elif temp6 == "GarlicBread":
                rightport = pygame.image.load('assets/garlicbread_hand.png').convert_alpha()
                WINDOW.blit(rightport, (560, 0))
            elif temp6 == "GhostPepper":
                rightport = pygame.image.load('assets/ghostpepper_hand.png').convert_alpha()
                WINDOW.blit(rightport, (560, 0))
            elif temp6 == "Shield":
                rightport = pygame.image.load('assets/shield_hand.png').convert_alpha()
                WINDOW.blit(rightport, (560, 0))
            else:
                rightport = pygame.image.load('assets/noitem.png').convert_alpha()
                WINDOW.blit(rightport,(560,0))
        pygame.draw.rect(WINDOW,WHITE,commandintbar,2)
        pygame.draw.rect(WINDOW, SCARLETRED, hpbarfill)
        hpdisplay = pygame.image.load('assets/colortheme_hpbar.png').convert_alpha()
        WINDOW.blit(hpdisplay,(800,0))
        pygame.draw.rect(WINDOW,GREEN,enemyhpbarfill)
        enemyhpdisplay = pygame.image.load('assets/colortheme_enemyhpbar.png').convert_alpha()
        golddisplay = pygame.image.load('assets/goldcounter.png').convert_alpha()
        effectbar = pygame.image.load('assets/effectbar.png')
        WINDOW.blit(effectbar,(0,640))
        effcount = len(effects)
        for i in range(effcount):
            xpos = i * 80
            # the regen effect thing actually was an accident but it saves RAM up so keep those accidents coming
            if effects[i] == "regen":
                regeneffect = pygame.image.load("assets/effect_regen.png")
            if effects[i] == "atkboost":
                regeneffect = pygame.image.load("assets/effect_atkboost.png")
            if effects[i] == "burnt":
                regeneffect = pygame.image.load("assets/effect_burnt.png")
            if effects[i] == "infected":
                regeneffect = pygame.image.load("assets/effect_infected.png")
            if effects[i] == "confused":
                regeneffect = pygame.image.load("assets/effect_confused.png")
            if effects[i] == "drowsy":
                regeneffect = pygame.image.load("assets/effect_drowsy.png")
            if effects[i] == "charmed":
                regeneffect = pygame.image.load("assets/effect_charmed.png")
            if effects[i] == "sad":
                regeneffect = pygame.image.load("assets/effect_sad.png")
            if effects[i] == "freeze":
                regeneffect = pygame.image.load("assets/effect_frozen.png")
            if effects[i] == "speed":
                regeneffect = pygame.image.load("assets/effect_speed.png")
            WINDOW.blit(regeneffect, (xpos, 640))
        WINDOW.blit(golddisplay,(1200,0))
        cancelbtn = pygame.image.load('assets/techtheme_cancelbtn.png').convert_alpha()
        if freezetimer > 0:
            freezebtn = pygame.image.load('assets/temp_frozen.png').convert_alpha()
            WINDOW.blit(freezebtn,(0,256))
        WINDOW.blit(cancelbtn,(0,512))
        WINDOW.blit(enemyhpdisplay,(800,24))
        WINDOW.blit(shopTerm,(5,240))
        WINDOW.blit(GoldTerm,(1252,15.50))
        WINDOW.blit(Terminal,(820, 49))
        WINDOW.blit(Terminal2,(820, 79))
        WINDOW.blit(Terminal3,(820, 109))
        WINDOW.blit(Terminal4,(820, 139))
        WINDOW.blit(Terminal5,(820, 169))
        WINDOW.blit(Terminal6,(820, 199))
        WINDOW.blit(Terminal7,(820, 229))
        WINDOW.blit(Terminal8,(820, 259))
        WINDOW.blit(Terminal9,(820, 289))
        WINDOW.blit(Terminal10,(820, 319))
        WINDOW.blit(Terminal11,(820, 349))
        WINDOW.blit(Terminal12,(820, 379))
        WINDOW.blit(Terminal13,(820, 409))
        WINDOW.blit(Terminal14,(820, 439))
        WINDOW.blit(Terminal15,(820, 469))
        WINDOW.blit(Terminal16,(820, 499))
        WINDOW.blit(Terminal17,(820, 529))
        WINDOW.blit(Terminal18,(820, 559))
        WINDOW.blit(Terminal19,(820, 589))
        WINDOW.blit(Terminal20,(820, 619))
        if infimg == True:
            ZombieImg2 = pygame.image.load('assets/zombie_infect.png')
            WINDOW.blit(ZombieImg2, (0,0))
        elif confimg == True:
            ConfImg2 = pygame.image.load('assets/ghost_confuse.png')
            WINDOW.blit(ConfImg2, (0,0))
        WINDOW.blit(FPSClockView,(1260, 620))
        pygame.display.update()
        if itemactive > 1:
            itemactive = itemactive - 1
        fpsClock.tick(FPS)
        if battleexit == 3:
            shop("silent")
main()
