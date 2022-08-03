
import random
import time
import emoji
from playsound import playsound
# bug log:
# if you and the enemy die at the same time, both battle exits are applied, maxing your HP and halving your gold.
# PROBABLY SOLVED
while True:
    char = input("Please choose a name for your character.")
    print("Are you sure this is the correct name?\nName:", char)
    print(emoji.emojize("Your character will be :neutral_face:.(can't change!)"))
    sure = input("").lower()
    if sure == "yes" or sure == "affirmative" or sure == "i'm sure":
        break
print("hello, beta tester! thanks for trying out Untitled RPG Game: .py version!\nthis will be the main branch for Untitled RPG Game.")
print("report bugs in the repo.")
time.sleep(5)
print("Untitled RPG Game")
time.sleep(1)
print("Made by Jes")
time.sleep(1)
print("Probably a mess right now")
time.sleep(2)
# this is all going in the save files, and you know it (well alright except enemyhp, and inf/conf/drow/sleeptimers)
hp = 100
hpmax = 100
revives = 0
gold = 10
inv = ["HealPot", "HealPot", "HealPot", "EffectClear"]
stats = ["none"]
enemyhp = 250
inftimer = 0  # this is the effect timer for INFECTED. I don't know how to make better code so ¯\_(ツ)_/¯
conftimer = 0  #inftimer but for CONFUSED
zzzztimer = 0 #conftimer but for ASLEEP
drowtimer = 0 #zzzztimer but for DROWSY
battleexit = 0  # affects shopkeep dialogue, prices, etc...
pricemulti = 1.1  # price multiplier for the shop: decreases if you die, increases if you win (so items are always in stock)
weap = "fists"  # currently these two things do nothing. they'll affect other things later!|
armr = "clothing"  # <--same as the last comment thingy|
gameround = 0  # round is APARENTLY a python function, so I can't declare that
accuracy = 100  # this is primarily for the Drowsy status effect
enemy = "it's random, my dudes"
version = "0.3prealpha" #used for saves
while True:  # man this relies on a lot of loops. main.py is going to be overloaded
    print("BATTLE Time!")
    if gameround == 0:
        randomenemy = 1
    else:
        randomenemy = random.randint(1, 3)
    if randomenemy == 1:
        enemy = "Zombie"
    elif randomenemy == 2:
        enemy = "Ghost"
    elif randomenemy == 3:
        if gameround > 1:
            enemy = "Wizard"
        elif gameround > 0:
            enemy = "Ghost"
        elif gameround <= 0:
            enemy = "Zombie"
    if enemy == "Zombie":
        enemyhp = 250
    elif enemy == "Ghost":
        enemyhp = 300
    elif enemy == "Wizard":
        enemyhp = 350
    print("You are battling against a", enemy, "a line of text says.")
    while True:
        atk = random.randint(10, 50)
        enemyatk = random.randint(10, 20)
        if hp <= 0 and revives <= 0:
            print("You lost...")
            battleexit = 0
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
            battleexit = 1
            break
        if enemyhp <= 0 and enemy == "Ghost":
            randgold = random.randint(25,100)  # ghosts are harder than zombies HOWEVER you can only find them after one round
            print("You win the battle!\nYou get", randgold, "Gold!")
            gold = gold + randgold
            battleexit = 1
            break
        if enemyhp <= 0 and enemy == "Wizard":
            randgold = random.randint(50,150)  # wizards are harder than ghosts HOWEVER you can only find them after one round
            print("You win the battle!\nYou get", randgold, "Gold!")
            gold = gold + randgold
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
                if atk > 40:
                    enemyhp = enemyhp - atk
                    print("CRIT! You deal", atk, "damage to the zombie.")
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
                        randgold = random.randint(10, 50)  # this is a secondary check, so you can't kill what's already dead
                        print("You win the battle!\nYou get", randgold, "Gold!")
                        gold = gold + randgold
                        battleexit = 1
                        break
        elif action == "defend":
            print("Incoming attack will hurt less.")
            enemyatk = enemyatk / 2
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
            hp = hp + 5
            accuracy = 100
            drowtimer = drowtimer - 1
            zzzztimer = 0
        time.sleep(1)
        enemyatk = random.randint(1, 10)
        if enemy == "Wizard":
            randommultiplier = random.randint(10, 30)
            randommultiplier = randommultiplier / 10
            randomdivider = random.randint(10, 25)
            randomdivider = randomdivider / 10
            enemyatk = (enemyatk * randommultiplier) / randomdivider
            print(enemyatk)
        if enemyatk < 10:
            print("The", enemy, "generically attacks you for", enemyatk, "HP!")
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
        elif enemyatk == 1 and enemy == "Ghost":
            enemyatk = enemyatk * 1.5
            enemyatkmulti = random.randint(1, 2)  # only used here, I'm not THAT evil
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
        elif enemyatk < 6 and enemyatk > 8 and enemy == "Wizard":
            enemyatk = enemyatk / 2
            print("The wizard casts a sleeping spell on you for 3 turns...\nYou're not sure if you're going to have the best accuracy now. Also, you lose", enemyatk, "HP.")
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
            if enemyatk < 6 and enemyatk > 8 and enemy == "Wizard" and zzzztimer >= 2:
                enemyatk = enemyatk / 2
                print("The wizard casts a sleeping spell on you for 3 turns...\nYou fall to the ground, asleep. The wizard, shocked, slowly leaves the battle arena. He isn't going to jail again.")
                hp = hpmax
                battleexit = 2
                break
        if hp <= 0 and revives <= 0:
            print("You lost...")  # secondary check so you can't double-down on deaths
            battleexit = 0
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
    shopinv = ["HealPot", "EffectClear", "MaxUp", "AlarmClock", "Armor", "Weapons"]
    stock = 6
    stock2 = 6
    stock3 = 1
    stock4 = 1
    currentweap = "sword"
    currentarmr = "leather"
    print("All status effects cleared.")
    time.sleep(3)
    inftimer = 0  # this is the effect timer for INFECTED. I don't know how to make better code so ¯\_(ツ)_/¯
    conftimer = 0  # inftimer but for CONFUSED
    zzzztimer = 0  # conftimer but for ASLEEP
    drowtimer = 0  # zzzztimer but for DROWSY
    if battleexit == 1 or battleexit == 2:
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
        while True:
            print("Shop Inventory:", shopinv)
            shopbuy = input("Buy something, or use the exit command when you're done.").lower()
            if shopbuy == "exit":
                print("You exit the store and head back into battle.")
                print("The Shopkeeper also gives you a band-aid, so you can recover some health.")
                regenhp = random.randint(20, 30)
                print("Recovered", regenhp, "HP.")
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
                    print(
                        "This AlarmClock makes so much noise it can literally raise one undead. Thankfully, this one comes set up to revive you!\nAlthough, it is quite fragile...")
                    surebuy = input("Are you sure you want to buy the AlarmClock for 75 gold?").lower()
                    if surebuy == "no":
                        print("No longer buying the AlarmClock.")
                    elif surebuy == "yes":
                        print("Bought one AlarmClock! You can now revive once.")
                        revives = revives + 1
                        inv.append("AlarmClock")
            elif shopbuy == "weapons" or shopbuy == "armor":
                print("todo: write this thingy")
                print("it's not done yet, so just buy maxups while you still can do cheaply")
                print("just tell the shopkeep (restocktest)")
            elif shopbuy == "restocktest":
                stock = 6
                stock2 = 6
                stock3 = 1
                stock4 = 1
                gold = gold * 2
                print("A celestial light shines upon the store...\nRestocked items and duplicated gold!")
    elif battleexit == 0:
        print("You enter the shop; as you are literally dying and there's an inn you can stay in if you pay some gold.")
        time.sleep(4.5)
        print("Shopkeeper: Hello and welcome to- OH NO, WHAT HAPPENED TO YOU?!")
        time.sleep(2)
        print("You promptly explain to her what happened to you and pay...")
        if gold > 0:
            gold = gold / 2
            print("You now have", gold, "gold coins.\nYou can buy something too, if you wish.")
            hp = hpmax
            print("Shop Inventory:", shopinv)
            shopbuy = input("Buy something, or use the exit command when you're done.").lower()
            if shopbuy == "exit":
                print("You exit the store and head back into battle.")
                print("The Shopkeeper also gives you a band-aid, so you can recover some health.")
                regenhp = random.randint(20, 30)
                print("Recovered", regenhp, "HP.")
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
                    print(
                        "This AlarmClock makes so much noise it can literally raise one undead. Thankfully, this one comes set up to revive you!\nAlthough, it is quite fragile...")
                    surebuy = input("Are you sure you want to buy the AlarmClock for 75 gold?").lower()
                    if surebuy == "no":
                        print("No longer buying the AlarmClock.")
                    elif surebuy == "yes":
                        print("Bought one AlarmClock! You can now revive once.")
                        revives = revives + 1
                        inv.append("AlarmClock")
            elif shopbuy == "weapons" or shopbuy == "armor":
                print("todo: write this thingy")
                print("it's not done yet, so just buy maxups while you still can do cheaply")
                print("just tell the shopkeep (restocktest)")
            elif shopbuy == "restocktest":
                stock = 6
                stock2 = 6
                stock3 = 1
                stock4 = 1
                gold = gold * 2
                print("A celestial light shines upon the store...\nRestocked items and duplicated gold!")
        elif gold <= 0:
            print("with your labor. You work for her, as you have NO money, and get back to adventuring...")
            hp = hpmax
