import pygame, sys, os, random, tkinter, locale, gc, math, json, re
from pygame.locals import *
import pygame.locals
pygame.init()
pygame.mixer.init()
pygame.mixer.set_num_channels(24)
scalelist = [(0.50),(0.6675),(0.75),(0.80),1,(1.0685),(1.25),(1.5),(2),(2.50),(3),(4)]
WHresolutiontable = [360,480,540,576,720,768,900,1080,1440,1800,2160,2880]
WWresolutiontable = [640,854,960,1024,1280,1366,1600,1920,2560,3200,3840,5120]
resscale = 5
print(locale.getlocale())
if locale.getlocale()[0] == 'es_ES':
    language = "Spanish"
else:
    language = "English"

try:
    with open('settings.dat', 'r') as settingsfile:
        line = settingsfile.read()
        lineholder = line.replace("(","")
        lineholder = lineholder.replace(")","")
        lineholder = lineholder.replace(" ","")
        lineholder = lineholder.split(',')
        print(lineholder)
        print("runningres")
        for i in range(len(WWresolutiontable)):
            if int(lineholder[0]) == WWresolutiontable[i]:
                resscale = i
        PREVIOUSVERSION = lineholder[2]
        if lineholder[3] == "True":
            FULLSCREENSWITCH = True
        else:
            FULLSCREENSWITCH = False
        language = lineholder[4]
        #doVSYNC = lineholder[5]
except Exception:
    resscale = 5
    FULLSCREENSWITCH = True
    root = tkinter.Tk()
    width = root.winfo_screenwidth()
    height = root.winfo_screenheight()
    method = (width,height)
    for i in range(len(WWresolutiontable)):
        if int(method[0]) == WWresolutiontable[i]:
            resscale = i
    root.withdraw()
print(resscale)


"""
Untitled RPG Game - PTB1

TIP: This version is horribly optimized, and a buggy mess.
Please report any bugs in the Issues tab along with instructions on how to reproduce them.

See credits.txt and LICENSE.md for credits and license information.
"""

# Game Setup
FPS = 60 # Target FPS right now.
fpsClock = pygame.time.Clock()
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
gameicon = pygame.image.load('assets/gameicon.png')
pygame.display.set_icon(gameicon)
WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Untitled RPG Game - Public Test Build')

resvar = (WWresolutiontable[resscale], WHresolutiontable[resscale])
WINDOW_WIDTH = resvar[0]
WINDOW_HEIGHT = resvar[1]
scaleH = WINDOW_WIDTH / 1280
scaleW = WINDOW_HEIGHT / 720
fusedscale = scalelist[resscale] #type:float

# NOTE: fonts moved here and new fonts have been added

text = ""
font = pygame.font.Font('fonts/RobotoMono-Regular.ttf', int(20 * fusedscale))
smallboldfont = smolfont = pygame.font.Font('fonts/RobotoMono-Bold.ttf', int(12 * fusedscale))
smolfont = pygame.font.Font('fonts/RobotoMono-Regular.ttf', int(8 * fusedscale))
bigfont = pygame.font.Font('fonts/RobotoMono-Regular.ttf', int(80 * fusedscale))

randtext = ["game's booting up just give it a sec",
            "crashing cars into eachother rq hold on",
            "untitled team please optimize game",
            "loading. just loading.",
            "idk how to make a good loading screen so you're stuck with this",
            "drinkin\' up a healpot and suddenly +30 HP",
            "i gently load up the game- why is everything broken again",
            "can you please wait a moment we gotta set up the pile of if statements kthx",
            "\"oh boy i sure hope i can get my passport\" guy exclaimed. little did they know it was an rpg. an untitled rpg. featuring the untitled",
            "you\'d think having all the code in one file would make it load quicker",
            "it untitles on my rpg until i game"]

WINDOW.blit(smallboldfont.render(randtext[random.randint(0,len(randtext)-1)],True,(255,255,255)),(0,700))
pygame.display.update()

del randtext

# NOTE: separated ITEM and WEAPON tables, updated WEAPON table a lot!
# NOTE: made a ton of tables. removed Save as an item. actually that'd slap as a debug feature so put a TODO here
# TODO: Deprecate IML if possible. exec() should do.
# NOTE: IML commands replaced with exec() statements.

itemtable = [["HealPot",pygame.image.load("assets/newui_healpot.png").convert_alpha(),"Heals 30HP. Contents unknown, but approved by health inspectors. Sweet tasting.","affected.hp += 30",10,pygame.image.load("assets/shopbtn_healpot.png").convert_alpha()],
                ["EffectClear",pygame.image.load("assets/newui_effectclear.png").convert_alpha(),"Clears all status effects. Pretty salty.","affected.effects = []",10,pygame.image.load("assets/shopbtn_effectclear.png").convert_alpha()],
                ["IceCog",pygame.image.load("assets/icecog.png").convert_alpha(),"Freezes you, but grants you speediness. Modeled after the ones in the AlarmClocks.","affected.effects.append([\"frozen\",1,1]);affected.effects.append([\"speedboost\",3,1])",50,pygame.image.load("assets/shopbtn_icecog.png").convert_alpha()],
                ["GhostPepper",pygame.image.load("assets/ghostpepper.png").convert_alpha(),"It burns! But it multiplies attack.","affected.effects.append([\"burning\",3,1]);affected.effects.append([\"atkboost\",1,2.5])",50,pygame.image.load("assets/shopbtn_ghostpepper.png").convert_alpha()],
                ["AlarmClock",pygame.image.load("assets/alarmclock.png").convert_alpha(),"Revive from the dead! You can only carry a few at a time, though...","TerminalObj.add(\"Well, it\'s on.\");affected.items[self.activeitem] += 1",100,pygame.image.load("assets/shopbtn_alarmclock.png").convert_alpha()], # this is only for revival things
                ["GarlicBread",pygame.image.load("assets/garlicbread.png").convert_alpha(),"Regenerative Bread. It\'s good!","affected.effects.append([\"regen\",1,1])",30,pygame.image.load("assets/shopbtn_garlicbread.png").convert_alpha()]]

# The layout for weapons is as follows: [[typename,[[weaponname,image,description,not-yet-deprecated IML command,price,weightclass,stats],...],typeicon,grabpoint,scale,rotation],
#                                        [typename,[[weaponname,image,description,not-yet-deprecated IML command,price,weightclass,stats],...],typeicon,grabpoint,scale,rotation],...]

weapontable =   [["Swords",[["Sword",pygame.image.load("assets/shop/weapons/shop_sword.png").convert_alpha(),"It's a big knife. The weapon of choice for most Venturers.","+weap(Sword)",250,1,(0,0,0,0,30,10),["specSwoBurst","specSwoSpin","specSwoThrow","specSwoVitals"]],
                ["Cog Sword",pygame.image.load("assets/shop/weapons/shop_cogsword.png").convert_alpha(),"The cogs aren't gold. They're just spray painted tin ones. Still sharp though.","+weap(Cog Sword)",350,1,(0,0,0,0,20,20),["specSwoBurst","specSwoSpin","specSwoThrow","specSwoVitals"]],
                ["Magma Sword",pygame.image.load("assets/shop/weapons/shop_magmasword.png").convert_alpha(),"Contrary to popular belief, it's not that hot. This is either an astounding feat or fake magma.","+weap(Magma Sword)",500,1,(0,0,0,0,25,15),["specSwoBurst","specSwoSpin","specSwoThrow","specSwoVitals"]],
                ["Knight Sword",pygame.image.load("assets/shop/weapons/shop_knightsword.png").convert_alpha(),"Yet amother big knife, but with a handle. Quite a bit sharper, too...","+weap(Knight Sword)",500,2,(0,0,0,0,50,20),["specSwoBurst","specSwoSpin","specSwoThrow","specSwoVitals"]],
                ["Graphical Sword",pygame.image.load("assets/shop/weapons/shop_gpusword.png").convert_alpha(),"Works as a space heater, expansion card and blunt object ...if you buy the good one for 2000 nuggets.","+weap(Graphical Sword)",750,2,(0,0,0,0,35,35),["specSwoBurst","specSwoSpin","specSwoThrow","specSwoVitals"]],
                ["Fire Sword",pygame.image.load("assets/shop/weapons/shop_firesword_frame0.png").convert_alpha(),"Who in their right mind thought it was a to attach a flamethrower to a sword?","+weap(Fire Sword)",650,1,(0,0,0,0,40,25),["specSwoBurst","specSwoSpin","specSwoThrow","specSwoVitals"]]],pygame.image.load("assets/shop/weapons/icons/icon_sword.png").convert_alpha(),(520*scaleH,215*scaleW),1.5,0,"SwordCombo"],
                # TODO: animate the firesword's asset
                ["Wands",[["Wand",pygame.image.load("assets/shop/weapons/shop_wand.png").convert_alpha(),"What happens when someone skewers an orb with a stick and wraps a vine around it? Magic.","+weap(Wand)",250,0,(0,0,0,0,15,30),["specWanDrown","specWanHeal","specWanElectrocute","specWanFireball"]],
                ["Healing Wand",pygame.image.load("assets/shop/weapons/shop_healwand.png").convert_alpha(),"Yet another skewered orb; but this one can stitch wounds for a bit. It does less damage though.","+weap(Healing Wand)",300,1,(0,0,0,0,5,60),["specWanDrown","specWanHeal","specWanElectrocute","specWanFireball"]],
                ["Sea Wand",pygame.image.load("assets/shop/weapons/shop_seawand.png").convert_alpha(),"Contains a tiny bit of the ocean inside of the orb. Careful; it\'s salty!","+weap(Sea Wand)",300,1,(0,0,0,0,10,40),["specWanDrown","specWanHeal","specWanElectrocute","specWanFireball"]],
                ["Advanced Wand",pygame.image.load("assets/shop/weapons/shop_advwand.png").convert_alpha(),"Apparently covering a side of the orb with a saucepan makes it more potent. The vine\'s for decoration, again.","+weap(Advanced Wand)",500,1,(0,0,0,0,20,50),["specWanDrown","specWanHeal","specWanElectrocute","specWanFireball"]],
                ["Advanced Healing Wand",pygame.image.load("assets/shop/weapons/shop_advhealwand.png").convert_alpha(),"Can disinfect wounds and relieve pain now! Also, it actually adheres to health regulations now.","+weap(Advanced Healing Wand)",650,0,(0,0,0,0,5,80),["specWanDrown","specWanHeal","specWanElectrocute","specWanFireball"]],
                ["Advanced Sea Wand",pygame.image.load("assets/shop/weapons/shop_advseawand.png").convert_alpha(),"The ocean inside is bigger now, both in size and depth. Opinions differ on whether or not that\'s a good thing.","+weap(Advanced Sea Wand)",700,1,(0,0,0,0,10,60),["specWanDrown","specWanHeal","specWanElectrocute","specWanFireball"]]],pygame.image.load("assets/shop/weapons/icons/icon_wand.png").convert_alpha(),(480*scaleH,205*scaleW),1.5,0,"MagicCombo"],
                ["Science Equipment",[["Test Tube",pygame.image.load("assets/shop/weapons/shop_testtube.png").convert_alpha(),"Just some acid in a tube. Don\'t put your hand inside. Seriously.","+weap(Test Tube)",150,0,(0,0,0,0,12,35),["specSciLACR","specSciAcid"]],
                ["Electromagnet",pygame.image.load("assets/shop/weapons/shop_electromagnet.png").convert_alpha(),"A rock wrapped in copper wire with a battery connected to it.","+weap(Electromagnet)",200,1,(0,0,0,0,15,30),["specSciLACR","specSciAcid"]],
                ["Burner",pygame.image.load("assets/shop/weapons/shop_burner.png").convert_alpha(),"How is it even powered...? Still works though.","+weap(Burner)",125,0,(0,0,0,0,10,30),["specSciLACR","specSciAcid"]],
                ["Energy in a Flask",pygame.image.load("assets/shop/weapons/shop_energyinaflask.png").convert_alpha(),"Turns out Nuggets don\'t like being shocked and become pure energy sometimes when doing that. Good weapon though.","+weap(Energy in a Flask)",600,0,(0,0,0,0,20,55),["specSciLACR","specSciDebuff","specSciAcid","specSciBuff"]],
                ["Magnetelectro",pygame.image.load("assets/shop/weapons/shop_magnetelectro.png").convert_alpha(),"Air is TECHNICALLY a conductor at high enough voltages. Don\'t ask how high they are.","+weap(Magnetelectro)",450,0,(0,0,0,0,25,45),["specSciLACR","specSciDebuff","specSciAcid","specSciBuff"]],
                ["Makeshift Flamethrower",pygame.image.load("assets/shop/weapons/shop_flamethrower.png").convert_alpha(),"Shouldn\'t work, but does. Made with scrap metal.","+weap(Makeshift Flamethrower)",850,2,(0,0,0,0,15,60),["specSciLACR","specSciDebuff","specSciAcid","specSciBuff"]]],pygame.image.load("assets/shop/weapons/icons/icon_science.png").convert_alpha(),(490*scaleH,260*scaleW),1.5,0,"ScienceCombo"],
                ["Joke Props",[["Ball Cluster",pygame.image.load("assets/shop/weapons/shop_balls.png").convert_alpha(),"Stolen from the circus. Yes, the bomb\'s supposed to be there. Go nuts.","+weap(Ball Cluster)",200,0,(0,0,0,0,25,15),["specBallMock","specBallPie","specBallSpeak","specBallBowl"]],
                ["Banana Gun",pygame.image.load("assets/shop/weapons/shop_bananagun.png").convert_alpha(),"Ripe, locked, and loaded. Yes, it\'s supposed to shoot balls.","+weap(Banana Gun)",350,1,(0,0,0,0,25,30),["specBallMock","specBallPie","specBallSpeak","specBallBowl"]],
                ["Horn",pygame.image.load("assets/shop/weapons/shop_horn.png").convert_alpha(),"Sounds funny at first, becomes annoying after the twentieth time you hear it...","+weap(Horn)",75,0,(0,0,0,0,10,30),["specBallMock","specBallPie","specBallSpeak","specBallBowl"]],
                ["Bowling Kit",pygame.image.load("assets/shop/weapons/shop_bowling.png").convert_alpha(),"You could seriously harm someone with this bowling ball. Which means this qualifies as weaponry!","+weap(Bowling Kit)",400,2,(0,0,0,0,40,30),["specBallMock","specBallPie","specBallSpeak","specBallBowl"]],
                ["Pie Launcher",pygame.image.load("assets/shop/weapons/shop_pielauncher.png").convert_alpha(),"An oven and a confetti cannon fused into one, ready to pie whoever comes near you. Pies not included.","+weap(Pie Launcher)",550,2,(0,0,0,0,25,45),["specBallMock","specBallPie","specBallSpeak","specBallBowl"]],
                ["Air Horn",pygame.image.load("assets/shop/weapons/shop_airhorn.png").convert_alpha(),"Also known as the eardrum destroyer 9000.","+weap(Air Horn)",600,0,(0,0,0,0,20,50),["specBallMock","specBallPie","specBallSpeak","specBallBowl"]]],pygame.image.load("assets/shop/weapons/icons/icon_clown.png").convert_alpha(),(520*scaleH,245*scaleW),1.5,0,"ClownCombo"],
                ["Guns",[["Toy Revolver",pygame.image.load("assets/shop/weapons/shop_toyrevolver.png").convert_alpha(),"Because there's a part in every kid that desires only war and chaos, and giving them a real gun would just make it worse.","+weap(Toy Revolver)",250,1,(0,0,0,0,35,12),["specGunBlunder","specGunScope","specGunScrap"]],
                ["Toy Shotgun",pygame.image.load("assets/shop/weapons/shop_toyshotgun.png").convert_alpha(),"It doesn\'t even have bullet spread. But it fires little rubber balls that really hurt.","+weap(Toy Shotgun)",300,1,(0,0,0,0,40,10),["specGunBlunder","specGunScope","specGunScrap"]],
                ["Toy Musket",pygame.image.load("assets/shop/weapons/shop_toymusket.png").convert_alpha(),"A rubber band launcher in the shape of a musket. Getting hit by one is irritating in more ways than one.","+weap(Toy Musket)",200,1,(0,0,0,0,30,15),["specGunBlunder","specGunScope","specGunScrap"]],
                ["Old Revolver",pygame.image.load("assets/shop/weapons/shop_oldrevolver.png").convert_alpha(),"A remnant from a long-gone war. Careful; even if it\'s old, it\'s still a revolver, and it\'s more than capable of blowing your brains off.","+weap(Old Revolver)",750,2,(0,0,0,0,55,15),["specGunLasso","specGunBlunder","specGunScope","specGunScrap"]], # TODO: add moss and rust to the Old Revolver, Old Butterfly Knife and Old Shotgun
                ["Old Shotgun",pygame.image.load("assets/shop/weapons/shop_oldshotgun.png").convert_alpha(),"A remnant from a long-gone war. The trigger\'s seen better days, but it\'s still, well, a shotgun. Be careful with it.","+weap(Old Shotgun)",800,2,(0,0,0,0,60,15),["specGunLasso","specGunBlunder","specGunScope","specGunScrap"]],
                ["Old Musket",pygame.image.load("assets/shop/weapons/shop_oldmusket.png").convert_alpha(),"A remnant from a long-gone war. Dust has accumulated inside, so one should take extreme caution when using it.","+weap(Old Musket)",775,2,(0,0,0,0,50,20),["specGunLasso","specGunBlunder","specGunScope","specGunScrap"]]],pygame.image.load("assets/shop/weapons/icons/icon_revolver.png").convert_alpha(),(580*scaleH,255*scaleW),1.5,0,"GunCombo"],
                ["Bow-esque Weapons",[["Basic Bow",pygame.image.load("assets/shop/weapons/shop_bow.png").convert_alpha(),"Arrow included. Not that precise, but it's cheap, so...","+weap(Bow)",150,0,(0,0,0,0,15,25),["specBowRain","specBowTriple","specBowBoomerang"]],
                ["Crossbow",pygame.image.load("assets/shop/weapons/shop_crossbow.png").convert_alpha(),"Similar to a bow, but less whimsical in nature and a bit quicker to reload.","+weap(Crossbow)",200,0,(0,0,0,0,20,20),["specBowRain","specBowTriple","specBowBoomerang"]],
                ["Stake Launcher",pygame.image.load("assets/shop/weapons/shop_stakelauncher.png").convert_alpha(),"Like a bow, but with a heavier arrow and a ton more force required to shoot.","+weap(Stake Launcher)",300,2,(0,0,0,0,30,10),["specBowRain","specBowTriple","specBowBoomerang"]],
                ["Makeshift Bow",pygame.image.load("assets/shop/weapons/shop_makeshiftbow.png").convert_alpha(),"Bows are one of the only weapons that look cooler when makeshift. The arrow also hurts a bit more, which is always nice.","+weap(Makeshift Bow)",500,0,(0,0,0,0,30,40),["specBowRain","specBowTriple","specBowBoomerang"]],
                ["Electrocrossbow",pygame.image.load("assets/shop/weapons/shop_electrocrossbow.png").convert_alpha(),"It\'s a normal crossbow with a battery attached to it and a better rubber band.","+weap(Electrocrossbow)",500,0,(0,0,0,0,40,30),["specBowRain","specBowTriple","specBowBoomerang"]],
                ["Windmill Launcher",pygame.image.load("assets/shop/weapons/shop_windmillauncher.png").convert_alpha(),"Launches windmills instead of stakes. The bow part was also reinforced.","+weap(Windmill Launcher)",650,2,(0,0,0,0,45,25),["specBowRain","specBowTriple","specBowBoomerang"]]],pygame.image.load("assets/shop/weapons/icons/icon_bow.png").convert_alpha(),(550*scaleH,185*scaleW),1.5,0,"BowCombo"],
                ["Small Knives",[["Old Pocket Knife",pygame.image.load("assets/shop/weapons/shop_oldpocketknife.png").convert_alpha(),"Mossy and rusty, but it's still sharp.","+weap(Old Pocket Knife)",250,0,(0,0,0,0,30,10),["specSwoVitals","specPktDouble","specPktTrick"]],
                ["Old Karambit",pygame.image.load("assets/shop/weapons/shop_oldkarambit.png").convert_alpha(),"Spinny knife. The blade has seen better days though.","+weap(Old Karambit)",250,0,(0,0,0,0,25,10),["specSwoVitals","specPktDouble","specPktThreat","specPktTrick"]],
                ["Old Butterfly Knife",pygame.image.load("assets/shop/weapons/shop_oldbutterflyknife.png").convert_alpha(),"An old knife with a dull blade. It can be concealed in its own handle. Rumors say a famous spy used to wield it...","+weap(Old Butterfly Knife)",275,0,(0,0,0,0,20,15),["specSwoVitals","specPktDouble","specPktThreat","specPktTrick"]],
                ["Pocket Knife",pygame.image.load("assets/shop/weapons/shop_pocketknife.png").convert_alpha(),"A small, sharp knife. Normally used to cut small things up.","+weap(Pocket Knife)",500,0,(0,0,0,0,50,15),["specSwoVitals","specPktDouble","specPktThreat","specPktTrick"]],
                ["Karambit",pygame.image.load("assets/shop/weapons/shop_karambit.png").convert_alpha(),"A curvy spinny knife. The blade\'s VERY sharp.","+weap(Karambit)",525,0,(0,0,0,0,45,20),["specSwoVitals","specPktDouble","specPktThreat","specPktTrick"]],
                ["Butterfly Knife",pygame.image.load("assets/shop/weapons/shop_butterflyknife.png").convert_alpha(),"A knife that can store its blade inside its handles. The blade suffers a bit from that, though.","+weap(Butterfly Knife)",525,0,(0,0,0,0,40,25),["specSwoVitals","specPktDouble","specPktThreat","specPktTrick"]]],pygame.image.load("assets/shop/weapons/icons/icon_pocketknife.png").convert_alpha(),(480*scaleH,225*scaleW),1.5,0,"DaggerCombo"],
                ["Hand to Hand",[["Fist",pygame.image.load("assets/shop/weapons/shop_fist.png").convert_alpha(),"Weak if untrained, strong when taken to their full potential. Yours are untrained though.","+weap(None)",0,0,(0,0,0,0,10,10),["specFstSlap","specFstKick","specFstUpper"]],
                ["Boxing Glove",pygame.image.load("assets/shop/weapons/shop_boxingglove.png").convert_alpha(),"Strenghtens your punches at the cost of being unable to slap properly.","+weap(Boxing Glove)",100,1,(0,0,0,0,30,5),["specFstSlap","specFstKick","specFstChoke","specFstUpper"]],
                ["CMDFist",pygame.image.load("assets/shop/weapons/shop_cmdfist.png").convert_alpha(),"Finally; affordable, portable computing. No, phones don\'t count as portable computing, shut up.","+weap(CMDFist)",350,2,(0,0,0,0,25,20),["specFstSlap","specFstKick","specFstChoke","specFstUpper"]],
                ["Brass Knuckle",pygame.image.load("assets/shop/weapons/shop_brassknuckle.png").convert_alpha(),"A piece of metal that strengthens attacks. It\'s got its weight...","+weap(Brass Knuckle)",200,1,(0,0,0,0,25,10),["specFstSlap","specFstKick","specFstChoke","specFstUpper"]],
                ["Advanced Boxing Glove",pygame.image.load("assets/shop/weapons/shop_advboxingglove.png").convert_alpha(),"Better quality than the other glove. This one can slap, but is prohibited in competitions.","+weap(Advanced Boxing Glove)",400,1,(0,0,0,0,45,10),["specFstSlap","specFstKick","specFstChoke","specFstUpper"]],
                ["Prototype Exoskeletic Fist",pygame.image.load("assets/shop/weapons/shop_protoexoskeleton.png").convert_alpha(),"No, it\'s not just copper bits and pieces wired together. Shut up.","+weap(Prototype Exoskeletic Fist)",550,2,(0,0,0,0,30,20),["specFstSlap","specFstKick","specFstChoke","specFstUpper"]]],pygame.image.load("assets/shop/weapons/icons/icon_fists.png").convert_alpha(),(185*scaleH,435*scaleW),0.85,175,"FistCombo"],
                ["Other",[["Hammer",pygame.image.load("assets/shop/weapons/shop_hammer.png").convert_alpha(),"bonk","+weap(Hammer)",750,1,(0,0,0,0,40,12),["specFstSlap"]],
                ["Egg Blaster",pygame.image.load("assets/shop/weapons/shop_eggblaster.png").convert_alpha(),"Put food in, shoot egg out. Simple.","+weap(Egg Blaster)",450,1,(0,0,0,0,17,20),["specGunBlunder"]],
                ["Mace",pygame.image.load("assets/shop/weapons/shop_mace.png").convert_alpha(),"Flail it around to completely anhilate people's skulls.","+weap(Mace)",750,2,(0,0,0,0,30,20),["specSwoSpin"]],
                ["Scythe",pygame.image.load("assets/shop/weapons/shop_scythe.png").convert_alpha(),"A handle with a curved blade. Most of the people who use these wear black or gray hoodies.","+weap(Scythe)",750,0,(0,0,0,0,20,20),["specSwoSpin"]],
                ["Spear",pygame.image.load("assets/shop/weapons/shop_spear.png").convert_alpha(),"Find the correct angle and throw; and that's how you make a hole.","+weap(Spear)",750,0,(0,0,0,0,25,13),["specSwoVitals"]],
                ["Cardboard SMG",pygame.image.load("assets/shop/weapons/shop_cardboardsmg.png").convert_alpha(),"Can\'t do anything.","+weap(Cardboard SMG)",29304802953720,-952,(0,0,0,0,-1240,9999),["specWanFireball"]]],pygame.image.load("assets/shop/weapons/icons/icon_others.png").convert_alpha(),(560*scaleH,245*scaleW),1.5,0,"FistCombo"]]

# Armor layout: name, image, description, cost, Tiering, weight class, stats, effectres
# TODO: remove IML commands from the armors, update all of them to use the 6 stats that weapons use
# Stats are: (HP,DEF,SPEED,COOLDOWN,ATK,SPECIAL). This applies to weapons too.
# effectres is formatted like this: [(effectname,resistanceint,chance)]
# resistanceint is the tier on which the effect will be resisted against. 
# chance is the chance of, well, resisting the effect. Chance will be higher if resistanceint is higher than the tier of the effect.
# For example: The enemy uses a Tier 1 Infect. You have armor that protects against Tier 2 or lower infects.
# The armor's chance was 33%. It raises to 66% due to the Tier difference. 
# We call random.randint and roll the die. If the result of the randint is lower than the chance, no effect's applied. 
# If the enemy used a Tier 3 Drowsy and you didn't have protection against it, it'd be almost guaranteed to hit unless you DODGED the attack.
# (and some attacks will be hard to dodge/impossible to dodge, so good luck staying awake there, bud)
# also NOTE: we're going to have to isinstance() the effect things, so ye
# TODO: fix how armor rendering works, it looks BAD

# NOTE: added armor render positioning and armor scaling
armortable =   [["Leather Reinforcement",pygame.image.load("assets/armor_leatherreinforcement.png").convert_alpha(),"Some cushioned leather to protect your weak spots.","",100,0,0,(10,1,0,0,0),[()],2,(333*scaleH,320*scaleW)],
                ["Mixed Armor",pygame.image.load("assets/armor_mixedset.png").convert_alpha(),"A leather set, with pieces of iron on top.","",250,1,1,(15,1.5,0,0,0),[()],2.05,(303*scaleH,320*scaleW)],
                ["Suit",pygame.image.load("assets/armor_suit.png").convert_alpha(),"Ooh, fancy.","",250,1,0,(5,0,3,0,1.25),[()],1.90,(300*scaleH,320*scaleW)],
                ["Iron Armor",pygame.image.load("assets/armor_ironset.png").convert_alpha(),"A knight's first true set of armor. Proven to be resistant to zombie attacks.","",500,2,2,(25,2.5,0,0,0),[("infected",1,20)],2,(300*scaleH,325*scaleW)],
                ["Cowboy Set",pygame.image.load("assets/armor_cowboyset.png").convert_alpha(),"\"Parry this, you filthy casual.\"","",350,2,0,(0,0,1,1,1.75),[()],2,(333*scaleH,320*scaleW)],
                ["Fancy Suit",pygame.image.load("assets/armor_fancysuit.png").convert_alpha(),"Ooh, fancier! Heavier than the standard Suit.","",625,2,1,(10,0,5,0,1.375),[()],1.90,(300*scaleH,320*scaleW)]]

# NOTE: added the badge table

# Badge Event Infrastructure:
# Badges change things in the game when equipped. Here's how to specify what changes.
# 1. HOW things change
# btw quick note here's how i write dicts in this comment so you don't get as confused:
# a:b   Defining a key; a being its name and b being the type of its value
# > c   Valid value of b
# } d   Required value or key when the above key equals the above value of b
# Changes are handled in DICTS. These DICTS must be in a list, and have to be written in a certain way:
# type:str,None             - The type of change that's supposed to happen, with the type being a string.
#   >timed                  - This change will be triggered once an x amount of turns pass.
#       }turns:int          - Amount of turns for the change to occur.
#   >event                  - Triggers upon a certain event.
#       }event:str          - Event to trigger the change when it occurs.
#   >None                   - Untriggered type so that badges can be added without a type.
#   >continous              - Always triggers.
# 2. how to specify WHAT changes
# action:str
# btw here are some shortcuts:
# wearer is whoever has the badge equipped
# all affects everything in the battle
# Write whatever expression you need to evaluate in the string. E.G: to increase the HP of the wearer by 10, you'd put "wearer.hp += 10".

badgetable = [["Bottle Cap",pygame.image.load("assets/shop/badges/badge_bottlecap.png").convert_alpha(),"It\'s a generic BottleCap. Doesn\'t come from a soda this time.",0,150,(0,1,0,0,0,0),[{"type":None}],"Does nothing."],
              ["Cassette Badge",pygame.image.load("assets/shop/badges/badge_cassette.png").convert_alpha(),"Don\'t forget to rewind it.",0,1000,(0,0,0,5,-10,10),[{"type":"event","event":"TurnEnd","action":"all.cooldown -= 1"}],"At the end of a turn, reduces the cooldown of everyone's abilities by 1 turn."],
              ["Classic Badge",pygame.image.load("assets/shop/badges/badge_classic.png").convert_alpha(),"A relic from the times when selling cookies was a profitable career choice.",0,200,(10,2,0,0,0,0),[{"type":"event","event":"TurnEnd","action":"if wearer.hp <= 15 and wearer.hp > 0 : wearer.hp += 10; TerminalObj.add(wearer.name + \"ate a cookie and recovered 10 HP.\")"}], "At the end of a turn, if your HP is lower or equal to 15, recover 10 HP."], # TODO: when anims are done add a cookie eating animation when this badge triggers
              ["Connector Badge",pygame.image.load("assets/shop/badges/badge_connector.png").convert_alpha(),"Oh, so THAT\'s how the burner gets electricity!",0,200,(0,0,0,0,1.5,1.25),[{"type":"event","event":"NewEffect","action":"affected.effects.electricity.duration -= 1"},{"type":"event","event":"NewAttack","action":"if affected.effects.electricity.duration > 0: attack.damage * 1.25"}], "Electricity lasts one turn less; and will multiply base attack damage by 1.25."],
              ["Cowboy Badge",pygame.image.load("assets/shop/badges/badge_cowboy.png").convert_alpha(),"Bring it a horse... It\'s gonna need it.",0,200,(0,0,1.5,2,0,0),[{"type":"event","event":"TurnEnd","action":"affected.cooldown -= 1"}],"At the end of a turn, reduces the cooldown of all of your abilities by 1 turn."],
              ["Cubic Badge",pygame.image.load("assets/shop/badges/badge_cubic.png").convert_alpha(),"Doesn\'t have real water.",0,200,(0,0,0,0,1.5,0),[{"type":"event","event":"NewSpecial","action":"for effect in spell.effects: if spell.type == \"wet\": spell.damage += 20"}],"Makes water related spells deal 20 more damage."],
              ["Debugger\'s Badge",pygame.image.load("assets/shop/badges/badge_DEBUG.png").convert_alpha(),"Cheater. Or contributor. We\'re fine with both <3",-1,21-14-20-9-20-12-5-4,(0,0,0,0,0,0),[{"type":None}],"Allows access to debug tools, if any are present in the current version."],
              ["Exploder Badge",pygame.image.load("assets/shop/badges/badge_exploder.png").convert_alpha(),"\"this won\'t explode or anything righ-\"",0,200,(-25,0,0,0,1.75,1.75),[{"type":"timed","turns":"3","action":"all.hp -= 25; TerminalObj.add(wearer.name + \"\'s badge exploded!\")"}], "Deals 25 damage to everyone every 3 turns. This includes allies."], # TODO: add an exploding animation to this too
              ["The Fat Fish",pygame.image.load("assets/shop/badges/badge_fatfish.png").convert_alpha(),"The biggest fish to fry; ready for cooking.",-1,21-14-20-9-20-12-5-4,(10,1,2,2,1.1,1.1),[{"type":"event","event":"TurnEnd","action":"if wearer.hp > 15: wearer.hp += 10; TerminalObj.add(wearer.name + \"bit the Fish and recovered 10 HP.\")"}], "At the end of a turn, if your HP is lower or equal to 15, recover 10 HP."], # TODO: and an eating animation to this too
              ["Flowered Badge",pygame.image.load("assets/shop/badges/badge_flowered.png").convert_alpha(),"Ooh, fancy!",0,200,(0,0,3,0,0,1.25),[{"type":"event","event":"Block","action":"if random.randint(1,10) == 7: enemy.effects.append(\"charmed\",2)"}],"Every time you block, there's a 1 in 10 chance to charm the enemy."],
              ["Healer Badge",pygame.image.load("assets/shop/badges/badge_healer.png").convert_alpha(),"Bidimensional potion. Cute.",0,225,(25,3,0,0,0,0),[{"type":"event","event":"Heal","action":"affected.hp += 10"}], "Every heal you get heals you 10 HP more than usual."],
              ["Hearted Badge",pygame.image.load("assets/shop/badges/badge_hearted.png").convert_alpha(),"Has a faint heartbeat. Expected, but creepy!",0,225,(40,2,0,0,0,0),[{"type":"event","event":"Heal","action":"affected.hp += 20"}], "Every heal you get heals you 20 HP more than usual."],
              ["Inspector Badge",pygame.image.load("assets/shop/badges/badge_inspector.png").convert_alpha(),"Look closely.",0,1000,(0,1,0,-1,0,0),[{"type":"continous","action":"WINDOW.blit(insert visual effect code here)"},{"type":"event","event":"BattleEnd","action":"affected.goldrecieve * 1.2"}], "Recolors every enemy to a golden hue while it's your turn, and, when the battle ends, gold gain is multiplied by 1.2."], # TODO: figure out how to do visual effects and add them
              ["Mortal Badge",pygame.image.load("assets/shop/badges/badge_mortal.png").convert_alpha(),"Decomposing.",0,1000,(-75,0,0,0,2.25,2.25),[{"type":"event","event":"TurnEnd","action":"affected.hp -= 5"}], "Lose 5 HP every turn."],
              ["Pencilcase Badge",pygame.image.load("assets/shop/badges/badge_pencilcase.png").convert_alpha(),"Filled with useful materials, like metal, metal, and paint. No refunds!",0,300,(5,0.5,1.5,1.5,1.05,1.05),[{"type":"event","event":"TurnStart","action":"affected.randstat += 5"},{"type":"event","event":"TurnEnd","action":"affected.randstat -= 5"}], "Every turn, a random stat will be raised by 5 points."],
              ["Plater Badge",pygame.image.load("assets/shop/badges/badge_plater.png").convert_alpha(),"It's just a steel plate.",0,225,(0,4,0,0,0,0),[{"type":None}],"Does nothing."],
              ["Starry Badge",pygame.image.load("assets/shop/badges/badge_starry.png").convert_alpha(),"Worst. Constellation. EVER.",0,250,(0,0,0,0,0,2),[{"type":"event","event":"NewSpecial","action":"special.damage * 1.25"}],"Multiplies special damage by 1.25 on top of the starting 2 times multiplier."],
              ["The Button",pygame.image.load("assets/shop/badges/badge_thebutton.png").convert_alpha(),"Do not press it.",0,400,(-35,0,0,0,2.5,2.5),[{"type":"timed","turns":"10","action":"affected.hp -= 32327526; TerminalObj.add(wearer.name + \"\'s badge exploded!\")"}], "Takes down EVERYONE after 10 turns. Bosses are inmune to this effect."],
              ["Timed Badge",pygame.image.load("assets/shop/badges/badge_timed.png").convert_alpha(),"You\'re late.",0,1000,(0,0,5,3,0,0),[{"type":"event","event":"TurnEnd","action":"all.cooldown -= 2"}], "At the end of a turn, reduces the cooldown of everyone's abilities by 2 turns."],
              ["UFO Badge",pygame.image.load("assets/shop/badges/badge_ufo.png").convert_alpha(),"The real ones make for astoundingly good frisbees.",0,250,(0,0,2,0,1.25,0),[{"type":"event","event":"NewAttack","action":"if random.randint(1,7) == 7: enemy.effects.append(\"bleeding\",3)"}], "Every time you attack, there's a 1 in 7 chance to make the enemy bleed."]] # TODO: same as the inspector badge

# TODO: deprecate hardcoded tables and load items armors and all of that from a definition file

# i gotchu fam ↑ 

specialdict={}

enemytable = []

def FilePathDecoder(filepath):
    # This should be deprecated. The os library already has something for this, I think? And whatever I was going to do with relative/absolute filepaths could be reimplemented later if needed.
    if filepath.startswith(".r/"):
        filepath = filepath.removeprefix(".r/")
    return filepath

def TextFixer(text):
    # Fixes a problem with encoding in other languages in Windows. It doesn't seem to happen under GNU/Linux, which is the only other platform I'm testing on; but if it happens in another one just put it in there.
    if sys.platform == "win32":
        try:
            return text.encode('latin-1').decode('utf-8')
        except Exception:
            return text
    else:
        return text

def JSONLoader(filepath):
    # Decodes a json file, and, according to its type, sorts its data into place.
    files = []
    for (dirpath,dirnames,filenames) in os.walk(filepath): # thanks StackOverflow
        files.extend(filenames)
    print("fp is", filepath)
    for file in files:
        if file != "example.json":
            try:
                decoder = json.load(fp=open(filepath+file))
                if decoder.get('filepath') != None:
                    decoder['filepath'] = FilePathDecoder(decoder['filepath'])
                entry = []
                print(decoder)
                if decoder['type'] == "URPGItem":
                    print("Item")
                    entry = [decoder['name'],pygame.image.load(decoder['filepath'] + decoder['img']).convert_alpha(),decoder['description'],decoder['command'],decoder['price'],pygame.image.load(decoder['filepath'] + decoder['btnimg']).convert_alpha()]
                    itemtable.append(entry)
                    print(itemtable)
                elif decoder['type'] == "URPGBadge":
                    print("Badge")
                    entry = [decoder['name'],pygame.image.load(decoder['filepath'] + decoder['img']).convert_alpha(),decoder['description'],decoder['tier'],decoder['price'],tuple(decoder['stats']),decoder['action'],decoder['actiondesc']]
                    badgetable.append(entry)
                    print(badgetable)
                elif decoder['type'] == "URPGArmor":
                    print("Armor")
                    entry = [decoder['name'],pygame.image.load(decoder['filepath'] + decoder['img']).convert_alpha(),decoder['description'],decoder['price'],decoder['tier'],"",decoder['weight'],tuple(decoder['stats']),decoder['resistance'],decoder['imgscale'],tuple(decoder['imgpos'])]
                    armortable.append(entry)   # we REALLY gotta deprecate IML 
                    print(armortable)
                elif decoder['type'] == "URPGWeapon":
                    print("Weapon")
                    category = 0
                    for i in range(len(weapontable)):
                        if isinstance(weapontable[i][0],str):
                            if weapontable[i][0] == decoder['category']:
                                category = i
                                break
                    entry = [decoder['name'],pygame.image.load(decoder['filepath'] + decoder['img']).convert_alpha(),decoder['description'],"",decoder['price'],decoder['tier'],tuple(decoder['stats']),decoder['specials']]
                    weapontable[category][1].append(entry)
                    print(weapontable[category][1])
                elif decoder['type'] == "URPGEnemy":
                    print("Enemy")
                    translations = decoder['translations']
                    for lang in decoder['translations']:    # this is weird but apparently i can't alter the dict i'm iterating over???? ok i guess it's some 80's arcane bull but if it's what i gotta do it's what i gotta do go my stupid second variable
                        for move in decoder['translations'][lang]:
                            if move == "name":
                                translations[lang]['name'] = TextFixer(decoder['translations'][lang]['name'])
                            else:
                                for key in decoder['translations'][lang][move]:
                                    print(decoder['translations'][lang][move][key])
                                    translations[lang][move][key] = TextFixer(decoder['translations'][lang][move][key])
                    entry=[decoder['name'],decoder['kind'],decoder['animations'],decoder['icon'],decoder['moves'],[decoder['hp'],decoder['def'],decoder['gold']],translations]
                    enemytable.append(entry)
                elif decoder['type'] == "URPGSpecial":
                    print("SPECIALS LOADED")
                    specialdict.update({str(file).removesuffix(".json"):decoder})
            except Exception:
                print("File", file, "wasn't a valid file.")
                pass # TODO: maybe log that it wasn't a JSON file?
    

JSONLoader("assets/definitions/items/")
JSONLoader("assets/definitions/badges/")
JSONLoader("assets/definitions/armors/")
JSONLoader("assets/definitions/weapons/")
JSONLoader("assets/definitions/specials/")
JSONLoader("assets/battle/enemies/main/")


nuggetsprite_normal = pygame.image.load("assets/nuggets.png").convert_alpha()
nuggetsprite_gold = pygame.image.load("assets/goldnuggets.png").convert_alpha()

for i in range(len(itemtable)):
    imager = itemtable[i][1].get_size()
    itemtable[i][1] = pygame.transform.scale(itemtable[i][1],(imager[0] * scaleW, imager[1] * scaleH))

for i in range(len(itemtable)):
    imager = itemtable[i][5].get_size()
    itemtable[i][5] = pygame.transform.scale(itemtable[i][5],(imager[0] * scaleW, imager[1] * scaleH))

for i in range(len(itemtable)):
    itemtable[i].append(pygame.transform.scale(itemtable[i][5],(28 * scaleW, 28 * scaleH)))

nuggetsprite_normal = pygame.transform.scale(nuggetsprite_normal,(nuggetsprite_normal.get_size()[0] * scaleW, nuggetsprite_normal.get_size()[1] * scaleH))
nuggetsprite_gold = pygame.transform.scale(nuggetsprite_gold,(nuggetsprite_gold.get_size()[0] * scaleW, nuggetsprite_gold.get_size()[1] * scaleH))

WINDOW.blit(smallboldfont.render("loaded definition tables",True,(255,255,255)),(0,0))
pygame.display.update()

def Outliner(img,color=(0,0,0,255),pos = (0,0),thickness=3):
    # Creates an image's outline, and returns the image with the applied outline in the specified color and rendering position for the image.
    # Code taken from a YouTube tutorial. (commented according to what it says in order to understand it myself)
    if isinstance(thickness,int) and thickness > 0:
        color = color
        mask = pygame.mask.from_surface(img) # Creates the image mask from the image. You know what that is, it's the black and white version of it.
        convmask = pygame.mask.Mask((thickness,thickness),True) # This is a 3x3 mask with all of it's bits set to 'the set mode'. I'm assuming that's either black or white.
        # For the pixels in the mask, we decide using the convmask what pixels we'll make drawable.
        outlined = mask.convolve(convmask).to_surface(setcolor=color,unsetcolor=(0,0,0,0)).convert_alpha() # This actually may cause problems in the future. WARN/NOTE: Set transparent pixels to a transparent tone on export.
        sizeoutline = outlined.get_rect().bottomright
        sizeimg = img.get_rect().bottomright
        renderpos = [pos[i] + ((sizeoutline[i] - sizeimg[i]) / 2) for i in range(len(sizeoutline))]
        return outlined,renderpos
    else:
        return pygame.surface.Surface((1,1)),(-1,-1)

def ErrorThrower(Error):
    # os.walk why don't you work >:C
    raise Error

class Animated():
    def __init__(self,frames=list(),default=41.66666667,changes=[]) -> None:
        # module updated 2025-09-15
        """
        Creates an animated object.

        Frames accepts a list with lists composed of a Surface, and either:
        1. an integer stating the FPS
        2. a float stating the milliseconds said frame will be on screen
        
        Changes in the framerate need to be passed manually in a [[frame,framerate],...] style.

        "default" specifies a fallback framerate. Can be useful for many an animation.
        It also accepts integers or floats.
        """
        # TODO: add an import from GIF or smth like that option, hardcoded shit fills up way too quick
        # maybe add pygame.image.load_animated() support?
        self.frames = frames
        for change in changes.copy():
            changes.remove(change)
            print(change)
            change[1] = (1000/change[1])/1000
            changes.append(change)
        default /= 1000
        if len(self.frames) > 0:
            if not isinstance(self.frames[0],list): # check that the data's correct
                # assuming that you just provided a list of images and not LISTS with an image inside:
                self.frames = [[frame,default] for frame in frames]
        for frame in self.frames.copy():
            if isinstance(frame,pygame.Surface):
                emptylist = list()
                emptylist.extend([frame,default])
                frame = emptylist
            if len(frame) == 1:
                frame.append(default)
            if isinstance(frame[1],int):
                frame[1] = (1000/frame[1])/1000
            for change in changes:
                try:
                    frame[change[0]][1] = change[1]
                except Exception:
                    pass
        self.timer = 0
        self.index = 0

    def import_from_folder(self,filepath,default=41.666666667,changes=[],regex=""):
        """
        Imports an animation from a folder containing its files.

        A regular expression/regex may be used to filter in/out certain files.
        """
        filepaths = []
        files = []
        default /= 1000
        for change in changes.copy():
            changes.remove(change)
            print(change)
            change[1] = (1000/change[1])/1000
            changes.append(change)
        print("entered",filepath)
        try:
            for (dirpath,dirnames,filenames) in os.walk(filepath,onerror=ErrorThrower): # reused from the JSON Loader
                if regex != "":
                    for filename in filenames.copy():
                        filenames.remove(filename)
                        if re.search(regex,filename) != None: # first time doing regex, please forgive
                            filepaths.append(filename)
                            print("fn:",filename)
                else:
                    filepaths.extend(filenames)
        except Exception:
            for (dirpath,dirnames,filenames) in os.walk(os.path.dirname(sys.argv[0])+filepath,onerror=ErrorThrower): # idk if this works on GNU and i hate this so much
                if regex != "":
                    for filename in filenames.copy():
                        filenames.remove(filename)
                        if re.search(regex,filename) != None: # first time doing regex, please forgive
                            filepaths.append(filename)
                            print("fn:",filename)
                else:
                    filepaths.extend(filenames)
        print(filepaths)
        for i in range(len(filepaths)):
            # i need to learn how lambda functions and shit work this sucks for performance
            framerate = default
            for change in changes:
                if i == change[0]:
                    framerate = change[1]
                    break
            files.append([pygame.image.load(filepath.removeprefix("/")+filepaths[i]).convert_alpha(),framerate])
        self.__init__(files,default)
        return self

    def draw(self, loop=True):
        """
        Draws said animated object.
        """
        if len(self.frames) > 0:
            self.timer += 1 * Game.milidt
            if self.timer >= self.frames[self.index][1]:
                self.index += 1
                self.timer = 0
            if self.index >= len(self.frames):
                self.timer = 0
                if loop == True:
                    self.index = 0
                else:
                    self.index -= 1
            try:
                return self.frames[self.index][0]
            except Exception:
                try:
                    return self.frames[self.index - 1][0]
                except Exception:
                    pass
        return Game.errorSurf

class Icons:
    # To load all the small icons here. I should probably split this into various classes or put it all in a dict with the filenames and let the game
    # load them or something. That actually sounds like a good idea.
    # NOTE: new class, and do that
    # NOTE: also this list is backported to the armor UI too
    stats = [pygame.image.load("assets/stats_hp.png").convert_alpha(),
             pygame.image.load("assets/stats_def.png").convert_alpha(),
             pygame.image.load("assets/stats_speed.png").convert_alpha(),
             pygame.image.load("assets/stats_cooldown.png").convert_alpha(),
             pygame.image.load("assets/stats_attack.png").convert_alpha(),
             pygame.image.load("assets/stats_special.png").convert_alpha(),
             pygame.image.load("assets/stats_better.png").convert_alpha(),
             pygame.image.load("assets/stats_worse.png").convert_alpha()]
    
WINDOW.blit(smallboldfont.render("animator and icons loaded",True,(255,255,255)),(0,12))
pygame.display.update()

class Menu:
    listitem = 0        # Selects an entry from a list.
    selector = 0
    subselector = 0
    cycle = 0
    if language == "Spanish":
        menuitems = [(("Iniciar Partida")),(("En Linea")),(("Configuración")),(("Mods")),(("Salir"))]
    else:
        menuitems = [(("Play")),(("Online")),(("Settings")),(("Mods")),(("Exit"))]
    if language == "Spanish":
        settingsitems = [(("Resolución")),(("{RESOLUTION}")),(("Pantalla Completa")),(("{CHECKBOX}")),(("Idioma")),(("{LANG}")),(("Guardar")),(("Volver"))]
    else:
        settingsitems = [(("Resolution")),(("{RESOLUTION}")),(("Fullscreen")),(("{CHECKBOX}")),(("Language")),(("{LANG}")),(("Save")),(("Back"))]

class Game:
    eventqueue = []     # NOTE: NEW SYSTEM FOR EVENT HANDLING; MOVE THAT HERE
    version = "PTB1"    # NOTE: updated version number
                        # IMPORTANT: remove timers when done with them. maybe add timer auto-cleanup? will check later
    timers = []         # Formatted as (100, ID), with the length being in frames and ID being an identifier
    idlookout = []      # This does not match a specific timerID to a specific object, it just makes it possible to check removed or expired timers
    state = "Menu"      # Selects the game's state.
    substate = ""       # Selects the game's substate.
    dt = float(1)
    milidt = float(1000)
    debug = False       # Activates Debug Mode. It's mostly a series of cheats you can toggle with the F3 key.
    cheatstates = { # TODO: Finish adding Debug Tools.
        "dbgOpen":False,
        "infiniteRevives":False
    }
    errorSurf = pygame.surface.Surface((16,16)).convert_alpha() # A fallback surface for when things go wrong.
    errorSurf.fill((255,0,255))
    time_since_start = 0.0
    """
    For reference: the mouse inputs are mLMB and mRMB, mPos for its pos.
    For keys, its k[Direction] for a directional input, kAccept to accept, and kDeny to deny.
    """
    inputs = {
        "kLeft":{
            "pressed":False,
            "justDown":False,
            "keys":[K_LEFT,K_a]
        },
        "kRight":{
            "pressed":False,
            "justDown":False,
            "keys":[K_RIGHT,K_d]
        },
        "kUp":{
            "pressed":False,
            "justDown":False,
            "keys":[K_UP,K_w]
        },
        "kDown":{
            "pressed":False,
            "justDown":False,
            "keys":[K_DOWN,K_s]
        },
        "kAccept":{
            "pressed":False,
            "justDown":False,
            "keys":[K_SPACE,K_RETURN,K_z]
        },
        "kDeny":{
            "pressed":False,
            "justDown":False,
            "keys":[K_ESCAPE,K_BACKSPACE,K_x]
        },
        "mLMB":{
            "pressed":False,
            "justDown":False
        },
        "mRMB":{
            "pressed":False,
            "justDown":False
        },
        "mPos":{
            "pos":()
        }
    }

def keyRemap(filepath="keybinds.dat"):
    try:
        with open(filepath) as f:
            for line in f:
                line = line.removesuffix("\n")
                split = line.split(":")
                constants = []
                for key in split[1].split(","):
                    constants.append(getattr(pygame.locals, key))   # VERY VERY IMPORTANT TODO: Make all exec() statements as safe as possible!
                                                                    # This is here because this was going to be an exec() and I was going crazy.
                Game.inputs[split[0]]["keys"] = constants
        return True
    except FileNotFoundError:
        return False
    

keyRemap()

class Battle: # TODO: probably make this into an object instead of a holder
    inputstate = "" # i think this is irrelevant but i gotta have it for now?
    battlebg = pygame.image.load("assets/testingroom_bg.png").convert_alpha()       # The background for the battle.
    battlebgrect = battlebg.get_size()
    battlebg = pygame.transform.scale(battlebg,(battlebgrect[0] * scaleW, battlebgrect[1] * scaleH)).convert_alpha()
    battlefloor = pygame.image.load("assets/testingroom_floor.png").convert_alpha() # The floor for the battle.
    battlefloorr = battlefloor.get_size()
    battlefloor = pygame.transform.scale(battlefloor,(battlefloorr[0] * scaleW, battlefloorr[1] * scaleH)).convert_alpha()
    particles = []
    music = pygame.mixer.Sound("sfx/untitledambiance-wind.wav")
    muson = False
    hpicon = pygame.transform.scale(pygame.image.load('assets/hpicon.png'),(pygame.image.load('assets/hpicon.png').get_size()[0] * scaleW, pygame.image.load('assets/hpicon.png').get_size()[1] * scaleH))
    ehpicon = pygame.transform.scale(pygame.image.load('assets/enemyhpicon.png'),(pygame.image.load('assets/enemyhpicon.png').get_size()[0] * scaleW, pygame.image.load('assets/enemyhpicon.png').get_size()[1] * scaleH))
    sendto = 0
    run=""
    holder = []
    combodata = ["",0]
    turn = 0
    playermovequeue = []

class Party():
    def __init__(self):
        self.partymembers = [Player()]
        self.membercount = 1
        self.alive = [True]
        self.defending = [False] # Yes, I'm aware I gotta fix this. But; it works, riiight?
        self.weapondict = {}
        self.armordict = {}
        self.badgedict = {}
    def save(self):
        # saves to the savefile.
        # NOTE: SAVE/LOAD FUNCTIONS ALTERED TO USE ; INSTEAD OF , FOR SPLITITNG DUE TO CONFLICTS WITH LISTS!
        #try:
            while True:
                try:
                    f = open("backupsave.sav", "w")
                    break
                except FileNotFoundError:
                    f = open("backupsave.sav", "x")
                    f = open("backupsave.sav", "w")
                except Exception:
                    print("ERROR: Game couldn't create savefile. Are you SURE you have write permissions?")
                    SystemError()
            f.write(Game.version + "\n")
            f.write(str(len(self.partymembers)) + "\n")
            for i in range(self.membercount):
                f.write(self.partymembers[i].name + ";")
                f.write(str(self.partymembers[i].hp) + ";")
                f.write(str(self.partymembers[i].hpmax) + ";")
                f.write(str(self.partymembers[i].gold) + ";")
                f.write(str(self.partymembers[i].mana) + ";")
                f.write(str(self.partymembers[i].weapon) + ";")
                f.write(str(self.partymembers[i].armor) + ";")
                badges = "["
                j = 0
                for badge in self.partymembers[i].badges:
                    print(badge)
                    if isinstance(badge,str):
                        badges += badge
                    else:
                        badges += str(badge)
                    if j == 0:
                        badges += ","
                    j += 1
                badges += "]"
                f.write(str(badges) + ";")
                f.write(str(self.partymembers[i].pos) + ";")
                f.write(str(self.partymembers[i].room) + ";")
                f.write("\n")
            # ugh this sucks but it's the things i do because i'm using the legacy saving shit
            # yes i am NOT moving to a new system i will deal with my legacy code for PTB1 >:C
            cycles = 0
            for flag in self.partymembers[0].flags:
                if cycles < len(self.partymembers[0].flags) - 1:
                    f.write(str(self.partymembers[0].flags[flag]) + ";")
                else:
                    f.write(str(self.partymembers[0].flags[flag]))
                cycles += 1
            f.write("\n")
            cycles = 0
            for item in self.partymembers[0].items:                      #the itemid thing was lazy but it works so who cares
                if cycles < len(self.partymembers[0].items) - 1:
                    f.write(str(self.partymembers[0].items[item]) + ";") #type: ignore
                else:
                    f.write(str(self.partymembers[0].items[item]))       #type: ignore
                cycles += 1
            f.write("\n")
            f.write(str(self.armordict) + ";" + str(self.weapondict) + ";" + str(self.badgedict))
            f.close()
            try:
                os.remove("save.sav")
            except Exception:
                if os.path.exists("save.sav") == True:
                    print("We... don't have write access to save.sav????")
                    return False
            os.rename("backupsave.sav","save.sav")
            return(True)
        #except Exception:
        #    return(False)

    def load(self,savefile="save.sav"):
        # loads from the savefile.
        # NOTE: SAVE/LOAD FUNCTIONS ALTERED TO USE ; INSTEAD OF , FOR SPLITITNG DUE TO CONFLICTS WITH LISTS!
        try:
            f = open(savefile, "r")
            lines = f.readlines()
            print("lines equals", lines)
            for i in range(len(lines)):
                line = lines[i]
                line = line.removesuffix("\n")
                print(i, "line equals", line)
                if i == 0:
                    print("versionCheck")
                    if line == Game.version:
                        print("Check passed. Save version:", line, "Game version:", Game.version)
                    else:
                        if line == "0.6.0PA":
                            print("PTB1+ savefiles are incompattible with 0.6.0PA save files; they use commas instead of semicolons and are missing crucial data.")
                        elif line.startswith("0.5.0PA"):
                            print("0.5.0 Prealpha savefiles are incompatible with the PTB1+ save format at a fundamental level.")
                        print("Previous save format used. Not compatible with this build. Try again later.")
                        exit()
                elif i == 1:
                    print("memberCount")
                    try:
                        self.partymembers = []
                        for j in range(int(line)):
                            self.partymembers.append(Player())
                        self.membercount = int(line)
                        self.alive = [True for i in range(self.membercount)]
                    except Exception:
                        print("Line 2 is not an int or float or anything intable or floatable; you've probably used an indev PTB1 build to make this save. Go and change that real quick so it supports multiple party members.")
                        exit()
                elif i in range(2,2+self.membercount):
                    print("playercharload")
                    liner = line.split(";")
                    self.partymembers[i-2].name = liner[0]
                    # fuck i gotta fix this one day
                    print(liner[0])
                    if liner[0] == "Thumbs":
                        self.partymembers[i-2].animations = [Animated([pygame.image.load("assets/battle/party/thumbs/neutral_0001.png").convert_alpha()],60),Animated([pygame.image.load("assets/battle/party/thumbs/neutral_0001.png").convert_alpha()],30),Animated([pygame.image.load("assets/battle/party/thumbs/neutral_0001.png").convert_alpha()],24)]
                        self.partymembers[i-2].hpimage = pygame.transform.scale(pygame.image.load("assets/hpicon_thumbs.png"),(pygame.image.load("assets/hpicon_thumbs.png").get_size()[0] * scaleW,pygame.image.load("assets/hpicon_thumbs.png").get_size()[1] * scaleH))
                    self.partymembers[i-2].hp = int(float(liner[1]))
                    self.partymembers[i-2].hpmax = int(float(liner[2]))
                    self.partymembers[i-2].gold = int(float(liner[3]))
                    self.partymembers[i-2].mana = int(float(liner[4]))
                    self.partymembers[i-2].weapon = liner[5]
                    self.partymembers[i-2].armor = liner[6]
                    self.partymembers[i-2].badges = liner[7].split(",")
                    self.partymembers[i-2].badges[0] = self.partymembers[i-2].badges[0].removeprefix("[")
                    self.partymembers[i-2].badges[1] = self.partymembers[i-2].badges[1].removesuffix("]")
                elif i == 2 + len(self.partymembers) and len(self.partymembers) != 0:
                    print("flag")
                    linesplit = line.split(";")
                    for j in range(len(self.partymembers[0].flags)):
                        self.partymembers[0].flags[j] = linesplit[j] # type: ignore
                elif i == 3 + len(self.partymembers) and len(self.partymembers) != 0:
                    print("items")
                    print(line)
                    linesplit = line.split(";")
                    print(linesplit)
                    for j in range(len(self.partymembers[0].items)):
                        self.partymembers[0].items[j] = int(linesplit[j]) # type: ignore
                        print(self.partymembers[0].items)
                elif i == 4 + len(self.partymembers) and len(self.partymembers) != 0:
                    print("equipment")
                    print(line)
                    linesplit=line.split(";")
                    self.armordict = eval(linesplit[0])
                    self.weapondict = eval(linesplit[1])
                    self.badgedict = eval(linesplit[2])
                    return True
            return True
        except Exception:
            return False

class Player():
    def __init__(self):
        # save.sav loading time
        self.hp = 100
        self.hpmax = 100
        self.name = "Guy"
        self.gold = 10
        self.weapon = "None"
        self.armor = "None"
        self.badges = ["None", "None"]
        self.mana = 100
        # NOTE: items shall be transfered to a "Party" class in the next versions.
        # NOTE: 2025-04-17: Even though I'm seeing that lil' note here, I'm editing how this goes since I also need this to be able to adapt for mods and for my sake.
        self.items = {}
        for i in range(len(itemtable)):
            self.items.update({i:0})
            if i == 0:
                self.items[i] = 3
            elif i == 1:
                self.items[1] = 1       # NOTE: this is a bad way of doing it but the 3 HealPots 1 EffectClear tradition MUST stand!
        self.pos = (0,0)
        self.room = "rooms/testingroom.urpg" # TODO: add save.sav loading. create the .urpg room format.
        self.effects = []
        self.animations = [Animated([pygame.image.load("assets/battle/party/guy/neutral0001.png").convert_alpha(),pygame.image.load("assets/battle/party/guy/neutral0002.png").convert_alpha(),pygame.image.load("assets/battle/party/guy/neutral0003.png").convert_alpha()],60),Animated([pygame.image.load("assets/urpg-guy-attacking.png").convert_alpha()],30),Animated([pygame.image.load("assets/urpg-guy-blocking.png").convert_alpha()],24)]
        self.hpimage = pygame.transform.scale(pygame.image.load("assets/hpicon_urpgguy.png"),(pygame.image.load("assets/hpicon_urpgguy.png").get_size()[0] * scaleW,pygame.image.load("assets/hpicon_urpgguy.png").get_size()[1] * scaleH))
        self.skipturn = False
        self.flags = {
            0 : False # Tutorial completion flag
        }
        self.hpbaraltpos = 0
        self.hpbaraltw = 0
        self.animqueue = [] # The current queue for animations.
        self.animtimer = 0

    def draw(self):
        # Calls the appropiate Animated Object and does what it needs to do.
        # Copy and paste as needed.
        # Last Updated: 2025-11-20.
        self.animtimer += 1*Game.milidt
        if self.animqueue != []:
            data = (self.animations[self.animqueue[0][0]].draw())
        else:
            data = (self.animations[0].draw()) # should probably make self.animations a dict
        if self.animqueue != [] and self.animqueue[0][1] < self.animtimer:
            self.animqueue.pop(0)
        return data
        
party = Party()
party.load("save.sav")

class Tickers:
    infoticker = pygame.image.load('assets/terminal_infoticker.png').convert_alpha()
    infotickerr = infoticker.get_size()
    infoticker = pygame.transform.scale(infoticker,(infotickerr[0] * scaleW, infotickerr[1] * scaleH)).convert_alpha()
    achticker = pygame.image.load('assets/terminal_achticker.png').convert_alpha()
    achtickerr = achticker.get_size()
    achticker = pygame.transform.scale(achticker,(achtickerr[0] * scaleW, achtickerr[1] * scaleH)).convert_alpha()

WINDOW.blit(smallboldfont.render("loaded player and game classes",True,(255,255,255)),(0,24))
pygame.display.update()

class Button():
    # NOTE: Updated predefs in __init__: it should be standard to declare scales only if needed. Also, maybe rename scaleH to scaleX and scaleW to scaleY in the future.
    # NOTE: Updated in 2024-08-26; apparently we could only blit to WINDOW when we should be able to blit to any surface
    # NOTE: Updated in 2024-12-18; there was a bug in the badge UI that probably affected all other UIs
    # NOTE: Updated in 2025-01-09; that bugfix introduced a new bug actually
    def __init__(self,x,y,image,scaleX = scaleH, scaleY = scaleW):
        # okay so these comments are more for myself since i'm new to this classes thing
        # this creates the button, assigns it the resized image, and sets its coords
        # check if this is a list
        if isinstance(image, list):
            width = image[0].get_width()
            height = image[0].get_height()
            self.images = [pygame.transform.scale(image[0],(int(width * scaleX), int(height*scaleY))),pygame.transform.scale(image[1],(int(width * scaleX), int(height*scaleY)))]
        else:
            width = image.get_width()
            height = image.get_height()
            self.imager = image
            for i in range(2):
                self.imager = pygame.transform.scale(image,(int(width * scaleX), int(height*scaleY)))
            self.images = [self.imager,self.imager]
        self.rect = self.images[0].get_rect() # we're assuming that image size will be equal.
        self.rect.topleft = (x,y)

    def draw(self,xoff=0,yoff=0,surface=WINDOW,surfacex=0,surfacey=0): # btw you shouldn't use surfacex and surfacey on WINDOW buttons
        global maag
        rectcopy = self.rect.copy()
        rectcopy.topleft = (xoff + self.rect.topleft[0], yoff + self.rect.topleft[1]) # this will break things but i am willing to fix em since THIS WILL BE SO MUCH FUCKING BETTER
        colliderect = rectcopy.move(surfacex,surfacey)
        action = False
        pos = pygame.mouse.get_pos()
        surfacerect = surface.get_rect().move(surfacex,surfacey)
        if surfacerect.collidepoint((rectcopy.centerx + surfacerect[0], rectcopy.centery + surfacerect[1])):
            # this renders the button and runs the code
            if colliderect.collidepoint(pos):
                if Game.inputs["mLMB"]["justDown"] == True:
                    if maag == False:
                        action = True
                        maag = True
                    surface.blit(self.images[1],(rectcopy))
                else:
                    surface.blit(self.images[0],(rectcopy))
            else:
                surface.blit(self.images[0],(rectcopy))
            if action == True and maag == False:
                action = False
            return action
        else:
            surface.blit(self.images[0],(rectcopy))    # NOTE: This is here because I'm not sure how to go about PROPERLY implementing render culling.
                                                        # The above code should be able to be modified to be render cull friendly.
    
    def copy(self):
        """
        Returns a copy of the button. Useful if you don't want to make new ones for some reason or another.
        """
        return self
        
class Dragable():
    # Acts like a Button, but dragable. Currently does not support holdover changes because those are implemented REALLY badly and I need to fix them.
    # TODO: Fix holdover changes in Buttons and Dragables
    def __init__(self,x,y,image,scaleX = scaleH, scaleY = scaleW):
        # okay so these comments are more for myself since i'm new to this classes thing
        # this creates the button, assigns it the resized image, and sets its coords
        # check if this is a list
        if isinstance(image, list):
            width = image[0].get_width()
            height = image[0].get_height()
            self.images = [pygame.transform.scale(image[0],(int(width * scaleX), int(height*scaleY))),pygame.transform.scale(image[1],(int(width * scaleX), int(height*scaleY)))]
        else:
            width = image.get_width()
            height = image.get_height()
            self.imager = image
            for i in range(2):
                self.imager = pygame.transform.scale(image,(int(width * scaleX), int(height*scaleY)))
            self.images = [self.imager,self.imager]
        self.rect = self.images[0].get_rect() # we're assuming that image size will be equal.
        self.rect.topleft = (x,y)
        self.active = False
    def draw(self,xoff=0,yoff=0,surface=WINDOW,surfacex=0,surfacey=0,limitx=(0,0),limity=(0,0),movefrom="topleft"): # btw you shouldn't use surfacex and surfacey on WINDOW buttons
        global maag
        self.rect.topleft = (xoff + self.rect.topleft[0], yoff + self.rect.topleft[1])
        colliderect = self.rect.move(surfacex,surfacey)
        # this renders the button and runs the code
        action = False
        pos = pygame.mouse.get_pos()
        if colliderect.collidepoint(pos):
            if Game.inputs["mLMB"]["pressed"] == True:
                self.active = True
                if maag == False:
                    action = True
                    maag = True
                surface.blit(self.images[1],(self.rect))
            else:
                surface.blit(self.images[0],(self.rect))
        else:
            surface.blit(self.images[0],(self.rect))
        if Game.inputs["mLMB"]["pressed"] == False:
            self.active = False
        if self.active == True:
            # this should be self explainatory but i'm explaining it anyways because i really gotta document URPG someday
            # x and y are the mouse's x and y
            # limitx and limity are the limits; they establish an area where the object can be dragged around
            # this area is a rect technically speaking and i could have made it one but it would have been messier i think
            # we check if x and y are within their limits
            # "but why do we substract the height from the upper boundary!" because we're measuring from the topleft and that makes it so
            # we measure correctly
            # ta-da
            # if this breaks you should probably try to fix it but check the code that's declaring this first and get a debugger handy
            # you do NOT want to see scrollbar hell
            # tip: if you're setting the values of limitx or y in a way that [0] == [1] and you get errors please check how you're declaring the obj
            # that seems to fix it rn

            # NOTE: 2025-09-05: what the fuck was i on while making this :sob:
            x,y = pos
            if limitx[0] != limitx[1]:
                if limitx[0] <= x <= limitx[1] - self.rect.width:
                    pass
                else:
                    if x > limitx[1] - self.rect.width:
                        x = limitx[1] - self.rect.width
                    elif x < limitx[0]:
                        x = limitx[0]
            else:
                x = limitx[0]
            if limity[0] != limity[1]:
                if limity[0] <= y <= limity[1] - self.rect.height:
                    pass
                else:
                    if y > limity[1] - self.rect.height:
                        y = limity[1] - self.rect.height
                    elif y < limity[0]:
                        y = limity[0]
            else:
                y = limity[0]
            if movefrom == "center":
                if limity[0] != limity[1]:
                    y += self.rect.height / 2
                if limitx[0] != limitx[1]:
                    x += self.rect.width / 2
                self.rect.center = x,y
            else:
                self.rect.topleft = x,y
        if surface != WINDOW:
            surfacerect = surface.get_rect()
            surfacerect = surfacerect.move(surfacex,surfacey)
            if surfacerect.collidepoint(pos) is False:
                return False, self.rect
        if action == True and maag == False:
            action = False, self.rect
        return action, self.rect 

class TextEng():
    # A text rendering engine.
    def __init__(self,fonts={},symbols={},decoration=pygame.Surface((1,1))) -> None:
        self.textlist = []
        if fonts == {}:
            self.fonts = {
                "default":pygame.font.Font("fonts/RobotoMono-Regular.ttf",20),
                "bold":pygame.font.Font("fonts/RobotoMono-Bold.ttf",20),
                "bolditalic":pygame.font.Font("fonts/RobotoMono-BoldItalic.ttf",20),
                "italic":pygame.font.Font("fonts/RobotoMono-Italic.ttf",20),
                "extralightitalic":pygame.font.Font("fonts/RobotoMono-ExtraLightItalic.ttf",20),
                "extralight":pygame.font.Font("fonts/RobotoMono-ExtraLight.ttf",20),
                "lightitalic":pygame.font.Font("fonts/RobotoMono-LightItalic.ttf",20),
                "medium":pygame.font.Font("fonts/RobotoMono-Medium.ttf",20),
                "mediumitalic":pygame.font.Font("fonts/RobotoMono-MediumItalic.ttf",20),
                "semibold":pygame.font.Font("fonts/RobotoMono-SemiBold.ttf",20),
                "semibolditalic":pygame.font.Font("fonts/RobotoMono-SemiBoldItalic.ttf",20),
                "thin":pygame.font.Font("fonts/RobotoMono-Thin.ttf",20),
                "thinitalic":pygame.font.Font("fonts/RobotoMono-ThinItalic.ttf",20)
            }
        else:
            self.fonts = fonts
        # The keys here should be:
        # "symbol:font"
        # To return to normacy, the normal symbol is [N] (or N:"default"). Hardcoded.
        # [IMG] will load and render an image.
        # The only other hardcoded symbol is [NL], which currently does newlines. We should probably make it do standard newlines.
        if symbols == {}:
            self.symbols = {
                "B":"bold",
                "BI":"bolditalic",
                "I":"italic",
                "ELI":"extralightitalic",
                "EL":"extralight",
                "LI":"lightitalic",
                "M":"medium",
                "MI":"mediumitalic",
                "SB":"semibold",
                "SBI":"semibolditalic",
                "T":"thin",
                "TI":"thinitalic"
            }
        else:
            self.symbols = symbols
        # Some other text options are hardcoded for now. TODO: Unhardcode them. Maybe do something with exec() again?
        # For instance, a "c=(RGB)" after a symbol can let you set the text's RGB value.
        # A "u" after a symbol can let you underline the text.
        # A "s=INT" specifies spacing with the latest text chunk. Works well with newlines.
        # You can join them together in this way: c=(RGB);u;...
        self.offset = 0
        self.imagedict = {

        }
        self.lastsize = [0,0]
        self.decoration = decoration
    def parser(self,text,space=(300,700)):
        parselist = []
        for chunk in text:
            font = "default"
            if self.symbols.get(chunk[0]) != None and self.symbols.get(chunk[0]) != "NL" and self.symbols.get(chunk[0]) != "N":
                font = self.symbols[(chunk[0])]
            rchunk = self.fonts[font].render(chunk[1],True,(255,255,255))
            if rchunk.get_width() > space[0]:
                sentence = ""
                additions = 0
                for word in chunk[1].split():
                    if self.fonts["default"].render(sentence + word,True,(255,255,255)).get_width() > space[0]:
                        parselist.append([chunk[0],sentence,chunk[2]])
                        additions += 1
                        sentence = ""
                    sentence += word + " "
                parselist.append([chunk[0],sentence,chunk[2]])
            else:
                if len(chunk) > 2:
                    parselist.append([chunk[0],chunk[1],chunk[2]])
                else:
                    parselist.append([chunk[0],chunk[1],""])
        if "]" in parselist[len(parselist)-2][1] and "[" in parselist[len(parselist)-2][1]:
            parselist.insert(0,parselist[len(parselist)-2])
            parselist.pop(len(parselist)-2)
        return parselist
    def draw(self,space=(300,700),decopos=(-1,-1)):
        drawsurf = pygame.Surface(space).convert_alpha()
        drawsurf.fill((50,50,50,0))
        position = [0,0]
        spacingbckup = 0
        if self.offset < 0:
            self.offset = 0
        for text in self.textlist.copy():
            # text drawer code here
            if text[0].lstrip() == "" or text[1].lstrip() == "" and text[0] != "NL":
                self.textlist.remove(text)
                continue
            font = "default"
            if self.symbols.get(text[0]) != None and text[0] != "NL" and text[0] != "N" and text[0] != "IMG":
                font = self.symbols[(text[0])]
            elif text[0] == "NL":
                position[1] += self.fonts["default"].get_height()
                position[0] = 0
                continue
            elif text[0] == "IMG" and text[1] != None:
                drawsurf.blit(self.imagedict[text[1]],(position[0],position[1]-self.offset))
                position[0] += self.imagedict[text[1]].get_rect()[2]
                if position[0] > space[0]:
                    position[0] = 0
                    position[1] += self.imagedict[text[1]].get_rect()[3]
                continue
            color = (255,255,255)
            underlining = False
            spacingbckup = 0
            if text[2] != "":
                data = text[2].split(";")
                for argument in data:
                    if argument.startswith("c="):
                        argument = argument.removeprefix("c=(").removesuffix(")")
                        color = [int(channel) for channel in argument.split(",")]
                    if argument == "u":
                        underlining = True
                    if argument.startswith("s="):
                        argument = argument.removeprefix("s=")
                        position[0] += int(argument)
                        spacingbckup = int(argument)
            rtext = self.fonts[font].render(text[1].strip(),True,color)
            if underlining == True:
                renderheight = rtext.get_rect().height
                pygame.draw.line(rtext,color,(0,renderheight - renderheight/ 8),(rtext.get_rect().width,renderheight - renderheight/ 8))
            if position[0] + rtext.get_rect().width > space[0] - 0:
                position[0] = 0 + spacingbckup
                position[1] += self.fonts[font].get_height()
            drawsurf.blit(rtext,(position[0],position[1]-self.offset)) # TODO: let aliasing change!
            position[0] += rtext.get_rect().width
        self.lastsize = [space[0],position[1]] # let's face it, we're always gonna have ONE full line o' text
        self.offset = position[1] - space[1]
        while self.offset > 50:
            if self.textlist[0][0] != 'NL' and self.textlist[0][0] != "N" and self.textlist[0][0] != "" and self.textlist[0][0] != "IMG":
                self.offset -= self.fonts[self.symbols[(self.textlist[0][0])]].get_height()
            elif self.textlist[0][0] != "":
                self.offset -= self.fonts['default'].get_height()
            if self.textlist[0][0] == "IMG":
                reused = 0
                for text in [text for text in self.textlist if text[0] == "IMG"]:
                    if text[1] == self.textlist[0][1]:
                        reused += 1
                        break
                if reused <= 0:
                    try:
                        self.imagedict.pop(self.textlist[0][1])
                    except:
                        pass # look i'm gonna be honest it'd be insane for this to happen somehow??
            self.textlist.pop(0)
        if decopos != (-1,-1):
            retsurf = self.decoration.copy()
            retsurf.blit(drawsurf,decopos)
            return retsurf
        return drawsurf
    def add(self,text,space=(300,700),noNL=False):
        text = TextFixer(str(text))
        # NOTE: remake this with regex possibly to split the text better, can't even >:3 now
        if not text.startswith("["):
            text = "[N]" + text
        text = text.split("[")
        textcopy = text.copy()
        for i in range(len(text)):
            if text[i].startswith("/"):
                textcopy[i] = textcopy[i-1] + "[" + textcopy[i].removeprefix("/")
                textcopy.pop(i-1)
        text = textcopy
        for i in range(len(text)):
            temp = text[i].split("]")
            extra = temp[0].split(" ")
            if len(extra) > 1:
                temp[0] = extra[0]
                temp.append(extra[1])
            else:
                temp.append("")
            if text[i].endswith("/]") == True:
                print("condition triggered")
                temp[1] = temp[1].removesuffix("/") + "]"
            text.pop(i)
            text.insert(i,temp) #type:ignore
        for item in text:
            if item[0].lstrip() == "":
                text.pop(0)
                continue
        for chunk in text.copy():
            if chunk[0] == "NL" and chunk[1] != "":
                chunk[0] = "N"#type:ignore
                text.insert(i,["NL","",""])#type:ignore
                i += 1
            elif chunk[0].split(" ")[0] == "NL":
                chunk[0] = "NL"#type:ignore
            elif chunk[0] == "IMG":
                self.imagedict.update({chunk[1]+" ":pygame.image.load(chunk[1])})#this is a dumb solution
            i += 1
        if noNL != True:
            text.append(["NL","",""])#type:ignore
        self.textlist.extend(self.parser(text,space))

class NoteInfo:
    btnsurf = pygame.surface.Surface((319,32)).convert_alpha()
    btnsurf.fill((50,50,50))
    pygame.draw.line(btnsurf,(255,255,255),(0,0),(319,0))
    btnsurf.blit(font.render("Notebook",True,(255,255,255)),(5,3))
    openNotebookButton = Button(961,688,btnsurf)
    del btnsurf

class Sounds:
    purchase = [pygame.mixer.Sound("sfx/purchase1.wav"),pygame.mixer.Sound("sfx/purchase2.wav")]
    listscrollsfx = pygame.mixer.Sound('sfx/listscroll.wav')
    selectsfx = pygame.mixer.Sound('sfx/select.wav')
    deniedsfx = pygame.mixer.Sound('sfx/denied.wav')
    swcombosfx = pygame.mixer.Sound('sfx/slashcombo.wav')
    clocktickfastsfx = pygame.mixer.Sound("sfx/clocktick-fast.wav")
    clocktickmidsfx = pygame.mixer.Sound("sfx/clocktick-mid.wav")
    clocktickslowsfx = pygame.mixer.Sound("sfx/clocktick-slow.wav")
    save = pygame.mixer.Sound("sfx/save.wav")
    slashsfx = pygame.mixer.Sound("sfx/slash1.wav")
    parrysfx = pygame.mixer.Sound("sfx/slash2.wav")

WINDOW.blit(smallboldfont.render("loaded sfx and buttons",True,(255,255,255)),(0,36))
pygame.display.update()

class Room:
    """
    Also known as a map. You can move around in it.
    """
    def __init__(self):
        """
        Creates a blank room. You should load its values from a file.
        """
        self.name = ""
        self.author = ""
        self.bgCol = pygame.Color(0,0,0)
        self.formatVer = 0
        self.saveIcon = Game.errorSurf
        self.mods = "vanilla"
        self.ppos = pygame.Vector2(0.0,0.0)
        self.cpos = pygame.Vector2(0.0,0.0)
        self.pspeed = pygame.Vector2(0.0,0.0)
        self.size = (0,0)
        self.tilesize = 0 # TODO: Probably allow per-layer tilesizing?
        self.tilesets = [
            # Quick note here: tiles only need the nnn key to be drawable. Other values are optional.
            # keys are written this way: s is side. c is corner. i is inner. e is external. n is neutral.
            # sec, sic, sen, sin, nnn are the valid values for a tileset right now.
            # The collision property automatically adds a hitbox to every tile in said tileset. TODO: Optimize that so it creates the minimum number of hitboxes possible.
            # If collision is set, the optional hitbox property can be used to specify a hitbox in pixels with a Rect.
            ]
        self.details = {
            # Key:value. Nothing to clarify here.
        }
        self.rendersurf = pygame.surface.Surface(self.size).convert_alpha()
        self.playerrenderlayer = 0 # The layer number to render the player on top of. This should probably be changed.
        self.layers = [] # Look at the testing layers below for an example, as there's no docs right now.
        self.entities = [] # Look at the testing entity list below for an example for that same reason.
        self.exits = {} # A dict of room names and filepaths to exit to.
    
    def _load_test_room(self):
        """
        Loads a hardcoded testing/error handling room.

        When creating mods, you should replace the values here and define a suitable room for your mod.
        """
        self.name = "base.test.testRoom"
        self.ppos = pygame.Vector2(0.0,0.0)
        self.cpos = pygame.Vector2(0.0,0.0)
        self.pspeed = pygame.Vector2(0.0,0.0)
        self.size = (1280,960)
        self.tilesize = 40
        self.bgCol = pygame.Color(80,80,80)
        self.saveIcon = Game.errorSurf
        self.formatVer = 0
        self.author = "The Untitled RPG Game Contributors"
        self.mods = "vanilla"
        self.tilesets = [
            {"nnn":pygame.image.load("assets/testtile.png").convert_alpha(),
             "collision":None},
            {"nnn":pygame.image.load("assets/testwall.png").convert_alpha(),
             "collision":pygame.Rect(0,20,40,80)}
        ]
        self.details = {"testflower":pygame.image.load("assets/testdetail.png").convert_alpha()}
        self.rendersurf = pygame.surface.Surface(self.size).convert_alpha()
        self.playerrenderlayer = 2 # The layer number to render the player on top of.
        self.layers = [
            {"type":0, # Layer type 0 is tilebased. Layer type 1 is detail/position based.
            "cmds":[ # This key stores the rects that will be drawn in this type of tile. Please note that you MUST sort the rects in ascending y order to avoid rendering issues.
                    {
                        "tile":0,
                        "rects":[pygame.Rect(0,0,36,24)]
                    }
                ]},
            {"type":1,
             "cmds":[
                 {
                     "detail":"testflower",
                     "positions":[(random.randint(0,720),random.randint(0,720)) for i in range(30)]
                 }
             ]},
            {"type":0,
             "cmds":[
                 {
                     "tile":1,
                     "rects":[pygame.Rect(3,9,3,1),pygame.Rect(10,10,1,1),pygame.Rect(15,15,2,1)]
                 }
             ]}
        ]
        self.entities = [
            # TODO: Determine if we can work with just triggers or if other things are needed.
            {
                "type":"trigger",
                "activateby":"collision",
                "exdata":[],
                "hitbox":pygame.Rect(60,60,90,90),
                "pos":[60,60],
                "runtimelogic":None,
                "execute":"print(\"triggered!\")"
            },
            {
                "type":"trigger",
                "activateby":"collision",
                "exdata":[pygame.image.load("assets/movingtestentity.png").convert_alpha()],
                "hitbox":pygame.Rect(400,60,90,90),
                "pos":[400,60],
                "runtimelogic":"self.entities[active][\"pos\"][1] += 3*Game.milidt;self.entities[active][\"hitbox\"].topleft = self.entities[active][\"pos\"];self.rendersurf.blit(self.entities[active][\"exdata\"][0],self.entities[active][\"pos\"])",
                "execute":"""pygame.draw.rect(self.rendersurf,(0,0,0),(self.ppos[0]-12.5,self.ppos[1]-40,60,30));
pygame.draw.rect(self.rendersurf,(255,255,255),(self.ppos[0]-7.5,self.ppos[1]-35,50,20));
self.rendersurf.blit(font.render(\"use\",(0,0,0),True),(self.ppos[0]-7.5,self.ppos[1]-40));
if Game.inputs[\"kAccept\"][\"justDown\"] is True:
    Game.state = \"Battle\"
    Game.substate = \"\"
    DodgeObj.moves = []""" # Hell yeah, we can do this now. I really should check if there's a way to make pylance and VSC autocomp work on this now.
                                              # Technically speaking you can run anything here now. Here be dragons until I try to sandbox and fix this.
            }
        ]
        self.exits = {"base.test.exampleRoom":"assets/definitions/rooms/example.json"}
        return self
    
    def loadFromJSON(self,filepath):
        """Loads a room from a JSON file."""
        # TODO: This and other loaders could benefit from multithread. Look into it.
        roomData = {}
        try:
            roomData = json.load(open(filepath))
            if roomData["type"] == "URPGRoom":
                if roomData["name"] == "base.test.exampleRoom" and Game.debug == False:
                    print("The room provided is the example room definition file. You probably don't want to load THIS room. Go put values in it.")
                    # originally was an exception but idgaf atp
                if roomData["formatver"] == 0:
                    if roomData["gamever"] != Game.version:
                        print(f"File {filepath} was made for a previous version of the game, though format hasn\'t changed. Here be dragons.")
                    # we don't have a modding API rn so we can skip the mod check for now
                    self.size = tuple(roomData["size"])
                    self.rendersurf = pygame.surface.Surface(self.size).convert_alpha()
                    if not self.size[0] > 0 and self.size[1] > 0:
                        raise Warning(f"Room size must be greater than 0 on all axis. Size: {self.size}")
                    self.formatVer = roomData["formatver"]
                    self.ppos = pygame.Vector2(roomData["startpos"])
                    self.tilesize = roomData["tilesize"] # once again we really should make this per-layer
                    self.tilesets = roomData["tilesets"]
                    self.details = roomData["details"]
                    self.playerrenderlayer = roomData["playerrenderlayer"]
                    self.layers = roomData["layers"]
                    self.bgCol = roomData["bgCol"]
                    for i in range(len(self.layers)):
                        if self.layers[i]["type"] == 0:
                            for j in range(len(self.layers[i]["cmds"])):
                                print("rect",self.layers[i]["cmds"][j]["rects"])
                                for k in range(len(self.layers[i]["cmds"][j]["rects"])):
                                    self.layers[i]["cmds"][j]["rects"][k] = pygame.Rect(self.layers[i]["cmds"][j]["rects"][k])
                    self.entities = roomData["entities"]
                    for i in range(len(self.entities)):
                        self.entities[i]["hitbox"] = pygame.Rect(self.entities[i]["hitbox"])
                        try:
                            if self.entities[i]["runtimelogic"].startswith("$"):
                                if self.entities[i]["runtimelogic"] == "$NONE":
                                    self.entities[i]["runtimelogic"] = None
                                else:
                                    self.entities[i]["runtimelogic"] = str(open(filepath.removesuffix(filepath.split("/")[len(filepath.split("/"))-1])+self.entities[i]["runtimelogic"].removeprefix("$")))
                            if self.entities[i]["execute"].startswith("$"):
                                if self.entities[i]["execute"] == "$NONE":
                                    self.entities[i]["execute"] = None
                                else:
                                    self.entities[i]["execute"] = str(open(filepath.removesuffix(filepath.split("/")[len(filepath.split("/"))-1])+self.entities[i]["execute"].removeprefix("$")))
                        except Exception:
                            raise Warning(f"A script file could not be found. See above for details.")
                    self.author = roomData["author"]
                    if roomData["saveIcon"] != "": self.saveIcon = roomData["saveIcon"]
                    return self
                else:
                   raise Warning(f"File {filepath} is using another format version.\nExpected: 0\nFound: {roomData["formatver"]}") 
            else:
                raise Warning(f"File {filepath} did not have the \"URPGRoom\" type.")
        except Exception:
            if roomData == {}:
                raise Warning(f"File {filepath} was not a JSON file.\n--- end of probably long debug message ---")
            else:
                raise Warning("--- end of probably long debug message ---")
        return False

    def draw(self):
        """
        Draws the room on screen based on the camera position and zoom.
        
        As is currently standard (2025-11-03) for all of this game's modules, this method also runs the logic of a room.
        """
        hitboxes = []
        lindex = 0
        playerRendered = False
        self.rendersurf.fill(self.bgCol)
        for layer in self.layers:
            if layer["type"] == 0:
                for cmd in layer["cmds"]:                
                    for rect in cmd["rects"]:
                        if rect[1]*self.tilesize > self.ppos[1] and not playerRendered and lindex == self.playerrenderlayer: # I'll be very frank here; if you want the effect this code tried to achieve, please just split your walls in two. Or fix this and commit. Any combo of the 2 works for me.
                            pygame.draw.rect(self.rendersurf,(255,0,0),(self.ppos[0],self.ppos[1],35,70))
                            playerRendered = True
                        for i in range(rect[2]):
                            for j in range(rect[3]):
                                self.rendersurf.blit(self.tilesets[cmd["tile"]]["nnn"],(self.tilesize*i+self.tilesize*rect[0],self.tilesize*j+self.tilesize*rect[1]))
                                if self.tilesets[cmd["tile"]].get("collision") != None:
                                    copyrect = self.tilesets[cmd["tile"]].get("collision").copy()
                                    hitboxes.append(copyrect.move(self.tilesize*i+self.tilesize*rect[0],self.tilesize*j+self.tilesize*rect[1]))
            elif layer["type"] == 1:
                for cmd in layer["cmds"]:
                    cmd["positions"].sort()
                    for position in cmd["positions"]:
                        if position[1] > self.ppos[1] and not playerRendered and lindex == self.playerrenderlayer: # TODO: this code is broken asf, fix it
                            pygame.draw.rect(self.rendersurf,(255,0,0),(self.ppos[0],self.ppos[1],35,70))
                            playerRendered = True
                        self.rendersurf.blit(self.details[cmd["detail"]],position)
            lindex += 1
        if playerRendered == False:
            pygame.draw.rect(self.rendersurf,(50,50,50),(self.ppos[0],self.ppos[1],35,70))
            # This is a failsafe. However, it'll trigger pretty often; so just call your normal player animation code.
        #if Game.debug == True:
        #    for hitbox in hitboxes:
        #        pygame.draw.rect(self.rendersurf,(255,255,0),hitbox)
        movementvector = pygame.Vector2(0,0)
        # yes, it's a pile of ifs. idk how to do this better.
        if Game.inputs["kLeft"]["pressed"] == True:
            movementvector[0] += -20*Game.milidt
            if self.pspeed[0] > 1:
                self.pspeed[0] = 1
        if Game.inputs["kRight"]["pressed"] == True:
            movementvector[0] += 20*Game.milidt
            if self.pspeed[0] < -1:
                self.pspeed[0] = -1
        if Game.inputs["kUp"]["pressed"] == True:
            movementvector[1] += -20*Game.milidt
            if self.pspeed[1] > 1 and movementvector[1] == 0:
                self.pspeed[1] = 1
        if Game.inputs["kDown"]["pressed"] == True:
            movementvector[1] += 20*Game.milidt
            if self.pspeed[1] < -1 and movementvector[1] == 0:
                self.pspeed[1] = -1
        if movementvector != pygame.Vector2(0,0):
            movementvector.normalize()
        self.pspeed += movementvector
        # I thought this'd be cleaner. It looks smarter, at least.
        for i in range(2): # if you're making 3D movement in this engine i am so fucking sorry for you
            if abs(self.pspeed[i]) > 5:
                self.pspeed[i] = math.copysign(5,self.pspeed[i])
            elif abs(self.pspeed[i]) > 0 and movementvector[i] == 0: # Decelerate ONLY when not trying to move, silly.
                if math.copysign(1,self.pspeed[i] + -40*math.copysign(1,self.pspeed[i])*Game.milidt) == math.copysign(1,self.pspeed[i]):
                    self.pspeed[i] += -40*math.copysign(1,self.pspeed[i])*Game.milidt
                else:
                    self.pspeed[i] = 0
        phitbox = pygame.Rect(self.ppos[0] + self.pspeed[0],self.ppos[1] + 60,35,10)
        if phitbox.collideobjects(hitboxes) != None:
            self.pspeed[0] = 0
        phitbox.topleft = self.ppos[0],self.ppos[1] + self.pspeed[1] + 60
        if phitbox.collideobjects(hitboxes) != None:
            self.pspeed[1] = 0
        phitbox.topleft = (self.ppos[0] + self.pspeed[0],self.ppos[1] + self.pspeed[1] + 60)
        if phitbox.collideobjects(hitboxes) != None:
            self.pspeed = pygame.Vector2(0,0)
        self.ppos += self.pspeed
        for i in range(2):
            if self.ppos[i] < 0:
                self.ppos[i] = 0
            elif self.ppos[i] > self.size[i]-10:
                self.ppos[i] = self.size[i]-10
        active = 0
        for entity in self.entities:
            # TODO: REALLY important to limit these execs before release.
            if entity["runtimelogic"] != None:
                exec(entity["runtimelogic"])
            if entity["type"] == "trigger":
                pygame.draw.rect(self.rendersurf,(0,0,255),entity["hitbox"],1)
                if entity["activateby"] == "collision":
                    if entity["hitbox"].collidepoint(self.ppos+(17.5,35)):
                        exec(entity["execute"])
                else:
                    if exec(entity["activateby"]) != False:
                        exec(entity["execute"])
            active += 1
        if self.size[0] > 960 and self.ppos[0] > 480 and self.ppos[0] < self.size[0] - 480:
            self.cpos[0] = self.ppos[0] - 480
        if self.size[1] > 720 and self.ppos[1] > 360 and self.ppos[1] < self.size[1] - 360:
            self.cpos[1] = self.ppos[1] - 360
        return self.rendersurf, -self.cpos

class RoomManager:
    """
    Deals with a set of rooms, and how they load.
    """
    def __init__(self,roomDict={},startIn=""):
        """
        Initialises the RoomManager with the specified Rooms. AKA "we move values around".
        """
        self.roomDict = roomDict
        self.curRoom = startIn
        if self.roomDict == {} and self.curRoom == "":
            self.roomDict = {"base.test.testRoom":Room._load_test_room(Room())}
            self.curRoom = "base.test.testRoom"
        newloads = self.roomDict[self.curRoom].exits.copy()
        for key in newloads.keys():
            self.roomDict.update({key:Room.loadFromJSON(Room(),newloads[key])}) # sometimes when pylance tells you smth it's not cuz you're wrong
                                                                                # but rather it's cuz you're stupid

    def draw(self):
        """
        Basically a forwarder.
        """
        return self.roomDict[self.curRoom].draw()

    def changeRoom(self,newRoom):
        roomsloaded = self.roomDict.keys()
        newrooms = {newRoom:Room.loadFromJSON(Room(),self.roomDict[self.curRoom].exits[newRoom])} # we gotta find a filepath
        for key in self.roomDict[newRoom].exits.keys():
            # format for rooms wanted: roomname:roompath
            if key not in roomsloaded:
                print({key:Room.loadFromJSON(Room(),self.roomDict[newRoom].exits[key])})
                newrooms.update({key:Room.loadFromJSON(Room(),self.roomDict[newRoom].exits[key])})
            elif key in roomsloaded:
                print({key:self.roomDict[key]})
                newrooms.update({key:self.roomDict[key]})
        self.roomDict = newrooms.copy()
        self.curRoom = newRoom
        print(self.roomDict, self.curRoom)

RoomHandler = RoomManager()

class Notebook:
    """The preferred UI method, since you can just make a JSON and use a page viewer and make most UI.\n
    World's your oyster, just don't use it for RCE."""
    def __init__(self,pages={},active="") -> None:
        self.pagesurf = pygame.Surface((1,1)).convert_alpha()
        self.offset = [0,0]
        self.pages = pages
        self.active = active
        self.assetdict = {}
        self.extradata = []
        self.listpos = [0,0]
        self.imirror = 0

    def loadFromJSON(self,filepath):
        addition = json.load(open(filepath))
        self.pages.update({addition["name"]:addition})
        return self

    def setActive(self,setActiveTo): # NOTE: gotta set up the inherits
        self.active = setActiveTo
        self.assetdict = {}
        self.extradata = []
        if self.pages[self.active].get("extradata") != None:
            self.extradata = [eval(data) for data in self.pages[self.active]["extradata"]]
        self.pagesurf = pygame.Surface((self.pages[setActiveTo]["frame"][2],self.pages[setActiveTo]["frame"][3])).convert_alpha()

    def textToPos(self,pos):
        """
        This only exists because of a nasty bug that I had no idea of how to solve in any other way at the moment and is not a performant solution to it. TODO: Find one.
        """
        try:
            for i in range(len(pos)):
                if isinstance(pos[i],str):
                    pos[i] = eval(pos[i])
        except TypeError:
            if isinstance(pos,str):
                pos = eval(pos)
            else:
                int(pos)
                # if you passed an unintable thingy here ya fucked up :3
        return pos

    def pageParse(self,element):
        self.cond = True
        if element.get("drawif") != None:
            exec(element["drawif"])
        if self.cond:
            if element["type"] == "text":
                if self.assetdict.get(element["text"]) is None:
                    temptexteng = TextEng()
                    if element["text"].startswith("$"):
                        self.textdata = ""
                        if element["text"].startswith("$ST/SCR"):
                            scriptdata = element["image"].removeprefix("$ST/SCR:").split(":")
                            exec(scriptdata[0])
                            exec(open(scriptdata[1]).read())
                            del scriptdata
                        elif element["text"].startswith("$STSCR"):
                            exec(element["text"].removeprefix("$STSCR:"))
                        elif element["text"].startswith("$SCR"):
                            scriptdata = open(element["text"].split(":")[1])
                            scriptdata = scriptdata.read()
                            exec(scriptdata)
                            del scriptdata
                        temptexteng.add(self.textdata,(element["space"][2],element["space"][3]))
                    else:
                        temptexteng.add(element["text"],(element["space"][2],element["space"][3]))
                    self.assetdict.update({element["text"]:temptexteng.draw((element["space"][2],element["space"][3]))})
                self.pagesurf.blit(self.assetdict[element["text"]],self.textToPos([element["space"][0],element["space"][1]]))
            elif element["type"] == "image":
                if self.assetdict.get(element["image"]) is None:
                    if element["image"].startswith("$"):
                        self.imgdata = pygame.Surface((1,1)).convert_alpha()
                        self.imgdata.fill((255,0,255))
                        if element["image"].startswith("$ST/SCR"):
                            scriptdata = element["image"].removeprefix("$ST/SCR:").split(":")
                            exec(scriptdata[0])
                            exec(open(scriptdata[1]).read()) # Dangerous as all hell. PTB 1.1 is gonna be the security update istfg
                            del scriptdata
                        elif element["image"].startswith("$STSCR"):
                            exec(element["image"].removeprefix("$STSCR:")) # You're kidding. It HAS to be a "self" variable to be editable like how I want it to? Why?!
                        elif element["image"].startswith("$SCR"):
                            scriptdata = open(element["image"].split(":")[1])
                            scriptdata = scriptdata.read()
                            exec(scriptdata) # Dangerous as all hell. PTB 1.1 is gonna be the security update istfg
                            del scriptdata
                        self.assetdict.update({element["image"]:self.imgdata})
                        del self.imgdata
                    else:
                        try:
                            self.assetdict.update({element["image"]:pygame.image.load(element["image"]).convert_alpha()})
                        except Exception:
                            self.assetdict.update({element["image"]:Game.errorSurf})
                self.pagesurf.blit(self.assetdict[element["image"]],self.textToPos(element["position"]))
            elif element["type"] == "animated":
                if self.assetdict.get(str(element["frames"]) + str(element["fpslist"])) == None:
                    framelist = []
                    for frame in element["frames"]:
                        if frame.startswith("$"):
                            self.imgdata = pygame.Surface((1,1)).convert_alpha()
                            self.imgdata.fill((255,0,255))
                            if frame.startswith("$STSCR"):
                                exec(frame.removeprefix("$STSCR:"))
                            elif frame.startswith("$SCR"):
                                scriptdata = open(frame.split(":")[1])
                                exec(scriptdata.read()) # Dangerous as all hell. PTB 1.1 is gonna be the security update istfg
                                scriptdata.close()
                                del scriptdata
                            framelist.append(self.imgdata)
                            del self.imgdata
                        else:
                            try:
                                framelist.append(pygame.image.load(frame).convert_alpha())
                            except Exception:
                                framelist.append(Game.errorSurf)
                    self.assetdict.update({str(element["frames"]) + str(element["fpslist"]):Animated(framelist,changes=[[i,element["fpslist"][i]] for i in range(len(element["fpslist"]))])}) # there MUST be a better way to do this
                data = self.assetdict[str(element["frames"]) + str(element["fpslist"])].draw(loop=element["loop"]==1)
                if not isinstance(data, pygame.Surface):
                    data = Game.errorSurf
                self.pagesurf.blit(data,self.textToPos(element["position"]))
            elif element["type"] == "button":
                if self.assetdict.get(element["image"] + element["execute"]+str(element["position"])) is None:
                    if element["image"].startswith("$"):
                        self.imgdata = pygame.Surface((1,1)).convert_alpha()
                        self.imgdata.fill((255,0,255))
                        if element["image"].startswith("$STSCR"):
                            exec(element["image"].removeprefix("$STSCR:"))
                        elif element["image"].startswith("$SCR"):
                            scriptdata = open(element["image"].split(":")[1])
                            exec(scriptdata.read()) # once again this is a major security vulnerability
                            scriptdata.close()
                            del scriptdata
                        self.assetdict.update({element["image"] + element["execute"]+str(self.imirror)+str(element["position"]):Button(self.textToPos(element["position"][0]),self.textToPos(element["position"][1]),self.imgdata)})
                        del self.imgdata
                    else:
                        try:
                            self.assetdict.update({element["image"] + element["execute"]+str(self.imirror)+str(element["position"]):Button(self.textToPos(element["position"][0]),self.textToPos(element["position"][1]),pygame.image.load(element["image"]))})
                        except Exception:
                            self.assetdict.update({element["image"] + element["execute"]+str(self.imirror)+str(element["position"]):Button(self.textToPos(element["position"][0]),self.textToPos(element["position"][1]),Game.errorSurf)}) # for future jes WHY DID YOU MAKE SETTING A BUTTON'S X AND Y POS LIKE THIS GRRAAAAHHHH
                if self.assetdict[element["image"]+element["execute"]+str(self.imirror)+str(element["position"])].draw(surface=self.pagesurf,surfacex=self.pages[self.active]["frame"][0]+self.listpos[0],surfacey=self.pages[self.active]["frame"][1]+self.listpos[1]):
                    exec(element["execute"])
            elif element["type"] == "list":
                backuppagesurf = self.pagesurf.copy()
                self.pagesurf = pygame.Surface(element["renderarea"]).convert_alpha()
                self.pagesurf.fill((0,0,0,0))
                self.imirror = 0
                self.listpos = element["position"]
                if element["iterate"] == "i":
                    for i in range(int(eval(element["repeat"]))):
                        try:
                            for component in element["contents"].copy():
                                self.pageParse(component)
                        except Exception:
                            pass
                        self.imirror += 1
                self.listpos = [0,0]
                self.imirror = 0
                backuppagesurf.blit(self.pagesurf,element["position"])
                self.pagesurf = backuppagesurf

    def draw(self):
        try:
            self.pagesurf.fill(self.pages[self.active]["bgcol"])
        except Exception:
            print("Invalid page color - filling with white.")
            self.pagesurf.fill((255,255,255))
        for component in self.pages[self.active]["elements"]:
            #try:
            self.pageParse(component)
            #except Exception:
            #    print("An element could not be rendered.")
        return self.pagesurf,(self.pages[self.active]["frame"][0],self.pages[self.active]["frame"][1]),self.offset

NotebookObj = Notebook.loadFromJSON(Notebook(),"assets/definitions/notebook/default.json")
NotebookObj.setActive("base.base.default")

WINDOW.blit(smallboldfont.render("UI frontend ready, terminal ready",True,(255,255,255)),(0,48))
pygame.display.update()

class ArmorShop():
    # TODO: Shop UIs require finishing asthetical changes. Apply them once they're in maingame and working.
    # While we're at it, fix up scrolling for the item shop UI. And button alignment. And buttons. And- you get the deal, don't 'cha?
    # Also; TODO: make a way to supply only certain items or armors or weapons to these UIs; that's the whole reason why
    # I'm making them adaptive to what's supplied.
    def __init__(self):
        self.btnlst = []
        self.buybtn = Button(984*scaleW,578*scaleH,pygame.image.load("assets/shop_buybtn.png").convert_alpha())
        self.scrollpos = 0
        self.doscroll = False
        self.activearmor = -1
        decosurf = pygame.Surface((320,720)).convert_alpha()
        decosurf.fill((50,50,50))
        pygame.draw.line(decosurf,(255,255,255),(0,0),(0,720))
        self.textobj = TextEng(decoration=decosurf)
        del decosurf
        btnimg = pygame.Surface((96 * scaleW,32 * scaleH)).convert_alpha()
        btnimg.fill((0,0,0,0))
        pygame.draw.rect(btnimg,(255,255,255),(0 * scaleW,0 * scaleH,72 * scaleW,32 * scaleH))
        pygame.draw.polygon(btnimg,(255,255,255),[(72 * scaleW,0 * scaleH),(72 * scaleW,32 * scaleH),(96 * scaleW,32 * scaleH)])
        btnimg.blit(font.render("Back",True,(0,0,0)),(4 * scaleW,4 * scaleH))
        self.backbtn = Button(0*scaleW,560*scaleH,btnimg)
        for armor in armortable:
            armorimg = pygame.transform.scale_by(armor[1],0.5) # Is this quicker? Or just easier? TODO: look at performance upon running this 1000 times
            btnimg = pygame.Surface((128,128)).convert_alpha()
            btnimg.fill((30,30,30))
            # Middling code. Literally.
            rect = armorimg.get_rect()
            btnimg.blit(armorimg,(abs(rect.width-128) / 2,abs(rect.height-128) / 2))
            self.btnlst.append(Button(0,0,btnimg,scaleW,scaleH))
        if 128 * len(self.btnlst) > WINDOW_WIDTH - (320 * scaleW):
            self.doscroll = True
        else:
            self.doscroll = False
        self.PlayerArmorStats = ()
        for i in range(len(armortable)):
            if armortable[i][1] == party.partymembers[0].weapon:
                self.PlayerArmorStats = armortable[i][7] # NOTE: if we can't find this all goes to shit so I better add something in case we can't
        self.bg = pygame.transform.scale_by(pygame.image.load("assets/notebookpaper.png").convert_alpha(),fusedscale)
        self.scrollSetter()


    def scrollSetter(self):
        self.scrolllimit = 960 - len(self.btnlst) * 128
        if self.scrolllimit > 0:
            self.doscroll = False
        else:
            self.doscroll = True
        self.scrollnum = len(self.btnlst) * 128
        if self.doscroll == True:
            scrollbarsurf = pygame.Surface((math.log(self.scrollnum) * 96,10)).convert_alpha()
            # WIP: Experimenting with scrollimit alternatives to fix a bug in badges.py and all other systems.
            # Returns self.scrollimit; maybe we can do something with this?
            self.SCROLLCONST = 960 + self.scrolllimit
        else:
            scrollbarsurf = pygame.Surface((1,1)).convert_alpha()
        self.scrollbar = Dragable(0,710,scrollbarsurf)

    def draw(self):
        WINDOW.blit(TerminalObj.draw(decopos=(10,10)),(960,0))
        if Game.substate == "Shop":
            Game.substate = "AShop"
        scaledsurface = pygame.Surface((960*scaleW,592*scaleH)).convert_alpha()
        scaledsurface.fill((0,0,0,0))
        scaledsurface.blit(self.bg,(0,0))
        scaledsurface.blit(pygame.transform.scale_by(pygame.image.load("assets/urpg-guy.png").convert_alpha(),3*fusedscale),(244*scaleH,40*scaleW))
        i = 0
        for armor in armortable:
            if i == self.activearmor:
                scaledsurface.blit(pygame.transform.scale_by(armor[1],armor[9]),armor[10])
                break
            else:
                i += 1
        for i in range(len(party.partymembers[0].badges)):    
            for badge in badgetable:
                if badge[0] == party.partymembers[0].badges[i]:
                    scaledsurface.blit(pygame.transform.scale_by(badge[1],0.18),(537 + i*32,370 + i*25))
        for category in weapontable:
            for weaponsel in category[1]:
                if weaponsel[0] == party.partymembers[0].weapon:
                    scaledsurface.blit(pygame.transform.rotate(pygame.transform.scale_by(weaponsel[1],category[4]*fusedscale),category[5]),category[3])
        WINDOW.blit(scaledsurface)
        # Maybe I should clear the Terminal instead of replacing it for this usecase? Could work. Who knows. If it doesn't I'll just implement the old-fashioned solution.
        pygame.draw.rect(WINDOW,(45,45,45),(0 * scaleW,624 * scaleH, 959 * scaleW, 720 * scaleH))
        drawsurface = pygame.Surface((959 * scaleW, 128 * scaleH)).convert_alpha()
        drawsurface.fill((55,55,55))
        if self.doscroll == True:
            action, rect = self.scrollbar.draw(limitx=(0,960),limity=(710,710))
            self.scrollpos = - abs(rect[0] * ((len(self.btnlst) * 128 - 960) / (960 - self.scrollbar.rect.width)))
            # Because I'll forget this: the calculations we're doing here are:
            #   1. (getting the amount of distance that we need to cover / the amount of space that we have to scroll)
            #   2. rect's x pos * 1's result
            #   3. abs(2's result) so we get a positive float
            #   4. -3's result because we really needed it negative but the abs makes sure we don't end up with a positive number where we wanted a negative
            # A bug could happen, resulting in a ZeroDivisionError, if self.scrollbar.rect.width == 960; but hopefully that doesn't happen.
        for i in range(len(self.btnlst)):
            self.btnlst[i].rect.x = (i * 128 + self.scrollpos) * scaleW
            if self.btnlst[i].draw(0,0,drawsurface,0*scaleW,592*scaleH) == True:
                pygame.mixer.Sound.play(Sounds.listscrollsfx)
                self.activearmor = i
                text = armortable[i][2]
                self.textobj.textlist = [] # this is probably the worst fucking way to do this but new additions are new additions
                self.textobj.add(text)
        if self.activearmor != -1:
            pygame.draw.rect(WINDOW,(55,55,55),(960 * scaleW,0 * scaleH,360 * scaleW,720 * scaleH))
            pygame.draw.rect(WINDOW,(255,255,255), pygame.Rect(960 * scaleH,0 * scaleW,1 * scaleH,720 * scaleW))
            WINDOW.blit(font.render(armortable[self.activearmor][0],True,(255,255,255)),(970*scaleW,4*scaleH))
            pygame.draw.line(WINDOW,(255,255,255),(970*scaleW,32*scaleH),(1270*scaleW,32*scaleH))
            WINDOW.blit(self.textobj.draw(),(970*scaleW,68*scaleH))
            WINDOW.blit(font.render("Weight Class: " + str(armortable[self.activearmor][6]),True,(255,255,255)),(970*scaleW, 36 *scaleH))
            self.textobj.draw(decopos=(10,10))
            pygame.draw.line(WINDOW,(255,255,255),(970*scaleW,(self.textobj.lastsize[1] + 98)*scaleH),(1270*scaleW,(self.textobj.lastsize[1] + 98)*scaleH))
            # Rendering the stats.
            statsrendered = 0
            i = 0 # it's a bit late at night when i'm coding this; we doing this this way
            for stat in armortable[self.activearmor][7]:
                if stat != 0:
                    WINDOW.blit(Icons.stats[i],(968,(self.textobj.lastsize[1] + 114 + statsrendered * 32) * scaleH))
                    statText = font.render(str(stat),True,(255,255,255))
                    WINDOW.blit(statText,(986,(self.textobj.lastsize[1] + 108 + statsrendered * 32) * scaleH)) # NOTE: altered this a bit, get it into armortable
                    statTextRect = statText.get_rect()
                    try:
                        if stat > self.PlayerArmorStats[i]:
                            WINDOW.blit(Icons.stats[6],((statTextRect.bottomright[0] + 996) * scaleW,(self.textobj.lastsize[1] + 114 + statsrendered * 32) * scaleH))
                        elif stat < self.PlayerArmorStats[i]:
                            WINDOW.blit(Icons.stats[7],((statTextRect.bottomright[0] + 996) * scaleW,(self.textobj.lastsize[1] + 114 + statsrendered * 32) * scaleH))
                    except Exception:
                        # this should only trigger if the player char has no armor. TODO: give the player char some armor by default
                        WINDOW.blit(Icons.stats[6],((statTextRect.bottomright[0] + 996) * scaleW,(self.textobj.lastsize[1] + 114 + statsrendered * 32) * scaleH))
                    statsrendered += 1
                i += 1
            if self.buybtn.draw():
                if party.partymembers[0].gold >= armortable[self.activearmor][4]:
                    if party.armordict.get(armortable[self.activearmor][0]) == None:
                        party.armordict.update({armortable[self.activearmor][0]:0})
                    party.armordict[armortable[self.activearmor][0]] += 1
                    party.partymembers[0].gold -= armortable[self.activearmor][4]
                    TerminalObj.add("Bought a " + str(armortable[self.activearmor][0]) + "!")
                    TerminalObj.add("You've got " + str(party.armordict.get(armortable[self.activearmor][0])) + ".")
                    pygame.mixer.Sound.play(Sounds.purchase[random.randint(0,1)])
                else:
                    TerminalObj.add("Not enough nuggets!")
                    pygame.mixer.Sound.play(Sounds.deniedsfx)
                self.activearmor = -1
            WINDOW.blit(font.render("Price: " + str(armortable[self.activearmor][4]),True,(255,255,255)),(984*scaleW, 522*scaleH))
            WINDOW.blit(font.render("Your Nuggets: " + str(party.partymembers[0].gold),True,(255,255,255)),(984*scaleW, 546*scaleH))
        WINDOW.blit(drawsurface,(0*scaleW,592*scaleH))
        if self.backbtn.draw() is True:
            pygame.mixer.Sound.play(Sounds.selectsfx)
            Game.substate = "Shop"
            return False
        pygame.draw.rect(WINDOW,(255,255,255),(self.scrollbar.rect))  # TODO: add transparency to this
            

ArmorShopItem = ArmorShop()

class WeaponShop():
    def __init__(self):
        self.chosenweapon = -1
        self.chosentype = -1
        self.scrollpos = 0
        self.doscroll = True
        self.scrolllimit = 0
        self.textobj = TextEng()
        self.btnlst = []
        self.typebtnlst = []
        self.buybtn = Button(984*scaleW,578*scaleH,pygame.image.load("assets/shop_buybtn.png").convert_alpha())
        self.scrollbar = Dragable(0,710,pygame.Surface((10,10)).convert_alpha())
        btnimg = pygame.Surface((96 * scaleW,32 * scaleH)).convert_alpha()
        btnimg.fill((0,0,0,0))
        pygame.draw.rect(btnimg,(255,255,255),(0 * scaleW,0 * scaleH,72 * scaleW,32 * scaleH))
        pygame.draw.polygon(btnimg,(255,255,255),[(72 * scaleW,0 * scaleH),(72 * scaleW,32 * scaleH),(96 * scaleW,32 * scaleH)])
        btnimg.blit(font.render("Back",True,(0,0,0)),(4 * scaleW,4 * scaleH))
        self.backbtn = Button(0*scaleW,560*scaleH,btnimg)
        j = 0
        for i in range(len(weapontable)):
            self.btnlst.append([])
            k = 0
            for weapon in weapontable[i][1]:
                armorimg = pygame.transform.scale_by(weapon[1],0.5)                 # Most of this is inherited from the armor shop code. This is middling and scaling code.
                                                                                    # NOTE: TURN THIS INTO A FUNCTION IF I END UP USING IT A TON! Don't want to end up with 0.5.0PA again.
                btnimg = pygame.Surface((128*scaleW,128*scaleH)).convert_alpha()
                btnimg.fill((0,0,0,0))
                btnimg.blit(armorimg,(0,0))
                self.btnlst[j].append(Button(0*scaleW,0*scaleH,btnimg,scaleW,scaleH))
                k += 1
            self.typebtnlst.append(Button(0,0,pygame.transform.scale_by(weapontable[i][2],0.5),scaleW,scaleH))
            j += 1
        self.bg = pygame.transform.scale_by(pygame.image.load("assets/notebookpaper.png").convert_alpha(),fusedscale)
        self.PlayerWeaponStats = (0,0,0,0,0,0,0)
        for i in range(len(weapontable)):
            for j in range(len(weapontable[i][1])):
                if weapontable[i][1][j][0] == party.partymembers[0].weapon:
                    self.PlayerWeaponStats = weapontable[i][1][j][6] # NOTE: if we can't find this all goes to shit so I better add something in case we can't
        scrollbarsurf = pygame.Surface((960,10)).convert_alpha() # Placeholder so that we have a value for this
        scrollbarsurf.fill((255,255,255,50))
        self.scrollbar = Dragable(0,710,scrollbarsurf)
        self.scrollnum = 0
        self.scrollSetter()

    def scrollSetter(self):
        if self.chosentype != -1:
            self.scrolllimit = 960 - len(self.btnlst[self.chosentype]) * 128
            if self.scrolllimit > 0:
                self.doscroll = False
            else:
                self.doscroll = True
            self.scrollnum = len(self.btnlst[self.chosentype]) * 128
        else:
            self.scrolllimit = 960 - (len(self.typebtnlst) * 128)
            if self.scrolllimit > 0:
                self.doscroll = False
            else:
                self.doscroll = True
            self.scrollnum = len(self.typebtnlst) * 128
        if self.doscroll == True:
            scrollbarsurf = pygame.Surface((math.log(self.scrollnum) * 96,10)).convert_alpha()
            # WIP: Experimenting with scrollimit alternatives to fix a bug in badges.py and all other systems.
            # Returns self.scrollimit; maybe we can do something with this?
            self.SCROLLCONST = 960 + self.scrolllimit
        else:
            scrollbarsurf = pygame.Surface((1,1)).convert_alpha()
        self.scrollbar = Dragable(0,710,scrollbarsurf)

    def draw(self):
        WINDOW.blit(TerminalObj.draw(decopos=(10,10)),(960,0))
        if Game.substate == "Shop":
            Game.substate = "WShop"
        scaledsurface = pygame.Surface((960*scaleW,592*scaleH)).convert_alpha()
        scaledsurface.fill((0,0,0,0))
        scaledsurface.blit(self.bg,(0,0))
        scaledsurface.blit(pygame.transform.scale_by(pygame.image.load("assets/urpg-guy.png").convert_alpha(),3*fusedscale),(244*scaleH,40*scaleW))
        for armor in armortable:
            if armor[0] == party.partymembers[0].armor:
                scaledsurface.blit(pygame.transform.scale_by(armor[1],armor[9]),armor[10])
        for i in range(len(party.partymembers[0].badges)):    
            for badge in badgetable:
                if badge[0] == party.partymembers[0].badges[i]:
                    scaledsurface.blit(pygame.transform.scale_by(badge[1],0.18),(537 + i*32,370 + i*25))
        if self.chosentype != -1 and self.chosenweapon != -1:
            scaledsurface.blit(pygame.transform.rotate(pygame.transform.scale_by(weapontable[self.chosentype][1][self.chosenweapon][1],weapontable[self.chosentype][4]*fusedscale),weapontable[self.chosentype][5]),weapontable[self.chosentype][3])
        
        WINDOW.blit(scaledsurface)
        if self.doscroll == True:
            action, rect = self.scrollbar.draw(limitx=(0,960),limity=(710,710))
            if self.chosentype != -1:
                self.scrollpos = - abs(rect[0] * ((len(self.btnlst[self.chosentype]) * 128 - 960) / (960 - self.scrollbar.rect.width)))
            else:
                self.scrollpos = - abs(rect[0] * ((len(self.typebtnlst) * 128 - 960) / (960 - self.scrollbar.rect.width)))
                # problem: self.scrollbar.rect.width may get bigger than 960; that breaks absolutely everything and is the reason for the report down there
            # Because I'll forget this: the calculations we're doing here are:
            #   1. (getting the amount of distance that we need to cover / the amount of space that we have to scroll)
            #   2. rect's x pos * 1's result
            #   3. abs(2's result) so we get a positive float
            #   4. -3's result because we really needed it negative but the abs makes sure we don't end up with a positive number where we wanted a negative
            # A bug could happen, resulting in a ZeroDivisionError, if self.scrollbar.rect.width == 960; but hopefully that doesn't happen.
        drawsurface = pygame.Surface((959 * scaleW, 128 * scaleH)).convert_alpha()
        drawsurface.fill((55,55,55))
        if self.chosentype != -1:
            for j in range(len(self.btnlst[self.chosentype])):
                self.btnlst[self.chosentype][j].rect.x = (j * 128 + self.scrollpos) * scaleW
                if self.btnlst[self.chosentype][j].draw(0,0,drawsurface,0*scaleW,592*scaleH) == True:
                    pygame.mixer.Sound.play(Sounds.listscrollsfx)
                    self.chosenweapon = j
                    text = weapontable[self.chosentype][1][self.chosenweapon][2]
        else:
            for i in range(len(self.typebtnlst)):
                self.typebtnlst[i].rect.x = (i * 128 + self.scrollpos) * scaleW
                if self.typebtnlst[i].draw(0,0,drawsurface,0*scaleW,592*scaleH) == True:
                    self.scrollpos = 0
                    self.chosentype = i
                    self.scrollSetter()
        WINDOW.blit(drawsurface,(0*scaleW,592*scaleH))
        pygame.draw.rect(WINDOW,(255,255,255),(self.scrollbar.rect))  # TODO: add transparency to this
        if self.backbtn.draw():
            pygame.mixer.Sound.play(Sounds.selectsfx)
            if self.chosentype != -1:
                self.chosentype = -1
                self.chosenweapon = -1
                self.scrollSetter()
            else:
                Game.substate = "Shop"
                return False
        if self.chosenweapon != -1 and self.chosentype != -1:
            try:
                boole = text == "b"
                del boole
            except Exception:
                text = weapontable[self.chosentype][1][self.chosenweapon][2]
            self.textobj.textlist = []
            self.textobj.add(str(text))
            pygame.draw.rect(WINDOW,(55,55,55),(960 * scaleW,0 * scaleH,360 * scaleW,720 * scaleH))
            pygame.draw.rect(WINDOW,(255,255,255), pygame.Rect(960 * scaleH,0 * scaleW,1 * scaleH,720 * scaleW))
            WINDOW.blit(font.render(weapontable[self.chosentype][1][self.chosenweapon][0],True,(255,255,255)),(970*scaleW,4*scaleH))
            pygame.draw.line(WINDOW,(255,255,255),(970*scaleW,32*scaleH),(1270*scaleW,32*scaleH))
            WINDOW.blit(font.render("Weight Class: " + str(weapontable[self.chosentype][1][self.chosenweapon][5]),True,(255,255,255)),(970*scaleW, 36 *scaleH))
            pygame.draw.line(WINDOW,(255,255,255),(970*scaleW,(self.textobj.lastsize[1] + 90)*scaleH),(1270*scaleW,(self.textobj.lastsize[1] + 90)*scaleH))
            # Rendering the stats.
            statsrendered = 0
            i = 0 # it's a bit late at night when i'm coding this; we doing this this way
            WINDOW.blit(self.textobj.draw(),(970*scaleW,(64)*scaleH))
            for stat in weapontable[self.chosentype][1][self.chosenweapon][6]:
                if stat != 0:
                    WINDOW.blit(Icons.stats[i],(968,(self.textobj.lastsize[1] + 102 + statsrendered * 32) * scaleH))
                    statText = font.render(str(stat),True,(255,255,255))
                    WINDOW.blit(statText,(986,(self.textobj.lastsize[1] + 96 + statsrendered * 32) * scaleH)) # NOTE: altered this a bit, get it into armortable
                    statTextRect = statText.get_rect()
                    if stat > self.PlayerWeaponStats[i]:
                        WINDOW.blit(Icons.stats[6],((statTextRect.bottomright[0] + 996) * scaleW,(self.textobj.lastsize[1] + 102 + statsrendered * 32) * scaleH))
                    elif stat < self.PlayerWeaponStats[i]:
                        #print(self.textobj) there was a random crash here??? idk why
                        WINDOW.blit(Icons.stats[7],((statTextRect.bottomright[0] + 996) * scaleW,(self.textobj.lastsize[1] + 102 + statsrendered * 32) * scaleH))
                    statsrendered += 1
                i += 1
            if self.buybtn.draw():
                if party.partymembers[0].gold >= weapontable[self.chosentype][1][self.chosenweapon][4]:
                    party.partymembers[0].gold -= weapontable[self.chosentype][1][self.chosenweapon][4]
                    if party.weapondict.get(weapontable[self.chosentype][1][self.chosenweapon][0]) == "None":
                        party.weapondict.update({weapontable[self.chosentype][1][self.chosenweapon][0]:0})
                    party.weapondict[weapontable[self.chosentype][1][self.chosenweapon][0]] += 1
                    TerminalObj.add("Bought a " + weapontable[self.chosentype][1][self.chosenweapon][0] + "!")
                    TerminalObj.add("You've got " + str(party.weapondict[weapontable[self.chosentype][1][self.chosenweapon][0]]) + ".")
                    pygame.mixer.Sound.play(Sounds.purchase[random.randint(0,1)])
                    for i in range(len(weapontable)):
                        for j in range(len(weapontable[i][1])):
                            if weapontable[i][1][j][0] == party.partymembers[0].weapon:
                                self.PlayerWeaponStats = weapontable[i][1][j][6] # NOTE: if we can't find this all goes to shit so I better add something in case we can't
                else:
                    TerminalObj.add("Not enough gold.")
                    pygame.mixer.Sound.play(Sounds.deniedsfx)
                self.chosenweapon = -1
            WINDOW.blit(font.render("Price: " + str(weapontable[self.chosentype][1][self.chosenweapon][4]),True,(255,255,255)),(984*scaleW, 522*scaleH))
            WINDOW.blit(font.render("Your Nuggets: " + str(party.partymembers[0].gold),True,(255,255,255)),(984*scaleW, 546*scaleH))

WeaponShopObj = WeaponShop()

class BadgeShop():
    # TODO: Shop UIs require finishing asthetical changes. Apply them once they're in maingame and working.
    # While we're at it, fix up scrolling for the item shop UI. And button alignment. And buttons. And- you get the deal, don't 'cha?
    # Also; TODO: make a way to supply only certain items or armors or weapons to these UIs; that's the whole reason why
    # I'm making them adaptive to what's supplied.
    def __init__(self):
        self.slotbtnlst = []
        for badge in party.partymembers[0].badges:
            btnsurf = pygame.Surface((96,96)).convert_alpha()
            btnsurf.fill((0,0,0))
            pygame.draw.rect(btnsurf,(255,255,255),(4,4,88,88),2)
            btnsurf.blit(font.render(str(len(self.slotbtnlst)),True,(255,255,255)), (40,36))
            if badge != None:
                text = smolfont.render(badge,True,(255,255,255))
                btnsurf.blit(text,((96 - text.get_width()) / 2,60))
            self.slotbtnlst.append(Button(990 + (96 * len(self.slotbtnlst)) + 60 * len(self.slotbtnlst),600,btnsurf))
        self.state = ""
        self.btnlst = []
        self.buybtn = Button(984*scaleW,578*scaleH,pygame.image.load("assets/shop_buybtn.png").convert_alpha())
        self.scrollpos = 0
        self.doscroll = False
        self.activebadge = -1
        decosurf = pygame.Surface((320,720)).convert_alpha()
        decosurf.fill((50,50,50))
        pygame.draw.line(decosurf,(255,255,255),(0,0),(0,720))
        self.textobj = TextEng(decoration=decosurf)
        del decosurf
        btnimg = pygame.Surface((96 * scaleW,32 * scaleH)).convert_alpha()
        btnimg.fill((0,0,0,0))
        self.desctextobj = TextEng()
        pygame.draw.rect(btnimg,(255,255,255),(0 * scaleW,0 * scaleH,72 * scaleW,32 * scaleH))
        pygame.draw.polygon(btnimg,(255,255,255),[(72 * scaleW,0 * scaleH),(72 * scaleW,32 * scaleH),(96 * scaleW,32 * scaleH)])
        btnimg.blit(font.render("Back",True,(0,0,0)),(4 * scaleW,4 * scaleH))
        self.backbtn = Button(0*scaleW,560*scaleH,btnimg)
        for badge in badgetable:
            badgeimg = pygame.transform.scale_by(badge[1],0.5) # Is this quicker? Or just easier? TODO: look at performance upon running this 1000 times
            btnimg = pygame.Surface((128,128)).convert_alpha()
            btnimg.fill((30,30,30))
            btnimg.blit(badgeimg)
            self.btnlst.append(Button(0,0,btnimg,scaleW,scaleH))
        if 128 * len(self.btnlst) > WINDOW_WIDTH - (320 * scaleW):
            self.doscroll = True
        else:
            self.doscroll = False
        self.PlayerBadgeStats = []
        for j in range(len(party.partymembers[0].badges)):
            for i in range(len(badgetable)):
                if badgetable[i][0] == party.partymembers[0].badges[j]:
                    self.PlayerBadgeStats.append(badgetable[i][5]) # NOTE: if we can't find this all goes to shit so I better add something in case we can't
                elif party.partymembers[0].badges[j] == "None":
                    self.PlayerBadgeStats.append((0,0,0,0,0,0))
        # replace all of this with code adapted to the bi-slot system
        self.bg = pygame.transform.scale_by(pygame.image.load("assets/notebookpaper.png").convert_alpha(),fusedscale)
        self.scrollSetter()

    def scrollSetter(self):
        self.scrolllimit = 960 - len(self.btnlst) * 128
        if self.scrolllimit > 0:
            self.doscroll = False
        else:
            self.doscroll = True
        self.scrollnum = len(self.btnlst) * 128
        if self.doscroll == True:
            scrollbarsurf = pygame.Surface((math.log(self.scrollnum) * 96,10)).convert_alpha()
            # WIP: Experimenting with scrollimit alternatives to fix a bug in badges.py and all other systems.
            # Returns self.scrollimit; maybe we can do something with this?
            self.SCROLLCONST = 960 + self.scrolllimit
        else:
            scrollbarsurf = pygame.Surface((1,1)).convert_alpha()
        self.scrollbar = Dragable(0,710,scrollbarsurf)

    def draw(self):
        WINDOW.blit(TerminalObj.draw(decopos=(10,10)),(960,0))
        if Game.substate == "Shop":
            Game.substate = "BShop"
        # TODO: prerender this because this probably uses a lot of processing power to run each frame
        scaledsurface = pygame.Surface((960*scaleW,592*scaleH)).convert_alpha()
        scaledsurface.fill((0,0,0,0))
        scaledsurface.blit(self.bg,(0,0))
        scaledsurface.blit(pygame.transform.scale_by(pygame.image.load("assets/urpg-guy.png").convert_alpha(),3*fusedscale),(244*scaleH,40*scaleW))
        i = 0
        for armor in armortable:
            if armor[0] == party.partymembers[0].armor:
                scaledsurface.blit(pygame.transform.scale_by(armor[1],armor[9]),armor[10])
                break
            else:
                i += 1
        for i in range(len(party.partymembers[0].badges)):    
            for badge in badgetable:
                if badge[0] == party.partymembers[0].badges[i]:
                    scaledsurface.blit(pygame.transform.scale_by(badge[1],0.18),(537 + i*32,370 + i*25))
        for category in weapontable:
            for weaponsel in category[1]:
                if weaponsel[0] == party.partymembers[0].weapon:
                    scaledsurface.blit(pygame.transform.rotate(pygame.transform.scale_by(weaponsel[1],category[4]*fusedscale),category[5]),category[3])
        WINDOW.blit(scaledsurface)
        # Maybe I should clear the Terminal instead of replacing it for this usecase? Could work. Who knows. If it doesn't I'll just implement the old-fashioned solution.
        pygame.draw.rect(WINDOW,(45,45,45),(0 * scaleW,624 * scaleH, 959 * scaleW, 720 * scaleH))
        drawsurface = pygame.Surface((959 * scaleW, 128 * scaleH)).convert_alpha()
        drawsurface.fill((55,55,55))
        if self.doscroll == True:
            action, rect = self.scrollbar.draw(limitx=(0,960),limity=(710,710))
            self.scrollpos = - abs(rect[0] * ((len(self.btnlst) * 128 - 960) / (960 - self.scrollbar.rect.width)))
            # Because I'll forget this: the calculations we're doing here are:
            #   1. (getting the amount of distance that we need to cover / the amount of space that we have to scroll)
            #   2. rect's x pos * 1's result
            #   3. abs(2's result) so we get a positive float
            #   4. -3's result because we really needed it negative but the abs makes sure we don't end up with a positive number where we wanted a negative
            # A bug could happen, resulting in a ZeroDivisionError, if self.scrollbar.rect.width == 960; but hopefully that doesn't happen.
        for i in range(len(self.btnlst)):
            self.btnlst[i].rect.x = (i * 128 + self.scrollpos) * scaleW
            if self.btnlst[i].draw(0,0,drawsurface,0*scaleW,592*scaleH) == True:
                pygame.mixer.Sound.play(Sounds.listscrollsfx)
                self.activebadge = i
                self.textobj.textlist = []
                self.textobj.add(badgetable[i][2])
        if self.activebadge != -1:
            pygame.draw.rect(WINDOW,(55,55,55),(960 * scaleW,0 * scaleH,360 * scaleW,720 * scaleH))
            pygame.draw.rect(WINDOW,(255,255,255), pygame.Rect(960 * scaleH,0 * scaleW,1 * scaleH,720 * scaleW))
            WINDOW.blit(font.render(badgetable[self.activebadge][0],True,(255,255,255)),(970*scaleW,4*scaleH))
            pygame.draw.line(WINDOW,(255,255,255),(970*scaleW,32*scaleH),(1270*scaleW,32*scaleH))
            WINDOW.blit(self.textobj.draw(),(970*scaleW,36*scaleH))
            pygame.draw.line(WINDOW,(255,255,255),(970*scaleW,(self.textobj.lastsize[1] + 38)*scaleH),(1270*scaleW,(self.textobj.lastsize[1] + 38)*scaleH))
            if self.buybtn.draw():
                if party.partymembers[0].gold >= badgetable[self.activebadge][4]:
                    party.partymembers[0].gold -= badgetable[self.activebadge][4]
                    if party.badgedict.get(badgetable[self.activebadge][0]) == None:
                        party.badgedict.update({badgetable[self.activebadge][0]:0})
                    party.badgedict[badgetable[self.activebadge][0]] += 1
                    TerminalObj.add("Bought the " + badgetable[self.activebadge][0] + ".")
                    TerminalObj.add("You have " + str(party.badgedict[badgetable[self.activebadge][0]]) + ".")
                    pygame.mixer.Sound.play(Sounds.selectsfx)
                    self.__init__()
                    pygame.mixer.Sound.play(Sounds.purchase[random.randint(0,1)])
                else:
                    self.activebadge = -1
                    TerminalObj.add("Not enough gold.")
                    pygame.mixer.Sound.play(Sounds.deniedsfx)
            # Rendering badge effect descriptions.
            text = badgetable[self.activebadge][7]
            self.desctextobj.textlist = [] # this is probably the worst fucking way to do this but new additions are new additions
            self.desctextobj.add(text)
            # Rendering the stats.
            statsrendered = 0
            i = 0 # it's a bit late at night when i'm coding this; we doing this this way
                    # i = current stat we're at
                    # j = index in PlayerBadgeStats; which shouldn't excede 1 and due to this is useable to check mainPlayer.Badges
            WINDOW.blit(self.desctextobj.draw(),(968,(self.textobj.lastsize[1] + 40) * scaleH))
            dtext = self.desctextobj.lastsize[1] + self.textobj.lastsize[1] - 32
            for stat in badgetable[self.activebadge][5]:
                if stat != 0:
                    for j in range(len(self.PlayerBadgeStats)):
                        WINDOW.blit(Icons.stats[i],(968 + j * 128,(90 + dtext + statsrendered * 32) * scaleH))
                        statText = font.render(str(stat),True,(255,255,255))
                        WINDOW.blit(statText,(986 + j * 128,(84 + dtext + statsrendered * 32) * scaleH)) # NOTE: altered this a bit, get it into armortable
                        statTextRect = statText.get_rect()
                        try:
                            if stat > self.PlayerBadgeStats[j][i]:
                                WINDOW.blit(Icons.stats[6],((statTextRect.bottomright[0] + 996 + j * 128) * scaleW,(90 + dtext + statsrendered * 32) * scaleH))
                            elif stat < self.PlayerBadgeStats[j][i]:
                                WINDOW.blit(Icons.stats[7],((statTextRect.bottomright[0] + 996 + j * 128) * scaleW,(90 + dtext + statsrendered * 32) * scaleH))
                        except Exception:
                            # same as the exception with the badges
                            WINDOW.blit(Icons.stats[6],((statTextRect.bottomright[0] + 996 + j * 128) * scaleW,(90 + dtext + statsrendered * 32) * scaleH))
                    statsrendered += 1
                i += 1
            i = 0
            for badge in party.partymembers[0].badges:
                if badge != "None" and badgetable[self.activebadge][5] != (0,0,0,0,0,0):
                    WINDOW.blit(smallboldfont.render(badge,True,(255,255,255)), ((968 + i * 128) * scaleW, (dtext + 80 + statsrendered * 32) * scaleH))
                i += 1
            WINDOW.blit(font.render("Price: " + str(badgetable[self.activebadge][4]),True,(255,255,255)),(984*scaleW, 522*scaleH))
            WINDOW.blit(font.render("Your Nuggets: " + str(party.partymembers[0].gold),True,(255,255,255)),(984*scaleW, 546*scaleH))
        WINDOW.blit(drawsurface,(0*scaleW,592*scaleH))
        if self.backbtn.draw() is True:
            return False
        pygame.draw.rect(WINDOW,(255,255,255),(self.scrollbar.rect))  # TODO: add transparency to this
            

BadgeShopItem = BadgeShop()

class Shop:
    # remaking this whole thing
    def __init__(self,objs = [0]):
        # You're meant to feed a list of ints into objs. Those ints correspond to objects in the itemtable.
        self.objs = objs
        self.btns = []
        j = 0
        itembtnimg = pygame.transform.scale_by(pygame.image.load("assets/shop/items/shopbutton.png").convert_alpha(),0.875)
        for i in range(len(self.objs)):
            surf = pygame.surface.Surface((120,120)).convert_alpha()
            surf.fill((0,0,0,0))
            surf.blit(itembtnimg,(4,4))
            surf.blit(pygame.transform.scale_by(itemtable[i][5],0.8),(12,12))
            self.btns.append(Button(970 + (5 + 40 * (i % 2) + (i % 2) * 128),j*128 + 10,surf))
            if i % 2:
                j += 1
        self.active = -1
        self.bg = pygame.image.load("assets/notebookpaper.png").convert_alpha()
        self.buybtn = Button(730,600,pygame.image.load("assets/shop_buybtn.png").convert_alpha(),scaleH/1.2,scaleW/1.2)
        self.buying = False
        self.amount = 0
        self.scrolling = False
        if int(len(self.btns) / 2) * 138 > 960:
            self.scrolling = True
            scrollsurface = pygame.surface.Surface((10,math.log(120 * int(len(self.btns) / 2)) * 72)).convert_alpha()
            scrollsurface.fill((255,255,255))
            self.scrollbar = Dragable(1270,0,scrollsurface)
        self.scrollpos = 0
        btnimg = pygame.Surface((96 * scaleW,32 * scaleH)).convert_alpha()
        btnimg.fill((0,0,0,0))
        pygame.draw.rect(btnimg,(255,255,255),(0 * scaleW,0 * scaleH,72 * scaleW,32 * scaleH))
        pygame.draw.polygon(btnimg,(255,255,255),[(72 * scaleW,0 * scaleH),(72 * scaleW,32 * scaleH),(96 * scaleW,32 * scaleH)])
        btnimg.blit(font.render("Back",True,(0,0,0)),(4 * scaleW,4 * scaleH))
        self.backbtn = Button(960*scaleW,688*scaleH,btnimg)
        self.textobj = TextEng()
        self.inputstr = "" # there 300% is a better way to do this
    def draw(self):
        WINDOW.blit(self.bg)
        pygame.draw.rect(WINDOW,(55,55,55),(960 * scaleW,0 * scaleH,360 * scaleW,720 * scaleH))
        pygame.draw.rect(WINDOW,(255,255,255), pygame.Rect(960 * scaleH,0 * scaleW,1 * scaleH,720 * scaleW))
        for i in range(len(self.btns)):
            bckupy = self.btns[i].rect[1]
            self.btns[i].rect[1] -= self.scrollpos
            if self.btns[i].draw():
                self.active = i
                self.buying = False
                self.amount = 0
            self.btns[i].rect[1] = bckupy
            # this is messy and bad
        if self.scrolling:
            action, rect = self.scrollbar.draw(limitx=(1270,1270), limity=(0,720))
            self.scrollpos = rect[1] / (960 / (round(len(self.btns) / 2) * 138))**2 * (960 / self.scrollbar.rect.height)
        if self.active > -1:
            self.textobj.textlist = []
            tempitemimg = itemtable[self.active][1]
            surface = tempitemimg.convert_alpha()
            del tempitemimg # not useful anymore
            surface.fill((0,0,0,0),special_flags=BLEND_RGBA_MAX)
            surface.fill((0,0,0,120),special_flags=BLEND_RGBA_MIN)  # this is from stack overflow. don't know how blend modes go so idk how this works :p
            WINDOW.blit(surface,(240,260))                          # also for some reason when i was implementing this this'd break trememdously without using a secondary var so WELP THERE IT IS NOW
            WINDOW.blit(itemtable[self.active][1],(250,250))
            pygame.draw.rect(WINDOW,(55,55,55),(720,0,240,720))
            pygame.draw.rect(WINDOW,(255,255,255), pygame.Rect(720 * scaleH,0 * scaleW,1 * scaleH,720 * scaleW))
            WINDOW.blit(font.render("Nuggets: " + (str(party.partymembers[0].gold)),True,(255,255,255)),(730,570))
            if not self.buying:
                self.textobj.add("[B]"+itemtable[self.active][0],space=(220,700))
                pygame.draw.line(WINDOW,(255,255,255),(730,self.textobj.lastsize[1] + 36),(950,self.textobj.lastsize[1] + 36))
                offset = self.textobj.lastsize[1] + 36
                # TODO: make a scrollable surface of some kind and apply it to all texts i can apply it to
                self.textobj.add("[NL][N]"+itemtable[self.active][2],space=(220,700))
                try:
                    self.textobj.add("In inventory: " + str(party.partymembers[0].items[self.active]),space=(220,700))
                except Exception:
                    self.textobj.add("ITEM DOES NOT EXIST IN PLAYER INVENTORY SYSTEM.",space=(220,700))
                if self.buybtn.draw():
                    self.buying = True
                WINDOW.blit(self.textobj.draw((220,700)),(730,10))
            else:
                self.textobj.textlist = []
                self.textobj.add("How many "+ itemtable[self.active][0] + "s do you want to buy?",space=(220,700))
                self.textobj.add("Price: ("+ str(itemtable[self.active][4]) + " Nuggets per unit) * " + str(self.amount) + " units: " + str(itemtable[self.active][4] * self.amount),space=(220,700))
                WINDOW.blit(self.textobj.draw((220,700)),(730,10))
                offset = self.textobj.lastsize[1] + 36
                if round(Game.time_since_start/3,1) % 2 == 0:
                    if self.inputstr == "_":
                        self.inputstr = ""
                    else:
                        self.inputstr = "_"
                WINDOW.blit(font.render("Amount: "+str(self.amount)+self.inputstr,True,(255,255,255)),(730*scaleH,(offset + 10)*scaleW))
                offset += 36
                # god i'm breaking so many things i may just readd textparser and the such until future PTBs
                # thing is that'd suck for mods so... :/ the things i do so for y'all (and mainly for myself >:3)
                # TODO: MAKE THE FACT THAT YOU ARE SUPPOSED TO BE INPUTTING TEXT HERE OBVIOUS >:C
                pygame.draw.line(WINDOW,(255,255,255),(730,offset),(950,offset))
                if self.buybtn.draw():
                    if party.partymembers[0].gold >= int(itemtable[self.active][4] * self.amount):
                        self.buying = False
                        TerminalObj.add("Bought "+str(self.amount) + " " + itemtable[self.active][0] + "s.")
                        party.partymembers[0].items[self.active] += self.amount
                        party.partymembers[0].gold -= itemtable[self.active][4] * self.amount
                        self.amount = 0
                        pygame.mixer.Sound.play(Sounds.purchase[random.randint(0,1)])
                    else:
                        self.buying = False
                        TerminalObj.add("Not enough gold.")
                        self.amount = 0
                        pygame.mixer.Sound.play(Sounds.deniedsfx)
                for event in Game.eventqueue:
                    if event.type == KEYDOWN:
                        if event.unicode.isdigit():
                            if len(str(self.amount)) < 10:
                                amount = str(self.amount)
                                amount += event.unicode
                                self.amount = int(amount)
                            else:
                                pygame.mixer.Sound.play(Sounds.deniedsfx)
                    elif event.type == KEYUP and event.key == K_BACKSPACE:
                        if self.amount > 0:
                            try:
                                self.amount = int(str(self.amount)[:-1])
                            except ValueError:
                                self.amount = 0
                        else:
                            pygame.mixer.Sound.play(Sounds.deniedsfx)
        if self.backbtn.draw() is True:
            pygame.mixer.Sound.play(Sounds.selectsfx)
            self.__init__(self.objs)
            return False  

WINDOW.blit(smallboldfont.render("shop modules ready",True,(255,255,255)),(0,60))
pygame.display.update()

class DialogueBox():
    # Creates a dialogue box on screen. Can be set to timeout after some time or require a spacebar press with the "trigger" parameter.
    # for trigger: True is Spacebar, False is timeout; timeout is in some value i gotta fix
    # TODO: fix timeout
    # TODO: also fix this up a little i mean it works but GOD is it ugly :(
    def __init__(self,dialogue="",charportrait="assets/urpg-guy.png",iconcharportrait="assets/gameicon.png",type="basic",timeout=60,expression="neutral",character="unknown",linkto=[],velocity=20,soundfile=Sounds.listscrollsfx,termdraw=True):
        self.charportrait = pygame.image.load(charportrait).convert_alpha()
        self.charportraitrect = self.charportrait.get_rect()
        self.iconcharportrait = iconcharportrait # we're not using it for now
        self.active = True
        self.type = type
        self.timeout = timeout * Game.dt
        self.choice = False
        self.linkto = linkto
        self.expression = expression
        self.character = character
        self.velocity = velocity
        self.dialogue = dialogue
        self.textobj = TextEng()
        self.textobj.add(dialogue,space=(960 - (self.charportraitrect.copy().width + 40), 180))
        self.diagqueue = self.textobj.textlist # wait a sec i got a neat party trick
        self.timer = 0
        self.currentline = 0
        self.talktimer = 0
        self.soundfile = soundfile
        self.termdraw = termdraw
    def draw(self):
        self.timer -= self.velocity * Game.dt
        self.talktimer -= 1 * Game.dt
        if self.active:
            if self.termdraw == True:
                WINDOW.blit(TerminalObj.draw(decopos=(10,10)),(960,0))
            if self.timeout > 0:
                self.timeout -= 1 * Game.dt
            pygame.draw.rect(WINDOW,(55,55,55),(10,530,940,180))
            pygame.draw.rect(WINDOW,(255,255,255),(12,532,936,176))
            pygame.draw.rect(WINDOW,(55,55,55),(15,535,930,170))
            WINDOW.blit(self.charportrait,(20,535-self.charportraitrect.height / 3))
            if self.type == "select":
                pygame.draw.rect(WINDOW,(55,55,55),(960 * scaleW,0 * scaleH,360 * scaleW,720 * scaleH))
                pygame.draw.rect(WINDOW,(255,255,255), pygame.Rect(960 * scaleH,0 * scaleW,1 * scaleH,720 * scaleW))
                i = 0
                for link in self.linkto:
                    WINDOW.blit(font.render("[" + str(i + 1) + "] " + link,True,(255,255,255)),(970,10 + i * 24))
                    i += 1
            for event in Game.eventqueue:
                if self.type == "select":
                    if event.type == KEYDOWN and event.unicode.isdigit():   # Copied from StackOverflow, once again.
                        try:
                            self.choice = self.linkto[int(event.unicode) - 1]
                            self.active = False
                            pygame.mixer.Sound.play(Sounds.selectsfx)
                        except Exception:
                            pass
                else:
                    if event.type == KEYDOWN and event.key == K_SPACE or self.type == "timed" and self.timeout <= 0:
                        self.active = False
                        pygame.mixer.Sound.play(Sounds.listscrollsfx)
        WINDOW.blit(self.textobj.draw(space=(960 - (self.charportraitrect.copy().width + 40), 180)),(30 + self.charportraitrect.copy().width,540))
        return (self.active,self.choice,self.expression,self.character)

class DialogueTree():
    # Basic dialogue tree system.
    # TODO: Add branching paths, options, etc. Fix up everything.
    def __init__(self,dialogboxes=list()):
        self.dialogueboxes = []
        self.dialoguepaths = {}
        for dialogbox in dialogboxes:
            self.dialogueboxes.append(DialogueBox(dialogbox[0],dialogbox[1],dialogbox[2],dialogbox[3]))
        self.current = 0
        self.active = True
        self.hasreported = False
        self.textobj = TextEng()
    def draw(self):
        self.textobj.textlist = []
        if self.hasreported == False:
            self.textobj.add("[N]" + self.dialogueboxes[self.current].dialogue,space=(276,700),noNL=True) # this is stupid
            for i in range(len(self.textobj.textlist)):
                if line[0] == "NL":
                    continue
                else:
                    if i == 0:
                        self.textobj.textlist.insert(0,["IMG",str(self.dialogueboxes[self.current].iconcharportrait),""])
                        self.textobj.imagedict.update({str(self.dialogueboxes[self.current].iconcharportrait):pygame.image.load(str(self.dialogueboxes[self.current].iconcharportrait)).convert_alpha()})
                    elif i != 1:
                        if self.textobj.textlist[i][2] != "":
                            self.textobj.textlist[i][2] = ";" + self.textobj.textlist[i][2]
                        self.textobj.textlist[i][2] = "s=24" + self.textobj.textlist[i][2]
            i +=1
            if i > 1:
                if self.textobj.textlist[i][2] != "":
                    self.textobj.textlist[i][2] = ";" + self.textobj.textlist[i][2]
                self.textobj.textlist[i][2] = "s=24" + self.textobj.textlist[i][2]
            print(self.textobj.textlist)
            TerminalObj.textlist.extend(self.textobj.textlist) # i really shouldn't be doing this but yolo
            TerminalObj.add("[NL]",noNL=True)
            TerminalObj.imagedict = TerminalObj.imagedict.copy() | self.textobj.imagedict
            self.hasreported = True
        if self.active:
            dialoguestatus = self.dialogueboxes[self.current].draw()
            if not dialoguestatus[0] and not dialoguestatus[1]:
                self.current += 1
                self.hasreported = False
            elif not dialoguestatus[0] and dialoguestatus[1]:
                self.dialogueboxes = []
                for box in self.dialoguepaths[dialoguestatus[1]]:
                    if not isinstance(box, str):
                        if box['type'] != 'select':
                            self.dialogueboxes.append(DialogueBox(TextFixer(box['diag']),self.chars[box['char']]['filepath']+self.chars[box['char']]['expressions'][box['expression']],self.chars[box['char']]['filepath']+self.chars[box['char']]['iconexpressions'][box['expression']],box['type'],box['timeout'],box['expression'],box['char'],soundfile=self.chars[box['char']]['soundfile']))
                        else:
                            self.dialogueboxes.append(DialogueBox(TextFixer(box['diag']),self.chars[box['char']]['filepath']+self.chars[box['char']]['expressions'][box['expression']],self.chars[box['char']]['filepath']+self.chars[box['char']]['iconexpressions'][box['expression']],box['type'],box['timeout'],box['expression'],box['char'],box['linkto'],soundfile=self.chars[box['char']]['soundfile']))
                self.current = 0
                self.hasreported = False
            if self.current >= len(self.dialogueboxes):
                self.active = False
                self.current = 0
        else:
            self.current = 0
        return self.active, dialoguestatus[2], dialoguestatus[3]
    def loadfromjson(self,path):
        decoding = json
        self.chars = {}
        self.dialogueboxes = []
        self.dialoguepaths = {}
        decoding = json.load(fp=open(path))
        if decoding['type'] != "URPGDiag":
            print("this isn\'t a dialogue file")
            return(False, "", "")
        self.chars = decoding['chars']
        for char in self.chars:
            self.chars[char].update({'loadedexpressions':[]})
            self.chars[char].update({'loadediconexpressions':[]})
            self.chars[char].update({'soundfile':pygame.mixer.Sound(self.chars[char]['filepath']+self.chars[char]['soundfile'])})
            for expression in self.chars[char]['expressions']:
                self.chars[char]['loadedexpressions'].append(self.chars[char]['filepath']+self.chars[char]['expressions'][expression]) # Currently useless. TODO: find a way to make this work; should optimize a bit
            for iconexpression in self.chars[char]['iconexpressions']:
                self.chars[char]['loadediconexpressions'].append(self.chars[char]['filepath']+self.chars[char]['iconexpressions'][expression]) # Currently useless. TODO: find a way to make this work; should optimize a bit
        self.dialoguepaths = decoding['dialogue']
        for box in self.dialoguepaths['init']:
            if box['type'] != 'select':
                self.dialogueboxes.append(DialogueBox(TextFixer(box['diag']),self.chars[box['char']]['filepath']+self.chars[box['char']]['expressions'][box['expression']],self.chars[box['char']]['filepath']+self.chars[box['char']]['iconexpressions'][box['expression']],box['type'],box['timeout'],box['expression'],box['char'],soundfile=self.chars[box['char']]['soundfile']))
            else:
                self.dialogueboxes.append(DialogueBox(TextFixer(box['diag']),self.chars[box['char']]['filepath']+self.chars[box['char']]['expressions'][box['expression']],self.chars[box['char']]['filepath']+self.chars[box['char']]['iconexpressions'][box['expression']],box['type'],box['timeout'],box['expression'],box['char'],box['linkto'],soundfile=self.chars[box['char']]['soundfile']))
        self.active = False
        self.current = 0
        self.hasreported = False

class ShopLinker():
    def __init__(self,diagoptions = ["Items","Weapons","Armors","Badges","Talk"],linkto=[Shop(range(len(itemtable))),WeaponShop(),ArmorShop(),BadgeShop(),DialogueTree()],dialogue="assets/definitions/dialogue/example.json"):
        self.items = [Animated().import_from_folder("assets/shop/general/healpot/",changes=[[0,1],[5,1]]),
                    Animated([pygame.image.load("assets/shop/general/effectclear/ef.png").convert_alpha()],1)]
        self.background = Animated().import_from_folder("/assets/shop/general/background/",regex=r"\Abg")
        self.idleanim = Animated().import_from_folder("/assets/shop/general/shopkeep/",regex=r"\Aidle1_")
        self.idletimer = random.randint(8,19)
        self.idling = False
        # NOTE: in the future this above approach probably shouldn't be done but here I go doing it AGAIN
        # TODO: ALSO i should probably separate static unanimated parts from the animated ones to reduce RAM cost
        self.counter = pygame.image.load("assets/shop/general/background/counter.png")
        self.diagoptions = diagoptions
        self.linkto = linkto
        self.diagoptions.append("Save")
        self.diagoptions.append("Exit")
        self.linkto.append("Save")
        self.linkto.append("Exit")
        self.dialogue = dialogue # TODO: probably make it so this goes better because this kinda sucks rn
        for i in range(len(self.linkto)):
            if isinstance(self.linkto[i],DialogueTree):
                self.linkto[i].loadfromjson(dialogue)
        self.state = -1
        self.lastvalue = ""
        self.lastchar = ""
    def draw(self):
        if self.state == -1 or isinstance(self.linkto[self.state],DialogueTree):
            WINDOW.blit(self.background.draw())
            WINDOW.blit(self.items[0].draw(),(820*scaleW,-10*scaleH))
            if self.lastvalue == "Neutral" and self.lastchar == "Shopkeeper":
                WINDOW.blit(pygame.image.load("assets/shop/general/shopkeep/idle1_1.png").convert_alpha())
            elif self.lastvalue == "Unamused" and self.lastchar == "Shopkeeper":
                WINDOW.blit(pygame.image.load("assets/shop/general/shopkeep/unamused.png").convert_alpha())
            else:
                WINDOW.blit(self.idleanim.frames[0][0])
            WINDOW.blit(self.counter)
            pygame.draw.rect(WINDOW,(55,55,55),(960 * scaleW,0 * scaleH,360 * scaleW,720 * scaleH))
            pygame.draw.rect(WINDOW,(255,255,255), pygame.Rect(960 * scaleH,0 * scaleW,1 * scaleH,720 * scaleW))
            if isinstance(self.linkto[self.state],DialogueTree):
                dg = self.linkto[self.state].draw()
                if not dg[0]:
                    self.state = -1
                    self.lastvalue = ""
                    self.lastchar = ""
                else:
                    self.lastvalue = dg[1]
                    self.lastchar = dg[2]
            else:
                for i in range(len(self.diagoptions)):
                    text = font.render("["+str(i + 1)+"] "+self.diagoptions[i],True,(255,255,255),None)
                    WINDOW.blit(text, (970, i * 24 + 10))
                for event in Game.eventqueue:
                    if event.type == KEYDOWN and event.unicode.isdigit():   # Copied from StackOverflow, once again.
                        if int(event.unicode) <= len(self.linkto):
                            pygame.mixer.Sound.play(Sounds.selectsfx)
                            self.state = int(event.unicode) - 1
                            if isinstance(self.linkto[self.state],DialogueTree):
                                self.linkto[self.state].loadfromjson(self.dialogue)
                                self.linkto[self.state].active = True
        else:
            #try: #NOTE: MARK THIS AGAIN
                if self.linkto[self.state] != "Save" and self.linkto[self.state] != "Exit":
                    if self.linkto[self.state].draw() == False:
                        self.state = -1
                elif self.linkto[self.state] == "Save":
                    party.save()
                    TerminalObj.add("GAME SAVED.")
                    pygame.mixer.Sound.play(Sounds.save)
                    self.state = -1
                    self.draw()
                elif self.linkto[self.state] == "Exit":
                    Game.state = "Rooms"
                    Game.substate = ""
                    pygame.mixer.music.fadeout(300)
                    TerminalObj.textlist = []
                    self.__init__(diagoptions=self.diagoptions[:-2],linkto=self.linkto[:-2],dialogue=self.dialogue)
            #except Exception:
                #self.state = -1 # Fallback.
        if pygame.mixer.music.get_busy() == False and Game.state == "Shop":
            if random.randint(1,100) > 66:
                pygame.mixer.music.load("ost/shopexci1.wav")
            elif random.randint(1,100) > 50:
                pygame.mixer.music.load("ost/shopexci2.wav")
            elif random.randint(1,100) > 33:
                pygame.mixer.music.load("ost/shopexci1.wav")
            else:
                pygame.mixer.music.load("ost/shopjes.wav")
            pygame.mixer.music.play(-1)

ShopLinkerObj = ShopLinker()

decosurf = pygame.Surface((320,720)).convert_alpha()
decosurf.fill((50,50,50))
pygame.draw.line(decosurf,(255,255,255),(0,0),(0,720))
TerminalObj = TextEng(decoration=decosurf)
del decosurf

class Inventory():
    def __init__(self):
        # this needs asthetic changes YESTERDAY
        self.activeitem = -1
        surface = pygame.Surface((72,30)).convert_alpha()
        surface.fill((0,0,0,0))
        surface.blit(font.render("> Use",True,(0,255,0)),(0*scaleH,0*scaleW))
        self.usebtn = Button(0,0,surface,scaleW,scaleH)
        del surface
        btnimg = pygame.Surface((96 * scaleW,40 * scaleH)).convert_alpha()
        btnimg.fill((0,0,0,0))
        pygame.draw.rect(btnimg,(255,255,255),(0 * scaleW,0 * scaleH,72 * scaleW,40 * scaleH))
        pygame.draw.polygon(btnimg,(255,255,255),[(72 * scaleW,0 * scaleH),(72 * scaleW,40 * scaleH),(96 * scaleW,40 * scaleH)])
        btnimg.blit(font.render("Back",True,(0,0,0)),(6 * scaleW,6 * scaleH))
        self.backbtn = Button(960*scaleW,680*scaleH,btnimg)
        self.textobj = TextEng()
        self.state = ""
        self.usebtns = []
    def draw(self):
        pygame.draw.rect(WINDOW,(0,0,0),(0 * scaleW,678 * scaleH,1280 * scaleW,720 * scaleH))
        pygame.draw.rect(WINDOW,(255,255,255),(0 * scaleW,680 * scaleH,1280 * scaleW,720 * scaleH))
        WINDOW.blit(font.render("Choose an Item!",True,(0,0,0)),(5 * scaleW,686 * scaleH))
        pygame.draw.rect(WINDOW,(55,55,55),(960 * scaleW,0 * scaleH,360 * scaleW,720 * scaleH))
        pygame.draw.rect(WINDOW,(255,255,255), pygame.Rect(960 * scaleH,0 * scaleW,1 * scaleH,720 * scaleW))    # this is just here so the terminal's hidden, once again
        if self.backbtn.draw():
            if self.state == "selecting":
                self.state = ""
            else:
                Game.substate = ""
        if self.activeitem >= 0:
            self.textobj.textlist = []
            self.textobj.add(itemtable[self.activeitem][2])
        itemoffset = 0
        rendered = 0
        if self.state == "":
            for i in range(len(itemtable)):
                if party.partymembers[0].items[i] > 0:
                    if i == self.activeitem:
                        itemtxtrndr = self.textobj.draw(space=(300,len(self.textobj.textlist) * 24)) # fuck fuck fuck this will break so many things for mods :sob: but i gotta do it to finish this on time
                        textRect = itemtxtrndr.get_rect()
                        textY = textRect.bottomright[1]
                        itemoffset += textY + 32
                        itemsurface = pygame.Surface((319,32 + itemoffset)).convert_alpha()
                        itemsurface.fill((0,0,0,0))
                        pygame.draw.line(itemsurface,(0,0,0),(0,32 + itemoffset - 1),(319,32+itemoffset - 1))
                        itemsurface.blit(pygame.transform.scale_by(itemtable[i][5],0.2 * scaleH),(2,4))
                        itemname = font.render(itemtable[i][0],True,(255,255,255))
                        itemsurface.blit(itemname,(30,4))
                        itemsurface.blit(itemtxtrndr,(2,32))
                        itembtn = Button(960 + 2,rendered * 32,itemsurface,scaleW,scaleH)
                        self.usebtn.rect.topleft = (962 * scaleW,(rendered * 32 + itemoffset) * scaleH)
                        if self.usebtn.draw():
                            self.state = "selecting"
                        WINDOW.blit(font.render("You have: x" + str(party.partymembers[0].items[i]),True,(255,255,255)),(1035 * scaleW,(rendered * 32 + itemoffset) * scaleH))
                        pygame.draw.line(WINDOW,(255,255,255),(962 * scaleW,(rendered * 32 + 28) * scaleH),((itemname.get_rect().bottomright[0] + 990) * scaleW,(rendered * 32 + 28) * scaleH))
                    else:
                        itemsurface = pygame.Surface((319*scaleW,32*scaleH)).convert_alpha()
                        itemsurface.fill((0,0,0,0))
                        print(itemtable)
                        itemsurface.blit(pygame.transform.scale_by(itemtable[i][5],0.2 * scaleW),(4*scaleW,4*scaleH))
                        itemsurface.blit(font.render(itemtable[i][0],True,(255,255,255)),(32*scaleW,4*scaleH))
                        itembtn = Button(960*scaleW,(rendered * 32 + itemoffset)*scaleH,itemsurface,scaleW,scaleH)
                    if itembtn.draw():
                        self.activeitem = i
                    rendered += 1
        elif self.state == "selecting":
            if self.usebtns == []:
                self.usebtns = [self.usebtn.copy() for i in range(party.membercount)]
            for i in range(len(self.usebtns)):
                self.usebtns[i].rect.topleft = (1210,10+i*24)
                WINDOW.blit(party.partymembers[i].hpimage,(970,10+i*24))
                WINDOW.blit(font.render(party.partymembers[i].name,True,(255,255,255)),(970+24,10+i*24))
                if self.usebtns[i].draw() == True:
                    self.usebtns = []
                    affected = party.partymembers[i]
                    exec(itemtable[self.activeitem][3])
                    party.partymembers[0].items[self.activeitem] -= 1
                    party.partymembers[i] = affected
                    Game.substate = ""
                    self.state = ""
                    TerminalObj.add(party.partymembers[i].name + " used 1 " + str(itemtable[self.activeitem][0])+ ".")
                    break
        
InvObj = Inventory()

# Assets - or my attempts at loading them
# NOTE: DEPRECATE DEPRECATE DEPRECATE OH GOD WHAT IS THIS
atkbtnimg = pygame.image.load("assets/resized_atk.png").convert_alpha()
defbtnimg = pygame.image.load("assets/resized_def.png").convert_alpha()
spcbtnimg = pygame.image.load("assets/resized_special.png").convert_alpha()
itmbtnimg = pygame.image.load("assets/resized_item.png").convert_alpha()


files = []
path = "assets/definitions/battle/effects/" # This is done this way to make my life easier in case I change how assets are organized later on.
for (dirpath,dirnames,filenames) in os.walk(path): # thanks StackOverflow
    files.extend(filenames)

effectdict = {}

for file in files:
    try:
        if effectdict.get(file.split(".")[0]) == None:
            effectdict.update({file.split(".")[0]:[Game.errorSurf,""]})
        if file.endswith(".png"):
            effectdict[file.split(".")[0]][0] = pygame.image.load(path + file).convert_alpha()
        elif file.endswith(".txt"):
            effectdict[file.split(".")[0]][1] = str(open(path + file, encoding='utf-8').read())
    except FileNotFoundError:
        raise FileNotFoundError("File at " + path + file + " was deleted, but it was detected at the moment of scanning files.")

WINDOW.blit(smallboldfont.render("UI ready",True,(255,255,255)),(0,72))
pygame.display.update()

# TODO: move any timing presses to some sort of async always running thing so timings aren't limited to 60fps and they're more consistent
# this is mostly here because it's the closest place i had to place this while making enemy stats

# Classes, variables and all of the sauce
# The term "class" may be used a bit liberally here though

def maximum_common_divisor(a, b):            # stolen outta the internet, as usual
    if b == 0:
        return a
    return maximum_common_divisor(b, a % b)

maag = False # maag: the return

class Enemy():
    def __init__(self,name=None):
        if len(enemytable) > 0:
            index = 0
            if name == None:
                index = random.randint(0,len(enemytable) - 1)
            else:
                for i in range(len(enemytable)):
                    if enemytable[i][0] == name:
                        index = i
            try:
                self.name,self.kind,self.animations,self.icon,self.moves,self.stats,self.translations = enemytable[index]
            except IndexError:
                raise Exception("DBG: here's the culprit my man",enemytable[index])
            loadedanims = {}
            for key in self.animations:
                loadedanims.update({key:pygame.image.load(self.animations[key]).convert_alpha()})
            self.icon = pygame.image.load(self.icon).convert_alpha()
            self.animations = loadedanims # i think i have to do it this way or i get a RuntimeError
            self.effects = []
            self.hp = self.stats[0]
            self.gold = random.randint(self.stats[2][0],self.stats[2][1])
        else:
            raise Exception("there\'s no enemies in the enemytable; go add at least one and restart the game. the enemytable looks like this: ", enemytable)
        
# Button class that I borrowed outta the Internet

# and here are the buttons

atkbtn = Button(0 * scaleW,520 * scaleH,atkbtnimg,scaleW,scaleH)
spcbtn = Button(240 * scaleW,520 * scaleH,spcbtnimg,scaleW,scaleH)
defbtn = Button(480 * scaleW,520 * scaleH,defbtnimg,scaleW,scaleH)
itmbtn = Button(720 * scaleW,520 * scaleH,itmbtnimg,scaleW,scaleH)

class MenuLoad:
    blackbar = pygame.image.load('assets/blacktribar.png').convert_alpha()
    whitebar = pygame.image.load('assets/whitetribar.png').convert_alpha()
    urpglogo = pygame.image.load('assets/urpglogo.png').convert_alpha()
    bgmenuimg = pygame.image.load('assets/INTERNALmenuimg.png').convert_alpha()
    blackbarh = blackbar.get_size()
    whitebarh = whitebar.get_size()
    urpglogoh = urpglogo.get_size()
    bgmenuimgh = bgmenuimg.get_size()
    blackbar = pygame.transform.scale(blackbar,(blackbarh[0] * scaleW, blackbarh[1] * scaleH)).convert_alpha()
    whitebar = pygame.transform.scale(whitebar,(whitebarh[0] * scaleW, whitebarh[1] * scaleH)).convert_alpha()
    urpglogo = pygame.transform.scale(urpglogo,(urpglogoh[0] * scaleW, urpglogoh[1] * scaleH)).convert_alpha()
    bgmenuimg = pygame.transform.scale(bgmenuimg,(bgmenuimgh[0] * scaleW, bgmenuimgh[1] * scaleH)).convert_alpha()
    print(FULLSCREENSWITCH)
    if FULLSCREENSWITCH is False:
        pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
    elif FULLSCREENSWITCH is True:
        pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT), pygame.FULLSCREEN)

MENUCYCLEEVENT = pygame.event.custom_type()
pygame.time.set_timer(MENUCYCLEEVENT, 32,-1)

class Particle():
    # NOTE: this system is not done yet. finish it later.
    def __init__(self,image,type = "Standard",hardcodedx = 0,hardcodedy = 0):
        self.tickspassed = 0
        self.type = type
        self.image = pygame.image.load(image).convert_alpha()
        self.backupimage = pygame.image.load(image).convert_alpha()
        if self.type.__contains__("VariedScale"):
            randomscale = random.randint(1,20)
            self.scale = randomscale / 10
            resuprect = self.backupimage.get_size()
            imgsize = self.image.get_size()
            self.image = pygame.transform.scale(self.image,(imgsize[0] * self.scale * scaleH, imgsize[1] * self.scale * scaleW))
            self.backupimage = pygame.transform.scale(self.image,(self.scale * resuprect[0] * scaleH, self.scale * resuprect[1] * scaleW))
        self.x = 0
        self.xoffset = 0
        self.y = 0
        self.yoffset = 0
        if type.startswith("Rotating"): 
            self.rotation = 0
        if hardcodedx != 0 or hardcodedy != 0:
            if hardcodedx == 0:
                if self.type.__contains__("LefttoRight"):
                    self.x = -10 - self.image.get_rect()[0]
                elif self.type.__contains__("RighttoLeft"):
                    self.x = 1290 + self.image.get_rect()[0]
            else:
                self.x = hardcodedx
            if hardcodedy == 0:
                if self.type.__contains__("UptoDown"):
                    self.y = -10 - self.image.get_rect()[0]
                elif self.type.__contains__("DowntoUp"):
                    self.y = 1290 + self.image.get_rect()[0]
            else:
                self.y = hardcodedy
        else:
            if hardcodedx != 0:
                if self.type.__contains__("LefttoRight"):
                    self.x = -10 - self.image.get_rect()[0]
                elif self.type.__contains__("RighttoLeft"):
                    self.x = 1290 + self.image.get_rect()[0]
            else:
                self.x = random.randint(1,1279)
            if hardcodedy != 0:
                if self.type.__contains__("UptoDown"):
                    self.y = -10 - self.image.get_rect()[1]
                elif self.type.__contains__("DowntoUp"):
                    self.y = 730 + self.image.get_rect()[1]
            else:
                self.y = random.randint(1,519)
        if type.__contains__("VariedX"):
            try:
                self.x += random.randint(0,1280)
            except Exception:
                self.x += random.randint(1290,2570)
            self.xoffset += self.x
        if type.__contains__("VariedY"):
            try:
                self.y += random.randint(0,720)
            except Exception:
                self.y += random.randint(730,1450)
            self.yoffset += self.y
    
    def draw(self):
        if self.type.startswith("Rotating"):
            if self.tickspassed <= 5:
                self.tickspassed = 0
                self.image = pygame.transform.rotate(self.backupimage,self.rotation)
                self.rotation += 1 * Game.dt
                if self.rotation == 360:
                    self.rotation = 0
            else:
                self.tickspassed += 1 * Game.dt
        if self.type.__contains__("LefttoRight"):
            self.x += 1 * Game.dt
        elif self.type.__contains__("RighttoLeft"):
            self.x -= 1 * Game.dt
        if self.type.__contains__("UptoDown"):
            self.y += 1 * Game.dt
        elif self.type.__contains__("DowntoUp"):
            self.y -= 1 * Game.dt
        WINDOW.blit(self.image,(self.x * scaleW,self.y * scaleH))
        
def ParticleSpawner(image,type,x,y,amount,currentparticlelist = []):
    if isinstance(currentparticlelist,list) is True:
        if len(currentparticlelist) != amount:
            currentparticlelist.append(Particle(image,type,x,y))
        else:
            pass

nuggetsprite_normal = pygame.image.load("assets/nuggets.png").convert_alpha()
nuggetsprite_gold = pygame.image.load("assets/goldnuggets.png").convert_alpha()

for i in range(len(itemtable)):
    imager = itemtable[i][1].get_size()
    itemtable[i][1] = pygame.transform.scale(itemtable[i][1],(imager[0] * scaleW, imager[1] * scaleH))

nuggetsprite_normal = pygame.transform.scale(nuggetsprite_normal,(nuggetsprite_normal.get_size()[0] * scaleW, nuggetsprite_normal.get_size()[1] * scaleH))
nuggetsprite_gold = pygame.transform.scale(nuggetsprite_gold,(nuggetsprite_gold.get_size()[0] * scaleW, nuggetsprite_gold.get_size()[1] * scaleH))

WINDOW.blit(smallboldfont.render("battle system and various misloaded assets ready",True,(255,255,255)),(0,84))
pygame.display.update()


def maketimer(ID=False,duration=False):
    # Coded by Jes
    # Creates an entry in Game.timers and Game.idlookout
    # Used in conjunction with checktimer to count down until something
    if ID == False or duration == False:
        print("ERROR: ID or duration not missing")
    else:
        Game.timers.append((str(ID),duration))
        Game.idlookout.append(str(ID))

def checktimer(ID=False):
    for i in range(len(Game.idlookout)):
        if Game.idlookout[i] == ID:
            amount = 0
            for i in range(len(Game.timers)):
                if Game.timers[i][0] == ID:
                    amount += 1
            if amount > 0:
                return False
            else:
                Game.idlookout.remove(ID)
                return True
            
def deltimer(ID=False):
    for i in range(len(Game.idlookout)):
        if Game.idlookout[i] == ID:
            for i in range(len(Game.timers)):
                if Game.timers[i][0] == ID:
                    Game.idlookout.remove(ID)
                    Game.timers.pop(i)


# attack corner
# TODO: add other attacks, parry calculator, combo calculator and the such

def attack(PlayerIndex,target,presetdmg=None,effectinflicted=None):
    PlayerObj = party.partymembers[PlayerIndex]
    # Coded by Jes
    # It does an attack.
    while target >= 0:
        try:
            EnemyObj = enemyHolder.enemies[target]
            break
        except IndexError:
            target -= 1
    if target < 0:
        return
    if presetdmg == None:
        weapmulti = 1
        for category in weapontable:
            for weaponsel in category[1]:
                if weaponsel[0] == party.partymembers[0].weapon:
                    print(weaponsel)
                    weapmulti = weaponsel[6][4] / 10
        playeratk = random.randint(10,50) * weapmulti
    else:
        try:
            playeratk = int(presetdmg)
            print("worked")
        except Exception:
            Warning("what the fuck did you pipe in this shite this cannot be made into an integer")
            playeratk = 10
    for i in range(len(PlayerObj.effects)):
        if PlayerObj.effects[i][0] == "charm" and Game.substate != "Combo":
            TerminalObj.add("You can't bring yourself to attack the " + str(EnemyObj.name) + "...")
            return # It returns nothing. Just using this as an exit statement.
        elif PlayerObj.effects[i][0] == "charm" and Game.substate == "Combo":
            TerminalObj.add("With tears in your eyes, " + PlayerObj.name + "attacks the "+ str(EnemyObj.name) + " for " + str(int(playeratk / 2)) + "damage.")
            playeratk /= 2
    TerminalObj.add(PlayerObj.name + " attacks the " + str(EnemyObj.name) + " for " + str(playeratk) + " damage.") # type: ignore
    if effectinflicted != None:
        EnemyObj.effects.append([effectinflicted,3])
        flavortext = random.randint(1,10) # changes the flavor text
        if effectinflicted == "infected":
            if flavortext != 10:
                TerminalObj.add(str(EnemyObj.name) + " feels sick...")
            else:
                TerminalObj.add(str(EnemyObj.name) + " suddenly became diseased.")
        elif effectinflicted == "confuse":
            if flavortext != 10:
                TerminalObj.add(str(EnemyObj.name) + " is now dizzy!")
            else:
                TerminalObj.add(str(EnemyObj.name) + " now has a severe case of nausea.")
        elif effectinflicted == "drowsy":
            if flavortext != 10:
                TerminalObj.add(str(EnemyObj.name) + " is starting to daydream...")
            else:
                TerminalObj.add(str(EnemyObj.name) + "\'s mind wanders off to dreamland...")
        elif effectinflicted == "charm":
            if flavortext != 10:
                TerminalObj.add(str(EnemyObj.name) + " feels butterflies in their stomach...")
            else:
                TerminalObj.add(str(EnemyObj.name) + " doesn\'t want to hurt " + str(PlayerObj.name) + " anymore. However, battle rules prevent giving up in the midst of battle...")
        elif effectinflicted == "sad":
            if flavortext != 10:
                TerminalObj.add(str(EnemyObj.name) + " feels saddened...")
            else:
                TerminalObj.add(str(EnemyObj.name) + " is now sad.")
        elif effectinflicted == "bleed":
            # okay these are enemies, lemme just take out my pent up anger on them.
            if flavortext != 10:
                TerminalObj.add(str(EnemyObj.name) + " is bleeding!")
            else:
                TerminalObj.add(str(EnemyObj.name) + " should probably be dead from blood loss by now.")
    PlayerObj.animqueue = [] # wiping it here should do for now.
    PlayerObj.animqueue.append((1,5))
    EnemyObj.hp -= playeratk
    enemyHolder.update_enemy(target,EnemyObj)
    party.partymembers[PlayerIndex] = PlayerObj

def movequeuer():
    global enemyHolder
    # Coded by Jes
    # Queues up enemy moves.
    # TODO: we really really gotta clean things up round here before release
    queued = []
    playercounts = [i for i in range(len(party.alive)) if party.alive[i] == True]
    i = 0
    if len(playercounts) > 0:
        for EnemyObj in enemyHolder.enemies:
            enemyatk = 0
            move = ""
            weights = []
            for move in EnemyObj.moves:
                weights.append([move,EnemyObj.moves[move]['weight']])
            weightsum = 0
            point = random.randint(1,100)
            for weight in weights:
                weightsum += weight[1]
                if point <= weightsum:
                    move = weight[0]
                    break
            atkmulti = 1 # TODO: make it take armors and badges into consideration
            movetype = "ATK"
            try:
                enemyatk = random.randint(EnemyObj.moves[move]["dmg"][0],EnemyObj.moves[move]["dmg"][1]) * atkmulti
            except Exception:
                # assuming that the move had no attack...
                try:
                    enemyatk = random.randint(EnemyObj.moves[move]["heal"][0],EnemyObj.moves[move]["heal"][1])
                    movetype = "HEAL"
                except Exception:
                    TerminalObj.add("The enemy tried to summon an enemy, but the fabric of reality itself isn\'t ready for that yet.")
                    movetype = "SUMMON"
            doeffect=False
            possibleeffect = ""
            if movetype == "ATK":
                try:
                    possibleeffect = EnemyObj.moves[move]["effect"]
                    if possibleeffect == "$ANY":
                        try:
                            possibleeffect = random.choice(list(effectdict.items()))[0]
                        except Exception:
                            pass
                    effectpossibilities = random.randint(1,10)
                    if effectpossibilities <= int(EnemyObj.moves[move]["chance"] * 10):
                        doeffect = True
                except KeyError:
                    possibleeffect = ""
                    effectpossibilities = 0
            queued.append([EnemyObj.moves[move],doeffect,possibleeffect,enemyatk,i,playercounts[random.randint(0,len(playercounts)-1)]])
            i += 1
        DodgeObj.__init__(moves=queued)
        Game.substate = "dodge"
    

def effectcycle(PlayerObj,target):
    topop = []  # Note: After actually reading the Python Tutorial, it turns out that topop is unnecessary in ALL cases.
                # One can just iterate over a copy of a list.
                # ... we use topop 24 times.
                # I really should read documentation instead of winging things, huh?
    global enemyHolder
    # Coded by Jes
    # Cycles effects and durations.
    # TODO: FINISH THIS
    # TODO: ACTUALLY REWRITE THIS
    EnemyObj = enemyHolder.enemies[target]
    randeffect = -1
    print(PlayerObj.effects)
    print("looping started")
    rangehandler = len(PlayerObj.effects)
    for i in range(rangehandler):
        PlayerObj.effects[i][1] -= 1
        if PlayerObj.effects[i][0] == 'all':
            randeffect = random.randint(1,10)
        if PlayerObj.effects[i][0] == 'infected' or randeffect == 0:
            if PlayerObj.effects[i][1] == 0:
                TerminalObj.add("The infection subsides...")
                topop.append(i)
            else:
                inflost = random.randint(3,7)
                TerminalObj.add(str(PlayerObj.name) + "\'s infection creeps forward.")
                TerminalObj.add("Lost " + str(inflost) + " HP.")
                PlayerObj.hp -= inflost
        if PlayerObj.effects[i][0] == 'confuse' or randeffect == 1:
            if PlayerObj.effects[i][1] == 0:
                TerminalObj.add(str(PlayerObj.name) + " no longer feels dizzy.")
                topop.append(i)
        if PlayerObj.effects[i][0] == 'drowsy' or randeffect == 2:
            if PlayerObj.effects[i][1] == 0:
                TerminalObj.add(str(PlayerObj.name) + " jolts back awake.")
                topop.append(i)
            else:
                TerminalObj.add(str(PlayerObj.name) + " 's eyes continue to close...")
        if PlayerObj.effects[i][0] == 'charm' or randeffect == 3:
            if PlayerObj.effects[i][1] == 0:
                TerminalObj.add(str(PlayerObj.name) + " snaps back to reality.")
                topop.append(i)
            else:
                TerminalObj.add(str(PlayerObj.name) + " is daydreaming about " + str(EnemyObj.name) + "...")
        if PlayerObj.effects[i][0] == 'sad' or randeffect == 4:
            if PlayerObj.effects[i][1] == 0:
                TerminalObj.add(str(PlayerObj.name) + " tries to put themselves back together, emotionally speaking.")
                topop.append(i)
            else:
                TerminalObj.add(str(PlayerObj.name) + " is crying..")
        if PlayerObj.effects[i][0] == 'bleed' or randeffect == 5:
            if PlayerObj.effects[i][1] == 0:
                TerminalObj.add(str(PlayerObj.name) + "\'s wound coagulates.")
                topop.append(i)
            else:
                bloodloss = random.randint(1,10)
                TerminalObj.add(str(PlayerObj.name) + " is still bleeding! Lost " + str(bloodloss) + " HP.")
                PlayerObj.hp -= bloodloss
        if PlayerObj.effects[i][0] == 'speed' or randeffect == 6:
            if PlayerObj.effects[i][1] == 0:
                topop.append(i)
                TerminalObj.add(str(PlayerObj.name) + " feels the rush go away...")
            else:
                TerminalObj.add(str(PlayerObj.name) + " is sprinting!")
                PlayerObj.skipturn = True
        if PlayerObj.effects[i][0] == 'bleed' or randeffect == 7:
            if PlayerObj.effects[i][1] == 0:
                TerminalObj.add(str(PlayerObj.name) + " stops burning alive.")
                topop.append(i)
            else:
                bloodloss = random.randint(1,10)
                TerminalObj.add(str(PlayerObj.name) + " is still burning! Lost " + str(bloodloss) + " HP.")
                PlayerObj.hp -= bloodloss
        if PlayerObj.effects[i][0] == 'atkmulti':
            if PlayerObj.effects[i][1] == 0:
                TerminalObj.add(str(PlayerObj.name) + "\'s ATTACK MULTIPLIER ends.")
                topop.append(i)
    for i in range(len(topop)):
        try:
            PlayerObj.effects.pop(topop[i])
        except Exception:
            print("effect cycle failed: why? diagnosis:", topop)
    for i in range(len(PlayerObj.effects)):
        for j in range(len(PlayerObj.effects)):
            if PlayerObj.effects[i][0] == PlayerObj.effects[j][0] and i != j:
                if PlayerObj.effects[i][1] >= PlayerObj.effects[j][1]:
                    topop.append(j)
                else:
                    topop.append(i)
    for i in range(len(topop)):
        try:
            PlayerObj.effects.pop(topop[i])
        except Exception:
            print("effect cycle failed: why? diagnosis:", topop)
    party.partymembers[0] = PlayerObj
    topop = [] # Enemy effect cycling started.
    # TODO: REMAKE ALL OF EFFECT CYCLE THIS SUCKS SO BAD
    enemyHolder.update_enemy(target,EnemyObj)

slash = pygame.mixer.Sound('sfx/slash2.wav')

def avg(iterable):
    # Calculates the average of an iterable.
    sumofiter = 0
    for item in iterable:
        sumofiter += int(item)
    return sumofiter / len(iterable)

# TODO: While all combos are functional, the MAGIC, SCIENCE and CLOWN combos are in need of some... "touch ups".
# The BOW Combo needs a bit of a recode to feel correct. Scratch that; a ton of a rework.
# Merge the DAGGER, FIST and SWORD Combos into just the Sword one; and get new ideas for the DAGGER and FIST combos.

class SwordCombo:
    def __init__(self, complexity=5, basedmg = 50,target=-1):
        del target
        holder = []
        self.basedmg = basedmg
        self.timings = []
        self.accuracy = 100
        self.speed = 180*math.log(complexity,2)
        for i in range(random.randint(2,2+complexity)):
            type = 0
            if random.randint(1,int(10/math.log(complexity))) == 1:
                type = 1
            holder.append({"type":type,"timings":[],"hit":0,"holding":[0,0]})
        holder = sorted(holder, key=lambda x: x['type'], reverse=True)
        for timing in holder:
            brakes = 0
            while True:
                holdadder = 5 + random.randint(1,480 + complexity * 5)
                timing["timings"].append(random.randint(100,920 - holdadder * timing["type"]))
                timing["timings"].append(timing["timings"][0] + 40 + holdadder * timing["type"])
                triggered = 0
                brakes += 1
                for compared in self.timings:
                    if compared["timings"][0] < timing["timings"][0] < compared["timings"][1] or compared["timings"][0] < timing["timings"][1] < compared["timings"][1]:
                        triggered = 1
                if brakes == 7:
                    break  
                elif triggered == 0:
                    self.timings.append(timing)
                    break
        self.pointerpos = 0
        self.holding = False
        self.hits = 0

    def damage(self):
        damage = self.basedmg
        accuracy = 100
        timinglist = []
        for timing in self.timings:
            if timing["type"] == 0:
                if timing["hit"] != 0:
                    timinglist.append(100)
                else:
                    timinglist.append(0)
            if timing["type"] == 1:
                print(timing["hit"])
                if timing["hit"] != 0:
                    timinglist.append(((timing["holding"][1] - timing["holding"][0]) / (timing["timings"][1] - timing["timings"][0])) * 100)
                else:
                    timinglist.append(0)
        try:
            accuracy = avg(timinglist) * (len(timinglist) / self.hits)
        except ZeroDivisionError:
            accuracy = 0
        print(timinglist)
        print("a", accuracy)
        damage = accuracy * 1.4 + 10
        return damage    
    def draw(self):
        pygame.draw.rect(WINDOW,(30,30,30),(0,518,960,202))
        pygame.draw.rect(WINDOW,(55,55,55),(0,523,960,197))
        for timing in self.timings:
            color = (200,200,200)
            if timing['holding'][0] != 0 and timing['hit'] == 3 and self.holding: 
                color = (150,150,150)
            elif timing['holding'][0] != 0 and timing['hit'] != 0: 
                color = (100,100,100)
            pygame.draw.rect(WINDOW,color,(timing["timings"][0],523,timing["timings"][1] - timing["timings"][0],197))
        pygame.draw.rect(WINDOW,(255,0,0),(self.pointerpos,523,1,197))
        if self.pointerpos >= 965:
            return self.damage()
        else:
            self.pointerpos += self.speed * Game.milidt # milidt seems to be the correct deltatime... TODO: move Game.dt to milidt
        for event in Game.eventqueue:
            if event.type == KEYDOWN and event.key == K_SPACE:
                if self.holding == False:
                    self.hits += 1
                for timing in self.timings:
                    oltiming = timing
                    if timing["timings"][0] - 5 < self.pointerpos < timing["timings"][1] + 5:
                        if timing['type'] == 0:
                            timing['hit'] = 1
                            timing['holding'][0] = 1
                            pygame.mixer.Sound.play(Sounds.slashsfx)
                        elif timing['type'] == 1:
                            if timing['holding'][1] == 0:
                                timing['hit'] = 3
                                timing['holding'][0] = self.pointerpos - timing["timings"][0]
                    self.timings.remove(oltiming)
                    self.timings.append(timing)
                self.holding = True
            if event.type == KEYUP and event.key == K_SPACE:
                self.holding = False
                if timing['holding'][1] == 0 and timing['type'] == 1 and timing['hit'] == 3:
                    oltiming = timing
                    timing['hit'] = 2
                    timing['holding'][1] = self.pointerpos - timing["timings"][0]
                    self.timings.remove(oltiming)
                    self.timings.append(timing)
        return False

class DaggerCombo:
    # TODO: Do some fixups. They're severely needed before PTB1's final release. Mostly it's visuals and collisions.
    def __init__(self,target=-1):
        del target
        self.slashes =[]
        for i in range(random.randint(3,6)):
            self.slashes.append(((random.randint(0,240),random.randint(0,240)),random.randint(0,1)))
        self.timer = 7
        self.slashed = 0
        self.imousepos = (-0.1,-0.1)
    def draw(self):
        self.timer -= 1 * Game.milidt
        if maag == False:
            if pygame.mouse.get_just_pressed()[0]:
                self.imousepos = pygame.mouse.get_pos() # i'm getting a lot of mouse shit. TODO: make a custom way to do inputs so we don't even have to loop thru Game.eventqueue? should make the game slightly quicker and also allow for things like keyremapping i think
            if pygame.mouse.get_just_released()[0]:
                cmousepos = pygame.mouse.get_pos()
                if self.slashes[self.slashed][1] != 1:
                    points = [(240/6*i + 610,(self.slashes[self.slashed][0][1] - self.slashes[self.slashed][0][0])/6*i+295) for i in range(6)]
                    mousepoints = [(cmousepos[0] - self.imousepos[0]/24*i, cmousepos[1] - self.imousepos[1]/24*i) for i in range(12)]
                    collided = 0
                    for point in points:
                        for mousepoint in mousepoints:
                            if point[0] - 30 < mousepoint[0] < point[0] + 30 and point[1] - 30 < mousepoint[1] < point[1] + 30:
                                collided += 1
                    if collided > 3:
                        self.slashed += 1
                    print(points)
                    print(mousepoints)
                else:
                    self.slashed += 1
        if self.timer <= 0 or self.slashed == len(self.slashes):
            try:
                print(self.slashed/(len(self.slashes)+1))
                value = random.randint(100,300) * (self.slashed/(len(self.slashes) + 1))
            except Exception:
                value = random.randint(100,300) * self.slashed + 1/len(self.slashes) + 2
            if value < 10:
                return 10
            return value
        if self.slashes[self.slashed][1] == 0:
            pygame.draw.line(WINDOW,(50,50,50),(600,self.slashes[self.slashed][0][0] + 200),(840,self.slashes[self.slashed][0][1] + 200))
        else:
            pygame.draw.circle(WINDOW,(50,50,50),(720,305),6,20)
        if pygame.mouse.get_just_pressed()[2]:
            self.slashed += 1
        if self.imousepos[0] != -0.1:
            pygame.draw.line(WINDOW,(255,0,0),self.imousepos,pygame.mouse.get_pos())
        return False


class BowCombo:
    # This just needs an overall visual rework... but somehow, gambling on code, it works.
    def __init__(self,target):
        self.strength = 0.0
        self.angle = 0.0
        self.gravity = 1.0
        self.pos = [300.0,300.0]
        self.ogpos = self.pos
        self.active = False
        self.selector = [8.0,1]
        self.time = 0
        self.enemyrect = enemyHolder.enemies[target].animations["PTBIdle"].get_rect()
        self.enemyrect.topleft = (700 * scaleW, (450 * scaleH) - enemyHolder.enemies[target].animations["PTBIdle"].get_size()[1])

    def draw(self):
        if self.strength == 0:
            if self.selector[0] >= 16:
                self.selector[1] = -1
            elif self.selector[0] <= 10:
                self.selector[1] = 1
            self.selector[0] += 10 * Game.milidt * self.selector[1]
        elif self.angle == 0:
            if self.selector[0] >= 80:
                self.selector[1] = -1
            elif self.selector[0] <= 10:
                self.selector[1] = 1
            self.selector[0] += 100 * Game.milidt * self.selector[1]
        trajectorysurf = pygame.surface.Surface((192,192)).convert_alpha()
        trajectorysurf.fill((0,0,0,0))
        if self.strength == 0.0: # should probably merge these with the above if statements
            pygame.draw.line(trajectorysurf,(255,255,255),(0,186),((self.selector[0] - 10)*13,186),6)
        elif self.angle == 0.0:
            pygame.draw.line(trajectorysurf,(255,255,255),(0,186),((self.strength - 10)*13,186),6)
            pygame.draw.arc(trajectorysurf,(255,255,255),(-96 - (2*(self.strength - 10)),96,192 - (2*(self.strength - 10)),192 - (2*(self.strength - 10))),0,math.radians(self.selector[0]),6)
            ttime = 0
            pos = [0.0,0.0]
            for i in range(10):
                ttime += 0.7*i*5
                pos[0] = -4 + self.ogpos[1] - (math.sin(math.radians(self.selector[0]))*self.strength*ttime)+ .5*72*ttime**2 
                pos[1] = 4 + self.ogpos[0] + (math.cos(math.radians(self.selector[0]))*self.strength*ttime) * 2
                pygame.draw.circle(WINDOW,(0,0,0),pos,6)
        else:
            pygame.draw.line(trajectorysurf,(255,255,255),(0,186),((self.strength - 10)*13,186),6)
            pygame.draw.arc(trajectorysurf,(255,255,255),(-96 - (2*(self.strength - 10)),96,192 - (2*(self.strength - 10)),192 - (2*(self.strength - 10))),0,math.radians(self.angle),6)
        troutline,renderpos = Outliner(trajectorysurf,pos=(250,200))
        WINDOW.blit(troutline,(250,200))
        WINDOW.blit(trajectorysurf,renderpos)
        if self.active == True:
            self.time += 0.7 * Game.milidt
            self.pos[1] = -4 + self.ogpos[1] - (math.sin(math.radians(self.angle))*self.strength*self.time)+ .5*72*self.time**2
            self.pos[0] = 4 + self.ogpos[0] + (math.cos(math.radians(self.angle))*self.strength*self.time) * 2
            pygame.draw.circle(WINDOW,(0,0,0),self.pos,6)
            if self.pos[1] > 960 or self.pos[1] < 0 or self.pos[0] < 0 or self.pos[0] > 1280:
                return 10
            return self.collide(self.enemyrect)
        else:
            for event in Game.eventqueue:
                if event.type == KEYDOWN and event.key == K_SPACE:
                    if self.strength == 0.0:
                        self.strength = self.selector[0]
                    elif self.angle == 0.0:
                        self.angle = self.selector[0]
                        self.active = True
        return False
    
    def collide(self,rect=pygame.Rect(0,0,1,1)):
        print("r", rect)
        if rect.collidepoint(self.pos): # TODO: fix this up a ton, make actual hitboxes
            dmg = 100
            return dmg
        return 0


class GunCombo:
    def __init__(self,target=-1):
        del target
        self.bullets = [{"type":random.randint(0,4),"shot":False,"time":1,"image":""} for i in range(6)]
        for i in range(len(self.bullets)):
            self.bullets[i]['image'] = pygame.image.load("assets/battle/combos/gun/" + str(self.bullets[i]["type"]) + ".png").convert_alpha()
            if self.bullets[i]['type'] == 1:    # ugly af but works
                self.bullets[i]["time"] = 8
            elif self.bullets[i]['type'] == 3:
                self.bullets[i]["time"] = 12
            elif self.bullets[i]['type'] == 4:
                self.bullets[i]["time"] = random.randint(20,100) / 10
        self.chamber = pygame.transform.scale_by(pygame.image.load("assets/battle/combos/gun/chamber.png").convert_alpha(),0.6)
        self.cooldown = [0.0,0.0,0.0]
        self.shootrect = pygame.Rect(295,135,56,56)
        self.timer = 8
    def draw(self):
        if self.timer > 0:
            self.timer -= 1.5 * Game.milidt
        if self.cooldown[2] > 0:
            self.cooldown[2] -= 5 * Game.milidt
        if self.cooldown[2] < 0:
            self.cooldown[2] = 0
        WINDOW.blit(self.chamber,(250,150))
        WINDOW.blit(font.render(str(round(self.timer,2)),True,(255,255,255)),(300,200))
        i = 0
        for bullet in self.bullets:
            WINDOW.blit(bullet['image'],(300 + 60 * math.cos(math.radians(i*60 + 270)),200 + 60 * math.sin(math.radians(i*60 + 270))))
            i += 1
        try:
            pygame.draw.circle(WINDOW,(int(255-10*self.cooldown[2]),int(255-10*self.cooldown[2]),int(255-10*self.cooldown[2])),(324 + 60 * math.cos(math.radians(270)),224 + 60 * math.sin(math.radians(270))),self.cooldown[2]*5 + 24,4)
        except ValueError:
            pygame.draw.circle(WINDOW,(0,0,0),(324 + 60 * math.cos(math.radians(270)),224 + 60 * math.sin(math.radians(270))),self.cooldown[2]*5 + 24,4)
        for event in Game.eventqueue:
            if event.type == KEYDOWN and event.key == K_SPACE and self.cooldown[2] <= 0:
                if self.shootrect.colliderect((300 + 60 * math.cos(math.radians(270)),200 + 60 * math.sin(math.radians(270)),30,30)):
                    self.cooldown[2] = self.bullets[0]['time']
                    self.bullets.pop(0)
            elif event.type == KEYDOWN and event.key == K_SPACE:
                self.cooldown[2] += 5
        if len(self.bullets) == 0 or self.timer <= 0:
            return self.timer * 50 + 10*(6 - len(self.bullets))
        return False

        
class FistCombo:
    def __init__(self,target=-1):
        del target
        # 0 is LMB 1 is RMB 2 is both
        combinations = [
            [0,0,1],
            [1,0,1,2],
            [1,2,0,0,1],
            [1,1,1],
            [0,1,0,1,2],
            [0,0,0,2],
            [2,0,2],
            [1,2,1],
            [0,0,0,1,1,1],
            [1,2,0,0,2,1]
        ]
        self.combination = combinations[random.randint(0,len(combinations) - 1)]
        self.offset = 320/len(self.combination)
        self.pos = 0
        self.pressed = 0
        self.combposit = [(self.offset / 1.5) + 200 + i * self.offset for i in range(len(self.combination))]
        """
        so:
        - we split the combination up so you have around 20-30 frames to press the button
        - we make it so every button you press is registered
        - if you fail an input it's so fucking joever and you take damage to self
        - TODO: make it so you take damage to self
        """
        self.images = (pygame.image.load("assets/icons/mouse/click_lq0002.png").convert_alpha(),
                       pygame.image.load("assets/icons/mouse/click_lq0003.png").convert_alpha(),
                       pygame.image.load("assets/icons/mouse/click_lq0004.png").convert_alpha(),
                       pygame.image.load("assets/icons/mouse/click_lq0001.png").convert_alpha())
    def draw(self):
        self.pos += 80 * Game.milidt
        pygame.draw.line(WINDOW,(0,0,0),(200,200),(520,200),10)
        pygame.draw.line(WINDOW,(200,0,0),(201,200),(519,200),8)
        pygame.draw.line(WINDOW,(155,0,0),(self.pos + 201,200),(519,200),8)
        pygame.draw.line(WINDOW,(255,255,255),(self.pos + 200, 195),(self.pos + 200, 205),2)
        toreplace = [] # yes, doing this again. hey, it works. don't blame me.
        for i in range(len(self.combination)):
            WINDOW.blit(self.images[self.combination[i]],(self.combposit[i],184))
            if self.combposit[i] - 230 < self.pos < self.combposit[i] - 170:
                buttons = pygame.mouse.get_pressed()
                if self.combination[i] == 2:
                    if buttons[0] == True and buttons[2] == True:
                        self.pressed += 1
                        toreplace.append((i))
                elif self.combination[i] == 0:
                    if buttons[0] == True:
                        self.pressed += 1
                        toreplace.append((i))
                elif self.combination[i] == 1:
                    if buttons[2] == True:
                        self.pressed += 1
                        toreplace.append((i))
                print(buttons)
        for i in toreplace:
            self.combination.pop(i)
            self.combposit.pop(i)
        if self.pos > 320:
            return random.randint(160,320) / (len(self.combination) + 1)
        return False



class MagicCombo():
    def __init__(self,target=-1):
        del target
        values = [[(4, 10), (5, 8), (5, 9), (5, 10), (6, 6), (6, 7), (6, 10), (7, 4), (7, 5), (7, 10), (8, 6), (8, 7), (8, 10), (9, 8), (9, 9), (9, 10), (10, 10)],
          [(4, 3), (4, 4), (4, 5), (4, 6), (4, 7), (4, 8), (4, 9), (4, 10), (4, 11), (5, 3), (5, 11), (6, 3), (6, 11), (7, 3), (7, 11), (8, 3), (8, 11), (9, 3), (9, 11), (10, 3), (10, 4), (10, 5), (10, 6), (10, 7), (10, 8), (10, 9), (10, 10), (10, 11)],
          [(4, 8), (5, 6), (5, 7), (5, 8), (6, 4), (6, 5), (6, 8), (7, 2), (7, 3), (7, 8), (7, 11), (7, 12), (7, 13), (8, 8), (8, 10), (8, 11), (9, 8), (9, 9), (10, 8)],
          [(8, 1), (8, 2), (8, 3), (8, 4), (8, 5), (8, 6), (8, 7), (8, 8), (8, 9), (8, 10), (8, 11), (8, 12), (8, 13), (8, 14)],
          [(2, 6), (3, 6), (3, 7), (4, 6), (4, 8), (4, 12), (4, 13), (5, 6), (5, 9), (5, 10), (5, 11), (5, 13), (6, 3), (6, 4), (6, 11), (7, 1), (7, 10), (7, 11), (8, 3), (8, 4), (8, 12), (8, 13), (9, 6), (9, 9), (9, 10), (9, 11), (9, 13), (10, 6), (10, 9), (10, 13), (10, 14), (11, 6), (11, 7), (12, 6)],
          [(3, 5), (3, 6), (3, 7), (3, 8), (3, 9), (4, 4), (4, 5), (5, 4), (5, 5), (6, 4), (6, 5), (7, 6), (7, 7), (8, 7), (8, 8), (9, 8), (9, 9), (10, 9), (10, 10), (11, 7), (11, 8), (11, 9), (11, 10), (12, 4), (12, 5), (12, 6), (12, 7), (12, 8)],
          [(3, 6), (3, 7), (3, 8), (3, 9), (3, 10), (4, 5), (4, 10), (4, 11), (5, 4), (5, 11), (6, 4), (6, 11), (7, 4), (7, 11), (8, 4), (8, 11), (9, 4), (9, 11), (10, 4), (10, 11), (11, 4), (11, 5), (11, 10), (11, 11), (12, 6), (12, 7), (12, 8), (12, 9), (12, 10)],
          [(4, 5), (4, 6), (4, 7), (4, 8), (4, 9), (4, 10), (5, 4), (5, 11), (6, 3), (6, 12), (7, 3), (7, 12), (8, 3), (8, 11), (8, 12), (9, 5), (9, 6), (9, 7), (9, 8), (9, 9), (9, 10), (9, 11)]]
        self.value = values[random.randint(0,len(values) - 1)]
        del values
        self.pointarray = []
        self.drawsurf = pygame.Surface((350,200)).convert_alpha()
        for i in range(70):
            self.pointarray.append([])
            for j in range(40):
                self.pointarray[i].append(None)

        for coordinate in self.value:
            self.pointarray[coordinate[0]][coordinate[1]] = True

        for coordinate in self.value:
            # reusing this bc, well, i think it's faster to run on coordinate than to do an i,j loop here?
            # also already using i,j here so don't want 4 for loops running at the same time
            altrdcrd = [coordinate[0]-1, coordinate[1]-1]
            for i in range(3):
                for j in range(3):
                    try:
                        if i == 1 or j == 2:
                            if self.pointarray[altrdcrd[0] + i][altrdcrd[1] + j] == None:
                                self.pointarray[altrdcrd[0] + i][altrdcrd[1] + j] = 3
                    except Exception:
                        pass
        self.timer = 5
        self.mousecursor = []
        self.trigger = None

    def accuracyChecker(self):
        valhit = 0
        invhit = 0
        for i in range(len(self.pointarray)):
            for j in range(len(self.pointarray[i])):
                if self.pointarray[i][j] == False and (i,j) in self.value:
                    valhit += 1
                elif self.pointarray[i][j] == False and (i,j) not in self.value:
                    invhit += 1
        ratio = 1/len(self.value)
        print(invhit, valhit)
        value = (valhit * ratio) - (invhit * ratio)
        if value > 0:
            return value
        else:
            return 0
        
    def draw(self):
        self.drawsurf.fill((0,150,150,30))
        self.timer -= 1*Game.milidt
        if self.timer <= 0 or pygame.mouse.get_just_released()[0] and self.trigger == False:
            return self.accuracyChecker() * random.randint(50,100)
        if pygame.mouse.get_just_released()[0] and self.trigger == None:
            self.trigger = True
        elif pygame.mouse.get_pressed()[0]:
            self.trigger = False
        for i in range(len(self.pointarray)):
            for j in range(len(self.pointarray[i])):
                pos = (i*23.33333333333,j*13.33333333333)
                color = (0,0,0,0)
                if self.pointarray[i][j] == True:
                    color = (255,255,0)
                    pygame.draw.circle(self.drawsurf,color,pos,4)
                elif self.pointarray[i][j] == False:
                    color = (255,0,255)
                    pygame.draw.circle(self.drawsurf,color,pos,4)
                for item in self.mousecursor:
                    if item[0] - 10 < pos[0] < item[0] + 10 and item[1] - 10 < pos[1] < item[1] + 10 and self.pointarray[i][j] != 3:
                        self.pointarray[i][j] = False
        addmouse = True
        pos = pygame.mouse.get_pos()
        pos = (pos[0] - 150, pos[1] - 200)
        print(pos)
        for item in self.mousecursor:
            pygame.draw.circle(self.drawsurf,(0,0,255),item,2)
            if item[0] - 3 > pos[0] > item[0] + 3 and item[1] - 3 > pos[1] > item[1] + 3:
                addmouse = False
        if addmouse == True and pygame.mouse.get_pressed()[0] == True:
            self.mousecursor.append(pos)
        WINDOW.blit(self.drawsurf,(150,200))
        text = font.render(str(round(self.timer,2)),True,(255,255,255))
        textoutline =  Outliner(text,pos=(250,180),thickness=2)
        WINDOW.blit(textoutline[0],textoutline[1])
        WINDOW.blit(text,(250,180))
        return False

class ScientistCombo:
    def __init__(self,target=-1):
        del target
        self.filling = 20
        self.objective = random.randint(180,400)
        self.filltype = random.randint(1,3)
        self.fillsurf = pygame.surface.Surface((120,480)).convert_alpha()
        self.effecttimer = 0
        self.lasty = 0
        self.color = (255,255,255)
        if self.filltype == 3:
            self.color = (20,random.randint(50,255),10,70)
        elif self.filltype == 2:
            self.color = (0,20,random.randint(50,255),70)
        elif self.filltype == 1:
            self.color = (random.randint(50,255),10,70,70)
        self.testtubemask = pygame.image.load("assets/battle/combos/science/testtubemask.png").convert_alpha()
        self.fillsurf.set_colorkey((23,53,83))
        self.inobj = 0
        self.timer = 7
    def draw(self):
        self.timer -= 1 * Game.milidt
        print(self.timer)
        if self.objective < self.filling < self.objective + 50:
            self.inobj += 1 * Game.milidt
        elif self.objective - 30 < self.filling < self.objective + 80:
            self.inobj += 0.5 * Game.milidt
        if self.effecttimer <= 0:
            self.effecttimer = random.randint(1,3)
            if self.filltype == 3:
                self.filling -= random.randint(30,60)
            elif self.filltype == 2:
                self.filling += random.randint(30,60)
            elif self.filltype == 1:
                self.filling += random.randint(-30,30)
        else:
            self.effecttimer -= 1*Game.milidt
        self.fillsurf.fill((0,255,255,60))
        if self.filling > 3:
            self.filling -= 10 * Game.dt
        if pygame.mouse.get_pressed()[0] == True:
            if pygame.mouse.get_pos()[1] - self.lasty > 0:
                if self.filling <= 465:
                    self.filling += (pygame.mouse.get_pos()[1] - self.lasty) / 3
            self.lasty = pygame.mouse.get_pos()[1]
        pygame.draw.rect(self.fillsurf,(self.color),(0,480 - self.filling,120,480))
        pygame.draw.line(self.fillsurf,(200,30,30),(0, self.objective + 50),(120, self.objective + 50),4)
        pygame.draw.line(self.fillsurf,(200,30,30),(0, self.objective),(120, self.objective),4)
        pygame.draw.line(self.fillsurf,(200,200,30),(0, self.objective + 80),(120, self.objective + 80),4)
        pygame.draw.line(self.fillsurf,(200,200,30),(0, self.objective - 30),(120, self.objective - 30),4)
        # I am NOT using a mask. (mainly because IDK how the pygame mask module works.)
        self.fillsurf.blit(self.testtubemask)
        WINDOW.blit(pygame.transform.scale_by(self.fillsurf,0.5),(266,150))
        WINDOW.blit(font.render(str(round(self.timer,2)),True,(255,255,255)),(270,126))
        if self.timer <= 0:
            if self.inobj > 0:
                return random.randint(20,80) * self.inobj
            else:
                return 10
        return False

class ClownCombo():
    def __init__(self,target=-1):
        del target # actually for animations and shit we may have to use targets in this combo in the future
        # Sequences have offsets in 9/10ths of a millisecond and always end in kaboom.
        sequences = [[900,1350,1650,2100,2550],
                     [600,825,1050,1650,2100],
                     [300,450,750,900,1200],
                     [450,900,1350,1800,2250],
                     [375,525,975,1624,1775],
                     [747,1245,1627,1978,2163]]
        self.sequence = sequences[random.randint(0,len(sequences) - 1)]
        self.imgs = [pygame.image.load("assets/clown_redball.png").convert_alpha(),pygame.image.load("assets/clown_blueball.png").convert_alpha(),
                     pygame.image.load("assets/clown_yellowball.png").convert_alpha(),pygame.image.load("assets/clown_bomb.png").convert_alpha()]
        self.ballart = []
        for i in range(len(self.sequence)):
            if i != len(self.sequence) - 1:
                self.ballart.append(self.imgs[random.randint(0,2)])
            else:
                self.ballart.append(self.imgs[3])
        del self.imgs
        self.timer = 0
        self.collidesurf = pygame.surface.Surface((180,180)).convert_alpha()
        self.collidesurf.fill((0,0,0,0))
        pygame.draw.circle(self.collidesurf,(0,0,0,90),(90,90),90)
        self.collidesurf.blit(pygame.image.load("assets/clown_objective.png").convert_alpha())
        self.pressed = [0 for item in self.sequence]
    def draw(self):
        self.timer += 1000 * Game.milidt
        WINDOW.blit(self.collidesurf,(300,300))
        spacePressed = False
        for event in Game.eventqueue:
            if event.type == KEYDOWN and event.key == K_SPACE:
                spacePressed = True
        for i in range(len(self.sequence)):
            if self.pressed[i] == 0:
                WINDOW.blit(self.ballart[i],(300,480+self.timer-self.sequence[i]))
                if 240 < (480+self.timer-self.sequence[i]) < 540 and spacePressed == True:
                    self.pressed[i] = 1
                    print("SPACE")
        if self.timer > self.sequence[len(self.sequence) - 1] + 500:
            damage = random.randint(6,33) * self.pressed.count(1)
            print(damage)
            print(self.pressed)
            if damage > 10:
                return damage
            return 10
        return False

# As always, all of the combos need visual touchups and reworks... but if it works, it works and all o' dat.

class Dodger():
    # Dodger code. Sucks, but works.
    # Needs some fixing, too.
    def __init__(self,moves=[]):
        self.moves = moves
        print(self.moves)
        self.timer = 0
        self.active = 0
        self.finishtime = -1
        self.cooldown = 0

    def enemyExistenceCheck(self):
        offenders = 0
        for move in self.moves.copy():
            if move[4] > len(enemyHolder.enemies):
                offenders += 1
                self.moves.remove(move)
        return offenders
        
    def draw(self):
        try:
            # placing this here cuz ik i'll need it later:
            # A return value of -2 means there has been an error, and we're skipping to the next move.
            # A return value of -1 means nothing has happened yet.
            # A return value of 0 means the move hasn't been dodged, and you should deal full damage.
            # A return value of 1 means that the move has been blocked/dodged.
            # A return value of 2 means that the move has been parried/countered!
            if self.moves[self.active][0].get("timings") == None:
                self.moves[self.active][0].update({"timings":{
                    "atk":[-1,-1],
                    "counter":[-1,-1],
                    "block":[-1,-1]
                }})
            if self.finishtime == -1:
                if self.moves[self.active][0]["timings"]["counter"][1] > -1:
                    self.finishtime = self.moves[self.active][0]["timings"]["counter"][1]
                elif self.moves[self.active][0]["timings"]["block"][1] > -1:
                    self.finishtime = self.moves[self.active][0]["timings"]["block"][1] > -1
                else:
                    self.finishtime = 100
            if self.enemyExistenceCheck() > 0:
                return -2, self.moves[self.active]
            self.timer += 1000*Game.milidt
            if Game.inputs["kAccept"]["justDown"] == True:
                if self.moves[self.active][0]["timings"]["counter"][0] < self.timer < self.moves[self.active][0]["timings"]["counter"][1]:
                    return 2, self.moves[self.active]
                elif self.moves[self.active][0]["timings"]["block"][0] < self.timer < self.moves[self.active][0]["timings"]["block"][1]:
                    return 1, self.moves[self.active]
            if self.timer > self.finishtime:
                return 0, self.moves[self.active]
            return -1, self.moves[self.active]
            # we need to return move data and if we've dodged or not
        except Exception:
            return -1, []

DodgeObj = Dodger()

class EnemyParty():
    def __init__(self,enemies=[Enemy()]):
        self.enemies = enemies
        self.hp = 0
        self.gold = 0
        for enemy in self.enemies:
            self.hp += enemy.hp
            self.gold += enemy.gold
        self.btns = []
        buttonscale = (960 / len(self.enemies))*scaleW
        for i in range(len(self.enemies)):
            btnsurf = pygame.Surface((buttonscale,200)).convert_alpha()
            btnsurf.fill((255,255,255))
            pygame.draw.rect(btnsurf,(0,0,0),(0,0,buttonscale,200))
            btnsurf.blit(font.render(str(i),True,(255,255,255)),(int(buttonscale/2-10),90))
            self.btns.append(Button(i * buttonscale,520,btnsurf))
    def update_enemy(self, index, entry):
        self.enemies[index] = entry
        self.refresh()
    def refresh(self):
        self.hp = 0
        for enemy in self.enemies:
            if enemy.hp < 0:
                enemy.hp = 0
            self.hp += enemy.hp
        for enemy in self.enemies:
            if enemy.hp == 0:
                self.enemies.remove(enemy)
        self.btns = []
        try:
            buttonscale = (960 / len(self.enemies))*scaleW
        except ZeroDivisionError:
            buttonscale = 960
        for i in range(len(self.enemies)):
            btnsurf = pygame.Surface((buttonscale,200)).convert_alpha()
            btnsurf.fill((255,255,255))
            pygame.draw.rect(btnsurf,(0,0,0),(10,10,buttonscale - 20,180))
            btnsurf.blit(font.render(str(i),True,(255,255,255)),(int(buttonscale/2-10),90))
            self.btns.append(Button(i * buttonscale,520,btnsurf))

enemyHolder = EnemyParty()

def enemyAttack(playerIndex=0,target=random.randint(0,len(enemyHolder.enemies)),data=(False,"",0,-1)):
    limit = 0
    while party.alive[playerIndex] is False:
        if playerIndex == 0:
            playerIndex = len(party.partymembers) - 1
        playerIndex -= 1
        limit += 1
        if limit > len(party.partymembers) *2:
            return False
    PlayerObj = party.partymembers[playerIndex]
    print("data is", data)
    #... Damages the player.
    # TODO: vary things depending on the enemy and things like those, and animate things and things like those, and-
    if target > len(enemyHolder.enemies) - 1: # oh god we gotta bugfix this properly someday
        target = len(enemyHolder.enemies) - 1
    TerminalObj.add("The " + str(enemyHolder.enemies[target].name) + " attacks " + PlayerObj.name + " for " + str(data[0][3]) + " damage!")
    PlayerObj.hp -= data[0][3]
    if data[0] == True:
        PlayerObj.effects.append((data[1],3))
        text = str(effectdict[data[1]][1])
        text = text.replace('[PLAYER_NAME]',party.partymembers[0].name)
        TerminalObj.add(text)
    party.partymembers[playerIndex] = PlayerObj
    return True

combos = {
    "SwordCombo":SwordCombo(),
    "BowCombo":BowCombo(target=Battle.sendto),
    "MagicCombo":MagicCombo(),
    "ClownCombo":ClownCombo(),
    "ScienceCombo":ScientistCombo(),
    "DaggerCombo":DaggerCombo(),
    "FistCombo":FistCombo(),
    "GunCombo":GunCombo()
}

WINDOW.blit(smallboldfont.render("combos ready",True,(255,255,255)),(0,96))
pygame.display.update()

WINDOW.blit(smallboldfont.render("booting up!",True,(255,255,255)),(0,108))
pygame.display.update()

LAUNCHPARAMETERS=sys.argv
for argument in LAUNCHPARAMETERS:
    if argument.startswith("--"):
        if argument == ("--debug"):
            Game.debug = True

try:
    print(IS_CE)
except Exception:
    IS_CE = 0

def dbglog(str):
    return NotImplementedError

class Debug:
    # TODO: FIX THIS
    inputbuffer = ""
    cmdlist = [("help","for cmd in self.cmdlist: TerminalObj.add(str(cmd[0]) + \": \" + str(cmd[2]))","Prints out a list of all available commands."),
               ("exit","exit()","Quits out of the game."),
               ("changeState","Game.state = str([-0-])","Changes the Game's state. You shouldn\'t mess with it too much."),
               ("disableCmdErrorHandler","self.crashhandling = False;TerminalObj.add(\"Error handling disabled.\")","Disables any crash handling for commands. YOU SHOULD NOT TURN THIS ON."),
               ("getVar","TerminalObj.add([-0-])","Gets a value.")]
    crashhandling = True
    def cmds(self,input):
        input = str(input)
        for cmd in self.cmdlist:
            if input.startswith(cmd[0]) or input == cmd[0]:
                try:
                    finishedcmd = cmd[1]
                    # ok here's what i need to do:
                    # - split the input into its arguments
                    # - for every argument, replace a section in cmd[1] with said argument
                    # - exec cmd[1]
                    i = 0
                    print(finishedcmd)
                    arguments = input.split(" ")[1:]
                    for argument in arguments:
                        print(arguments)
                        finishedcmd = finishedcmd.replace("[-"+str(i)+"-]", argument)
                        i += 1
                    print(finishedcmd)
                    exec(finishedcmd)
                    return 1
                except Exception:
                    if self.crashhandling == False:
                        raise(Exception)
                    TerminalObj.add("An error has occurred executing command " + input + ".")
                    return 0
        TerminalObj.add("No command matches " + input + ".")
        return 0

DebugObj = Debug()

class AssetHandler:
    # Handles Assets.
    def __init__(self) -> None:
        self.assetdict = {}
    def Create(self,asset,handle):
        # Adds an asset into assetdict.
        # Because dicts can't, by design, handle repeat entries; the handle changes if there's already an asset with the same handle.
        # This is why we return the assethandle.
        # NOTE: Assets are deleted after 5 seconds of not being used by default. TODO: Maybe figure out a way to change this without using too many variables?
        assettype = type(asset)
        assethandle = handle
        redo = 0
        while True:
            if assethandle in self.assetdict:
                redo += 1
                assethandle = handle + str(redo)
            else:
                break
        self.assetdict.update({assethandle:{"asset":asset,"type":assettype,"time":5}})
        return assethandle
    
    def Load(self,handle,rmethod="",arguments="",rfunction="",createifnotfound=(False,"")):
        # Loads the asset.
        # Mostly exists to update the asset's timer. A method of said object, or a transformation to said object, may optionally be run.
        # The "createifnotfound" variable calls AssetHandler.Create().
        load = False
        if self.assetdict.get(handle) != None:
            load = True
        else:
            if createifnotfound[0] != False:
                try:
                    handle = self.Create(createifnotfound[1],handle)
                    load = True
                except Exception:
                    pass
        if load == True:
            self.assetdict[handle]["time"] = 5
            if rmethod != "":
                try: 
                    return exec("self.assetdict[" + handle + "][\"asset\"]" + "." + rmethod + "(" + arguments + ")"), handle
                except Exception:
                    pass
            if rfunction != "":
                try: 
                    return exec(rfunction + "(" + self.assetdict[handle]["asset"] + "," + arguments + ")"), handle
                except Exception:
                    pass
            return self.assetdict[handle]["asset"], handle
        return [None, None]

    def Update(self):
        # Ticks down every asset's time based on DeltaTime...
        # ... and deletes the unused ones.
        updatedict = self.assetdict.copy()
        for asset in updatedict:
            self.assetdict[asset]['time'] -= Game.milidt
            if self.assetdict[asset]['time'] <= 0:
                self.assetdict.pop(asset)
    
    def Unload(self,handle):
        # Could technically be used to make an AssetHandler friendly load/unload method, even though this should handle it by itself. I'm just putting it here for ASTHETICS.
        self.assetdict.pop(handle) 

def ColorChanger(surf, oldColor, newColor): # Harvested from StackOverflow. The only thing I did was change the symbols.
    colormask = pygame.mask.from_threshold(surf, oldColor, threshold=(1,1,1,255))
    colorchanger = colormask.to_surface(setcolor=newColor, unsetcolor=(0,0,0,0))
    surfcopy = surf.copy()
    surfcopy.blit(colorchanger, (0, 0))
    return surfcopy

Assets = AssetHandler()

class SpecialList():
    def __init__(self,specialList=[]):
        self.specialList = specialList
        del specialList
        self.btnlist = []
        for i in range(len(self.specialList)):
            btnsurf = pygame.surface.Surface((544*scaleW,48*scaleH)).convert_alpha()
            btnsurf.fill((0,0,0))
            pygame.draw.rect(btnsurf,(255,255,255),(1*scaleW,1*scaleH,542*scaleW,46*scaleH))
            pygame.draw.line(btnsurf,(0,0,0),(30*scaleW,0*scaleH),(30*scaleW,48*scaleH))
            btnsurf.blit(font.render(str(specialdict[self.specialList[i]]["cooldown"]) + "  " +str(specialdict[self.specialList[i]]["name"]),True,(0,0,0)),(10*scaleW,10*scaleH))
            category = 8
            for j in range(len(weapontable)): # i WILL have to change this later on
                if specialdict[self.specialList[i]]["combo"] == weapontable[j][0]:
                    category = j
                    break
            iconsurf = pygame.transform.scale(weapontable[category][2],(44*scaleH,44*scaleW))
            iconsurf = ColorChanger(iconsurf,(255,255,255),(0,0,0))
            btnsurf.blit(iconsurf,(506*scaleW,2*scaleH)) # TODO: ughhh i forgot to readd things to scaleH and scaleW shiiitttt
            self.btnlist.append(Button(2*scaleW,6+i*50*scaleH,btnsurf)) # TODO: i gotta make buttons compatible with the Asset system one day man
        btnsurf = pygame.surface.Surface((40*scaleW,32*scaleH)).convert_alpha()
        btnsurf.fill((0,0,0,0))
        btnsurf.blit(smallboldfont.render("Back",True,(0,0,0)),(2,8))
        pygame.draw.line(btnsurf,(0,0,0),(32,0),(32,32))
        self.backbtn = Button(4,688,btnsurf)
        self.scrollpos = 0
        self.scrollrect = pygame.Rect(0,0,0,0)
        try:
            sizeform = 169 ** 1/(len(self.specialList) - 2)
            if sizeform >= 169:
                self.scrollbar = Dragable(-5,-5,pygame.surface.Surface((1,1)).convert_alpha())
            else:
                dragsurf = pygame.surface.Surface((8,sizeform)).convert_alpha()
                self.scrollbar = Dragable(554,524,dragsurf) # note to self: I REALLY GOTTA FIX DRAGABLES AND SCROLLING IN THIS GAME
        except Exception:
            self.scrollbar = Dragable(-3,-3,pygame.Surface((1,1)))
            self.scrollpos = 0
        self.btnsurf = pygame.surface.Surface((548,164)).convert_alpha()
        self.btnsurf.fill((0,0,0,0))
        self.timer = 0
        self.descsize = -1
        self.textobj = TextEng()
        self.textswitch = 1 #ughhh i hate doing this THIS way but idk how to do it properly
        self.pos = 0

    def draw(self):
        self.timer += 1 * Game.milidt
        holdmenu = Menu.listitem
        if Game.inputs["kDown"]["justDown"] == True:
            Menu.listitem += 1
            self.timer = 0
            self.descsize = -1
        elif Game.inputs["kUp"]["justDown"] == True:
            Menu.listitem -= 1
            self.timer = 0
            self.descsize = -1
        if Game.inputs["kAccept"]["justDown"] == True:
            return True, [self.specialList[Menu.listitem],specialdict[self.specialList[Menu.listitem]]["mult"],specialdict[self.specialList[Menu.listitem]]["combo"]]
        if Menu.listitem >= len(self.specialList):
            Menu.listitem = 0
            self.timer = 0
            self.descsize = -1
        elif Menu.listitem < 0:
            Menu.listitem = len(self.specialList) - 1
            self.timer = 0
            self.descsize = -1
        if holdmenu != Menu.listitem and len(self.btnlist) > 3:
            self.scrollpos = 166 / len(self.btnlist) * Menu.listitem
        pygame.draw.rect(WINDOW,(0,0,0),(0,520,960,320))
        pygame.draw.rect(WINDOW,(255,255,255),(4,524,952,316))
        pygame.draw.line(WINDOW,(0,0,0),(562,524),(562,720),2)
        self.btnsurf.fill((0,0,0,0))
        for i in range(len(self.btnlist)):
            if self.btnlist[i].draw(yoff= -self.scrollpos,surface=self.btnsurf,surfacex=4,surfacey=524):
                Menu.listitem = i
                self.timer = 0
                self.descsize = -1
        pygame.draw.rect(self.btnsurf,(255,0,0),(0,Menu.listitem*50-self.scrollpos + 4,548,50),4,4)
        WINDOW.blit(self.btnsurf,(4,524))
        pygame.draw.rect(WINDOW,(150,150,150),(4,688,558,32))
        pygame.draw.line(WINDOW,(0,0,0),(0,688),(562,688),2)
        if len(self.btnlist) > 3:
            tmpscrollrect = self.scrollbar.draw(limitx=(558,558),limity=(524,690),movefrom="center")[1]
            if tmpscrollrect != self.scrollrect:
                print(tmpscrollrect,self.scrollrect)
                self.scrollrect = tmpscrollrect.copy() # yagottabekiddinme
                self.scrollpos = (166 / ((len(self.btnlist)) * 50)) * (self.scrollrect[1] - 520)
                print(self.scrollpos)
                print(self.scrollrect[1] - 520)
        self.textobj.textlist = []
        self.textobj.add("[N c=(0,0,0)]" + specialdict[self.specialList[Menu.listitem]]["description"],(800000,64),noNL=True)
        if self.descsize == -1:
            self.descsize = font.render(specialdict[self.specialList[Menu.listitem]]["description"],True,(0,0,0)).get_rect()[2]
        if self.timer > 1 and self.descsize > 524:
            self.pos += (self.textobj.lastsize[0]/15)*Game.milidt*self.textswitch
            print((60/(self.descsize+1))*Game.milidt*self.textswitch)
            if self.pos >= self.textobj.lastsize[0] - 520:
                self.pos = self.textobj.lastsize[0] - 520
                self.textswitch = -1
                self.timer = 0
            elif self.pos < 0:
                self.pos = 0
                self.textswitch = 1
                self.timer = 0
        WINDOW.blit(self.textobj.draw(space=(self.descsize,64)),(44,692),(self.pos,0,self.pos+524,64))
        print(self.pos,self.timer)
        try:
            img, handle = Assets.Load(self.specialList[Menu.listitem],createifnotfound=(True,pygame.image.load(specialdict[self.specialList[Menu.listitem]]['img']).convert_alpha()))
        except Exception:
            img = None
            handle = ""
        if img == None:
            img = pygame.Surface((16,16))
        WINDOW.blit(pygame.image.load("assets/notebookpaper.png").convert_alpha(),(564,524),(100,0,394,196))
        WINDOW.blit(img,(564,524),(0,0,394,196))
        if self.backbtn.draw():
            Game.substate = ""
        return False, []

SpecialListObj = SpecialList()

def InputGather():
    """
    Gathers most of the inputs. All Game.eventqueue things should be moved here someday or another. But Game.eventqueue will never truly vanish, will it?
    """
    # NOTE: updated 2025-10-28 to implement a missing feature
    Game.inputs['mPos']['pos'] = pygame.mouse.get_pos()
    mclicks = pygame.mouse.get_pressed()
    mjustclicked = pygame.mouse.get_just_pressed()
    for input in Game.inputs:
        if input.startswith("m"):
            if input == "mLMB":
                Game.inputs[input]['pressed'] = mclicks[0]
                Game.inputs[input]['justDown'] = mjustclicked[0]
            elif input == "mRMB":
                Game.inputs[input]['pressed'] = mclicks[1]
                Game.inputs[input]['justDown'] = mjustclicked[1]
        else:
            if Game.inputs[input]['justDown'] == True:
                Game.inputs[input]['justDown'] = False
            for event in Game.eventqueue:
                if event.type == KEYDOWN:
                    for key in Game.inputs[input]['keys']:
                        if event.key == key:
                            Game.inputs[input]['pressed'] = True
                            Game.inputs[input]['justDown'] = True
                            break
                if event.type == KEYUP:
                    for key in Game.inputs[input]['keys']:
                        if event.key == key:
                            Game.inputs[input]['pressed'] = False
                            Game.inputs[input]['justDown'] = False
                            break



def menu():
    global WINDOW_HEIGHT
    global WINDOW_WIDTH
    global scaleH
    global scaleW
    global resscale
    global FULLSCREENSWITCH
    global language
    # TODO: i don't really know where to leave this at but add a tutorial and a way to remap binds or controls
    # TODO: also add controller support
    # TODO: also add mobile support
    # TODO: also add scroll bars and scroll wheel and keyboard and right stick scrolling to everything that supports scrolling
    # NOTE: 2025-08-28: this menu system sucks so hard (but i made it 2 years ago so ok. rewrite when?)
    pygame.mixer.music.load('ost/menu_UNPOLISHED.wav')
    pygame.mixer.music.play(-1)
    Game.state = "Menu"
    while True:
        Game.eventqueue = pygame.event.get()
        InputGather()
        WINDOW.fill((30,30,30))
        WINDOW.blit(MenuLoad.bgmenuimg,(0,0))
        pygame.draw.rect(WINDOW,(0,0,0),(0,0,320 * scaleH,720 * scaleW))
        for event in Game.eventqueue:
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MENUCYCLEEVENT:
                Menu.cycle += 1
                if Menu.cycle > 720:
                    Menu.cycle = 0
        if Game.state == "Settings":
            if Game.inputs["kDown"]["justDown"] == True:
                pygame.mixer.Sound.play(Sounds.listscrollsfx)
                if Menu.selector != 7:
                    Menu.selector += 1
                else:
                    Menu.selector = 1
                if Menu.selector == 2:
                    Menu.selector = 3
                if Menu.selector == 4:
                    Menu.selector = 5
            elif Game.inputs["kUp"]["justDown"] == True:
                pygame.mixer.Sound.play(Sounds.listscrollsfx)
                if Menu.selector != 1:
                    Menu.selector -= 1
                else:
                    Menu.selector = 7
                if Menu.selector == 2:
                    Menu.selector = 1
                if Menu.selector == 4:
                    Menu.selector = 3
        if Game.inputs["kAccept"]["justDown"] == True:
            pygame.mixer.Sound.play(Sounds.selectsfx)
            if Game.state == "Menu":
                if Menu.selector == 4:
                    pygame.quit()
                    sys.exit()
                elif Menu.selector == 0:
                    Game.state = "Shop"
                    pygame.mixer.music.stop()
                    return("ENTER")
                elif Menu.selector == 1:
                    pygame.mixer.Sound.stop(Sounds.selectsfx)
                    pygame.mixer.Sound.play(Sounds.deniedsfx)
                elif Menu.selector == 2:
                    try:
                        open("settings.dat", 'x')
                    except Exception:
                        pass
                    Game.state = "Settings"
                    Menu.selector = 1
                elif Menu.selector == 3:
                    pygame.mixer.Sound.stop(Sounds.selectsfx)
                    pygame.mixer.Sound.play(Sounds.deniedsfx)
            if Game.state == "Settings":
                if Menu.selector == 7:
                    Game.state = "Menu"
                    Menu.selector = 0
                if Menu.selector == 6:
                    with open('settings.dat', 'w') as settingsfile:
                        # oh god it's happening again
                        # TODO: Try to find a better way to do this. If there is none, suffer.
                        # 2025-06-22: there is a way and it'll probably also improve performance
                        # problem is that i'd have to rewrite massive amounts of code
                        # it'd free up so much RAM thoooo :sob:
                        global blackbar
                        global whitebar
                        global urpglogo
                        global bgmenuimg
                        global resvar
                        global language
                        WINDOW_WIDTH = resvar[0]
                        WINDOW_HEIGHT = resvar[1]
                        scaleH = WINDOW_WIDTH / 1280
                        scaleW = WINDOW_HEIGHT / 720
                        MenuLoad.blackbar = pygame.image.load('assets/blacktribar.png').convert_alpha()
                        MenuLoad.whitebar = pygame.image.load('assets/whitetribar.png').convert_alpha()
                        MenuLoad.urpglogo = pygame.image.load('assets/urpglogo.png').convert_alpha()
                        MenuLoad.bgmenuimg = pygame.image.load('assets/internalmenuimg.png').convert_alpha()
                        MenuLoad.blackbarh = MenuLoad.blackbar.get_size()
                        MenuLoad.whitebarh = MenuLoad.whitebar.get_size()
                        MenuLoad.urpglogoh = MenuLoad.urpglogo.get_size()
                        MenuLoad.bgmenuimgh = MenuLoad.bgmenuimg.get_size()
                        MenuLoad.blackbar = pygame.transform.scale(MenuLoad.blackbar,(MenuLoad.blackbarh[0] * scaleW, MenuLoad.blackbarh[1] * scaleH)).convert_alpha()
                        MenuLoad.whitebar = pygame.transform.scale(MenuLoad.whitebar,(MenuLoad.whitebarh[0] * scaleW, MenuLoad.whitebarh[1] * scaleH)).convert_alpha()
                        MenuLoad.urpglogo = pygame.transform.scale(MenuLoad.urpglogo,(MenuLoad.urpglogoh[0] * scaleW, MenuLoad.urpglogoh[1] * scaleH)).convert_alpha()
                        MenuLoad.bgmenuimg = pygame.transform.scale(MenuLoad.bgmenuimg,(MenuLoad.bgmenuimgh[0] * scaleW, MenuLoad.bgmenuimgh[1] * scaleH)).convert_alpha()
                        if FULLSCREENSWITCH != True:
                            pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
                        else:
                            pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT), pygame.FULLSCREEN)
                        settingsfile.write(str(resvar) +  "," + str(Game.version) + "," + str(FULLSCREENSWITCH) + "," + language)
                        if language == "Spanish":
                            Menu.menuitems = [(("Iniciar Partida")),(("En Linea")),(("Configuración")),(("Mods")),(("Salir"))]
                        else:
                            Menu.menuitems = [(("Play")),(("Online")),(("Settings")),(("Mods")),(("Exit"))]
                        if language == "Spanish":
                            Menu.settingsitems = [(("Resolución")),(("{RESOLUTION}")),(("Pantalla Completa")),(("{CHECKBOX}")),(("Idioma")),(("{LANG}")),(("Guardar")),(("Volver"))]
                        else:
                            Menu.settingsitems = [(("Resolution")),(("{RESOLUTION}")),(("Fullscreen")),(("{CHECKBOX}")),(("Language")),(("{LANG}")),(("Save")),(("Back"))]
        if Game.inputs["kLeft"]["justDown"] == True:
            if Game.state == "Settings":
                if Menu.settingsitems[Menu.selector] == "{RESOLUTION}":
                    if resscale <= 0:
                        pygame.mixer.Sound.play(Sounds.deniedsfx)
                    else:
                        resscale -= 1
                if Menu.settingsitems[Menu.selector] == "{CHECKBOX}":
                    FULLSCREENSWITCH = False
                if Menu.settingsitems[Menu.selector] == "{LANG}":
                    if language == "Spanish":
                        language = "English"
                    else:
                        language = "Spanish"
        if Game.inputs["kRight"]["justDown"] == True:
            if Game.state == "Settings":
                if Menu.settingsitems[Menu.selector] == "{RESOLUTION}":
                    if resscale >= 11:
                        pygame.mixer.Sound.play(Sounds.deniedsfx)
                    else:
                        resscale += 1
                if Menu.settingsitems[Menu.selector] == "{CHECKBOX}":
                    FULLSCREENSWITCH = True
                if Menu.settingsitems[Menu.selector] == "{LANG}":
                    if language == "Spanish":
                        language = "English"
                    else:
                        language = "Spanish"
        if Game.state == "Menu":
            if Game.inputs["kDown"]["justDown"] == True:
                pygame.mixer.Sound.play(Sounds.listscrollsfx)
                if Menu.selector != 4:
                    Menu.selector += 1
                else:
                    Menu.selector = 0
            elif Game.inputs["kUp"]["justDown"] == True:
                pygame.mixer.Sound.play(Sounds.listscrollsfx)
                if Menu.selector != 0:
                    Menu.selector -= 1
                else:
                    Menu.selector = 4
            WINDOW.blit(MenuLoad.urpglogo,(30,0))
            for i in range(len(Menu.menuitems)):
                font = pygame.font.Font('fonts/RobotoMono-Regular.ttf', int(20 * scaleW))
                if Menu.menuitems[i] == "Online" or Menu.menuitems[i] == "En Linea" or Menu.menuitems[i] == "Mods":
                    text = font.render(Menu.menuitems[i],True,(120,120,120))
                else:
                    text = font.render(Menu.menuitems[i],True,(255,255,255))
                textRect = text.get_rect()
                textRect.x = int(35 * scaleH)
                textRect.y = int(i * (24 * scaleW) + (232 * scaleW) + 20 * scaleW) # three multipliers. wow. how ORIGINAL.
                WINDOW.blit(text,textRect)
        elif Game.state == "Settings":
            for i in range(len(Menu.settingsitems)):
                font = pygame.font.Font('fonts/RobotoMono-Regular.ttf', int(20 * scaleW))
                if Menu.settingsitems[i] == "{RESOLUTION}":
                    resvar = (WWresolutiontable[resscale], WHresolutiontable[resscale])
                    text = font.render(str(resvar[0]) + "x" + str(resvar[1]),True,(255,255,255))
                elif Menu.settingsitems[i] == "{CHECKBOX}":
                    if FULLSCREENSWITCH == True:
                        if language == "Spanish":
                            fsvar = "Si"
                        else:
                            fsvar = "Yes"
                    else:
                        fsvar = "No"
                    text = font.render(fsvar,True,(255,255,255))
                elif Menu.settingsitems[i] == "{LANG}":
                    if language == "Spanish":
                        langvar = "Español"
                    else:
                        langvar = "English"
                    text = font.render(langvar,True,(255,255,255))
                else:
                    text = font.render(Menu.settingsitems[i],True,(255,255,255))
                textRect = text.get_rect()
                textRect.x = int(35 * scaleH)
                textRect.y = int(i * (24 * scaleW) + (232 * scaleW) + 20 * scaleW)
                WINDOW.blit(text,textRect)
        wbary = Menu.cycle - 696
        bbary = Menu.cycle - 720
        WINDOW.blit(MenuLoad.whitebar,(320 * scaleH,wbary * scaleW))
        WINDOW.blit(MenuLoad.blackbar,(320 * scaleH,bbary * scaleW))
        pygame.draw.polygon(WINDOW,(255,255,255),(((20 * scaleH, (Menu.selector * (24 * scaleW) + (250 * scaleW) + 20 * scaleW)),(20 * scaleH, (Menu.selector * (24 * scaleW) + (240 * scaleW) + 20 * scaleW)),(30 * scaleH, (Menu.selector * (24 * scaleW) + (245 * scaleW) + 20 * scaleW)))))
        pygame.display.update()
        Game.dt = fpsClock.tick(FPS) / 1000
        Game.time_since_start += Game.dt

def main():
    # TODO: Clean this up, please. This is ugly as all hell, and could frankly do with a few recodes and fixes!
    global maag
    global enemyHolder
    enemyHolder.enemies = [Enemy() for i in range(random.randint(1,3))]
    enemyHolder.refresh()
    looping = True
    if party.load() == True:
        pass
    else:
        print("There wasn't a preexisting savefile - creating a new one.")
        party.save()
        Game.state = "Battle"
    # Battle Gameloop
    while looping:
        if Battle.turn < len(party.alive) and party.alive[Battle.turn] == False:
            Battle.turn += 1
        InputGather()
        Game.eventqueue = pygame.event.get()
        if Game.state == "Battle" or Game.state == "Victory" or Game.state == "Loss":
            WINDOW.blit(Battle.battlebg,(0,0))
            topop = []
            ParticleSpawner('assets/particle_square.png','RotatingRighttoLeftVariedXVariedScale',0,0,10,Battle.particles) # TODO: UGH NO NO HATE THIS REMAKE THIS RIGHT NOW
            for i in range(len(Battle.particles)):
                particle = Battle.particles[i]
                particle.draw()
                if particle.x < (-110 - particle.xoffset) * particle.scale or particle.x > (1390 + particle.xoffset) * particle.scale or particle.y < (-110 - particle.yoffset) * particle.scale or particle.y > (830 + particle.yoffset) * particle.scale:
                    topop.append(i)
            for i in range(len(topop)):
                index = topop[i - i]
                Battle.particles.pop(index)
            WINDOW.blit(Battle.battlefloor,(0,0))
            pygame.draw.rect(WINDOW,(20,20,20),(960 * scaleW,0 * scaleH,360 * scaleW,720 * scaleH))
            if Game.state == "Victory" or Game.state == "Battle":
                for i in range(len(party.partymembers)):
                    WINDOW.blit(party.partymembers[i].draw(),((0+i*100) * scaleW,(180+i*20) * scaleH))
            if Game.state == "Battle" or Game.state == "Loss":
                for i in range(len(enemyHolder.enemies)):
                    enemyanim = enemyHolder.enemies[i].animations["PTBIdle"] #obv a placeholder
                    WINDOW.blit(enemyanim,(600 * scaleW + i * 60, (450 * scaleH) - enemyHolder.enemies[i].animations["PTBIdle"].get_size()[1] + i * 30))
                    # what the hell was i on while making this
                    # no really did i miss the choccy milk powder and grab chocolate flavored crack or smth?
                    if Game.state != "Loss":
                        if len(DodgeObj.moves) > 0 and len(DodgeObj.moves[0]) != 0:
                            if i == DodgeObj.moves[DodgeObj.active][4]:
                                try:
                                    if DodgeObj.timer <= DodgeObj.moves[0][0]['timings']['atk'] + 10:
                                        # there was, in fact, a way
                                        enemyanimmask = pygame.mask.from_surface(enemyanim)
                                        fillsurf = pygame.surface.Surface(enemyanim.get_size()).convert_alpha()
                                        transparency = (DodgeObj.timer+1)/(DodgeObj.moves[0][0]['timings']['atk']-100)*128
                                        try:
                                            if DodgeObj.moves[0][0]['timings']['parry'][1] > DodgeObj.timer  > DodgeObj.moves[0][0]['timings']['parry'][1]:
                                                transparency = 180
                                        except Exception:
                                            if DodgeObj.timer + 180 > DodgeObj.moves[0][0]['timings']['atk'] + 10:
                                                transparency = 180
                                        try:
                                            fillsurf = enemyanimmask.to_surface(fillsurf,setcolor=(255,0,0,transparency),unsetcolor=(0,0,0,0))
                                        except Exception:
                                            fillsurf = enemyanimmask.to_surface(fillsurf,setcolor=(255,0,0,255),unsetcolor=(0,0,0,0))
                                        WINDOW.blit(fillsurf,(600 * scaleW + i * 60, (450 * scaleH) - enemyHolder.enemies[i].animations["PTBIdle"].get_size()[1] + i * 30))
                                except Exception:
                                    pass

            if Game.state == "Battle":
                if Battle.muson == False:
                    pygame.mixer.Sound.set_volume(Battle.music,25.0)
                    pygame.mixer.Sound.play(Battle.music,-1)
                    Battle.muson = True
        else:
            WINDOW.fill((20,20,20))
            Battle.muson = False
        # TODO: Does anything even use the Timer system? Deprecate.
        for i in range(len(Game.timers)):
            # Untuples the tuples.
            temp = Game.timers[i][0]
            temp2 = Game.timers[i][1]
            temp2 -= Game.dt # it's the equivalent to 1, ye? i think so
            Game.timers.pop(i)
            if temp2 <= 0:
                break
            Game.timers.append((temp,temp2)) # Thankfully we don't have to worry about order since we have the ID system in place
            gc.collect()
        # Buttony things
        if Battle.turn > party.membercount-1 and Game.substate != "Combo" or Game.substate == "moving":
            if len(Battle.playermovequeue) > 0:
                for move in Battle.playermovequeue.copy():
                    if move[0] == "atk":
                        attack(move[1],move[2])
                    elif move[0] == "spc":
                        if move[3] != "":
                            try:
                                Battle.combodata = move[3]
                                for category in weapontable:
                                    for i in range(len(category[1])):
                                        if category[0] == move[3][2]: # Holder should have the correct information if we've reached this state.
                                            move[3][0] = category[6]
                                            break
                                Game.substate = "Combo"
                                combos[move[3][0]].__init__(target=Battle.sendto)
                                move[3] = ""
                                break # we break free of the loop at that moment to enter combos
                            except Exception:
                                TerminalObj.add("DBG: Something went wrong. [TARGET COMBO INIT]")
                                Game.substate = ""
                    elif move[0] == "def":
                        # TODO: implement defense button
                        pass
                    Battle.playermovequeue.remove(move)
            else:
                if len(DodgeObj.moves) > 0 and Game.substate != "dodge": # yes this is stupid. yes it works. idgaf bout stupidity now
                    DodgeObj.moves = []
                if len(DodgeObj.moves) == 0 and Game.substate != "dodge":
                    Game.substate = "dodge"
                    for i in range(len(enemyHolder.enemies)):
                        movequeuer()
                        Battle.run = ""
                else:
                    Battle.turn = 0
        if Game.state == "Battle":
            # TODO: Add a selector here for controllers and keyboards alike.
            if Game.substate == "":
                if atkbtn.draw():
                    Game.substate = "Targeter"
                    Battle.run = "atk"
                if defbtn.draw():
                    print("defense")
                    pygame.mixer.Sound.play(Sounds.selectsfx)
                    Battle.playermovequeue.append(["def",Battle.turn,-1])
                    Battle.turn += 1
                if itmbtn.draw():
                    print("item")
                    pygame.mixer.Sound.play(Sounds.selectsfx)
                    Game.substate = "Item"
                if spcbtn.draw():
                    for category in weapontable:
                        for i in range(len(category[1])):
                            if category[1][i][0] == party.partymembers[Battle.turn].weapon:
                                Game.substate = "SpecialList"
                                Menu.listitem = 0
                                # moving things to their own objects is actually pretty cool if
                                # i do say so myself
                                speciallist = []
                                for category in weapontable:
                                    for i in range(len(category[1])):
                                        if category[1][i][0] == party.partymembers[Battle.turn].weapon:
                                            print(category[1][i])
                                            speciallist = category[1][i][7]
                                SpecialListObj.__init__(speciallist)
                                break
                            elif i > len(weapontable):
                                TerminalObj.add(party.partymembers[Battle.turn].name + " " + "doesn\'t have a weapon with special attacks equipped.")
                                pygame.mixer.Sound.play(Sounds.deniedsfx)
                                Game.substate = ""
            elif Game.substate == "Combo":
                #try:
                    pygame.draw.rect(WINDOW,(30,30,30),(0*scaleW,520*scaleH,960*scaleW,240*scaleH))
                    dmg = combos[Battle.combodata[0]].draw()
                    if dmg != False:
                        weapmulti = 1
                        for category in weapontable:
                            for weaponsel in category[1]:
                                if weaponsel[0] == Battle.combodata[2]: # TODO: Read from stats and actually get those working.
                                    print(weaponsel)
                                    weapmulti = weaponsel[6][5] / 10
                        attack(Battle.playermovequeue[0][1],Battle.playermovequeue[0][2],dmg*weapmulti*Battle.combodata[1])
                        Game.substate = "moving"
                #except Exception:
                #    Game.substate = ""
                #    pygame.mixer.Sound.play(Sounds.deniedsfx)
                #    TerminalObj.add("DBG: Something went wrong. [/IN COMBO SUBSTATE/]")
            elif Game.substate == "Targeter":
                try:
                    btnimg = pygame.Surface((96 * scaleW,32 * scaleH)).convert_alpha()
                    btnimg.fill((0,0,0,0))
                    pygame.draw.rect(btnimg,(255,255,255),(24 * scaleW,0 * scaleH,72 * scaleW,32 * scaleH))
                    pygame.draw.polygon(btnimg,(255,255,255),[(0 * scaleW,32 * scaleH),(24 * scaleW,32 * scaleH),(24 * scaleW,0 * scaleH)])
                    btnimg.blit(font.render("Back",True,(0,0,0)),(28 * scaleW,4 * scaleH))
                    backbtn = Button(864*scaleW,488*scaleH,btnimg)
                    if backbtn.draw() == True:
                        Game.substate = ""
                    # NOTE: we gotta reimplement this ASAP
                    for i in range(len(enemyHolder.enemies)):
                        if enemyHolder.btns[i].draw() == True:
                            Battle.sendto = i
                            pygame.mixer.Sound.play(Sounds.selectsfx)
                            if Battle.run == "atk":
                                Battle.playermovequeue.append(["atk",Battle.turn,Battle.sendto])
                            elif Battle.run == "spc":
                                Battle.playermovequeue.append(["spc",Battle.turn,Battle.sendto,Battle.combodata])
                            Battle.turn += 1
                            Game.substate = ""
                except IndexError:
                    # that means an enemy died and we tried to render; we can pass
                    # NOTE: NO NO NO WE CANNOT PASS WHAT THE FUCK DID I SMOKE THIS CAN CAUSE SOME HELLISH ERRORS WE GOTTA FIX THIS :sob:
                    # actually this isn't even handled by this anymore i think :/
                    pass
            elif Game.substate == "dodge":
                attained = DodgeObj.draw()
                state = attained[0]
                data = attained[1:]
                print(state, data)
                if state == -2:
                    TerminalObj.add("[B]Something has gone CATASTROPHICALLY wrong.")
                    if Battle.sendto >= len(enemyHolder.enemies):
                        Game.substate = ""
                    else:
                        pass # We used to call movequeuer here but that's uhh BAD
                elif state == 0:
                    enemyAttack(data[0][5],data[0][4],data)
                elif state == 1:
                    TerminalObj.add("[I]" + party.partymembers[data[0][5]].name + " blocked the attack.")
                    neodata = []
                    neodata.append((data[0][0],data[0][1],data[0][2],data[0][3]/2,data[0][4],data[0][5]))
                    enemyAttack(data[0][5],data[0][4],neodata)
                elif state == 2:
                    TerminalObj.add("[B]" + party.partymembers[data[0][5]].name + " countered the attack!")
                    pygame.mixer.Sound.play(Sounds.parrysfx)
                    attack(data[0][5],data[0][4],data[0][3]/10)
                if state >= 0:
                    DodgeObj.timer = 0
                    DodgeObj.finishtime = -1
                    if DodgeObj.active < len(DodgeObj.moves) - 1:
                        DodgeObj.active += 1
                    else:
                        Game.substate = ""
            elif Game.substate == "SpecialList":
                state, data = SpecialListObj.draw()
                if state != False:
                    Game.substate = "Targeter"
                    Battle.run = "spc"
                    TerminalObj.add("Choose a target...") # TODO: Add multi-target attack support.
                    # also we should really move the battle code to a battle object this is hecc
                    Battle.combodata = data
        if Game.state == "Victory" and Game.inputs["kAccept"]["justDown"] == True:
            Game.state = "Shop"
            enemyHolder.enemies = [Enemy() for i in range(random.randint(1,3))]
            enemyHolder.refresh()
            TerminalObj.textlist = []
        if Game.state == "Loss" and Game.inputs["kAccept"]["justDown"] == True:
            party.load()
            Game.state = "Shop"
            enemyHolder.enemies = [Enemy() for i in range(random.randint(1,3))]
            enemyHolder.refresh()
            TerminalObj.textlist = []
        for event in Game.eventqueue:
            if event.type == QUIT:
                exit()
            if event.type == KEYDOWN and event.key == K_F3 and Game.debug == True:
                Game.cheatstates['dbgOpen'] = not Game.cheatstates['dbgOpen']

        # Rendering most things
        # TODO: Create a new rendering pipeline, to handle an OpenGL and a Software renderer

        WINDOW.blit(TerminalObj.draw(decopos=(10,10)),(960,0))
        if Game.substate == "Item":
            InvObj.draw()
        if Game.state == "Battle":
            i = 0
            for partymember in party.partymembers:
                offset = 10
                if i == Battle.turn:
                    offset = 0
                pygame.draw.rect(WINDOW,(30,30,30),((6+ 288*i) * scaleW,(464+ offset) * scaleH,278 * scaleW, (56-offset) * scaleH))
                pygame.draw.rect(WINDOW,(255,255,255),((12+ 288*i) * scaleW,(470+ offset) * scaleH,266 * scaleW, (50-offset) * scaleH))
                mcdholder = maximum_common_divisor(4,partymember.hpmax)
                pygame.draw.rect(WINDOW,(30,30,30),((15+ 288*i) * scaleW,(495+ offset) * scaleH,(partymember.hpmax * mcdholder * scaleW) / 1.55, (20-0.5*offset) * scaleH))
                hprect = pygame.Rect((15+ 288*i) * scaleW,(495+ offset) * scaleH,(partymember.hp * mcdholder * scaleW) / 1.55, (20-(0.5*offset)) * scaleH)
                pygame.draw.rect(WINDOW,(200,0,0),((10+ 288*i) + (partymember.hp * mcdholder * scaleW) / 1.55 ,(495+ offset) * scaleH,(partymember.hpbaraltw * mcdholder * scaleW) / 1.55, (20-offset) * scaleH))
                pygame.draw.rect(WINDOW,(255,0,0), hprect)
                WINDOW.blit(partymember.hpimage, ((15+ 288*i) * scaleW, (450+ offset) * scaleH))
                WINDOW.blit(Battle.hpicon,((17+ 288*i) * scaleW,(497+offset) * scaleH),(0,0,16,16-(0.3*offset)))
                amountblitted = 0
                for effect in partymember.effects:
                    WINDOW.blit(pygame.transform.scale_by(effectdict[effect[0]][0],scaleW),(amountblitted * 25 + 15 + 288*i, 470+offset))
                    amountblitted += 1
                pygame.draw.line(WINDOW,(30,30,30),((6+ 288*i) * scaleW,519 * scaleH),((283+ 288*i) * scaleW,519 * scaleH))
                i += 1
            # NOTE: REMAKE ALL OF THE HEALTH CODE!
            for i in range(len(enemyHolder.enemies)):
                scale = 250 / enemyHolder.enemies[i].stats[0]
                pygame.draw.rect(WINDOW,(30,30,30),((6 + i * 300) * scaleW,0 * scaleH,278 * scaleW, 56 * scaleH))
                pygame.draw.rect(WINDOW,(255,255,255),((12 + i * 300) * scaleW,0 * scaleH,266 * scaleW, 50 * scaleH))
                ehprect = pygame.Rect((15 + i * 300) * scaleW,6 * scaleH,(enemyHolder.enemies[i].hp * scale * scaleW),15 * scaleH)
                pygame.draw.rect(WINDOW,(0,255,0),ehprect)
                WINDOW.blit(pygame.transform.scale(pygame.image.load('assets/enemyhpicon.png'),(pygame.image.load('assets/enemyhpicon.png').get_size()[0] * scaleH, pygame.image.load('assets/enemyhpicon.png').get_size()[1] * scaleW)),((16 + i * 300) * scaleW,7 * scaleH))
                WINDOW.blit(enemyHolder.enemies[i].icon, ((15 + i * 300) * scaleW, 45 * scaleH))
        for i in range(len(party.partymembers)):
            if party.partymembers[i].hp > party.partymembers[i].hpmax:
                party.partymembers[i].hp = party.partymembers[i].hpmax
            elif party.partymembers[i].hp <= 0 and party.partymembers[0].items[5] > 0:
                TerminalObj.add(party.partymembers[i].name + " almost died!")
                TerminalObj.add("Revived by an ALARMCLOCK.")
                party.partymembers[0].hp = int(party.partymembers[0].hpmax / 2)
                party.partymembers[0].items[5] -= 1
            elif party.partymembers[i].hp <= 0 and party.alive[i] == True:
                TerminalObj.add("[I]" + party.partymembers[i].name + " has fallen.")
                party.alive[i] = False
                party.partymembers[i].hp = 0
        # Win/Lose Conditions
        if party.alive.count(True) <= 0 and party.partymembers[0].items[5] <= 0 and Game.state == "Battle":
            Game.state = "Loss"
            Game.substate = ""
            DodgeObj.moves = []
            TerminalObj.add("You lost...")
            TerminalObj.add("Press [/SPACE/][N] to reload your save file.")
            pygame.mixer.Sound.fadeout(Battle.music,333)
            DodgeObj.__init__()
        elif party.alive.count(True) == 0 and party.partymembers[0].items[5] > 0:
            pass # they're gonna revive soon if they haven't already
        elif enemyHolder.hp <= 0 and Game.state == "Battle":
            Game.state = "Victory"
            Game.substate = ""
            DodgeObj.moves = []
            for i in range(len(party.partymembers)):
                party.alive[i] = True
                party.partymembers[i].animqueue = [] # wiping it here should do for now.
                oldhp = party.partymembers[i].hp
                party.partymembers[i].hp += random.randint(10,30)
                party.partymembers[i].hpbaraltpos += party.partymembers[i].hp - oldhp
                TerminalObj.add(party.partymembers[i].name + "recovered " + str(party.partymembers[i].hp-oldhp) + " HP.")
            TerminalObj.add("You win!")
            party.partymembers[0].gold += enemyHolder.gold 
            TerminalObj.add("Got " + str(enemyHolder.gold) + " Nuggets.")
            pygame.mixer.Sound.fadeout(Battle.music,333)
            pygame.mixer.Sound.play(pygame.mixer.Sound("ost/GG.mp3"))
            TerminalObj.add("Press [/SPACE/][N]​  ​[N]to continue.") # TODO: Replace that with the "Continue" key.
        if party.partymembers[0].hpbaraltw > 0 and int(fpsClock.get_fps()) % 5 == 0:
            party.partymembers[0].hpbaraltw -= 1
        if Game.state == "Shop":
            ShopLinkerObj.draw()
        if Game.state == "Rooms":
            looping = False
        if Game.cheatstates['dbgOpen'] == True:
            WINDOW.blit(font.render("> " + DebugObj.inputbuffer,True,(255,255,255)),(960,696))
            for event in Game.eventqueue:
                if event.type == KEYDOWN and event.key != K_RETURN and event.key != K_BACKSPACE:
                    DebugObj.inputbuffer += event.unicode
                elif event.type == KEYDOWN and event.key == K_BACKSPACE:
                    DebugObj.inputbuffer = DebugObj.inputbuffer[:-1]
                elif event.type == KEYDOWN and event.key == K_RETURN:
                    DebugObj.cmds(DebugObj.inputbuffer)
                    DebugObj.inputbuffer = ""
        pygame.display.update()
        Game.dt = fpsClock.tick(FPS)
        Game.milidt = Game.dt / 1000
        Game.dt /= 60
        Game.time_since_start += Game.dt
        if maag == True and Game.inputs["mLMB"]["pressed"] is False:
            maag = False
        elif Game.inputs["mLMB"]["pressed"] == True:
            maag = True
while True:
    if Game.state == "Menu" or Game.state == "Settings":
        menu()
    elif Game.state == "Rooms":
        # I should probably also make a function for this. Whelp.
        Game.eventqueue = pygame.event.get()
        InputGather()
        for event in Game.eventqueue:
            if event.type == QUIT:
                exit()
        RoomObjData = RoomHandler.draw()
        WINDOW.blit(RoomObjData[0],RoomObjData[1]) # apparently one can't unpack a tuple into WINDOW.blit. or at least I couldn't. idk can someone try and save some ram
        WINDOW.blit(TerminalObj.draw(decopos=(10,10)),(960,0))
        if NoteInfo.openNotebookButton.draw():
            if Game.substate != "Notebook":
                Game.substate = "Notebook"
            else:
                Game.substate = ""
        if Game.substate == "Notebook": # TODO: pause game while in notebook UI
            data = NotebookObj.draw()
            WINDOW.blit(data[0],data[1])
        pygame.display.update()
        Game.milidt = fpsClock.tick(FPS) / 1000
        if maag == True and Game.inputs["mLMB"]["pressed"] is False:
            maag = False
        elif Game.inputs["mLMB"]["pressed"] == True:
            maag = True
    else:
        main()
