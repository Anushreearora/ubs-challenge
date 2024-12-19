import json
import math
import sys

# Function to calculate Euclidean distance
def euclid_dist(school_loc, home_loc):
    return math.dist(school_loc, home_loc)

# Function to calculate weightings
def weightings(school, student):
    dist = euclid_dist(school['location'], student['homeLocation'])
    weight = (1 / (1 + dist)) * 50

    if 'alumni' in student and school['name'] == student['alumni']:
        weight += 30
    
    if 'volunteer' in student and school['name'] == student['volunteer']:
        weight += 20
    
    return weight

# Main function
def main(input_file):
    with open(input_file, 'r') as file:
        data = json.load(file)

    # Allocate students to schools
    allocations = {school['name']: [] for school in data['schools']}

    for school in data['schools']:
        weighted_students = []
        for student in data['students']:
            weighting = weightings(school, student)
            weighted_students.append((student['id'], weighting))

        # Sort students by weightings and by ID if weightings are equal
        weighted_students.sort(key=lambda x: (-x[1], x[0]))

        # Allocate students until the school's max allocation is reached
        for student_id, _ in weighted_students:
            if len(allocations[school['name']]) < school['maxAllocation']:
                # Check if the student is already allocated
                allocated = any(student_id in alloc for alloc in allocations.values())
                if not allocated:
                    allocations[school['name']].append(student_id)

    output = [{school: students} for school, students in allocations.items()]

    # Save the output to output.json
    with open('output.json', 'w') as outfile:
        json.dump(output, outfile, separators=(',', ':'))

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python main.py input.json")
    else:
        input_file = sys.argv[1]
        main(input_file)

'''Assumptions:
1. Allocations are assigned at the time of calculating all the students' weightings for that particular school, not once all the schools' weightings are calculated. 
2. If a student has been allocated already to a school, then even if they top the list for another school they cannot be allocated. 
3. A school's maxAllocation can be greater than 1. 
4. The total maxAllocations for all the school cannot exceed the number the students. 
'''

