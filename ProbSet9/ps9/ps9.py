# 6.00 Problem Set 9
#
# Intelligent Course Advisor
#
# Name:
# Collaborators:
# Time:
#

SUBJECTS_FILENAME = "subjects.txt"
SHORT_SUBJECTS_FILENAME = "shortened_subjects.txt"
VALUE, WORK = 0, 1

#
# Problem 1: Building A Subject Dictionary
#
def loadSubjects(filename):
    """
    Returns a dictionary mapping subject name to (value, work), where the name
    is a string and the value and work are integers. The subject information is
    read from the file named by the string filename. Each line of the file
    contains a string of the form "name,value,work".

    returns: dictionary mapping subject name to (value, work)
    """

    # The following sample code reads lines from the specified file and prints
    # each one.
    subjects = {}
    inputFile = open(filename)
    for line in inputFile:
        line = line.strip()
        line = line.split(",")
        subjects[line[0]] = (int(line[1]), int(line[2]))
    return subjects

def printSubjects(subjects):
    """
    Prints a string containing name, value, and work of each subject in
    the dictionary of subjects and total value and work of all subjects
    """
    totalVal, totalWork = 0,0
    if len(subjects) == 0:
        return 'Empty SubjectList'
    res = 'Course\tValue\tWork\n======\t=====\t====\n'
    subNames = subjects.keys()
    subNames.sort()
    for s in subNames:
        val = subjects[s][VALUE]
        work = subjects[s][WORK]
        res = res + s + '\t' + str(val) + '\t' + str(work) + '\n'
        totalVal += val
        totalWork += work
    res = res + '\nTotal Value:\t' + str(totalVal) +'\n'
    res = res + 'Total Work:\t' + str(totalWork) + '\n'
    print res

#
# Problem 2: Subject Selection By Greedy Optimization
#

def cmpValue(subInfo1, subInfo2):
    """
    Returns True if value in (value, work) tuple subInfo1 is GREATER than
    value in (value, work) tuple in subInfo2
    """
    if subInfo1[0] > subInfo2[0]:
        return True
    return False

def cmpWork(subInfo1, subInfo2):
    """
    Returns True if work in (value, work) tuple subInfo1 is LESS than than work
    in (value, work) tuple in subInfo2
    """
    if subInfo1[1] < subInfo2[1]:
        return True
    return False

def cmpRatio(subInfo1, subInfo2):
    """
    Returns True if value/work in (value, work) tuple subInfo1 is 
    GREATER than value/work in (value, work) tuple in subInfo2
    """
    if (subInfo1[0]/float(subInfo1[1])) > (subInfo2[0]/float(subInfo2[1])):
        return True
    return False

def greedyAdvisor(subjects, maxWork, comparator):
    """
    Returns a dictionary mapping subject name to (value, work) which includes
    subjects selected by the algorithm, such that the total work of subjects in
    the dictionary is not greater than maxWork.  The subjects are chosen using
    a greedy algorithm.  The subjects dictionary should not be mutated.

    subjects: dictionary mapping subject name to (value, work)
    maxWork: int >= 0
    comparator: function taking two tuples and returning a bool
    returns: dictionary mapping subject name to (value, work)
    """
    
    courses = {}
    while count_work(subjects, courses) < maxWork:
        maxCourse, work = None, count_work(subjects, courses)
        for course_num in subjects.keys():
            if (course_num in courses.keys()) or ((subjects[course_num][1] + work) > maxWork):
                continue
            elif maxCourse == None:
                maxCourse = course_num
                continue
            if comparator(subjects[course_num], subjects[maxCourse]) is True:
                maxCourse = course_num
        if maxCourse == None:
            break
        else:
            courses[maxCourse] = subjects[maxCourse]
            work += subjects[maxCourse][1]
    return courses


#
# Problem 3: Subject Selection By Brute Force
#
def bruteForceAdvisor(subjects, maxWork):
    """
    Returns a dictionary mapping subject name to (value, work), which
    represents the globally optimal selection of subjects using a brute force
    algorithm.

    subjects: dictionary mapping subject name to (value, work)
    maxWork: int >= 0
    returns: dictionary mapping subject name to (value, work)
    """
    course_numbers = sort_by_work(subjects, subjects.keys())
    course_numbers.reverse()
    maxCourses = recursive(subjects, course_numbers, maxWork)
    return maxCourses

def recursive(subjects, course_numbers, maxWork, courses = {}):
    if count_work(subjects, courses) == maxWork or len(course_numbers) == 0:
        return courses
    
    courses_with = courses.copy()
    courses_with[course_numbers[0]] = subjects[course_numbers[0]]
    if count_work(subjects, courses_with) > maxWork:
        return courses

    taking = recursive(subjects, course_numbers[1:], maxWork, courses_with)
    not_taking = recursive(subjects, course_numbers[1:], maxWork, courses)
    if compare_value(subjects, taking, not_taking):
        return taking
    else:
        return not_taking

def sort_by_work(subjects, course_numbers):
    """
    Sorts courses highest work first
    Courses with the same levels of work are sorted highest value to lowest.
    """    
    courses = []
    for i in range(20, 0, -1):
        temp = []
        for num in course_numbers:
            if i == subjects[num][1]:
                temp.append(num)
        sort_by_value(subjects, temp)
        courses.extend(temp)
    return courses

def sort_by_value(subjects, course_numbers):
    """
    Sort highest value to lowest.
    """
    courses = []
    for i in range(20, 0, -1):
        temp = []
        for num in course_numbers:
            if i == subjects[num][0]:
                courses.append(num)
    return courses

def count_work(subjects, courses):
    work = 0
    if len(courses) == 0:
        return work
    for key in courses.keys():
        work += subjects[key][1]
    return work

def count_value(subjects, courses):
    value = 0
    if len(courses) == 0:
        return value
    for course_num in courses.keys():
        value += subjects[course_num][0]
    return value

def compare_value(subjects, courses1, courses2):
    """
    returns True if: courses1 > courses2
    """
    value1, value2 = count_value(subjects, courses1), count_value(subjects, courses2)
    if value1 > value2:
        return True
    return False

def calc_years(num_subjects):
    """
    Returns years
    """
    x = 2 ** (num_subjects - 1)
    print x, 'calculations'
    ops, text = [10**6, 60, 60, 24, 365], ['seconds', 'minutes', 'hours', 'days', 'years']
    for i in range(5):
        x = round(x/float(ops[i]), 2)
        print x, text[i]

'Algorithmic efficiency:'
'Greedy algorithm: n**(max work/avg)'
'brute force: 2**(n-1)'

smallCatalog = loadSubjects(SHORT_SUBJECTS_FILENAME)
catalog = loadSubjects(SUBJECTS_FILENAME)
