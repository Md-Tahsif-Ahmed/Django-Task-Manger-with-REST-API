# Django-Task-Manger-with-REST-API

<h1>Setup and Run the Project </h1>
<ol>
  <li>At first Create a directory folder then create virtual environment using python -m venv venv</li>
  <li>Activate virtual environment using venv/Scripts/activate and install django, djangorestframewotk,psycopg2,pillow and other nessecary package using pip </li>
  <li>Create a project using Django-admin startproject projectname and run the project using python manage.py runserver</li>
  <li>Create apps and superadmin and migrates models using python manange.py makemigrations and migrate </li>
  <li>Settings media and static directory</li>
 
</ol>

<h1> API Endpoints and Usage </h1>
<ol>
  <li>GET: This method is used to retrieve data from an API. It is a read-only operation that fetches information without modifying it. When you make a GET request to an API endpoint, you are requesting data to be returned to you. </li>
  <li>POST: POST is used to create new resources or data on the server. When you send a POST request to an API endpoint, you typically include data in the request body to be stored on the server.</li>
  <li>PUT is used to update an entire resource. When you make a PUT request to an API, you are replacing the existing resource with the new data you provide. It typically requires sending the complete resource representation, including any fields you want to update.</li>
  <li>PATCH is used to partially update a resource. It allows you to make changes to one or more specific fields of an existing resource without replacing the entire resource. You provide the updated fields in the request body. </li>
  <li>DELETE is used to remove a resource from the server. When you make a DELETE request to an API endpoint, you are requesting that the resource identified by the URL be removed.</li>
</ol>
