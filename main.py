import os
import random
import time
# thank you, stack overflow and quora
try:
    python_file = open("save.sav", "r+")
    python_file.close()
except Exception:
    print("Temporal save created so that my code doesn't want to die inside. DON'T LOAD IT PLEASE. I still haven't woked out the quirks...")
    os.umask(0)
    with open(os.open('save.sav', os.O_CREAT | os.O_WRONLY, 0o777), 'w') as fh:
        fh.write("amogus")
        time.sleep(5)
hp = 100
hpmax = 100
revives = 0
gold = 10
inv = ["HealPot", "HealPot", "HealPot", "EffectClear"]
stats = ["none"]
enemyhp = 250
inftimer = 0  # this is the effect timer for INFECTED. i dunno how to make better code so ¯\_(ツ)_/¯
conftimer = 0  # inftimer but for CONFUSED
zzzztimer = 0 # conftimer but for ASLEEP
drowtimer = 0 # zzzztimer but for DROWSY
charmtimer = 0 # you get the deal. i'll explain the effects here now. this effect makes it so your attack heals the mermaid.
sadtimer = 0 # and this causes you to attack weaker and heal less.
battleexit = 0  # affects shopkeep dialogue, prices, etc...
weap = "fists"  # currently these two things do nothing. they'll affect other things later!|
armr = "clothing"  # <--same as the last comment thingy|
gameround = 0  # round is APARENTLY a python function so I can't declare that
accuracy = 100  # this is primarily for the Drowsy status effect
enemy = "it's random, my dudes" # this is mainly so PyCharm shuts up about enemies being able to be undeclared
version = "0.4.0prealpha" # used for saves
badge = "none"
versiondiff = False
# the reason this is now here is to make my life easier in case I add some new thing. also this is good practice
# buglog:
# if you and the enemy die at the same time, both battle exits are applied, maxing your HP and halving your gold.
# PROBABLY SOLVED
char = "John Eggbert" # it's the Homestuck protagonist's name. used in case a name can't be found.
while True:
    print("This game has manual saves only. Remember to save once every while.")
    time.sleep(5)
    loadattempt = input("Do you want to load a Save File? yes/no").lower()
    if loadattempt == "yes":
        #welcome to spaghetti land, population: me
        incremental = 0
        numbers = ""
        strings = ""
        invload = ""
        python_file = open("save.sav" , "r+")
        with open("save.sav") as file:
            for line in file:
                incremental = incremental + 1
                if incremental == 1:
                    numbers = line
                if incremental == 2:
                    strings = line
                if incremental == 3:
                    invload = line
        strings = strings.split(",")
        numbers = numbers.split(",")
        #conversion to inventory
        invload = invload.split(",")
        inv = invload
        #string time
        if version != strings[0]:
            print("Woah, hey there. We're gonna need to do some conversion.")
            versiondiff = True
            if strings[0] == "0.3.1prealpha" or strings[0] == "0.3prealpha":
                badge = "none"
                badgereadd = True
        char = strings[1]
        weap = strings[2]
        armr = strings[3]
        if badgereadd != True:
            badge = strings[4]
        #oh boy it's time to truly whip out the SPAGHETTI CODIFICATION
        #stackoverflow, thanks guys.
        numbers = [int(item) for item in numbers]
        hp = numbers[0]
        hpmax = numbers[1]
        gold = numbers[2]
        gameround = numbers[3]
        python_file.close()
        print("Save loaded.")
        battleexit = 3
        break
    else:
        print("New saved data will be created.")
        time.sleep(3)
        break
while True:
    if battleexit == 3:
        break
    char = input("Please choose a name for your character.")
    print("Are you sure this is the correct name?\nName:", char)
    print("Your character'll be 😐 (can't change!)")
    sure = input("").lower()
    if sure == "yes" or sure == "affirmative" or sure == "i'm sure":
        break
print("hello, betatester! thanks for trying out Untitled RPG Game: .py version! this'll be the main branch for Untitled RPG Game.")
print("report bugs in the repo.")
time.sleep(5)
print("Untitled RPG Game")
time.sleep(1)
print("Made by Jes")
time.sleep(1)
print("Probably a mess right now")
time.sleep(2)
# this is all going in the save files and you know it (well aight except enemyhp, enemy, and inf/conf/drow/sleep/charm/sadtimers)
while True:  # man this relies on a lot of loops. main.py is going to be overloaded
    print("BATTLE Time!")
    if gameround > 0:
        randomenemy = random.randint(1, 4)
    if randomenemy == 1:
        enemy = "Zombie"
    elif randomenemy == 2:
        enemy = "Ghost"
    elif randomenemy == 3:
        enemy = "Wizard"
    elif randomenemy == 4:
        enemy = "Mermaid"
    if gameround%5 == 0:
        enemy == "Swordsman"
    if gameround == 0:
        randomenemy = 1
    if enemy == "Zombie":
        enemyhp = 250
    elif enemy == "Ghost":
        enemyhp = 300
    elif enemy == "Wizard":
        enemyhp = 350
    elif enemy == "Mermaid":
        enemyhp = 400
    elif enemy == "Swordsman":
        enemyhp = 600
        randomenemy = 5
    if randomenemy < 5:
        print("You are battling against a", enemy, "a line of text says.")
    else:
        print("You are fighting against the Effectless Swordsman, another line of text says. It's boss time.")
    while True:
        atk = random.randint(10, 50)
        if weap == "Sword":
            atk = atk * 1.5
        if battleexit == 3:
            break
        if hp <= 0 and revives <= 0:
            print("You lost...")
            battleexit = 0
            gameround = gameround + 1
            break
        elif hp == 0 and revives > 0:
            print("You collapse into the ground...")
            time.sleep(3)
            print("Wait, what's that noise-")
            hp = hpmax / 1.25
            print("You rise from the dead, promptly smashing the AlarmClock!")
        if enemyhp <= 0 and enemy == "Zombie":
            randgold = random.randint(10, 50)  # this is for zombies, obviously better mobs are going to drop more coins
            print("You win the battle!\nYou get", randgold, "Gold!")
            gold = gold + randgold
            gameround = gameround + 1
            battleexit = 1
            break
        if enemyhp <= 0 and enemy == "Ghost":
            randgold = random.randint(25,100)  # ghosts are harder than zombies HOWEVER you can only find them after one round
            print("You win the battle!\nYou get", randgold, "Gold!")
            gold = gold + randgold
            gameround = gameround + 1
            battleexit = 1
            break
        if enemyhp <= 0 and enemy == "Wizard":
            randgold = random.randint(50,150)  # wizards are harder than ghosts HOWEVER you can only find them after one round
            print("You win the battle!\nYou get", randgold, "Gold!")
            gold = gold + randgold
            gameround = gameround + 1
            battleexit = 1
            break
        if enemyhp <= 0 and enemy == "Mermaid":
            randgold = random.randint(60,200)  # mermaids are around the same difficulty as wizards but you need loads of effectclears
            print("You win the battle!\nYou get", randgold, "Gold!")
            gold = gold + randgold
            gameround = gameround + 1
            battleexit = 1
            break
        if enemyhp <= 0 and enemy == "Swordsman":
            randgold = random.randint(100,300)  # you only find these every 5 rounds
            print("You defeated the miniboss!\nYou get", randgold, "Gold!")
            gold = gold + randgold
            gameround = gameround + 1
            battleexit = 1
            break
        action = input("What will you do? (attack, items, defend)").lower()
        if action == "items":
            while True:
                print("Your items:", inv)
                action = input("What item will you use?").lower()
                if action == "effectclear":
                    itemhave = inv.count("EffectClear")
                    if itemhave > 0:
                        inv.remove("EffectClear")
                        print("You drink the EffectClear.")
                        time.sleep(1)
                        none = stats[0]
                        if none == "none":
                            print("But it did nothing...")
                            break
                        else:
                            print("You feel WAY better now. All negative stat effects removed.")
                            inftimer = 0
                            sleptimer = 0
                            conftimer = 0
                            zzzztimer = 0
                            break
                    elif itemhave <= 0:
                        print("No items found.")
                    time.sleep(1)
                if action == "healpot":
                    itemhave = inv.count("HealPot")
                    if itemhave > 0:
                        inv.remove("HealPot")
                        print("You drink the Health Potion. HP + 30.")
                        hp = hp + 30
                        if hp > hpmax:
                            hp = hpmax
                        time.sleep(2)
                        break
                    elif itemhave <= 0:
                        print("No items found.")
                if action == "alarmclock":
                    itemhave = inv.count("AlarmClock")
                    if itemhave > 0:
                        print("The AlarmClock is still working. You'll rise up even if you die.")
                        break
                    elif itemhave <= 0:
                        print("You don't have one.")
                else:
                    print("Either you don't have that item, or it's unusable in battle.")
        elif action == "attack":
            missrange = random.randint(0,100)
            if missrange > accuracy:
                print("You missed...")
            else:
                if charmtimer > 1:
                    print("You try to attack, but are charmed by the Mermaid's look on her face...")
                    atk = atk / 2
                    if weap == "fists":
                        print("The mermaid forces you to heal her for", atk ,"HP!")
                        enemyhp = enemyhp + atk
                    else:
                        print("The mermaid tries to make you heal her, but her spell is cut short by you dropping your", weap + ".")
                        time.sleep(1)
                        atk = atk / 2
                        print("However, you still healed her", atk ,"HP.")
                        enemyhp = enemyhp + atk
                if atk > 40:
                    enemyhp = enemyhp - atk
                    print("CRIT! You deal", atk, "damage to the", enemy ,".")
                    time.sleep(1)
                elif atk < 20:
                    enemyhp = enemyhp - atk
                    print("You deal pitiful damage to the", enemy, ". For pitiful, we mean", atk, "damage, which is a low number.")
                    time.sleep(1)
                else:
                    enemyhp = enemyhp - atk
                    print("You deal", atk, "damage to the", enemy, ".")
                    time.sleep(1)
                    if enemyhp <= 0:
                        randgold = random.randint(10, 50)  # this is a secondary check so you can't kill what's already dead
                        print("You win the battle!\nYou get", randgold, "Gold!")
                        gameround = gameround + 1
                        gold = gold + randgold
                        battleexit = 1
                        break
        elif action == "defend":
            print("Incoming attack will hurt less.")
            time.sleep(2)
        else:
            print("You do nothing.")
        if inftimer > 1:
            print("The infection lurches deeper... Lost 10 HP, too.")
            hp = hp - 10
            inftimer = inftimer - 1
        elif inftimer == 1:
            print("You defeat the infection... but lose 10 HP in the process.")
            stats.remove("Infected")
            inftimer = inftimer - 1
        elif conftimer > 1:
            print("You can't quite see where you're going... and you get hit by your own attack.")
            hp = hp - atk / 5
            conftimer = conftimer - 1
        elif conftimer == 1:
            print("You focus on the enemy for once, and stop being confused.")
            stats.remove("Confused")
            conftimer = conftimer - 1
        elif drowtimer > 1:
            print("You're still tired out, but you're recovering energy.")
            accuracy = accuracy + 20
            drowtimer = drowtimer - 1
        elif drowtimer == 1:
            print("You fully restore your energy. You gain 5 HP, too.")
            stats.remove("Drowsy")
            hp = hp + 5
            if hp > hpmax:
                hp = hpmax
            accuracy = 100
            drowtimer = drowtimer - 1
            zzzztimer = 0
        elif charmtimer > 1:
            print("You're still hypnotized by the Mermaid's singing...")
            charmtimer = charmtimer - 1
        elif charmtimer == 1:
            print("You break out of the mermaid's spell!")
            stats.remove("Charmed")
            charmtimer = charmtimer - 1
        elif sadtimer > 1:
            print("You're still saddened by the song...")
            sadtimer = sadtimer - 1
        elif sadtimer == 1:
            print("You finally recover from your sadness.")
            stats.remove("Depressed")
            sadtimer = sadtimer - 1
        time.sleep(1)
        enemyatk = random.randint(1, 10)
        if action == "defend":
            enemyatk = enemyatk / 2
        if badge == "BottleCap":
            enemyatk = enemyatk - 1
        if armr == "Leather":
            enemyatk = enemyatk - 3
        if enemy == "Swordsman":
            print("The Swordsman hits you for", enemyatk*2, "damage!")
            enemyatk = enemyatk*2
            hp = hp - enemyatk
        if enemyatk < 10 or enemyatk > 10:
            print("The", enemy, "generically attacks you for", enemyatk, "HP!")
            hp = hp - enemyatk
            if enemy == "Wizard":
                enemyatk = enemyatk / 2
                print("The Wizard's spell also hurts you from the inside... Lost", enemyatk ,"HP.")
                hp = hp - enemyatk
        elif enemyatk == 10 and enemy == "Zombie":
            enemyatk = enemyatk * 1.5
            print("The zombie bites you! You get *INFECTED* for 3 turns, so you'll lose HP quicker. Also, you lose",enemyatk, "HP.")
            hp = hp - enemyatk
            none = stats.count("none")
            if none == 1:
                stats.pop(0)
                stats.append("Infected")
                inftimer = 3
            else:
                inftimer = 3
        elif enemyatk == 10 and enemy == "Ghost":
            enemyatkmulti = random.randint(1,2)  # only used here, i'm not THAT evil
            print("The ghost casts a curse of confusion upon you for 3 turns...\nYou may hurt yourself by attacking. Also, you lose",enemyatk * enemyatkmulti, "HP.")
            enemyatk = enemyatk * enemyatkmulti
            hp = hp - enemyatk
            none = stats.count("none")
            if none == 1:
                stats.pop(0)
                stats.append("Confused")
                conftimer = 3
            else:
                conftimer = 3
        if enemyatk == 10 and zzzztimer >= 2:
            print("The wizard casts a sleeping spell on you for 3 turns...\nYou fall to the ground, asleep. The wizard, shocked, slowly leaves the battle arena. He isn't going to jail again.")
            hp = hpmax
            battleexit = 2
            break
        elif enemyatk == 10 and enemy == "Wizard":
            enemyatk = enemyatk / 2
            print("The wizard casts a sleeping spell on you for 3 turns...\nYou're not sure if you're going to have the best accuracy now. Also, you lose", enemyatk, "HP.")
            hp = hp - enemyatk
            none = stats.count("none")
            if none == 1:
                stats.pop(0)
                stats.append("Drowsy")
                drowtimer = 3
                zzzztimer = zzzztimer + 1
                print(zzzztimer)
            else:
                drowtimer = 3
                zzzztimer = zzzztimer + 1
                print(zzzztimer)
            time.sleep(1)
        elif enemyatk == 1 and enemy == "Wizard":#if anyone has a better idea on how to fix this, let me know now
            enemyatk = enemyatk / 2
            print("The wizard casts a sleeping spell on you for 3 turns...\nYou're not sure if you're going to have the best accuracy now. Also, you lose",enemyatk, "HP.")
            hp = hp - enemyatk
            none = stats.count("none")
            if none == 1:
                stats.pop(0)
                stats.append("Drowsy")
                drowtimer = 3
                zzzztimer = zzzztimer + 1
            else:
                drowtimer = 3
                zzzztimer = zzzztimer + 1
            time.sleep(1)
        elif enemyatk < 8 and enemyatk > 6 and enemy == "Mermaid":
            enemyatk = enemyatk / 4
            print("The mermaid sings a hypnotizing song...\nGot charmed for 3 turns. You also lost", enemyatk, "HP, since the spell broke your brain.")
            hp = hp - enemyatk
            none = stats.count("none")
            if none == 1:
                stats.pop(0)
                stats.append("Charmed")
                charmtimer = 3
            else:
                charmtimer = 3
        elif enemyatk < 4 and enemyatk > 2 and enemy == "Mermaid":
            enemyatk = enemyatk * 2
            print("The mermaid sings a sad song...\nGot depressed for 3 turns. You also lost", enemyatk, "HP, since the song lowered your morale.")
            hp = hp - enemyatk
            none = stats.count("none")
            if none == 1:
                stats.pop(0)
                stats.append("Depressed")
                sadtimer = 3
            else:
                sadtimer = 3
        if hp <= 0 and revives <= 0:
            print("You lost...")  # secondary check so you can't double-down on deaths
            battleexit = 0
            gameround = gameround + 1
            break
        elif hp == 0 and revives > 0:
            print("You collapse into the ground...")
            time.sleep(3)
            print("Wait, what's that noise-")
            hp = hpmax / 1.25
            print("You rise from the dead, promptly smashing the AlarmClock!")
        print("HP:", hp, "\n", enemy, "HP:", enemyhp)
    # shopscript
    # shopkeep is actually a really nice person tho, but how does she get all of those coins?
    shopinv = ["HealPot", "EffectClear", "MaxUp", "AlarmClock", "Armor", "Weapons","Badge"]
    stock = 6
    stock2 = 6
    stock3 = 1
    stock4 = 1
    currentweap = "sword"
    currentarmr = "leather"
    currentbadge = "bottlecap"
    print("All status effects cleared.")
    time.sleep(3)
    inftimer = 0  # this is the effect timer for INFECTED. i dunno how to make better code so ¯\_(ツ)_/¯
    conftimer = 0  # inftimer but for CONFUSED
    zzzztimer = 0  # conftimer but for ASLEEP
    drowtimer = 0  # zzzztimer but for DROWSY
    if battleexit == 1 or battleexit == 2 or battleexit == 0 or battleexit == 3:
        if battleexit == 1:
            print("You enter the shop before going back to adventuring or whatever you're doing right now.")
            time.sleep(3)
            print("Shopkeeper: Hello, and welcome to The Adventurer's Stash! What item do you want to buy?")
            time.sleep(4)
        if battleexit == 2:
            print("You wake up in the shop's inn. The Shopkeeper greets you on your way to, well, the store floor.")
            time.sleep(3)
            print("Shopkeeper: Oh, you're finally awake! You collapsed in battle. Since I'm the closest shop and innkeeper to the arena, I had to go and bring you back. Free of charge, of course.")
            time.sleep(5)
            print("Shopkeeper: Anyways, want to buy someting,", char, "?")
        if battleexit == 0:
            print("You enter the shop; as you are literally dying and there's an inn you can stay in if you pay some gold.")
            time.sleep(4.5)
            print("Shopkeeper: Hello and welcome to- OH NO, WHAT HAPPENED TO YOU?!")
            time.sleep(2)
            print("You promptly explain to her what happened to you and pay...")
            if gold > 0:
                gold = gold / 2
                print("You now have", gold, "gold coins.\nYou can buy something too, if you wish.")
                hp = hpmax
            elif gold <= 0:
                print("with your labor. You work for her, as you have NO money, and get back to the storefront, to prepare and leave.")
                hp = hpmax
        if battleexit == 3 and versiondiff == 1:
            print("Resolving version differences...")
            #note to self: there are none right now, so i'm just stalling for time
            time.sleep(3)
            print("Data loaded and prepared for this version.")
        if battleexit == 3:
            print("Data loaded.")
        while True:
            save = input("Do you want to save? yes/no").lower()
            if save == "yes":
                print("Game saved.")
                if save == "yes":  # oh boy this is hell why did i implement this (note to self: you implemented this because it's needed for the game to be beatable in multiple sessions if you go through with this game)
                    python_file = open("save.sav", "r+")
                    hp = int(hp)
                    hpmax = int(hpmax)
                    gold = int(gold)
                    gameround = int(gameround)
                    # all of this because of an error. bruh
                    strings = [version, ",", char, ",", weap, ",", armr]
                    variables = [hp, ",", hpmax, ",", gold, ",", gameround]
                    saveinv = []
                    for element in inv:
                        saveinv.append(element + ",")
                    x = "x"
                    saveinv.append(x)
                    saveinv.remove(x)
                    begintransform = ''.join(str(x) for x in variables)
                    saveline1 = ''.join(begintransform)
                    saveline2 = ''.join(strings)
                    saveline3 = ''.join(saveinv)
                    python_file.write(saveline1)
                    python_file.write("\n")
                    python_file.write(saveline2)
                    python_file.write("\n")
                    python_file.write(saveline3)
                    python_file.close()
                    print("Saved succesfully. Hopefully.")
                else:
                    print("Saving cancelled.")
                break
            else:
                break
            print("Shop Inventory:", shopinv)
            shopbuy = input("Buy something, save your data, or use the exit command when you're done.").lower()
            if shopbuy == "exit" and battleexit > 0:
                print("You exit the store and head back into battle.")
                print("The Shopkeeper also gives you a band-aid, so you can recover some health.")
                regenhp = random.randint(20, 30)
                print("Recovered", regenhp, "HP.")
                if hp > hpmax:
                    hp = hpmax
                battleexit = 4
                break
            elif shopbuy == "exit" and battleexit == 0:
                print("You thank the Shopkeeper for letting you stay, and leave in search for adventure.")
                break
            elif shopbuy == "maxup" and gold > 50 and stock3 > 0:
                surebuy = input("Are you sure you want to buy the MaxUp for 50 gold?").lower()
                if surebuy == "no":
                    print("No longer buying MaxUp.")
                elif surebuy == "yes":
                    print("Bought one MaxUp! HP increased by 10.")
                    gold = gold - 50
                    hpmax = hpmax + 10
                    hp = hp + 10
            elif shopbuy == "healpot":
                amount = int(input("How many?"))
                if amount * 10 <= gold and amount <= stock and amount > 1:
                    print("You are buying", amount, "HealPots for", amount * 10, "gold.")
                    surebuy = input("Are you sure you want to buy this?").lower()
                    if surebuy == "no":
                        print("No longer buying HealPots.")
                    elif surebuy == "yes":
                        print("Bought", amount, "HealPots!!")
                        for i in range(amount):
                            inv.append("HealPot")
                elif amount * 10 <= gold and amount <= stock and amount == 1:
                    print("You are buying", amount, "HealPot for 10 gold.")
                    surebuy = input("Are you sure you want to buy this?").lower()
                    if surebuy == "no":
                        print("No longer buying a HealPot.")
                    elif surebuy == "yes":
                        print("Bought", amount, "HealPot!!")
                        inv.append("HealPot")
            elif shopbuy == "effectclear":
                amount = int(input("How many?"))
                if amount * 15 <= gold and amount <= stock and amount > 1:
                    print("You are buying", amount, "EffectClears for", amount * 15, "gold.")
                    surebuy = input("Are you sure you want to buy this?").lower()
                    if surebuy == "no":
                        print("No longer buying EffectClears.")
                    elif surebuy == "yes":
                        print("Bought", amount, "EffectClears!!")
                        for i in range(amount):
                            inv.append("EffectClear")
                elif amount * 10 <= gold and amount <= stock and amount == 1:
                    print("You are buying", amount, "EffectClear for 10 gold.")
                    surebuy = input("Are you sure you want to buy this?").lower()
                    if surebuy == "no":
                        print("No longer buying a EffectClear.")
                    elif surebuy == "yes":
                        print("Bought", amount, "EffectClear!!")
                        inv.append("EffectClear")
            elif shopbuy == "alarmclock":
                if gold > 75 and stock4 > 0:
                    print("This AlarmClock makes so much noise it can literally raise one undead. Thankfully, this one comes set up to revive you!\nAlthough, it is quite fragile...")
                    surebuy = input("Are you sure you want to buy the AlarmClock for 75 gold?").lower()
                    if surebuy == "no":
                        print("No longer buying the AlarmClock.")
                    elif surebuy == "yes":
                        print("Bought one AlarmClock! You can now revive once.")
                        revives = revives + 1
                        inv.append("AlarmClock")
            elif shopbuy == "weapons" or shopbuy == "armor":
                print("Hey, Jes here. This feature HAS been implemented PARTIALLY.\nSome parts may not work.")
                print("Anyways, I'm selling the Shopkeeper's armor and a Sword as a bundle right now!")
                time.sleep(7.5)
                print("They'll be quite expensive later on, so I'll let you have them for 100 gold.")
                if gold >= 100:
                    surebuy = input("Do you want to buy the Armor and Sword bundle?").lower()
                if surebuy == "yes":
                    gold = gold - 100
                    weap = "sword"
                    armr = "leather"
                    print("Alright! Thanks for the cash, now here's your stuff. They'll protect you.")
                    time.sleep(3)
                    print("Got the Armor and Sword set!")
            elif shopbuy == "badge":
                print("This is just a Bottle Cap that increases your defense by 10...(equals to 1dmg)")
                if gold >= 10:
                    surebuy = input("Do you want to buy the BottleCap for 10 gold?")
                if surebuy == "yes":
                    badge = "BottleCap"
                    print("Got the BottleCap Badge.")
                    time.sleep(2)
            elif shopbuy == "restocktest":
                stock = 6
                stock2 = 6
                stock3 = 1
                stock4 = 1
                gold = gold * 2
                print("A celestial light shines upon the store...\nRestocked items and duplicated gold!")
            elif shopbuy == "save":
                save = input("Do you want to save? yes/no").lower()
                if save == "yes": #oh boy this is hell why did i implement this (note to self: you implemented this because it's needed for the game to be beatable in multiple sessions if you go through with this game)
                    python_file = open("save.sav", "r+")
                    hp = int(hp)
                    hpmax = int(hpmax)
                    gold = int(gold)
                    gameround = int(gameround)
                    #all of this because of an error. bruh
                    strings = [version,",",char,",",weap,",",armr,",",badge]
                    variables = [hp,",",hpmax,",",gold,",",gameround]
                    saveinv = []
                    for element in inv:
                        saveinv.append(element + ",")
                    x = "x"
                    saveinv.append(x)
                    saveinv.remove(x)
                    begintransform = ''.join(str(x) for x in variables)
                    saveline1 = ''.join(begintransform)
                    saveline2 = ''.join(strings)
                    saveline3 = ''.join(saveinv)
                    python_file.write(saveline1)
                    python_file.write("\n")
                    python_file.write(saveline2)
                    python_file.write("\n")
                    python_file.write(saveline3)
                    python_file.close()
                    print("Saved succesfully. Hopefully.")
                else:
                    print("Saving cancelled.")
