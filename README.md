<div align="center">
<img width="500" alt="Logo1" src="https://user-images.githubusercontent.com/64307441/224562391-4b009058-6854-4af5-90ca-342511a5e4de.png">
</div>


<h1 align="center">Rogithaas</h1>
<h3 align="center">Creating an online centralized health system to completely transform the way we manage healthcare in India.</h3>
<br><br>
<p align="center" style="margin-top:10px">
<hr>

<h2 align="center"><strong>Our Mission</strong> - To Make India's all रोग an इतिहास and keep an इतिहास of all रोग and in turn create a centralized platform where all medical entities could interact</h2>

<hr>
<h3 align="center">
Project Documentation
</h3> 
<hr>
<br> 
<ul>
<li>In the current scenerio in India,we are rapidly growing on the pathway of transforming each and every sector with the help of technology.Our Prime Minister Shri Narendra Modi has also been enthusiastically supporting the growth of technology in various sectors.</li>
<li>But still there always remains a scope wherein we could introduce technology and ease the entire procedure and develop something that could make our lives easier and better.</li>
<li>Our team figured out such a gap in the heathcare sector wherein we believed that people faced a lot of difficulties - 
<ul>
<li>Managing and maintaing all the recent and old medical records.</li>
<li>There was a lot of paper wastage in the medical industry as we are still reliant on hardcopy prescription.</li>
<li>We have the system of online consultation in place and also we have the online medicine delivery in place, but we do not have a single platform to manage both.</li>
</ul>
<li>In emergency cases it will not be a practical situtation to search for all the medical records and present them to the doctor which adds on to the challanges.</li>
<li>It is also a major difficulty for the people living in villages to travel long distances and get medical help.Thus we also aim to add in an a feature known as diagnosis and prescription to diagnose the disease and prescribe an online prescription with the doctor in between to provide necessary consualtation.</li>
<li>In the present situation, the doctor has to take the concern of family before any critical surgery and this process takes time as it might be that the patient's family might not be able to travel to the hospital immediately and this process is time consuming.</li> 
</ul>

<hr>
<h3 align="center">
Project Architecture
</h3> 
<hr>
<p>Our entire project is divided into 5 parts-</p>
<ol>
<li><strong>Doctor Section</strong>-First of all as a doctor you have to sign up with all your details if you are not a member.If you have already registered then login to the application directly.After login you will, find a <em>two factor authentication</em> for security purpose after which you will see a Doctor dashboard with some basic details.Here you have a section to create a sample prescription by uploading your clinic logo,name,etc. details<br>
A doctor also has a section to view the prescription he/she has prescribed in his/her lifetime.<br>
The doctor section also has a search bar at the top to search for patients they want to access.</li>
<li><strong>Patient Section</strong>-The patient will have to first sign up with all the details.While signing up, you have two options - To register as an infant(without addhaar card) which is valid for 3 months and with an addhaar card.If already registered the patient can directly login to use the application.After logging in, the patient will have to undergo a two factor authentication after which he/she can see a patient dashboard with all the sections like medical records , a personalized soft copy of health card, order medicine,medicine delivery tracking,prescription repository and diagnosis and the ability to accept the consent form in case of emergency situation to one of your family members.<br>
<li><strong>Patient-Doctor interaction</strong>-This is sort of a hidden section which can only be viewed once a doctor enters and accesses the patient section.This section is similar to the patient section but has read-only capabilities so that the patient data remains secure and intact.The doctor can view past medical history,get an overview of patient's health condition and in succession write an online prescription to the patient in our online prescription system which will be automatically uploaded to medical records of patient on successful submission.In emergency situations, the doctor can also send a consent to their family memebers.</li>
<li><strong>Pharmacy Section</strong>-To access the pharmacy section, the pharmacy needs to sign up and fill the details to create an account.Once done, the pharmacy can directly login to the system and undergo a two factor authentication after which you can track the medicines in their shop, online delivery tracking, can generate a bill online and accept or reject patient's request for medicine.</li>
<li><strong>QR Code Emergency Section</strong>-In case of emergency, if someone scans the QR code (provided uniquely to each user), the person could view the name,address and the emergency contact of the patient and also the doctor can login from the same dashboard and see the patient's medical history and also send a consent to the family.</li>
</ol>
</p>
<br>
<br>

<div align="center">
<img width="1500" alt="Logo1" src="https://github.com/shahhilag4/RogItihaas/assets/64307441/45c7fac6-7f5e-4b4c-aabc-54a01b642358">
</div>

<hr>
<h3 align="center">Unique Features</h3>
<hr>
<ol>
<li><strong>Simplicity</strong>-The UI is built with an aim to make it so easy to understand that anyone from a small child to an elder person could easily navigate and figure out how to use the application.In case someone is facing problems and unable to figure his/her way out, we have also added a video demonstration to give a walkthrough of our application</li>
<li><strong>Patient and doctor-centric approach</strong>-Mostly the healthcard pltforms are more dctor centric than patient centric, but our platform focuses on providing unique features benefiting both the parties.</li>
<li><strong>Data Security</strong>-The entire database is encrypted via our python security code and data security is one of the most unique faetures of our application.Encryption is not the only thing we focus on.We have added email alerts for each login session into a doctor or patient account.In addition we have also leveraged the power procided by the combination of AMD and Google cloud and used the Convidential VM on the C2D system which will keep the data encrypted on the fly during data transfer and handling</li>
<li><strong>QR code</strong>-We rely on a QR code system rather than a unique card number.This will procide ease of use to the patients as well as the doctor by providing instant access to the health account.</li>
<li><strong>100% Paperless</strong>-We have kept all the document in a soft copy format from health card to medical prescription.The soft copy will not only save paper but will also help to keep our medical records safer with no worry of documents getting lost.We have also provided a facility to send prescription on mobile.The soft copy will save approximately 25 lakh trees.</li>
<li><strong>The Doctor and Pharmacy gap bridging</strong>-We have tried to bridge the gap between the doctor and pharmacist, two important pillars of our health system and centralized the entire process keeping in mind that if a patient is unable to come to the clinic he/she is also not able to go to the pharmacy store and thus centralizing the system will help transform and help many people.In addition, we will also be able to stardadize the prescription type for the pharmacist to reduce the complexity at their end.</li>
<li><strong>Two Factor Authentication</strong>-The two factor authentication is used to add an extra layer of security to each section.The two factor authentication is conducted with the user's mobile number which confirms the authenticity of the user.</li>
<li><strong>Online Consultation Efficiency</strong>-We tried to reduce the online consultation which is normally done via an online video call in most applications but we have used a 3 stage process wherein the user first enters the symptoms he/she faces,then the doctor verifies the request to download a particular prescription and the doctor could suggest some tests before confirming the prescription download.After the doctor is satisfied, the doctor can confirm the prescription download by charging some fees.</li>
<li><strong>Medicine Delivery</strong>-If a patient consults a doctor online it is obvious that he/she is not in a position to travel outside his/her home and thus we have added a service of medicine delivery wherein the request is made to your nearest store to deliver the medicines directly at the patient's residence.</li>
<li><strong>Consent System</strong>-A consent form system will reduce the rapid action time for the family members to accept the consent form.The emergency contact of the patient directly recieves an update in his/her dasboard in the case if the patient suffers an emergency.This will take away the felling of guilt over from doctor ,let doctors readily act in emergency situation and also alert the family about the situation.</li>
<li><strong>Facility for infant</strong>-The infant babies who suffer from the disease as soon as they are born are not in a situtation to get a aadhar card for themselves which should not affect their registration to our platform and thus we have a temporary id linked with the infant's father aadhaar card which will be made for the period of 3 months after which the infant could register with the aadhaar card.</li>
<li><strong>Online billing and medicine storage repository</strong>-We have also created an online billing and medcinine storage repository for the pharmacy wherein the pharmacy could update the medicine record by uploading a CSV of the medicines and they could also perform billing online and handle their online medcine delivery.</li>
</ol>
<br>
<br>
<hr>
<h3 align="center">Future Scope</h3>
<hr>
<ol>
<li><strong>Mobile Number based authentication</strong>-Currently we rely on the mobile number based  two factor authentication but in future we aim to add in email and mobile OTP based authentication.</li>
<li><strong>Improve Emergency dashboard security</strong>-The masking of mobile number could produce additional security in our system along with improving security of QR Code.</li>
<li><strong>Make a profitable app for doctors</strong>-In future we aim to add some extra benefits to the doctors which could make them come to our application daily.</li>
<li><strong>Benefits for poor people</strong>-We aim to add in benefits for the poor by linking our application to online donation agencies which will be very beneficial to procide free healthcare facilities for the poor.</li>
<li><strong>A centralized application for all medical needs</strong>-Our final destination is to add value to humanity with centralizing all medical needs for the people not diverting from our original goal.We want to contribute to the easy availability of doctors,medical equipments,blood and organ donors,oxygen cylinder,etc. This will ensure that we are not underprepared in case a global pandemic such as COVID-19 hits us again.</li>
<li><strong>We aim to centralize the finances of the pharmacy and doctors so that we could track their income and prevent malpractice.</strong></li>
<li><strong>We also want to integrate an online billing system for pharmasist to make their job easier.</strong></li>
<li><strong>Integration of ML for diagnosis</strong>-By integrating ML into our system we could more precisely figure out the disease the person is suffering and recommend relevant prescription to the patient.</li>
</ol>
<br>
<br>
<hr>
<h3 align="center">Business Model</h3>
<hr>
<p>Our business model revolves around the doctor and the pharmacy section wherein we will charge the doctor and the patient.</p><br>
<ol>
<li>
Pharmacy Section - The earnings of a pharmacy in India can vary significantly based on several factors, such as the location of the pharmacy, the type of medicines sold, and the size of the business.As a rough estimate, according to PayScale, the average monthly salary of a pharmacy in India can range from around INR 20,000 to INR 50,000 or more. However, it is important to note that these figures may vary widely based on several factors.</li>
<li>Doctor Section - The monthly earnings of a doctor in India can vary greatly depending on several factors, such as the type of medical practice, the level of experience and specialization, and the location of practice.As a rough estimate, according to PayScale, the average monthly salary of a medical doctor in India is around INR 77,000 to INR 1,50,000. However, this can vary widely based on factors such as the doctor's level of experience, the type of medical practice they are in, and their specialization.</li>
<li>Charges by medical delivery agencies today - The exact commission charged by Tata 1mg and PharmEasy for medicine delivery may vary depending on several factors, such as the type and quantity of medicines, the location of delivery, and the partnership agreements with individual pharmacies. However, based on publicly available information, it is estimated that Tata 1mg and PharmEasy charge a commission of around 15-20% on the total value of medicine orders placed through their platforms.</li>
<li>What will we charge? - The bussiness model we aim to implement will charge 10% commission per billing month revenue of doctor/pharmacy via our platform.We aim to generate a revenue of around 4850₹(considering 50% sales via our platform) with one doctor and one pharmacy.If we are able to get 10 pharmacies and 10 doctors interested in our business model initially we will be able to earn 48,500.If we calulate our instance usage per month we have a liability of 9,136₹ which could be approximated to a upper limit of 10,000₹ per month.So we could calculate a final value of 48.000₹-10,000₹=38,000₹</li>
<li>Our main aim with this application is more social than business, and thus we have an additional future scope related to business which aims to reward each patient with some reward points for helping a patient in accident by calling the ambulance,emergency contact and the police.This will help them earn some Amazon Pay coupons of 250₹ for each life saved.This reward system will inturn push the people to help any person in need of help.</li>
</ol>
<br>
<br>

<hr>
<h3 align="center">Steps for installation</h3>
<hr>
<ol>
<li>Install all the dependencies stored in requirements.txt (For installing dlib library you need to install visual studio and cmake first).</li>
<li>Run app.py.</li>
<li>Change directory to RogIthaas.</li>
<li>Open http://127.0.0.1:5000/ in browser.</li>
<li>You are all set. Welcome to the RogIthaas family ☺️</li>
</ol>

<h4 align="center"><b>Video Demonstartion can be found <a href="https://youtu.be/3EVEM0wBYlc">here</a>.</b></h4>

<h4 align="center"><b>The deployed application can be found <a href="https://rogitihaas.onrender.com/">here</a>.</b></h4> 
<br>

<hr>
<h3 align="center">Tech stack</h3>
<hr>

![HTML](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white&style=plastic) ![CSS](https://img.shields.io/badge/CSS-239120?&style=for-the-badge&logo=css3&logoColor=white&style=plastic) ![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=white&style=plastic) ![Python](https://img.shields.io/badge/Python-00008B?style=for-the-badge&logo=python&logoColor=white&style=plastic) ![MongoDB](https://img.shields.io/badge/MongoDB-4EA94B?style=for-the-badge&logo=mongodb&logoColor=white&style=plastic) ![Flask](https://img.shields.io/badge/Flask-FF8C00?style=for-the-badge&logo=flask&logoColor=white&style=plastic)
<br><br>

<div align="center">
  <br>
  <p><b>Thank you for your time.</b><br>
  </p>
</div>
