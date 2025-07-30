class PP_Warning(UserWarning): pass

###############################################################
#                WARNINGS FOR THE EXT INFO GEN                #
###############################################################

class PP_UnexpectedPropertyAccessWarning(PP_Warning): pass
class PP_UnexpectedTemplateLiteralWarning(PP_Warning): pass


__all__ = ["PP_Warning", "PP_UnexpectedPropertyAccessWarning", "PP_UnexpectedTemplateLiteralWarning"]

