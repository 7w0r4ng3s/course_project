# this version only works with subjects with all lower, upper, and graduate 
# or the index out of range error will happen in code block 6
import urllib.request
from bs4 import BeautifulSoup
import csv
import os

# url of ucsc computer science courses & description page
# can be modified by changing the subject tag name before .html
url = 'https://registrar.ucsc.edu/catalog/programs-courses/course-descriptions/cmps.html'
# read the url and parse the page using BeautifulSoup html parser
page = urllib.request.urlopen(url)
soup = BeautifulSoup(page, 'html.parser')
# get the div of course title and description
course = str(soup.find('div', attrs={'class':'content contentBox'}))

# get the subject tag name
course_type = url[url.find('course-descriptions/')+20:url.find('.html')]
course = course.replace('\n', '')

# divide the string into lower/upper/graduate class and remove useless title
# which os course_dic[0]
course_div = course.split('<h2>')

# remove the useless info
course_div = course_div[1:]


def remove_html_tags(text):
    ''' remove html tags from a string '''
    import re
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)


def make_dict(title, description):
	''' make a dictionary using two lists '''
    return dict(zip(title, description))


def write_csv(dictionary, name):
	''' write a csv file using a dictionary '''
    with open(f'{name}.csv', 'w') as csv_file:
        writer = csv.writer(csv_file)
        for key, value in dictionary.items():
            writer.writerow([key, value])


# lower division courses
lower_div = course_div[0].split('</h2>')
lower_div[1] = lower_div[1].split('<br/> <br/>')
# upper division courses
upper_div = course_div[1].split('</h2>')
upper_div[1] = upper_div[1].split('<br/> <br/>')
# graduate courses
graduate = course_div[2].split('</h2>')
graduate[1] = graduate[1].split('<br/> <br/>')


lower_list = lower_div[1]
upper_list = upper_div[1]
graduate_list = graduate[1]

# remove html tags
for i in range(len(lower_list)):
    lower_list[i] = remove_html_tags(lower_list[i]).lstrip()
    
for i in range(len(upper_list)):
    upper_list[i] = remove_html_tags(upper_list[i]).lstrip()
    
for i in range(len(graduate_list)):
    graduate_list[i] = remove_html_tags(graduate_list[i]).lstrip()

print(f'Lower division: {len(lower_list)} courses')
print(f'Upper division: {len(upper_list)} courses')
print(f'Graduate: {len(graduate_list)} course')

# remmove all whitespaces and check the lengths of title and description are the same
lower_title = [i[:i.find('  ')] for i in lower_list]
lower_des = [i[i.find('  '):].lstrip() for i in lower_list]
assert len(lower_title) == len(lower_des)

upper_title = [i[:i.find('  ')] for i in upper_list]
upper_des = [i[i.find('  '):].lstrip() for i in upper_list]
assert len(upper_title) == len(upper_des)

graduate_title = [i[:i.find('  ')] for i in graduate_list]
graduate_des = [i[i.find('  '):].lstrip() for i in graduate_list]
assert len(graduate_title) == len(graduate_des)

lower_dict = make_dict(lower_title, lower_des)
upper_dict = make_dict(upper_title, upper_des)
graduate_dict = make_dict(graduate_title, graduate_des)

os.chdir('courses')
os.mkdir(course_type)
os.chdir(course_type)
write_csv(lower_dict, 'lower_div')
write_csv(upper_dict, 'upper_div')
write_csv(graduate_dict, 'graduate')