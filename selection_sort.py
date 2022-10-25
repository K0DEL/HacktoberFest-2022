def selectionSort(arr):
    for y in range(len(arr)):
        min_idx = y
        for j in range(y+1, len(arr)):
            if arr[min_idx] &gt; arr[j]:
                 min_idx = j
    arr[y], arr[min_idx] = arr[min_idx], arr[y]
def insertionSort(arr):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i-1
        while j &gt;= 0 and key &lt; arr[j] :
            arr[j + 1] = arr[j]
            j -= 1
            arr[j + 1] = key
arr=[]
n = int(input(&quot;Enter the size:&quot;))
for i in range(n):
    arr.append(int(input(&quot;Enter the element:&quot;)))
selectionSort(arr)
# insertionSort(arr)
print (&quot;Sorted array:&quot;)
for i in range(len(arr)):
    print(arr[i],end=&quot; &quot;)