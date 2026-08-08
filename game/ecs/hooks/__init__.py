HOOK_REGISTRY = {}
#--------------------------------#
def hook(component:object):
    #--------------------------------#
    def wrapper(func):
        #--------------------------------#
        HOOK_REGISTRY[component] = func
        return func
    #--------------------------------#
    return wrapper
