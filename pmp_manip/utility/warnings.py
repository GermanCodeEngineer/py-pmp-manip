class MANIP_Warning(UserWarning): pass

###############################################################
#                WARNINGS FOR THE EXT INFO GEN                #
###############################################################

class MANIP_UnexpectedPropertyAccessWarning(MANIP_Warning): pass
class MANIP_UnexpectedNotPossibleFeatureWarning(MANIP_Warning): pass


__all__ = ["MANIP_Warning", "MANIP_UnexpectedPropertyAccessWarning", "MANIP_UnexpectedNotPossibleFeatureWarning"]

