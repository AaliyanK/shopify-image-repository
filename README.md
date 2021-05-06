# Winter 2022 Shopify Developer Intern Challenge: Build an Image Repository

Hello Shopify! My name is Aaliyan Kapadia and this is my repo for the Developer Image Repository Project! I am seeking a 4 or 8 month backend developer internship that starts in January 2022! I am a Chemical Engineering student who has self learnt software engineering principles through hundreds of hours of online certifications! I have also worked at Pepsi as a Data Analyst Intern, at Pronti AI as a Backend Software Engineering Intern, and at Borealis AI as a Data Engineering Intern.

# How Does It Work?
The application I have created has a React frontend, Flask backend, and utilizes a Postgres database. In the example use cases, the images are uploaded to AWS S3 in a public bucket; the public url for the image is then stored in the Postgres database. The home page then makes a GET request to continuously grab the image urls from the database. The application also has register and login functionalities, so that each user gets to view their own images in the repository. Additionally, each endpoint is authenticated with a JWT session token.

The React frontend isn't the best! But I did learn a lot by creating the components from scratch and sending axios requests to the backend! I wanted to mention that although I am applying for the backend developer role, I am actively trying to learn frontend development principles to become a more effective fullstack developer. Maybe a 8 month split internship between two teams would be something to consider as well (insert eye-emoji).

Finally, I created this project over two weeks by referring to multiple tutorials, medium posts, and YouTube videos! This was a great learning experience. I hope you guys enjoy it!

# How Do We Set Up The Application?
1. Create an AWS account and set up the IAM access key and secret access key
2. Create a publicly accessible bucket ex: 

![bucket](https://user-images.githubusercontent.com/48164949/117222841-6beb7180-adda-11eb-8231-ac7eefe9e012.png)

4. You must have Postgres server running locally, note the database URI ex: "postgresql://user:password@localhost:5432/image_repository" where image_repository is the database name
5. To start the frontend: `npm start`
6. Open another terminal and `cd Backend`
7. Use `pip install -r requirements.txt` to install dependencies
8. Set your environment variables: 
  - `set JWT_SECRET_KEY=test`, 
  - `set SQLALCHEMY_DATABASE_URI=postgresql://postgres:password@localhost:5432/image_repository`, 
  - `set AWS_ACCESS_KEY_ID = AKIA****`, 
  - `set AWS_SECRET_ACCESS_KEY = mENEBUrSG8bf****`
9. Note that the environment variables you set will be different based on your database URI and IAM credentials, I added mines as an example. Also, as I am not deploying this project to production, the app will be using Dev environment configs:

![dev](https://user-images.githubusercontent.com/48164949/117223042-d13f6280-adda-11eb-834e-ed8404c7eb54.png)

10. To setup the database locally from the schema:
  - `python manage.py db init`
  - `python manage.py db migrate`
  - `python manage.py db upgrade`

 ![Picture2](https://user-images.githubusercontent.com/48164949/117223226-38f5ad80-addb-11eb-9685-2b9a67cf6c74.png)
 
 We should see the **users** and **images** tables pop up on Postgres or PGadmin

11. `python run.py` to start the backend server

# A Complete Application Tour
The first page we see is the Register page. 

![REGISTER](https://user-images.githubusercontent.com/48164949/117223383-7fe3a300-addb-11eb-94bf-58415a34b3e5.png)

Enter an email and confirm your password. The details will be sent as a POST request to a Flask endpoint. The API will check to see if it has recieved an email and password (otherwise send a 400 status code: Valid JSON properties required) and if the user exists in the database already (send a 400 status code). If these checks are not met, the frontend will display error messages like: "your account already exists", "please enter a valid email/password", or "passwords do not match". If all the checks are passed in the backend, the user data is saved to the "user" table in the database with a hash password as we do not want to see the users password. 

![register_db](https://user-images.githubusercontent.com/48164949/117223427-a1448f00-addb-11eb-8658-a65c3f82854b.png)

Once the operation is complete, a success message will be returned (200 status code) and you will be redirected to the login page

![success_reg](https://user-images.githubusercontent.com/48164949/117223454-b4eff580-addb-11eb-924e-c8f81ff8b209.png)

You can now log in! Once the submit button is clicked, a GET request is sent with the email and password as "query params". The backend will check if the user exists in the DB and if the password is correct with a hash function. If the checks pass, a JWT token is generated and returned to the frontend. This token will be sent as a header to every request and then authenticated at every endpoint.

![JWT](https://user-images.githubusercontent.com/48164949/117223693-36478800-addc-11eb-954f-5a57dda4a320.png)

![Home](https://user-images.githubusercontent.com/48164949/117223780-6c850780-addc-11eb-944f-292b3c728009.png)

You will then be directed to the home page. The home page is a private route, so you can only access it if you are logged in with a JWT token. If you decide to logout, your session token will be removed, and you will be granted a new one when relogging in. You will be redirected to the login/register page when logging out.

You can now add images by clicking the button and selectign a single file. Once selected, a check will be done to make sure that the file extension is PNG or JPEG. The flask endpoint (POST request) initializes an S3 client, uploads the image to S3, and saves the user_id and image_url to the database. React will then refresh the page and will display the image on the page.

![home2](https://user-images.githubusercontent.com/48164949/117224051-0cdb2c00-addd-11eb-86e7-f4aebf073a6f.png)

![s3](https://user-images.githubusercontent.com/48164949/117224084-1bc1de80-addd-11eb-8a0a-68f9ccf96df0.png)
The image has been uploaded to S3.

![dbout](https://user-images.githubusercontent.com/48164949/117224105-29776400-addd-11eb-822c-280ca53af6c3.png)
The user_id and image_url, which is used to display the image to the frontend.

![home3](https://user-images.githubusercontent.com/48164949/117224207-53c92180-addd-11eb-9aa7-223c17d84eb9.png)

We can now click the delete button, which will send a DELETE request to the backend; the image will be deleted from S3 and the database.

# Testing

# Future Improvements/features
1. The most prominent improvement would be the frontend. I would focus on improving the image sizing, enhancing the register/login UI, and adding animations.
2. I would also look towards containerizing the front-end and back-end to create a production-grade workflow with travis-CI and AWS EBS for deployments. By creating dockerfiles and docker-compose we can locally test the application with ease. And with Travis-CI and AWS EBS, we can test any commits made to master and deploy the code all in one workflow.
3. Better testing! I have not had much experience with testing, but it is an important principle, applying more tests to the APIs would create a more effective workflow.
4. We could also add another page for favourites. A user would be able to favourite an image in the repository. The schema would have to change to include a “favourite” column in the “image” table with a Boolean value, set to True if the user decides to favourite the image. The frontend could have another page where the image would be added to as a "favourites page".
