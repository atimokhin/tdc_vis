from select_particle        import      Select_Particle
from operator               import      itemgetter

"""
Module for handling all searching
"""
def index_search(idts_array, ID_array, idts, ID):
    """
    Returns index of particle with matching idts and ID.
    Returns None if no matching particle found
    """
    for i in range(0,len(idts_array)):
        if idts[i] == idts and ID_array[i] == ID:
            return i
    print "particle with idts %i and ID %i not found" %(idts, ID)
    return None            
def quick_search(idts_array, ID_array, update, select_list):
    """
    Checks that particles remain at same index in ID and idts arrays
    Returns dict with idts/ID keys and index of particle (-1 if not found)
    """
    index_list = {}
    for key in update:
        index_guess = select_list[key].index
        try:
            if key[0] == idts_array[index_guess] and key[1]==ID_array[index_guess]:
                index_list[key]=index_guess
                print str(key) + " found with static quick_read."
            else:
                index_list[key]=-1
        except IndexError:
            index_list[key]=-1
    return index_list
        
def lin_search(idts_array, ID_array, update):
    """
    Linear search of data. Sorts update by idts
    Returns dict with idts/ID keys and index of particle (-1 if not found)
    """
    update = sorted(update, key = itemgetter(0))
    index_list = {}
    temp = update[:]
    for i in range(0,len(idts_array)):
        for key in update:
            if key[0] == idts_array[i] and key[1] == ID_array[i]:
                print "match at index %i with idts %i=%i and ID %i = %i" \
                            %(i, key[0], idts_array[i], key[1], ID_array[i])
                index_list[key]=i
                try:                
                    temp.remove(key)
                #should not occur
                except ValueError:
                    print "ValueError, particle " + str(key) + "not removed."
            elif key[1]>idts_array[i]:
                break
        if len(temp)==0:
            print "terminated search at index ", i
            break
    update = temp[:]
    #deals with destroyed particles
    if len(update)>0:
        for key in update:
            print "(idts, ID) %s not found" %(str(key))
            index_list[key]=-1
            temp.remove(key)
    #Checks that all particles are dealt with. Message should never appear
    if len(temp) != 0:
        print "failed to sort using lin_read"
    return index_list
        
def bin_search(idts_array, ID_array, update):
    """
    Reads and searches data using recursive binary search. Sorts sort_array by idts
    Returns dict with idts/ID keys and index of particle (-1 if not found)
    """
    #sorts by ID
    sort_array = zip(idts_array, ID_array, range(0,len(idts_array)))
    sort_array = sorted(sort_array, key = itemgetter(0))
    index_list = {}
    for key in update:
        index_list[key] = bin_recursion(sort_array,key)
    return index_list
def bin_recursion(sort_array, key):
    """
    Actual recursive algorithm used by bin_search
    """
    if len(sort_array) == 0:
        print str(key) + " not found."
        return -1
    test_index = len(sort_array)/2
    if key[0] == sort_array[test_index][0] and key[1]==sort_array[test_index][1]:
        print str(key)+ "found using bin_read."
        idx = sort_array[test_index][2]
    elif key[0]<sort_array[test_index][0]:
        idx = bin_recursion(sort_array[0:test_index], key)
    else:
        idx = bin_recursion(sort_array[test_index+1:], key)
    return idx