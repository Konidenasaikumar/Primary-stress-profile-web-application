import streamlit as st
import numpy as np
import pandas as pd
import math
st.title('Primary_stress_profile')
st.write('')
st.image('Joints.PNG')
inp1=st.radio(label='Select the type of loading and type of weld', 
         options=['Double V- Tension','Double V- Bending', 'Single V- Tension',
                  'Single V- Bending'], horizontal=True, index=0, help='Double V can aslo be used for Cruciform joints.')

if inp1=='Double V- Tension':
    p1=1.9220
    p2=0.3224
    p3=1.1257
    p4=1.5481
    p5=0.4002

    # considering (x/ρ)0 as const
    const=0.10
    #Constants for coefecients.
    q1 =0.081
    q2 = 0.919
    q3 = 3.0
    q4 = 0.8
    q5 = 0.6199
    q6 = -0.2210
    q7 = -0.1541
    q8 = -0.1939
    q9 = -0.2346
    q10= 1.7375
    q11= 0.1502
    q12= 0.0081

elif inp1=='Double V- Bending':
    p1=1.1399
    p2=0.2062
    p3=1.0670
    p4=1.6775
    p5=0.4711

    const=0.12
    q1=0.080
    q1 =0.080
    q2 = 0.920
    q3 = 2.5
    q4 = 0.8
    q5 = 1.8240
    q6 = -0.1340
    q7 = -0.1805
    q8 = -0.2011
    q9 = -0.3214
    q10= 3.1312
    q11= 0.0567
    q12= 0.0052

elif inp1=='Single V- Tension':
    p1=1.3905
    p2=0.2081
    p3=1.0756
    p4=1.7483
    p5=0.4413

    const=0.12
    q1 =0.060
    q2 = 0.940
    q3 = 2.5
    q4 = 0.8
    q5 = 1.7872
    q6 = -0.1105
    q7 = -0.2309
    q8 = -0.1441
    q9 = -0.4331
    q10= 2.7871
    q11= 0.0800
    q12= 0.0016


elif inp1=='Single V- Bending':
    p1=1.5326
    p2=0.2081
    p3=1.1036
    p4=1.5436
    p5=0.4287

    const=0.12
    q1=0.080
    q1 =0.080
    q2 = 0.920
    q3 = 2.5
    q4 = 0.8
    q5 = 1.8240
    q6 = -0.1340
    q7 = -0.1805
    q8 = -0.2011
    q9 = -0.3214
    q10= 3.1312
    q11= 0.0567
    q12= 0.0052


st.write('')
st.write('Input Geometrical parameters in mm')
col1, col2, col3,col4,col5 = st.columns(5)
with col1:
   h=st.number_input(label='weld attachment length (h)', min_value=0.1, max_value=100.0,
                 value=0.1, step=1.0)
with col2:
   r=st.number_input(label='Enter weld toe radius (ρ)', min_value=0.1, max_value=5.0,
                 value=0.1, step=0.25)
with col3:
   a=st.number_input(label='Enter flank angle in deg α (°)', min_value=0.1, max_value=60.0,
                 value=0.1, step=5.0)
a=float(math.radians(a))
with col4:
   T=st.number_input(label='Enter plate thickness (T)', min_value=5.0, max_value=100.0,
                 value=5.1, step=1.0)
with col5:
   sn=st.number_input(label='Enter the nominal stress (σn)', min_value=50.0, max_value=500.0,
                 value=50.1, step=10.0)
st.image(image='Kt_equation.PNG', caption='Kt approximation by Yusuf Kiyak et al.')                 


kt=1+(p1*((h/T)**(p2*a))*(a**p3)*(math.exp((-p4)*a)))*((r/T)**(-0.285*a))*((0.021+(r/T))**-p5)

kt=round(kt,3)
#print(p1,p2,p3)
st.success(f'Stress concentration Factor solution Kt is {kt}.')


#z=0
z = ['%.2f'% i for i in np.arange(0, 1, 0.01)]
G=[]
E1=round(q5*(r/T)**((q6*(a**q7)))+(1.5*(a**(q8*(r**q9))))-(q10*((h/T)**(q11*a)))-(q12*((h*a)/r)),5)
for x in z:
    #print(x)
    if (float(x)/r) <= (const):
        Gl=1
        G.append(Gl)
    else:
        T1=(float(x)/T)-((const)*(a/T))
        Gl=q1+((q2*math.exp(-(E1*T1))/1+((E1**q3)*(T1**q4)*(math.exp(-E1*T1)))))
        G.append(Gl)


dictionary = {'E1': G, 'x': z}

dt=pd.DataFrame(dictionary)
#st.table(dt)

sl=[]
if inp1=='Double V- Tension' or 'Single V- Tension':
    for index, row in dt.iterrows():
        x=float(row['x'])
        Gl = row['E1']
        #si=((kt*sn)/(2*math.sqrt(2)))*((((x/r)+1/2)**-1/2)+(0.5*((x/r)+1/2)**-3/2))*(1/Gl)
        #si = (((kt*sn))/(2*math.sqrt(2)))*(((x/r)+(0.5))**(-(1/2))+(0.5*((x/r)+(0.5))**(-(3/2))))*(1/Gl)
        
        w = ((kt*sn)/(2*math.sqrt(2)))

        b = ((x/r)+(0.5))**(-(1/2))

        c = (0.5*((x/r)+(0.5))**(-(3/2)))

        d = (1/Gl)

        si = w*(b+c)*d
        
        sl.append(round(si,5))

elif inp1=='Double V- Bending' or 'Single V- Bending':
    for index, row in dt.iterrows():
        x=float(row['x'])
        Gl = row['E1']
        #si=(((kt*sn)/(2*math.sqrt(2)))*((((x/r)+1/2)**(-1/2))+(0.5*((x/r)+1/2)**(-3/2))))*(1/Gl)*((1-2*(x/T)))
        #si = (((kt*sn)/(2*math.sqrt(2)))*(((x/r)+(0.5))**(-(1/2))+(0.5*((x/r)+(0.5))**(-(3/2))))*(1/Gl))*((1-(2*(x/T))))
        w = ((kt*sn)/(2*math.sqrt(2)))

        b = ((x/r)+(0.5))**(-(1/2))

        c = (0.5*((x/r)+(0.5))**(-(3/2)))

        d = (1/Gl)

        f = (1-(2*(x/T)))

        si = w*(b+c)*d*f
        sl.append(round(si,5))

dict1 = {'σI': sl, 'x': z}
dict=pd.DataFrame(dict1, columns = ['σI', 'x'])

if st.checkbox(label='Thickness profile results', help='click to view profile results'):
    st.write(dict)
st.write('  ')
col1, col2 = st.columns(2)
with col1:
   save_name=st.text_input(label='File name', value="", max_chars=None,
                            placeholder='Desirable name of file to be saved',
                            help='File will be saved in the same folder')
 
with col2:
   st.write('')
   st.write('')
   if st.button("Download"):
      dict.to_excel(f"{save_name}.xlsx",index=False)
