"""
Meant to be ran inside the Notebook system.
"""
for badge in badgetable: # type:ignore
    if badge[0] == party.partymembers[self.extradata[0]].badges[self.extradata[1]]:# type:ignore
        self.imgdata = pygame.transform.scale_by(badge[1],0.5)# type:ignore
    else:
        self.imgdata = pygame.transform.scale_by(pygame.image.load("assets/shop/badges/badge_nobadge.png").convert_alpha(),0.5)#type:ignore