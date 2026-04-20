"""
Meant to be ran inside the Notebook system.
"""
completion = False
imgdatabackup = self.imgdata # type:ignore
while completion == False:
    for category in weapontable: # type:ignore
        for weapon in category[1]:
            if weapon[0] == party.partymembers[self.extradata[0]].weapon:# type:ignore
                self.imgdata = pygame.transform.scale_by(weapon[1],0.5)# type:ignore
                completion = True
    else:
        if self.imgdata == imgdatabackup: #type:ignore
            self.imgdata = pygame.transform.scale_by(pygame.image.load("assets/shop/badges/badge_nobadge.png").convert_alpha(),0.5)#type:ignore
            completion = True