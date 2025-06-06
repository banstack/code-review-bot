# Hello.py: A sample python script used for testing reviews

def twoSum(array, targetSum):
    for i in range(0, len(array)):
        for j in range(i+1, len(array)):
            if array[i] + array[j] == targetSum:
                return ([array[i], array[j]])
        return []
    
twoSum([2,7,11,15], 9)
