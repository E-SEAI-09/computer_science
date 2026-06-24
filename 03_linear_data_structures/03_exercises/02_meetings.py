# Solution One
def can_attend_meetings(intervals):
    for i in range(len(intervals) - 1):
        for j in range(i + 1 ,len(intervals)):
            int_1_start = intervals[i][0]
            int_1_end = intervals[i][1]
            int_2_start = intervals[j][0]
            int_2_end = intervals[j][1]

            if (
                int_1_start >= int_2_start and int_1_start < int_2_end
            ) or (
                int_2_start >= int_1_start and int_2_start < int_1_end
            ):
                return False
            
    return True

# Solution Two
def can_attend_meetings_2(intervals):
    intervals.sort()

    for i in range(len(intervals) - 1):
        # if intervals[i + 1][0] < intervals[i][1]:
        # OR
        if intervals[i][1] > intervals[i + 1][0]:
            return False
    
    return True
