"""
Meant to be ran inside the Notebook system.
"""
for armor in armortable: # type:ignore
    if armor[0] == party.partymembers[self.extradata[0]].armor:# type:ignore
        self.imgdata = pygame.transform.scale_by(armor[1],0.5)# type:ignore
    else:
        self.imgdata = pygame.transform.scale_by(pygame.image.load("assets/shop/badges/badge_nobadge.png").convert_alpha(),0.5)#type:ignore