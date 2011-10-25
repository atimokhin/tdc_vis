
def tdc_get_bound_index(val, array):
    """
    return largest index idx of the element in array
    such that array[idx] <= val
    ---> if val<array[0] => idx=0
    """
    if val >= array[-1]:
        idx = len(array)-1
    else:
        idx = ( idx for idx,entry in enumerate(array) if entry>val ).next()-1 
    return max(0,idx)
