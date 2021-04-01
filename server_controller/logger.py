
class Logger():
    def __init__(this):
        this.SUPPRESS = False
        this.VERBOSE = False
        
    def logWarn(this, string):
        if not this.SUPPRESS:
            print("(WARN) " + string)

    def logInfo(this, string):
        if this.VERBOSE:
            print("(INFO) " + string)

