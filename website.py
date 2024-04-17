import streamlit as st
import pandas as pd
import PIL.Image
import pickle as pkl
import pandas as pd
import numpy as np
import streamlit as st
import scipy.io as sio
import matplotlib.pyplot as plt


    





with open("result.pkl","rb") as f:
	file=pkl.load(f)

df=pd.DataFrame(file)
df.to_csv(r'results.csv')


with open("resultsal.pkl","rb") as fi:
	file1=pkl.load(fi)
df1=pd.DataFrame(file1)
df1.to_csv(r'resultss.csv')

#######################################
# Security LOGIN
import hashlib

def make_hashes(password):
	return hashlib.sha256(str.encode(password)).hexdigest()


def check_hashes(password,hashed_text):
	if make_hashes(password) == hashed_text:
		return hashed_text
	return False

# DB Management
import sqlite3
conn = sqlite3.connect('data.db')
c = conn.cursor()

# DB  Functions
def create_usertable():
	c.execute('CREATE TABLE IF NOT EXISTS userstable(username TEXT,password TEXT)')

def add_userdata(username,password):
	c.execute('INSERT INTO userstable(username,password) VALUES (?,?)',(username,password))
	conn.commit()

def login_user(username,password):
	c.execute('SELECT * FROM userstable WHERE username =? AND password = ?',(username,password))
	data = c.fetchall()
	return data

def view_all_users():
	c.execute('SELECT * FROM userstable')
	data = c.fetchall()
	return data

######################################

def loadData():
    data = sio.loadmat('Indian_pines_corrected.mat')['indian_pines_corrected']
    labels = sio.loadmat('Indian_pines_gt.mat')['indian_pines_gt']
    return data,labels
data,labels=loadData()


def load_Data():
    data1 = sio.loadmat('Salinas_corrected.mat')['salinas_corrected']
    labels1 = sio.loadmat('Salinas_gt.mat')['salinas_gt']
    return data1,labels1
data1,labels1=load_Data()

def main():

	

	menu = ["Home","Login","SignUp"]
	choice = st.sidebar.selectbox("Menu",menu)



	if choice == "Home":

		st.subheader("Hyperspectral Image  Classification")
        ############################


        ###########################





	elif choice == "Login":
		st.subheader("Hyperspectral Image Classification")

		username = st.sidebar.text_input("User Name")
		password = st.sidebar.text_input("Password",type='password')


		if st.sidebar.checkbox("Login"):

			create_usertable()
			hashed_pswd = make_hashes(password)

			result = login_user(username,check_hashes(password,hashed_pswd))



			if result:

				st.success("Logged In as {}".format(username))

				task = st.selectbox("Choose Dataset",["Indianpines","salinas"])
				if task == "Indianpines":
					
					c=st.number_input("Enter number between 0 and 199",0,199)
					if st.button("bandvisualization"):
						fig = plt.figure(figsize = (7, 7))
						ax=fig.subplots(1, 1)
						ax.imshow(data[:, :, c], cmap='nipy_spectral')
						ax.axis('off')
						ax.title.set_text(f"Band - {c}")
								
						fig1 = plt.gcf()
						st.pyplot(fig1)
									
						st.write(" visualization of Indian Pines band ",format(c))
    		
    																
    								
							
					if st.button("GroundTruth"):
									image2=PIL.Image.open("Groundtruth.png")
									st.image(image2)
									st.text("Groundtruth of Indian Pines")
					
					if st.button("RGB Composite"):
									image3=PIL.Image.open("rgbcomposite.png")
									st.image(image3)
									st.text("RGB Image of the Indian Pines")
					
					if st.button("classification map"):
									image4=PIL.Image.open("predictionIndianpines.png")
									st.image(image4)
									st.text("Predicted of Indian Pines")

					if st.button("classification"):
									d1=df.iloc[0:,0:]
									d2=df.iloc[0:,1]
									st.write(d1,d2)
									for x in (d1):
										for y in (d2):
											st.write(x,"has the area of",y,"Sq.mtr")					

									
    												
									
									

 
				elif task == "salinas":
					c1=st.number_input("Enter number between 0 and 225",0,203)
					if st.button("bandvisualization"):
						figsa = plt.figure(figsize = (7, 7))
						ax1=figsa.subplots(1, 1)
						
						ax1.imshow(data1[:, :, c1], cmap='nipy_spectral')
						ax1.axis("off")
						ax1.title.set_text(f"Band - {c1}")
						figs = plt.gcf()
						st.pyplot(figs)
									
						st.write(" visualization of salinas band ",format(c1))
					
					if st.button("GroundTruth"):
									image2=PIL.Image.open("gt_salina.png")
									st.image(image2)
									st.text("Ground Truth of Salinas")
					
					if st.button("RGB Composite"):
									image3=PIL.Image.open("salina_rgb.png")
									st.image(image3)
									st.text("RGB image of Salinas")
					if st.button("classification map"):
									image4=PIL.Image.open("predictions.jpg")
									st.image(image4)
									st.text("classification map of Salina")

					if st.button("classification"):
									ds1=df1.iloc[0:,0:]
									ds2=df1.iloc[0:,1]
									st.write(ds1,ds1)
									for i in (ds1):
										for j in (ds2):
											st.write(i,"has the area of",j,"Sq.mtr")					



				elif task == "Profiles":
					st.subheader("User Profiles")
					user_result = view_all_users()
					clean_db = pd.DataFrame(user_result,columns=["Username","Password"])
					st.dataframe(clean_db)
			else:
				st.warning("Incorrect Username/Password")












	elif choice == "SignUp":
		st.subheader("Create New Account")
		new_user = st.text_input("Username")
		new_password = st.text_input("Password",type='password')
        #ceck if new_password has at least 8 characters



		if st.button("Signup"):


			create_usertable()
			add_userdata(new_user,make_hashes(new_password))
			st.success("You have successfully created an Account")
			st.info("Go to Login Menu to login")




if __name__ == '__main__':
	main()