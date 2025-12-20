"""
Meant to be ran inside the Notebook system.
"""
for weapon in weapontable: # type:ignore
    if weapon[0] == party.partymembers[self.extradata[0]].weapon:# type:ignore
        self.imgdata = pygame.transform.scale_by(weapon[1],0.5)# type:ignore
    else:
        self.imgdata = pygame.transform.scale_by(pygame.image.load("assets/shop/badges/badge_nobadge.png").convert_alpha(),0.5)#type:ignore