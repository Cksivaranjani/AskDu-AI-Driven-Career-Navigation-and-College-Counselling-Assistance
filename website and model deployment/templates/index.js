const express = require('express');
const mongoose = require('mongoose');
const bodyParser = require('body-parser');
const path = require('path');
const app = express();
const PORT = process.env.PORT || 3002;

// Connect to MongoDB
mongoose.connect('mongodb://localhost:27017/studentdb', { useNewUrlParser: true, useUnifiedTopology: true });
const db = mongoose.connection;

// Define MongoDB Schema
const studentSchema = new mongoose.Schema({
    email: String,
    password: String
});

// Define MongoDB Schema for cutoff scores
const cutoffSchema = new mongoose.Schema({
    physicsMark: Number,
    chemistryMark: Number,
    mathsMark: Number,
    cutoffScore: Number
});

// Create Mongoose Model
const Student = mongoose.model('Student', studentSchema);

// Create Mongoose Model for cutoff scores
const Cutoff = mongoose.model('Cutoff', cutoffSchema);

// Handle MongoDB connection events
db.on('error', console.error.bind(console, 'connection error:'));
db.once('open', () => {
    console.log('Connected to MongoDB');
});

// Middleware to parse JSON and handle form submissions
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));

// Serve static files from the 'public' directory
app.use(express.static(path.join(__dirname, 'public')));

// Route to handle form submission 
app.post('/signup-form', async (req, res) => {
    try {
        const { email, password } = req.body;

        // Check if a user with the same email already exists
        const existingUser = await Student.findOne({ email });

        // If user with the same email exists, return an error
        if (existingUser) {
            console.log('User with this email already exists.');
            return res.status(400).send('User with this email already exists.');
        }

        const newStudent = new Student({ email, password });
        await newStudent.save();
        console.log('Signup successful:', newStudent);
        res.status(201).send('Signup successful!');
    } catch (error) {
        console.error('Signup failed:', error);
        res.status(500).send('Error signing up.');
    }
});

// Route to retrieve all students
app.get('/students', async (req, res) => {
    try {
        // Query all documents and exclude _id and __v fields
        const students = await Student.find({}, { _id: 0, __v: 0 });
        res.json(students);
    } catch (error) {
        console.error('Error retrieving students:', error);
        res.status(500).send('Error retrieving students.');
    }
});


// Route to handle login form submission
app.post('/login-form', async (req, res) => {
    try {
        const { email, password } = req.body;
        
        // Find user by email
        const user = await Student.findOne({ email });
        console.log(user);

        // If user does not exist or password is incorrect, return error
        if (!user || user.password !== password) {
            return res.status(401).send('Invalid email or password.');
        }
        
        console.log('Login successful');
        // Redirect user to chatbot page if credentials are valid
        res.redirect('/chatbot.html');
    } catch (error) {
        console.error('Login failed:', error);
        res.status(500).send('Error logging in.');
    }
});


// Serve the HTML file
app.get("/", (req, res) => {
    res.sendFile(path.join(__dirname, '/public/index.html'));
});

// Start server
app.listen(PORT, () => {
    console.log("Server is running on http://localhost:" + PORT);
});
