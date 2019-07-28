#!/usr/bin/python

import cgi
import numpy as np
import pandas as pd

print "content-type:text/html"
print""

val=cgi.FieldStorage();

# Getting the roll_no of student
r=val.getvalue('rollno')
p=val.getvalue('passwd')

# Changing roll_no in int data type
roll=int(r)
password=int(p)

df3=pd.read_excel('/home/bhagat/Downloads/user_password.xlsx')
get_pass=df3.set_index('Student_ID').loc[roll].tolist()[0]
#print(get_pass)


# In[91]:

# Extracting the Dataset_new.xlsx file and take it into df data frame
df=pd.read_excel('/home/bhagat/Downloads/Dataset_new.xlsx')
# df.head()

# In[92]:

# Extracting the Elective_DataSet.xlsx file and take it into df2 data frame
df2=pd.read_excel('/home/bhagat/Downloads/Elective_DataSet.xlsx').set_index('Student_ID')
# df2.head()

# In[93]:

# Applying pivot_table() method on Grade coloumn and getting grade_crosstab data frame
grade_crosstab=pd.pivot_table(data=df,values='Grade',index='Course_Code',columns='Student_ID')

# In[94]:

# Selecting grade_crosstab only for roll coloumn
roll_grade = grade_crosstab[roll]

# In[95]:

# Finding the correlation using corrwith method

similar_to_roll = grade_crosstab.corrwith(roll_grade)

corr_roll = pd.DataFrame(similar_to_roll, columns=['sim_grade'])

# In[96]:

# Filling the nan value with 0.0
corr_roll.fillna(value=0.0)

# In[97]

faculty_crosstab=pd.pivot_table(data=df,values='Faculty_rating',index='Course_Code',columns='Student_ID')

# In[98]

roll_faculty = faculty_crosstab[roll]

# In[99]

similar_to_roll_f = faculty_crosstab.corrwith(roll_faculty)

# In[100]

corr_roll_f = pd.DataFrame(similar_to_roll_f, columns=['sim_faculty'])

# In[101]

corr_roll_f.fillna(value=0.0)

# In[102]

# Adding sim_faculty coloumn into sim_faculty
corr_roll['sim_faculty']=corr_roll_f['sim_faculty']

# In[103]
job_crosstab=pd.pivot_table(data=df,values='Job_oriented',index='Course_Code',columns='Student_ID')

# In[104]
roll_job = job_crosstab[roll]

# In[105]
similar_to_roll_j = job_crosstab.corrwith(roll_job)

# In[106]
corr_roll_j = pd.DataFrame(similar_to_roll_j, columns=['sim_job'])

# In[107]
corr_roll_j.fillna(value=0.0)

# In[108]
corr_roll['sim_job']=corr_roll_j['sim_job']

# In[109]
scoring_crosstab=pd.pivot_table(data=df,values='Scoring',index='Course_Code',columns='Student_ID')

# In[110]
roll_scoring = scoring_crosstab[roll]

# In[111]
similar_to_roll_s = scoring_crosstab.corrwith(roll_scoring)

# In[112]
corr_roll_s = pd.DataFrame(similar_to_roll_s, columns=['sim_score'])

# In[113]
corr_roll_s.fillna(value=0.0)

# In[114]
corr_roll['sim_score']=corr_roll_s['sim_score']

# In[115]
place_crosstab=pd.pivot_table(data=df,values='Placement_types',index='Course_Code',columns='Student_ID')

# In[116]
roll_place = place_crosstab[roll]

# In[117]
similar_to_roll_p = place_crosstab.corrwith(roll_place)

# In[118]
corr_roll_p = pd.DataFrame(similar_to_roll_p, columns=['sim_place'])

# In[119]
corr_roll_p.fillna(value=0.0)

# In[120]
corr_roll['sim_place']=corr_roll_p['sim_place']

# In[121]
research_crosstab=pd.pivot_table(data=df,values='Research_Purpose',index='Course_Code',columns='Student_ID')

# In[122]
roll_research = research_crosstab[roll]

# In[123]
similar_to_roll_r = research_crosstab.corrwith(roll_research)

# In[124]
corr_roll_r = pd.DataFrame(similar_to_roll_r, columns=['sim_research'])

# In[125]
corr_roll_r.fillna(value=0.0)

# In[126]
corr_roll['sim_research']=corr_roll_r['sim_research']

# In[127]
corr_roll['pearsonR']=corr_roll.mean(axis=1)

# corr_roll.head()

# In[128]
summary=corr_roll.reset_index()

# In[129]
summary=summary.sort_values('pearsonR',ascending=False)

# In[130]
result=summary[(summary['Student_ID']<1407056) & (summary['Student_ID']!=roll)].head(3)

# In[131]
result_list=result['Student_ID'].tolist()

#print(result_list)

# In[132]
final_A=[]
final_B=[]
for i in range(0,3):
	temp_list = df2.loc[result_list[i]].tolist()
	list_a = [temp_list[0],temp_list[1]]
	list_b = [temp_list[2],temp_list[3]]
	final_A.append(list_a)
	final_B.append(list_b)




# In[133]

print "<html>"
print "<head>"

print "<style>"
print "body{ background-color: #93B874; }"
print "</style>"

print "</head>"
print "<body>"

redun = set()
cancel=0

if get_pass!=password:
   cancel=1
   print('Password does not match')
else:
   print "<h4> Roll no is: %s </br></h2>" % (r)

#print "<b>First Elective Course Recommendation:</br></b>"
#print "<b>&nbsp &nbsp Course Code &nbsp  &nbsp &nbsp &nbsp Course Name </br></b>"

for i in range(0,3):
    if final_A[i][0] not in redun and cancel==0:
        if i==0:
                print "<b>First Elective Course Recommendation:</br></b>"
                print "<b>&nbsp &nbsp Course Code &nbsp  &nbsp &nbsp &nbsp Course Name </br></b>"
        print(' &nbsp &nbsp {} &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp  &nbsp &nbsp &nbsp &nbsp {} </br>'.format(final_A[i][0],final_A[i][1]))
        redun.add(final_A[i][0])

redun.clear()

#print "<b></br> </br> Second Elective Course Recommendation: </br></b>"
#print "<b>&nbsp &nbsp Course Code &nbsp &nbsp &nbsp &nbsp Course Name </br></b>"
for i in range(0,3):
    if final_B[i][0] not in redun and cancel==0:
        if i==0:
                print "<b></br> </br> Second Elective Course Recommendation: </br></b>"
                print "<b>&nbsp &nbsp Course Code &nbsp &nbsp &nbsp &nbsp Course Name </br></b>"
        print('&nbsp &nbsp  {} &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp {} </br>'.format(final_B[i][0],final_B[i][1]))
        redun.add(final_B[i][0])
   

redun.clear()

# print "<h2> Roll no is %s </h2>" % (roll)
print "</body>"
print "</html>"
