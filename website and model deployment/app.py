from flask import Flask, render_template, request, jsonify, redirect, url_for, flash , session
from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash
import pandas as pd

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Connect to MongoDB
try:
    client = MongoClient('mongodb://localhost:27017/')
    db = client['chatbot']
    users_collection = db['users']
    feedback_collection = db['feedback'] 
    profile_collection = db['profile']
    # marks_collection = db['marks']
    print("Connected to MongoDB successfully")
except Exception as e:
    print("Error connecting to MongoDB:", e)

class User:
    def __init__(self, email, password):
        self.email = email
        self.password = password

# Login route
@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        print(email,password)
        user = users_collection.find_one({'email': email})
        if user and check_password_hash(user['password'], password):
            flash('Login successful', 'success')
            return redirect(url_for('chatbot'))
        else:
            flash('Invalid email or password', 'error')
            return redirect(url_for('home'))
    else:
        return 'Method Not Allowed', 405

# Signup route
@app.route('/signup', methods=['POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        existing_user = users_collection.find_one({'email': email})
        if existing_user:
            flash('User with this email already exists. Please log in.', 'error')
            return redirect(url_for('home'))
        else:
            password = request.form.get('password')
            hashed_password = generate_password_hash(password)
            new_user = {'email': email, 'password': hashed_password}
            users_collection.insert_one(new_user)
            flash('Signup successful. Please log in.', 'success')
            return redirect(url_for('home'))
    else:
        return 'Method Not Allowed', 405
    
 # Existing feedback endpoint function
@app.route('/feedback-page', methods=['GET'])
def feedback_page():
    return render_template('feedback.html')

# New feedback endpoint function
@app.route('/feedback', methods=['POST'])
def submit_feedback():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        message = request.form.get('feedmessage')
        
        # Check if the email and password match a user in the database
        user = users_collection.find_one({'email': email})
        if user and check_password_hash(user['password'], password):
            # Store feedback in the database
            new_feedback = {'email': email, 'password': password, 'message': message}
            feedback_collection.insert_one(new_feedback)
            
            flash('Feedback submitted successfully.', 'success')
        else:
            flash('Invalid email or password.', 'error')
        
        return redirect(url_for('feedback_page'))
    else:
        return redirect(url_for('feedback_page'))


# Profile route
from flask import request

@app.route('/profile', methods=['POST'])
def create_profile():
    if request.method == 'POST':
        email = request.form.get('email')
        existing_profile = profile_collection.find_one({'email': email})
        if existing_profile:
            flash('Profile with this email already exists.', 'error')
            return redirect(url_for('home'))
        else:
            # Get profile data from the form
            first_name = request.form.get('firstName')
            last_name = request.form.get('lastName')
            date_of_birth = request.form.get('dateOfBirth')
            age = request.form.get('age')
            location = request.form.get('location')
            gender = request.form.get('gender')
            phone = request.form.get('phone')  # Get phone number data

            # Perform validation on phone number (you can add your validation logic here)
            if not phone.isdigit() or len(phone) != 10:
                flash('Please enter a valid 10-digit phone number.', 'error')
                return redirect(url_for('home'))

            # Store profile data in the profile collection
            new_profile = {
                'email': email,
                'first_name': first_name,
                'last_name': last_name,
                'date_of_birth': date_of_birth,
                'age': age,
                'location': location,
                'gender': gender,
                'phone': phone  # Include phone number in the new profile document
            }
            profile_collection.insert_one(new_profile)
            flash('Profile created successfully.', 'success')
            return redirect(url_for('home'))
    else:
        return 'Method Not Allowed', 405

# Add error handling for database operations
# @app.route('/calculate-cutoff', methods=['POST'])
# def calculate_cutoff():
#     print('function called')
#     if request.method == 'POST':
#         print('form')
#         try:
#             # Extract marks from the form
#             physics_mark = float(request.form.get('physicsMark'))
#             chemistry_mark = float(request.form.get('chemistryMark'))
#             maths_mark = float(request.form.get('mathsMark'))

#             print(physics_mark)

#             # Calculate aggregate marks (if needed)
#             aggregate_marks = (physics_mark + chemistry_mark + maths_mark) / 3

#             # Store all fields in the database
#             new_marks = {
#                 'physics_mark': physics_mark,
#                 'chemistry_mark': chemistry_mark,
#                 'maths_mark': maths_mark,
#                 'aggregate_marks': aggregate_marks
#             }
#             marks_collection.insert_one(new_marks)

#             # Flash a message to indicate successful storage
#             flash('Marks stored successfully.', 'success')

#             # Redirect to a relevant page (e.g., chatbot page)
#             return redirect(url_for('chatbot'))
#         except Exception as e:
#             # Handle any exceptions and flash an error message
#             flash(f'Error storing marks: {str(e)}', 'error')
#             return redirect(url_for('chatbot'))
#     else:
#         flash('Method Not Allowed', 'error')
#         return redirect(url_for('chatbot'))
    


# Load the dataset
df = pd.read_excel("C:/Users/sivar/OneDrive/Desktop/Mini Project Chatbot/model_deployment/dataset_chatbot.xlsx")

# Preprocess the DataFrame
col_to_drop = ['S NO', 'APPLN NO', 'NAME OF THE CANDIDATE', 'DOB', 'RANK', 'ALLOTTED\nCATEGORY']
df.drop(columns=col_to_drop, inplace=True)
df['COMMUNI\nTY'] = df['COMMUNI\nTY'].str.replace('COMMUNI\nTY', '')
df.replace('', pd.NA, inplace=True)
df.dropna(inplace=True)

# Group by relevant columns and aggregate min/max marks
co_range = df.groupby(['COLLEGE\nCODE', 'COMMUNI\nTY', 'BRANCH\nCODE']).agg({'AGGR\nMARK': ['min', 'max']})

def predict_colleges_and_branches(agg_marks, community):
    # Filter the DataFrame based on the provided community
    filtered_df = co_range.loc[(slice(None), community), :]
    
    # Initialize a list to store matching colleges and branches
    matches = []
    
    # Iterate over the filtered DataFrame
    for index, row in filtered_df.iterrows():
        college_code = index[0]
        branch_code = index[2]
        min_cutoff = float(row[('AGGR\nMARK', 'min')])  # Convert to float
        max_cutoff = float(row[('AGGR\nMARK', 'max')])  # Convert to float
        
        # Check if the aggregate marks fall within the range
        if min_cutoff <= float(agg_marks) <= max_cutoff:
            matches.append((college_code, branch_code))
    
    # Check if any matches were found
    if matches:
        # Convert the matches to a list of strings
        matches_str = [f"College code: {match[0]}, Branch: {match[1]}" for match in matches]
        return matches_str
    else:
        return ["No colleges found for the given aggregate marks and community."]

# Store conversation messages
conversation_messages = []

agg_marks = ""
community = ""
conversation_stage = 0  # Initialize conversation stage counter


def is_valid_community(community):
    valid_communities = ['BC', 'BCM', 'MBC', 'OC', 'SC', 'SCA', 'ST']
    return community.upper() in valid_communities

# @app.route('/')
# def home():
#     return render_template('chatbot.html', messages=conversation_messages) 

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/explore')
def explore():
    return render_template('explore.html')

@app.route('/aboutus')
def aboutus():
    return render_template('about.html')

@app.route('/feedback')
def feedback():
    return render_template('feedback.html')

@app.route('/profile')
def profile():
    return render_template('profile.html')

@app.route('/chatbot')
def chatbot():
    return render_template('chatbot.html', messages=conversation_messages) 

@app.route('/send-message', methods=['POST'])
def send_message():
    global agg_marks, community, conversation_stage
    
    user_message = request.form['message']
    print("User message:", user_message)
    conversation_messages.append(('user', user_message))
    
    # Bot response logic
    bot_response = ""

    # Handle different stages of the conversation
    if conversation_stage == 0:
        agg_marks = user_message
        print(agg_marks)
        bot_response = f"You entered aggregate marks: {agg_marks}. Please enter your community."
        conversation_stage = 1
    elif conversation_stage == 1:
        if is_valid_community(user_message):
            community = user_message.upper()
            print('comm',community)
            bot_response = f"You entered community: {community}. Please wait while I fetch the results...\nIt will take some time...."
            conversation_stage = 2
        else:
            bot_response = "Invalid community. Please enter a valid community from BC, BCM, MBC, OC, SC, SCA, ST."
    elif conversation_stage == 2:
        print("Agg marks:", agg_marks)
        print("Community:", community)
        result = predict_colleges_and_branches(agg_marks, community)
        print(result)
        if isinstance(result, list):
           bot_response = "\n".join(result)
           print(bot_response)
        else:
            bot_response = f"College code: {result[0]}, Branch: {result[1]}"
    # Send response back to the client
    jsonify_response = jsonify({'status': 'success', 'bot_messages': [bot_response]})
    
    # Append bot's response to conversation_messages
    conversation_messages.append(('bot', bot_response))
    print(conversation_messages)

    return jsonify_response


if __name__ == '__main__':
    app.run(debug=True)

